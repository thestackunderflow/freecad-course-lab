import json, subprocess, sys, time
cmd = sys.argv[1:]
p = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
req = {"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {"protocolVersion": "2025-06-18", "capabilities": {}, "clientInfo": {"name": "lab", "version": "0"}}}
try:
    p.stdin.write(json.dumps(req) + "\n"); p.stdin.flush()
    line = p.stdout.readline()
    print("reply:", line.strip()[:200] if line else "NONE")
except BrokenPipeError:
    print("reply: BROKEN PIPE")
time.sleep(2)
p.kill(); out, err = p.communicate()
print("exit:", p.returncode)
print("plug's stderr after exit:"); print(err)
