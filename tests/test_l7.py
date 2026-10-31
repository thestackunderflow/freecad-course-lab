"""Lesson 7 lab checks (unit tests; no display, no network, no Claude): our no-AI test script (lab/l7call.py) prints a
tool call and the plug's reply WORD FOR WORD (wrapped only at spaces, never shortened), says plainly whether the reply
was an error (MCP's isError), never prints a picture's base64, and reads a code file for execute_code."""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
LAB = os.path.abspath(os.path.join(HERE, '..'))
sys.path.insert(0, LAB)

from lab import l7call  # noqa: E402

REFUSED = ('Failed to connect to FreeCAD ([Errno 111] Connection refused). Make sure the FreeCAD addon is running.')
SUPPORT = "Failed to execute code: AttributeError: 'Sketcher.SketchObject' object has no attribute 'Support'"


def words(lines):
    return ' '.join(' '.join(lines).split())


def test_an_error_reply_is_printed_word_for_word_and_marked_as_an_error():
    r = {'isError': True, 'content': [{'type': 'text', 'text': REFUSED}]}
    lines = l7call.render('list_documents', {}, r)
    assert lines[0] == 'call: list_documents'
    assert lines[1] == 'reply: ERROR'
    assert words(lines[2:]) == REFUSED
    assert all(len(x) <= l7call.COLS for x in lines)


def test_long_words_are_never_cut_and_a_line_breaks_only_at_a_space():
    r = {'isError': True, 'content': [{'type': 'text', 'text': SUPPORT}]}
    body = l7call.render('execute_code', {'code': 'x'}, r)[2:]
    for ln in body:
        for w in ln.split():
            assert w in SUPPORT.split()
    assert words(body) == SUPPORT


def test_a_good_reply_says_ok_and_keeps_its_text():
    r = {'content': [{'type': 'text', 'text': '["Unnamed"]'}]}
    lines = l7call.render('list_documents', {}, r)
    assert lines[1] == 'reply: OK'
    assert words(lines[2:]) == '["Unnamed"]'


def test_a_picture_in_a_reply_is_named_not_printed():
    r = {'content': [{'type': 'text', 'text': 'Object created'}, {'type': 'image', 'data': 'iVBORw0' * 500, 'mimeType': 'image/png'}]}
    lines = l7call.render('create_object', {}, r)
    assert 'iVBOR' not in ' '.join(lines)
    assert lines[-1] == '(+ a picture of the 3D view)'


def test_a_warning_line_stays_first_as_the_plug_sent_it():
    warn = ('Warning: The FreeCAD addon is older than freecad-mcp 0.1.28 (protocol 1): it has no get_rpc_status. '
            "Update the addon: copy addon/FreeCADMCP from the matching freecad-mcp release into FreeCAD's Mod directory and restart FreeCAD.")
    r = {'content': [{'type': 'text', 'text': warn}, {'type': 'text', 'text': '["Unnamed"]'}]}
    lines = l7call.render('list_documents', {}, r)
    assert words(lines[2:]).startswith('Warning: The FreeCAD addon is older')
    assert words(lines[2:]).endswith('["Unnamed"]')


def test_execute_code_reads_its_code_from_a_file(tmp_path):
    f = tmp_path / 'support.py'
    f.write_text("sk.Support = (xz, [''])\n")
    name, args = l7call.parse(['execute_code', str(f)])
    assert name == 'execute_code' and args == {'code': "sk.Support = (xz, [''])\n"}


def test_other_tools_take_json_arguments_or_none():
    assert l7call.parse(['list_documents']) == ('list_documents', {})
    assert l7call.parse(['get_objects', '{"doc_name": "Hook"}']) == ('get_objects', {'doc_name': 'Hook'})


def test_the_plug_is_started_with_the_same_line_claude_code_uses():
    assert l7call.PLUG == ['uvx', 'freecad-mcp@0.1.28']


def test_a_transcript_line_is_written_for_the_call(tmp_path):
    log = tmp_path / 't.jsonl'
    l7call.log_call(str(log), 'list_documents', {}, {'isError': True, 'content': [{'type': 'text', 'text': REFUSED}]})
    row = json.loads(log.read_text().splitlines()[0])
    assert row['tool'] == 'list_documents' and row['isError'] is True and row['text'] == REFUSED
    assert os.path.getsize(log) > 0


STDERR = ['2026-10-31 00:58:39,111 - FreeCADMCPserver - WARNING - Could not connect to FreeCAD on startup: ' + REFUSED,
          '2026-10-31 00:58:39,116 - mcp.server.mcpserver.server - ERROR - Tool \'list_documents\' raised an unexpected exception',
          'Traceback (most recent call last):', '  File "x.py", line 1, in f', 'Exception: ' + REFUSED]


def test_the_plugs_own_log_reason_is_found_in_its_stderr():
    assert l7call.reason(STDERR) == REFUSED
    assert l7call.reason(['INFO - started']) is None


def test_an_error_reply_with_a_log_reason_prints_it_under_its_own_heading():
    r = {'isError': True, 'content': [{'type': 'text', 'text': 'Error executing tool list_documents'}]}
    lines = l7call.render('list_documents', {}, r, log_reason=REFUSED)
    i = lines.index("plug's log:")
    assert words(lines[2:i]) == 'Error executing tool list_documents'
    assert words(lines[i + 1:]) == REFUSED
