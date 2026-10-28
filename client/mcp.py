"""A minimal MCP client over stdio (from the earlier SolidCraft labs; + a log of every line): JSON-RPC 2.0, one
message per line, no SDK. It starts the server as a child process, exactly as Claude Code or Claude Desktop do."""
import datetime
import json
import queue
import subprocess
import threading

PROTOCOL = '2025-06-18'


class McpError(Exception):
    pass


class Hang(McpError):
    """No reply within the client-side timeout."""


def _now():
    return datetime.datetime.now(datetime.timezone.utc).isoformat(timespec='milliseconds')


class McpClient:
    def __init__(self, cmd, timeout_s=120, log_path=None, env=None):
        self.cmd, self.timeout_s, self.env = cmd, timeout_s, env
        self.proc = None
        self.next_id = 0
        self.init_result = None
        self._stderr = []
        self._log = open(log_path, 'a', encoding='utf-8') if log_path else None
        self._seq = 0
        self._lock = threading.Lock()

    def _write_log(self, d, msg):
        if not self._log:
            return
        with self._lock:
            self._seq += 1
            self._log.write(json.dumps({'t': _now(), 'seq': self._seq, 'dir': d, 'msg': msg}) + '\n')
            self._log.flush()

    def start(self):
        self.proc = subprocess.Popen(self.cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                     text=True, encoding='utf-8', bufsize=1, env=self.env)
        self._q = queue.Queue()
        threading.Thread(target=self._drain_stderr, daemon=True).start()
        threading.Thread(target=self._read_stdout, daemon=True).start()
        self.init_result = self.request('initialize', {'protocolVersion': PROTOCOL, 'capabilities': {},
                                                       'clientInfo': {'name': 'solidcraft-course-lab', 'version': '1'}})
        self.notify('notifications/initialized')
        return self.init_result

    def _read_stdout(self):
        for line in self.proc.stdout:
            self._q.put(line)
        self._q.put(None)

    def _drain_stderr(self):
        for line in self.proc.stderr:
            line = line.rstrip('\n')
            self._stderr.append(line)
            self._write_log('server-stderr', line)

    def stderr_text(self):
        return list(self._stderr)

    def close(self):
        if self.proc and self.proc.poll() is None:
            self.proc.stdin.close()
            try:
                self.proc.wait(timeout=10)
            except subprocess.TimeoutExpired:
                self.proc.kill()

    def kill(self):
        if self.proc and self.proc.poll() is None:
            self.proc.kill()
            self.proc.wait(timeout=10)

    def _send(self, msg):
        self._write_log('client->server', msg)
        self.proc.stdin.write(json.dumps(msg) + '\n')
        self.proc.stdin.flush()

    def notify(self, method, params=None):
        msg = {'jsonrpc': '2.0', 'method': method}
        if params is not None:
            msg['params'] = params
        self._send(msg)

    def request(self, method, params=None):
        self.next_id += 1
        rid = self.next_id
        msg = {'jsonrpc': '2.0', 'id': rid, 'method': method}
        if params is not None:
            msg['params'] = params
        self._send(msg)
        while True:
            try:
                line = self._q.get(timeout=self.timeout_s)
            except queue.Empty:
                raise Hang(f'HANG: no reply to {method} within {self.timeout_s}s')
            if not line:
                raise McpError(f'server closed stdout (exit {self.proc.poll()}); stderr: {self._stderr[-5:]}')
            m = json.loads(line)
            self._write_log('server->client', _short(m))
            if m.get('id') != rid:
                continue
            if 'error' in m:
                raise McpError(json.dumps(m['error']))
            return m['result']

    def list_tools(self):
        return self.request('tools/list', {})['tools']

    def call_tool(self, name, arguments):
        return self.request('tools/call', {'name': name, 'arguments': arguments})

    @staticmethod
    def text(result):
        return '\n'.join(c['text'] for c in result.get('content', []) if c.get('type') == 'text')

    @staticmethod
    def text_json(result):
        t = McpClient.text(result)
        try:
            return json.loads(t)
        except ValueError:
            try:
                return json.JSONDecoder().raw_decode(t)[0]
            except ValueError:
                return t

    def tool_json(self, name, arguments):
        r = self.call_tool(name, arguments)
        if r.get('isError'):
            raise McpError(f'{name} failed: {self.text(r)}')
        return self.text_json(r)


def _short(m):
    """The log keeps an image block's size, not its base64."""
    content = (m.get('result') or {}).get('content') if isinstance(m, dict) else None
    if not isinstance(content, list) or not any(c.get('type') == 'image' for c in content):
        return m
    m = json.loads(json.dumps(m))
    for c in m['result']['content']:
        if c.get('type') == 'image' and isinstance(c.get('data'), str):
            c['data'] = f'[{len(c["data"])} base64 chars]'
    return m
