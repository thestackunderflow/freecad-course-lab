# LAB-fx4: ModuleNotFoundError: No module named 'mcp.server.fastmcp': Why FreeCAD MCP Broke, and the uvx Fix — pre-registration v1, 2026-11-01 (before any run)

Lab repo freecad-course-lab, folder out/fx4/ (takes out/fx4/A, out/fx4/B, out/fx4/C, out/fx4/D, out/fx4/E (sub-takes E0, E1, E2), out/fx4/F1, out/fx4/F2, out/fx4/F3, out/fx4/F4 (SCRIPT §0 "take F" = these four, one re-resolve experiment per take), run out/fx4/runs/R1). Pins: FreeCAD 1.1.4 AppImage (take E2 only, for `sys.version`), freecad-mcp 0.1.19 (the pre-fix version), 0.1.20 (first version with the rewritten import), 0.1.28 (current), uv 0.13.6 (installed by uv's own installer as lesson 7 take B), mcp = whatever `uvx freecad-mcp@0.1.19` resolves on the take day (expected 2.3.0, PLAN §4.1; written into out/fx4/pins.txt from take B), Claude Code 2.1.31x (exact build written into out/fx4/pins.txt from `claude --version` at run start), model claude-sonnet-5-5 (as lesson 7; read back from session.jsonl), SolidCraft and PrusaSlicer not used. Docker image notes: the lesson 7 image (Linux, lab user `maker`, HOME /home/maker, `claude` on PATH, Firefox for take D, Xvfb for takes D and E2, Mesa only if the AppImage needs it, XDG_DATA_HOME unset, network on: uvx resolves from PyPI, uv downloads a CPython, Claude Code signs in). A second image, `fx4-py311`, with Python 3.11 only (no python3.12 binary anywhere on PATH, no uv-managed CPython present, `UV_PYTHON_INSTALL_DIR` pointing at an empty folder, uv 0.13.6 copied in, pip present for 3.11, network on), used by take E1 only; its Dockerfile is committed beside this file and copied to out/fx4/E/Dockerfile-py311.txt. Sources for every expected value: PLAN rev 3 §4 and §0.3/§0.4 (Q8, Q10, Q11), ACCURACY rev 3 block E, SCRIPT-fx4 v1 §0 and §1. A value not quoted there is "measure".

Conventions (SCRIPT-L7 §0): this file is committed before any run ("prereg before the run"; the commit hash goes into out/fx4/pins.txt). Each take is one screen recording out/fx4/TAKE/rec.mkv plus out/fx4/TAKE/events.tsv (event name, seconds from recording start); event names are exactly the SCRIPT §1 names so the footage cut can find them. Every terminal command's text is also kept as a file via `| tee` (`|&` where stderr matters: tracebacks, pip, uv all print to stderr). The no-AI test script of this video is `test_mcp.py` (section 3.0): it speaks MCP over stdio to a started plug and reads the plug's log only after the plug has exited (lesson 7 lesson: the log is flushed at exit). Terminal width 44 columns or wider; the footage wraps at 44.

Writing rule for this file: the pin is written "mcp[cli] below 2" in prose. The real quoted form with the less-than sign appears only inside fenced command lines, where it is unavoidable because the shell needs it; each such line says so. The same for "at least" bounds: prose says "mcp[cli] at least 1.12.2"; the real sign appears only inside fenced expected-output lines.

## 2. Questions this lab answers (PLAN §0.4, numbered as in the plan)

8. fx4, all parts, restated one testable sentence each:
   - 8a. On a fresh uvx, `uvx freecad-mcp@0.1.19` ends in a ModuleNotFoundError traceback and `uvx freecad-mcp@0.1.20` starts and waits on stdin.
   - 8b. The mcp version that `uvx freecad-mcp@0.1.19` resolves on the take day is read (expected 2.3.0).
   - 8c. The FULL last line of the 0.1.19 traceback is recorded verbatim and classified: long stub form (mcp 2.0.1, 2.1.1, 2.2.0, 2.3.0; about 330 characters) or bare one-line form (mcp 2.0.0, 2.1.0); the storyboard keeps or cuts the stub clauses accordingly.
   - 8d. The installed mcp version in the 0.1.19 set of parts is 2.x, the same with the pin mcp[cli] below 2 is 1.x (expected latest 1.x = 1.30.0), and 0.1.28's declared bound is mcp[cli] at least 1.28.1 and below 3.
   - 8e. `uvx` accepts `python` as the command with `--from`; otherwise the working line is recorded for the description.
   - 8f. `uvx --with` the pin `freecad-mcp@0.1.19` starts and waits on stdin.
   - 8g. Of the four candidate "fresh install" triggers (cleared uv cache, new machine, re-synced clone, unpinned run after the cache is gone), each is tested on its own and only those that produce the traceback are named in F4.
   - 8h. `python3.11 -m pip install freecad-mcp` prints the Requires-Python line and "No matching distribution found" (exact text recorded).
   - 8i. In a 3.11-only image, `uvx freecad-mcp@0.1.28` prints uv's CPython 3.12 download line (exact text recorded) and then starts.
   - 8j. Whether the lesson 7 image already has a 3.12 is checked first; if so, take E1 runs in the 3.11-only image.
   - 8k. `sys.version` in the FreeCAD 1.1.4 AppImage's Python console is read for the label "this FreeCAD: 3.11.x".
   - 8l. `pypi.org/pypi/freecad-mcp/0.1.19/json` renders readably in Firefox (the `requires_dist` line and `upload_time`); otherwise issue #98 is filmed.
10. All: the status-bar text after Start RPC Server with the 0.1.28 add-on equals lesson 7's "RPC Server started at 127.0.0.1:9875" (reused from out/l7; not re-filmed unless take E2 happens to show it; description only).
11. All Claude runs: the R1 prompt and the A/B/C score are written here before the run; one run; auto mode as lesson 7; the greyed suggested next prompt is cropped; the evidence frame for the split screen is take B `metadata: 2.x printed` (F5) and whether the reply matches is recorded.

## 3. Takes, in run order

Run order: A, B, C, D, E0, E1, E2, F1, F2, F3, F4, R1. Before take A: `claude --version | tee out/fx4/pins.txt`, `uv --version | tee -a out/fx4/pins.txt`, `git rev-parse HEAD | tee -a out/fx4/pins.txt` (the prereg commit), `cat /etc/os-release | tee -a out/fx4/pins.txt`, `date -u | tee -a out/fx4/pins.txt` (the take day, for "Tested: ... DATE" in the description).

### 3.0 The no-AI test script (used by takes A, C, E1, F1-F4)

Create `tools/test_mcp.py` in the lab repo (committed with this file). Content, exactly:

```
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
```

Call form: `python3 -I tools/test_mcp.py uvx freecad-mcp@0.1.20 |& tee out/fx4/TAKE/test-0.1.20.txt`. It prints `reply:` with the first JSON-RPC line (a result with serverInfo = the plug is alive), `exit:` and the plug's stderr read after exit. "Waits" is defined for every take as: the plain command run under `timeout 8` returns exit 124 (still running when killed) with no traceback in its output, and the test script's `reply:` line is a JSON object with `"result"`. A traceback is defined as: the output contains a line starting with `Traceback (most recent call last)`.

### 3.A Take A: 0.1.19 fails, 0.1.20 starts (Q8a, Q8c)

(a) Starting state: fresh /home/maker (no ~/.cache/uv, no ~/.local/share/uv, no ~/.local/bin/uv); uv 0.13.6 installed as lesson 7 take B (state-building, not a frame): `curl -LsSf https://astral.sh/uv/0.13.6/install.sh | sh |& tee out/fx4/A/uv-install.txt`, then a new login shell `bash -l`; `uv cache dir | tee out/fx4/A/uv-cache-dir.txt`; `ls -la "$(uv cache dir)" |& tee out/fx4/A/cache-before.txt` (expected: absent or empty). No FreeCAD open. Recording starts after the login shell.

(b) Commands, in order:
1. `uvx freecad-mcp@0.1.19 |& tee out/fx4/A/traceback-0.1.19.txt` — event `0.1.19: typed` at the Enter key; event `0.1.19: traceback last line` when the prompt returns; hold 15 s (F0 needs 14.6 s plus the S0 cut).
2. `tail -n 1 out/fx4/A/traceback-0.1.19.txt | tee out/fx4/A/last-line.txt`; `wc -c out/fx4/A/last-line.txt | tee out/fx4/A/last-line-chars.txt`; `grep -c "This is mcp 2" out/fx4/A/last-line.txt | tee out/fx4/A/last-line-form.txt` (1 = long stub form, 0 = bare form).
3. `timeout 8 uvx freecad-mcp@0.1.20 |& tee out/fx4/A/0.1.20.txt; echo "exit=${PIPESTATUS[0]}" | tee out/fx4/A/0.1.20-exit.txt` — event `0.1.20: typed`; event `0.1.20: waits` at 8 s after Enter if nothing but uv's install lines printed and the prompt has not returned.
4. `python3 -I tools/test_mcp.py uvx freecad-mcp@0.1.20 |& tee out/fx4/A/test-0.1.20.txt`.
5. For the record only (not a frame): `python3 -I tools/test_mcp.py uvx freecad-mcp@0.1.19 |& tee out/fx4/A/test-0.1.19.txt` (expected: `reply: NONE` or BROKEN PIPE, the traceback in the stderr block).
6. `ls -la "$(uv cache dir)" | tee out/fx4/A/cache-after.txt` (the tool environments now exist; used by take F1).

(c) Events: `0.1.19: typed`, `0.1.19: traceback last line`, `0.1.20: typed`, `0.1.20: waits`.

(d) Capture: out/fx4/A/rec.mkv, events.tsv, uv-install.txt, uv-cache-dir.txt, cache-before.txt, cache-after.txt, traceback-0.1.19.txt, last-line.txt, last-line-chars.txt, last-line-form.txt, 0.1.20.txt, 0.1.20-exit.txt, test-0.1.20.txt, test-0.1.19.txt, plus a full-resolution screenshot out/fx4/A/traceback-full.png at the `0.1.19: traceback last line` event (the Short S0 wants FreeCAD in frame too: that composite is made in the edit from this screenshot and take E2's FreeCAD window; no FreeCAD is opened in take A).

(e) EXPECTED: the last line of the 0.1.19 traceback begins with `ModuleNotFoundError: No module named 'mcp.server.fastmcp'` (ACCURACY E row 1, issue #98). Its full form, given the resolved mcp version (take B): with 2.0.1, 2.1.1, 2.2.0 or 2.3.0 it is the stub's long message, about 330 characters, continuing "This is mcp 2.x, where FastMCP was renamed to MCPServer (from mcp.server.mcpserver import MCPServer) and other APIs changed; see the migration guide at https://py.sdk.modelcontextprotocol.io/v2/migration/#fastmcp-renamed-to-mcpserver or pin 'mcp' below 2 to keep running v1 code." where the real text writes the pin with the less-than sign (ACCURACY E row 5, the unzipped wheels; PLAN §4.1); with 2.0.0 or 2.1.0 it is the bare one-line form (ACCURACY E row 4). Expected today: the long form, because 0.1.19's list has no bound and 2.3.0 is the latest (PLAN §4.1). 0.1.20 starts and waits on stdin: expected yes (PLAN §4.1: 0.1.20 falls back to `mcp.server.mcpserver`; bound below 3 allows 2.x); the exact uv lines printed before it waits: measure.

(f) PASS: 0.1.19 prints a traceback whose last line starts with the bare clause; 0.1.20 waits (exit 124 and a JSON result from test_mcp.py). Stub-vs-bare rule (PLAN Q8, SCRIPT §0 take A): if last-line-form.txt is 1, F0 keeps its second label "the error goes on: we come back to that", F2 keeps the stub clause ("Since late August a stub sits there ...") and F5 keeps "Since mcp 2.0.1 the error's own last line names that pin; in July it did not", and F0/F5 show the message's own words "pin 'mcp' below 2" as printed. If last-line-form.txt is 0 (the bare one-line form appears), cut F0's second label, F2's stub clause and F5's "the error names the pin" clause, cut the 4 s F0 return inside F5, and rerun retime.py (Time columns and chapters recomputed); no re-take. FAIL: 0.1.19 starts (no traceback): stop rule 6.1. 0.1.20 prints a traceback: stop rule 6.2.

### 3.B Take B: the metadata lines (Q8b, Q8d, Q8e)

(a) Starting state: the home of take A (cache present, the 0.1.19 and 0.1.20 environments exist). No FreeCAD open.

(b) Commands, in order:
1. `uvx --from freecad-mcp@0.1.19 python -c "import importlib.metadata as m; print(m.version('mcp'))" |& tee out/fx4/B/metadata-0.1.19.txt` — event `metadata 0.1.19: typed`; event `metadata: 2.x printed` when the version line prints; hold 6 s (this crop is the F5, S1 and F11 evidence frame).
2. The same with the pin (the less-than sign is unavoidable here; this is the one place it is written):
   ```
   uvx --with "mcp[cli]<2" --from freecad-mcp@0.1.19 python -c "import importlib.metadata as m; print(m.version('mcp'))" |& tee out/fx4/B/metadata-pinned.txt
   ```
   event `metadata pinned: typed`; event `metadata pinned: 1.x printed`; hold 6 s.
3. `uvx --from freecad-mcp@0.1.28 python -c "import importlib.metadata as m; print(m.version('mcp')); print(m.requires('freecad-mcp'))" |& tee out/fx4/B/metadata-0.1.28.txt` — event `metadata 0.1.28: printed` (not a SCRIPT §1 event; description and F6 bound check only).
4. If step 1 fails because uvx refuses `python` as the command (Q8e): try, in this order, each `|& tee out/fx4/B/python-form-N.txt` (N = 2, 3): `uvx --from freecad-mcp@0.1.19 --with pip python -c "..."` and `uv tool run --from freecad-mcp@0.1.19 python -c "..."`; the first one that prints a version is the working form; redo steps 1-3 with it so the footage shows the working line; write the working line to out/fx4/B/working-form.txt.
5. `cp out/fx4/B/metadata-0.1.19.txt out/fx4/pins-mcp-resolved.txt` and append the resolved version to out/fx4/pins.txt (`echo "mcp resolved by 0.1.19 today: $(tail -n 1 out/fx4/B/metadata-0.1.19.txt)" | tee -a out/fx4/pins.txt`).

(c) Events: `metadata 0.1.19: typed`, `metadata: 2.x printed`, `metadata pinned: typed`, `metadata pinned: 1.x printed`.

(d) Capture: out/fx4/B/rec.mkv, events.tsv, metadata-0.1.19.txt, metadata-pinned.txt, metadata-0.1.28.txt, python-form-N.txt (if any), working-form.txt.

(e) EXPECTED: step 1 prints 2.3.0 (PLAN §4.1 "resolves mcp 2.3.0 today"; any 2.x satisfies the storyboard, the digit after "2 point" is `[lab]`). Step 2 prints a 1.x, expected 1.30.0 (PLAN Q8 "latest 1.x is 1.30.0"). Step 3 prints a 2.x and a requires list containing the mcp line with the bound at least 1.28.1 and below 3, exact expected text (the signs are the real ones, inside this fence only):
```
mcp[cli]>=1.28.1,<3
```
plus anyio, certifi, pyjwt, validators lines (ACCURACY E row 6: anyio at least 4.14.2, certifi at least 2026.10.19, pyjwt at least 2.15.0, validators at least 0.34.0). Whether `python` is accepted as the command: measure (PLAN §4.6 step 4 writes the form with `python`; Q8 names the two fallbacks).

(f) PASS: step 1 a 2.x, step 2 a 1.x, step 3's bound below 3 present. The F5 narration digits and F6 "below 3 [lab: confirm the bound]" are filled from these files. FAIL: step 1 prints 1.x: stop rule 6.1 (the premise is gone). Step 2 prints 2.x: the pin did not apply; re-run once with `--refresh`; if still 2.x, stop rule 6.3. Step 3's requires has no below-3 bound: F6's "and its list has an upper limit too, below 3" clause is cut and retime.py rerun; the F13 question is reworded by rev 4 (report). None of the python forms works: record the error texts; take B's crops are made from `uv tool run` with a one-line Python file instead (`echo "import importlib.metadata as m; print(m.version('mcp'))" | tee out/fx4/B/v.py` then `uv run --with freecad-mcp@0.1.19 --no-project out/fx4/B/v.py`), and the description carries that line; report as a deviation.

### 3.C Take C: the workaround and the real fix (Q8f, Q11 your-turn)

(a) Starting state: the home of take B; Claude Code signed in as lesson 7; `claude mcp list | tee out/fx4/C/mcp-list-before.txt` expected "No MCP servers configured. Use `claude mcp add` to add a server." (lesson 7 take A wording). No FreeCAD open (lesson 7 take A connected without FreeCAD: "Connected" is the plug starting, not the socket).

(b) Commands, in order:
1. The workaround (the less-than sign is unavoidable inside this command; prose elsewhere says "mcp[cli] below 2"):
   ```
   timeout 8 uvx --with "mcp[cli]<2" freecad-mcp@0.1.19 |& tee out/fx4/C/pinned-0.1.19.txt; echo "exit=${PIPESTATUS[0]}" | tee out/fx4/C/pinned-0.1.19-exit.txt
   ```
   event `pinned 0.1.19: typed`; event `pinned 0.1.19: waits` at 8 s after Enter.
2. The test script on the pinned plug (the same sign, same reason, fenced only):
   ```
   python3 -I tools/test_mcp.py uvx --with "mcp[cli]<2" freecad-mcp@0.1.19 |& tee out/fx4/C/test-pinned.txt
   ```
3. `claude mcp add --scope user freecad -- uvx freecad-mcp@0.1.28 |& tee out/fx4/C/add-0.1.28.txt` — event `add 0.1.28: typed`.
4. `claude mcp list |& tee out/fx4/C/list.txt` — event `list: Connected` when the Connected line prints; hold 20 s (F1 needs 13.4 s, F14 holds it under the outro 14.6 s: record a second hold of 20 s at the end of the take).
5. `claude mcp get freecad |& tee out/fx4/C/get-freecad.txt` — event `your turn get: typed`; event `get freecad: printed`; hold 27 s with the cursor live (F13 is 26.6 s).
6. `claude mcp list |& tee out/fx4/C/list-2.txt` — hold 20 s (the F14 hold).

(c) Events: `pinned 0.1.19: typed`, `pinned 0.1.19: waits`, `add 0.1.28: typed`, `list: Connected`, `your turn get: typed`, `get freecad: printed`.

(d) Capture: out/fx4/C/rec.mkv, events.tsv, mcp-list-before.txt, pinned-0.1.19.txt, pinned-0.1.19-exit.txt, test-pinned.txt, add-0.1.28.txt, list.txt, get-freecad.txt, list-2.txt, and `cat ~/.claude.json | python3 -c "import json,sys; print(json.dumps(json.load(sys.stdin).get('mcpServers'), indent=1))" | tee out/fx4/C/user-config-mcp.txt` (the args line a Desktop user would read; file path as lesson 7 found it; if the user-scope config lives elsewhere, `claude mcp get` says where: copy that).

(e) EXPECTED: step 1 waits (PLAN §4.1: issue #98's workaround; SCRIPT §0 take C "[lab: confirm]"); step 3 prints the "Added ..." line, expected wording as lesson 7 take A with "user config": "Added stdio MCP server freecad with command: uvx freecad-mcp@0.1.28 to user config" (SCRIPT-L7 §0; exact text `[lab]`); step 4 prints a line with "Connected" (lesson 7: "✔ Connected"; exact line `[lab]`); step 5: measure (the your-turn output; it must show the version 0.1.28 in the command line).

(f) PASS: step 1 exit 124 and a JSON result in test-pinned.txt; step 4 contains "Connected"; step 5 shows `freecad-mcp@0.1.28`. FAIL: step 1 prints the traceback: stop rule 6.3. Step 4 prints "Failed to connect": if the text is lesson 7 take B's ENOENT (uvx not on PATH), open a login shell and redo steps 3-6 once; any other failure text: stop rule 6.4.

### 3.D Take D: the sources in Firefox (Q8l)

(a) Starting state: Xvfb running, Firefox installed in the image, a fresh profile (`firefox --new-instance -P lab` or the image's default), window 1280x800 or larger, no other windows. Network on.

(b) Commands and clicks, in order:
1. Open https://github.com/modelcontextprotocol/python-sdk/releases/tag/v2.0.0 — event `firefox: release v2.0.0 opened` when the page has rendered; scroll so the Highlights line "FastMCP is now MCPServer" and the release date line are both in frame; hold 32 s (F2 is 30.2 s). Screenshot out/fx4/D/release-v2.0.0.png.
2. Open https://pypi.org/pypi/freecad-mcp/0.1.19/json — event `firefox: pypi 0.1.19 json opened`; if Firefox shows its JSON viewer, use the "Raw Data" tab if the tree view hides the `requires_dist` array, and zoom (Ctrl-plus) until the `requires_dist` line and the `upload_time` line are readable at 44 columns; hold 17 s (F3 is 15.4 s). Screenshot out/fx4/D/pypi-0.1.19-json.png. Also `curl -s https://pypi.org/pypi/freecad-mcp/0.1.19/json | python3 -c "import json,sys; d=json.load(sys.stdin); print(d['info']['requires_dist']); print([u['upload_time'] for u in d['urls']])" | tee out/fx4/D/pypi-0.1.19-json.txt` for the record.
3. Readability decision, written to out/fx4/D/readable.txt as one word: "readable" if both lines are legible in the screenshot at the zoom the footage will use, else "unreadable". If unreadable: open https://github.com/neka-nat/freecad-mcp/issues/98, scroll to the author's quote of the parts-list line — event `firefox: issue 98`; hold 17 s; screenshot out/fx4/D/issue-98.png.
4. Open https://pypi.org/project/freecad-mcp/0.1.28/ — event `firefox: pypi 0.1.28` when the sidebar "Requires: Python" line is in frame; hold 10 s (Short fx4-02 S1). Screenshot out/fx4/D/pypi-0.1.28.png.

(c) Events: `firefox: release v2.0.0 opened`, `firefox: pypi 0.1.19 json opened`, `firefox: issue 98` (only if unreadable), `firefox: pypi 0.1.28`.

(d) Capture: out/fx4/D/rec.mkv, events.tsv, release-v2.0.0.png, pypi-0.1.19-json.png, pypi-0.1.19-json.txt, readable.txt, issue-98.png (if any), pypi-0.1.28.png.

(e) EXPECTED: the release page shows "FastMCP is now MCPServer, and there is a first-class Client" and the date 28 Jul (ACCURACY E row 2; the year is from PyPI's upload time). The JSON shows `requires_dist` containing the mcp line with the bound at least 1.12.2 and no upper bound, exact text inside this fence only:
```
mcp[cli]>=1.12.2
```
and `upload_time` 2026-07-05 (ACCURACY E row 8). Readability in Firefox: measure. The 0.1.28 project page shows "Requires: Python" with at least 3.12 (ACCURACY E rows 6 and 10: `requires-python` at least 3.12; the exact sidebar text: measure).

(f) PASS: both lit strings of F2 are on the release page as quoted; the JSON (or issue #98) shows the no-bound line and the July date. FAIL: the release page wording differs from the quote: the F2 lit words become the page's words, rev 4 is told (no re-take). The JSON shows a bound on the mcp line for 0.1.19: stop rule 6.1. Firefox does not start in Xvfb: stop rule 6.5.

### 3.E Take E: the Python 3.12 cousin (Q8h, Q8i, Q8j, Q8k)

#### 3.E0 Sub-take E0: does the lesson 7 image already have a 3.12? (Q8j)

(a) Starting state: the lesson 7 image, the home of take C. No recording needed (a text check), but the terminal is recorded anyway for the record.

(b) Commands: `ls /usr/bin/python3* | tee out/fx4/E/E0-ls-python.txt`; `python3 --version |& tee -a out/fx4/E/E0-ls-python.txt`; `uv python list |& tee out/fx4/E/E0-uv-python-list.txt`; `uv python find 3.12 |& tee out/fx4/E/E0-uv-find-312.txt`; `uv python find 3.11 |& tee out/fx4/E/E0-uv-find-311.txt`.

(c) Events: none.

(d) Capture: the three files.

(e) EXPECTED: measure (PLAN Q8 "Does the Docker image have a 3.12 already"). uv has by now downloaded a CPython for takes A-C if the image had none that satisfies 0.1.19 (Requires-Python at least 3.12, ACCURACY E row 6): `uv python list` shows it as a managed install.

(f) Rule: if the image has any 3.12 (system or uv-managed), E1 runs in the 3.11-only image `fx4-py311` (PLAN Q8). If the image has no 3.12 and no uv-managed CPython and a system 3.11, E1 may run in the lesson 7 image on a fresh home with an empty `UV_PYTHON_INSTALL_DIR` (record which; expected: the 3.11-only image is needed, since takes A-C already made uv download a CPython). Default: E1 runs in `fx4-py311` regardless, so the take is clean; E0 only documents why.

#### 3.E1 Sub-take E1: pip under 3.11, uvx downloads 3.12 (Q8h, Q8i)

(a) Starting state: a fresh container from `fx4-py311`, HOME /home/maker empty, uv 0.13.6 on PATH, `UV_PYTHON_INSTALL_DIR=/home/maker/.local/share/uv/python` pointing at an empty folder, no uv cache. Pre-check, kept as files: `python3.11 --version | tee out/fx4/E/E1-python-version.txt`; `ls /usr/bin/python3* /usr/local/bin/python3* |& tee out/fx4/E/E1-ls-python.txt` (expected: 3.11 only); `uv python list |& tee out/fx4/E/E1-uv-python-list-before.txt` (expected: no 3.12 marked installed; downloadable entries are fine). No FreeCAD.

(b) Commands, in order:
1. `python3.11 -m pip install freecad-mcp |& tee out/fx4/E/E1-pip-3.11.txt` — event `pip 3.11: typed`; event `pip 3.11: error block` when the ERROR lines print; hold 18 s (F8 is 17.4 s).
2. `python3.11 -m pip --version | tee out/fx4/E/E1-pip-version.txt` (for the record: which pip printed it).
3. `timeout 90 uvx freecad-mcp@0.1.28 |& tee out/fx4/E/E1-uvx-0.1.28.txt; echo "exit=${PIPESTATUS[0]}" | tee out/fx4/E/E1-uvx-0.1.28-exit.txt` — event `uvx 0.1.28: typed`; event `uv: downloading cpython 3.12` when uv's download line prints; event `0.1.28: waits` when nothing more prints and the prompt has not returned (hold until timeout; F10 is 25.0 s and S2 11.0 s). The timeout is 90 s because the CPython download precedes the wait; "waits" is judged from the last printed line, not from exit 124 alone.
4. `uv python list |& tee out/fx4/E/E1-uv-python-list-after.txt` (expected: one 3.12 now marked as installed under UV_PYTHON_INSTALL_DIR); `ls "$UV_PYTHON_INSTALL_DIR" | tee out/fx4/E/E1-ls-python-dir.txt`.
5. `python3 -I tools/test_mcp.py uvx freecad-mcp@0.1.28 |& tee out/fx4/E/E1-test-0.1.28.txt` (python3 here is 3.11; the script itself needs nothing beyond the standard library).
6. `grep -n -i "download" out/fx4/E/E1-uvx-0.1.28.txt | tee out/fx4/E/E1-download-line.txt`; `grep -n "Requires-Python\|No matching distribution" out/fx4/E/E1-pip-3.11.txt | tee out/fx4/E/E1-pip-lit-lines.txt`.

(c) Events: `pip 3.11: typed`, `pip 3.11: error block`, `uvx 0.1.28: typed`, `uv: downloading cpython 3.12`, `0.1.28: waits`.

(d) Capture: out/fx4/E/rec-E1.mkv, events-E1.tsv, E1-python-version.txt, E1-ls-python.txt, E1-uv-python-list-before.txt, E1-pip-3.11.txt, E1-pip-version.txt, E1-pip-lit-lines.txt, E1-uvx-0.1.28.txt, E1-uvx-0.1.28-exit.txt, E1-download-line.txt, E1-uv-python-list-after.txt, E1-ls-python-dir.txt, E1-test-0.1.28.txt, Dockerfile-py311.txt, and `docker image inspect fx4-py311 | tee out/fx4/E/E1-image-inspect.json`.

(e) EXPECTED: pip prints an ERROR block containing a Requires-Python clause for every version (issue #140: "all versions require Python 3.12 or newer", ACCURACY E row 9; PLAN Q8 expected "Requires-Python at least 3.12", written with the real sign inside this fence only) and the line "No matching distribution found":
```
Requires-Python >=3.12
ERROR: No matching distribution found for freecad-mcp
```
The exact wording and line order: measure (Q8 "Exact pip text"); the F8 lit words are whatever pip printed. uv's download line: measure (PLAN Q8 "the cpython 3.12 download line"; uv's documented behaviour "uv will automatically download Python versions if they cannot be found on the system", PLAN §4.1). Then the plug waits (PLAN F10).

(f) PASS: pip ends with "No matching distribution found" and names Requires-Python 3.12 in its block; uvx prints a line about downloading a CPython 3.12 and then waits (test_mcp.py returns a JSON result). FAIL: pip installs freecad-mcp under 3.11 (a wheel now allows 3.11): stop rule 6.6. uvx prints no download line (a 3.12 was found): the image is not 3.11-only; rebuild `fx4-py311`, verify E1 pre-check (a) again, re-do E1 (one rebuild; if the second attempt also shows no download line, stop rule 6.6). uvx downloads a version other than 3.12 (e.g. 3.13): record it; the F10 words "a 3.12" become the downloaded version in narration and label, rev 4 is told; no re-take.

#### 3.E2 Sub-take E2: sys.version in the FreeCAD 1.1.4 AppImage console (Q8k, Q10)

(a) Starting state: the lesson 7 image, Xvfb running, XDG_DATA_HOME unset, the FreeCAD 1.1.4 AppImage as lesson 7 used it, the 0.1.28 add-on installed as lesson 7 left it (so the MCP Addon workbench exists; Q10 reuse). No plug running.

(b) Commands and clicks, in order:
1. Start FreeCAD (`./FreeCAD-1.1.4-*.AppImage |& tee out/fx4/E/E2-freecad-stdout.txt`, the exact file name as in out/l7). Wait for the main window.
2. View, Panels, Python console. Type `import sys; print(sys.version)` and Enter — event `console: sys.version` when the line prints; hold 12 s (Short S1 is 9.4 s). Screenshot out/fx4/E/E2-console-sys-version.png.
3. Also type `print(sys.version_info[:3])` and `import platform; print(platform.python_implementation())` (for the record).
4. Q10 (reuse check, cheap since FreeCAD is open): switch to the MCP Addon workbench, Start RPC Server; read the status bar — event `status: rpc started` (not a SCRIPT §1 event; description only); screenshot out/fx4/E/E2-status-bar.png; copy the text to out/fx4/E/E2-status-bar.txt by hand from the screenshot (typed by the lab, marked "transcribed").
5. Keep the FreeCAD window open and take one full-screen screenshot out/fx4/E/E2-freecad-window.png (for the S0 composites of both Shorts: "the FreeCAD window with the plug dead in the terminal beside it" is composed in the edit from this and take A's traceback-full.png; the console is in frame for fx4-02 S0).
6. Close FreeCAD (File, Exit). After exit, copy the Report view text if it was saved, else nothing.

(c) Events: `console: sys.version`, `status: rpc started`.

(d) Capture: out/fx4/E/rec-E2.mkv, events-E2.tsv, E2-freecad-stdout.txt, E2-console-sys-version.png, E2-sys-version.txt (the printed line, copied from the console with Ctrl-C into a file: `xclip -o | tee out/fx4/E/E2-sys-version.txt` if xclip exists, else transcribed and marked), E2-status-bar.png, E2-status-bar.txt, E2-freecad-window.png.

(e) EXPECTED: `sys.version` starts with "3.11." (PLAN §4.1 "the Linux AppImage's own Python version is read in its console"; issue #140 saw 3.11.14 on Windows 1.1.3, ACCURACY E row 9; the Linux AppImage's value: measure). Status bar: "RPC Server started at 127.0.0.1:9875" (PLAN Q10, lesson 7).

(f) PASS: a version line prints; the label "this FreeCAD: 3.11.x" takes its first three fields. If it starts with something other than 3.11: the label and the F8/F9/F12 narration digits take the measured value ("This FreeCAD runs [measured]"), the F9 card text changes, rev 4 is told; the "needs 3.12 or later" clause stands only if the measured version is below 3.12; if the AppImage's Python is 3.12 or later, the whole F8-F10 half is reported (Open 4: the producer decides; see stop rule 6.7). Status bar text differs from lesson 7's: record it; Q10's answer is the new text. FreeCAD does not start in Xvfb: stop rule 6.5.

### 3.F Takes F1-F4: when does uvx re-resolve for a user who changed nothing (Q8g)

All four takes use the same definition: "the traceback" = take A's ModuleNotFoundError traceback appears (grep for `Traceback (most recent call last)` and the bare clause); "starts" = waits as defined in 3.0. Each take is scored on its own; F4's card and clause name only the takes scored PASS-trigger. The July state ("ran last month") is built with uv's `--exclude-newer` at a date before mcp 2.0.0's upload (2026-07-28T13:45:28 UTC, PLAN §4.1): `2026-07-27T00:00:00Z`.

#### 3.F1 Take F1: a cleared cache (`uv cache clean`)

(a) Starting state: a fresh container from the lesson 7 image, fresh /home/maker, uv 0.13.6 installed as in take A, login shell, empty cache (`ls -la "$(uv cache dir)" |& tee out/fx4/F1/cache-0.txt`).

(b) Commands, in order:
1. Build the July state: `timeout 8 uvx --exclude-newer 2026-07-27T00:00:00Z freecad-mcp@0.1.19 |& tee out/fx4/F1/july-run.txt; echo "exit=${PIPESTATUS[0]}" | tee out/fx4/F1/july-run-exit.txt` — event `july run: typed`; expected: starts (the resolver sees no mcp 2.x). `uvx --exclude-newer 2026-07-27T00:00:00Z --from freecad-mcp@0.1.19 python -c "import importlib.metadata as m; print(m.version('mcp'))" |& tee out/fx4/F1/july-mcp-version.txt` (expected: a 1.x; measure which).
2. The "old copy" test, no flag: `timeout 8 uvx freecad-mcp@0.1.19 |& tee out/fx4/F1/reuse-run.txt; echo "exit=${PIPESTATUS[0]}" | tee out/fx4/F1/reuse-run-exit.txt` — event `old copy: typed`. Measure: does uvx reuse the July environment (starts) or re-resolve because the request differs (traceback)? `ls -la "$(uv cache dir)"/environments-v* |& tee out/fx4/F1/cache-1.txt` (the folder name as uv 0.13.6 writes it; if it differs, `find "$(uv cache dir)" -maxdepth 2 -name "*environ*"` and record).
3. If step 2 re-resolved (traceback), the baseline is rebuilt with an installed tool instead: `uv tool install --exclude-newer 2026-07-27T00:00:00Z freecad-mcp@0.1.19 |& tee out/fx4/F1/tool-install-july.txt`; `timeout 8 freecad-mcp |& tee out/fx4/F1/tool-run-before.txt; echo "exit=${PIPESTATUS[0]}" | tee out/fx4/F1/tool-run-before-exit.txt` (expected: starts). Record in out/fx4/F1/baseline.txt which baseline (uvx env or installed tool) represents "your old copy".
4. `uv cache clean |& tee out/fx4/F1/cache-clean.txt` — event `cache clean: typed`; `ls -la "$(uv cache dir)" |& tee out/fx4/F1/cache-2.txt`.
5. `timeout 8 uvx freecad-mcp@0.1.19 |& tee out/fx4/F1/after-clean-run.txt; echo "exit=${PIPESTATUS[0]}" | tee out/fx4/F1/after-clean-run-exit.txt` — event `after clean: typed`; event `after clean: traceback` if the traceback prints.
6. If step 3 was used: `timeout 8 freecad-mcp |& tee out/fx4/F1/tool-run-after.txt; echo "exit=${PIPESTATUS[0]}" | tee out/fx4/F1/tool-run-after-exit.txt` (does an installed tool survive `uv cache clean`? measure; `uv tool list | tee out/fx4/F1/tool-list-after.txt`).

(c) Events: `july run: typed`, `old copy: typed`, `cache clean: typed`, `after clean: typed`, `after clean: traceback` (F4 is a DIA card; these events are for the lab record and a possible rev 4 REC insert, not SCRIPT §1 names).

(d) Capture: out/fx4/F1/rec.mkv, events.tsv, cache-0.txt, july-run.txt, july-run-exit.txt, july-mcp-version.txt, reuse-run.txt, reuse-run-exit.txt, cache-1.txt, tool-install-july.txt, tool-run-before(-exit).txt, baseline.txt, cache-clean.txt, cache-2.txt, after-clean-run.txt, after-clean-run-exit.txt, tool-run-after(-exit).txt, tool-list-after.txt.

(e) EXPECTED: step 1 starts with a 1.x mcp (by the dates in PLAN §4.1; the version: measure). Steps 2, 5, 6: measure (ACCURACY E row 12: "uv docs ... describe uvx's isolated environments but not the re-resolve triggers").

(f) PASS-trigger: step 5 prints the traceback after a baseline that started (step 2 or step 3). Then F4's card-bound-4 and the F4 clause name "a cleared uv cache". PASS-not-a-trigger: step 5 starts (uvx did not re-resolve after the clean, or re-resolved to 1.x): "a cleared uv cache" is NOT named; report why from cache-2.txt and the printed lines. FAIL: step 1 does not start (the July state cannot be built: `--exclude-newer` unsupported in uvx 0.13.6 or no 1.x satisfies 0.1.19): stop rule 6.8.

#### 3.F2 Take F2: a new machine

(a) Starting state: a brand-new container from the lesson 7 image (`docker run --rm -it` with a fresh anonymous home volume), nothing of takes A-F1 present (`ls -la ~/.cache ~/.local |& tee out/fx4/F2/home-before.txt`, expected: no uv folders), uv 0.13.6 installed as in take A, login shell. This is the user who ran the plug in July on another machine and sets up a second one today with the same pinned line.

(b) Commands, in order:
1. `timeout 8 uvx freecad-mcp@0.1.19 |& tee out/fx4/F2/new-machine-run.txt; echo "exit=${PIPESTATUS[0]}" | tee out/fx4/F2/new-machine-run-exit.txt` — event `new machine: typed`; event `new machine: traceback` if it prints.
2. `uvx --from freecad-mcp@0.1.19 python -c "import importlib.metadata as m; print(m.version('mcp'))" |& tee out/fx4/F2/new-machine-mcp-version.txt`.

(c) Events: `new machine: typed`, `new machine: traceback`.

(d) Capture: out/fx4/F2/rec.mkv, events.tsv, home-before.txt, new-machine-run.txt, new-machine-run-exit.txt, new-machine-mcp-version.txt, `docker image inspect` of the image id used (out/fx4/F2/image-id.txt).

(e) EXPECTED: the traceback, mcp 2.3.0 (PLAN §4.1: an unbounded list resolves the latest on a fresh install). Take A is the same experiment on a different fresh home; F2 is kept as its own take so the card's trigger has its own evidence file.

(f) PASS-trigger: the traceback prints; "a new machine" is named in F4. PASS-not-a-trigger: it starts: not named (and stop rule 6.1 applies, since take A then contradicts it). No FAIL class beyond that.

#### 3.F3 Take F3: a re-synced clone (`uv sync` in an old checkout)

(a) Starting state: the container of take F2 after its commands (cache holds 0.1.19 with 2.x; irrelevant to `uv sync`, which resolves the project). The 0.1.19 source is the sdist from PyPI (the Git tag v0.1.19 is unverified, ACCURACY E row 8: the sdist is the stand-in, said so in the record): `python3 -m pip download --no-deps --no-binary :all: --ignore-requires-python freecad-mcp==0.1.19 -d out/fx4/F3/sdist |& tee out/fx4/F3/sdist-download.txt` (if pip is absent in the image: `uv run --no-project --with pip python -m pip download ...` with the same flags); `mkdir -p out/fx4/F3/checkout; tar -xzf out/fx4/F3/sdist/freecad_mcp-0.1.19.tar.gz -C out/fx4/F3/checkout --strip-components=1` (the archive name as pip wrote it; `ls out/fx4/F3/sdist` first); `ls -la out/fx4/F3/checkout | tee out/fx4/F3/checkout-ls.txt` (does the sdist carry uv.lock? measure; expected: no); `grep -n "mcp\|requires-python" out/fx4/F3/checkout/pyproject.toml | tee out/fx4/F3/pyproject-lines.txt`.

(b) Commands, in order (all run inside out/fx4/F3/checkout; use `--directory out/fx4/F3/checkout` on every uv call so no `cd` is needed):
1. Build the July clone state (the lock a user made in July): `uv lock --directory out/fx4/F3/checkout --exclude-newer 2026-07-27T00:00:00Z |& tee out/fx4/F3/lock-july.txt`; `grep -n -A2 '^name = "mcp"' out/fx4/F3/checkout/uv.lock | tee out/fx4/F3/lock-july-mcp.txt` (expected: a 1.x). `uv sync --directory out/fx4/F3/checkout |& tee out/fx4/F3/sync-july.txt`; `timeout 8 uv run --directory out/fx4/F3/checkout freecad-mcp |& tee out/fx4/F3/run-july.txt; echo "exit=${PIPESTATUS[0]}" | tee out/fx4/F3/run-july-exit.txt` — event `clone july: typed`; expected: starts.
2. Sub-case (i), the lock is committed and the user re-syncs today: `cp -r out/fx4/F3/checkout out/fx4/F3/checkout-i; rm -rf out/fx4/F3/checkout-i/.venv`; `uv sync --directory out/fx4/F3/checkout-i |& tee out/fx4/F3/sync-i.txt`; `timeout 8 uv run --directory out/fx4/F3/checkout-i freecad-mcp |& tee out/fx4/F3/run-i.txt; echo "exit=${PIPESTATUS[0]}" | tee out/fx4/F3/run-i-exit.txt` — event `resync locked: typed`. Measure: does `uv sync` honour the lock (starts) or re-resolve (traceback)?
3. Sub-case (ii), the user upgrades: `uv sync --directory out/fx4/F3/checkout-i --upgrade |& tee out/fx4/F3/sync-ii.txt`; `grep -n -A2 '^name = "mcp"' out/fx4/F3/checkout-i/uv.lock | tee out/fx4/F3/lock-ii-mcp.txt`; `timeout 8 uv run --directory out/fx4/F3/checkout-i freecad-mcp |& tee out/fx4/F3/run-ii.txt; echo "exit=${PIPESTATUS[0]}" | tee out/fx4/F3/run-ii-exit.txt` — event `resync upgrade: typed`.
4. Sub-case (iii), no lock file in the clone (the lock was never committed): `cp -r out/fx4/F3/checkout out/fx4/F3/checkout-iii; rm -rf out/fx4/F3/checkout-iii/.venv out/fx4/F3/checkout-iii/uv.lock`; `uv sync --directory out/fx4/F3/checkout-iii |& tee out/fx4/F3/sync-iii.txt`; `grep -n -A2 '^name = "mcp"' out/fx4/F3/checkout-iii/uv.lock | tee out/fx4/F3/lock-iii-mcp.txt`; `timeout 8 uv run --directory out/fx4/F3/checkout-iii freecad-mcp |& tee out/fx4/F3/run-iii.txt; echo "exit=${PIPESTATUS[0]}" | tee out/fx4/F3/run-iii-exit.txt` — event `resync nolock: typed`.
5. Sub-case (iv), the old-video command form (PLAN §4.2: `uv --directory ... run freecad-mcp`) on the July checkout after its .venv is removed (a "re-synced" run without an explicit sync): `rm -rf out/fx4/F3/checkout/.venv`; `timeout 20 uv --directory out/fx4/F3/checkout run freecad-mcp |& tee out/fx4/F3/run-iv.txt; echo "exit=${PIPESTATUS[0]}" | tee out/fx4/F3/run-iv-exit.txt` — event `uv run old form: typed`.

(c) Events: `clone july: typed`, `resync locked: typed`, `resync upgrade: typed`, `resync nolock: typed`, `uv run old form: typed` (lab record; F4 is a DIA card).

(d) Capture: out/fx4/F3/rec.mkv, events.tsv, sdist-download.txt, checkout-ls.txt, pyproject-lines.txt, lock-july.txt, lock-july-mcp.txt, sync-july.txt, run-july(-exit).txt, sync-i.txt, run-i(-exit).txt, sync-ii.txt, lock-ii-mcp.txt, run-ii(-exit).txt, sync-iii.txt, lock-iii-mcp.txt, run-iii(-exit).txt, run-iv(-exit).txt, and the three uv.lock files copied as lock-july.lock, lock-ii.lock, lock-iii.lock.

(e) EXPECTED: step 1 starts (1.x). Sub-cases (i)-(iv): measure (ACCURACY E row 12). The 0.1.19 pyproject's own mcp line and requires-python: measure (PyPI's `requires_dist` for 0.1.19 is the no-bound line, ACCURACY E row 6; the sdist's pyproject should agree: record a mismatch).

(f) Scoring: for each sub-case, PASS-trigger if the traceback prints, PASS-not-a-trigger if it starts. The F4 wording is chosen by which sub-cases are triggers, and only these wordings are allowed: all of (i)-(iv) trigger: "a re-synced clone"; (ii) and (iii) (and (iv) if it re-resolves) trigger but (i) does not: "a re-synced clone without a committed lock file, or synced with upgrade" (one card line, may be split into two spoken items; retime.py rerun if the word count changes); only (ii) triggers: "a clone synced with upgrade"; none trigger: the clone is NOT named and rev 4 is told (PLAN §4.2's "re-synced" wording in "who searches it" is reworded by rev 4). FAIL: step 1 does not start: stop rule 6.8. `uv sync` refuses the project (requires-python or build error): record the text; sub-cases are reported as "not testable", the clone is not named.

#### 3.F4 Take F4: `uvx freecad-mcp` with no version pinned, after the cache is gone

(a) Starting state: the container of take F3; `uv cache clean |& tee out/fx4/F4/cache-clean.txt`; `ls -la "$(uv cache dir)" |& tee out/fx4/F4/cache-after-clean.txt`.

(b) Commands, in order:
1. `timeout 60 uvx freecad-mcp |& tee out/fx4/F4/unpinned-run.txt; echo "exit=${PIPESTATUS[0]}" | tee out/fx4/F4/unpinned-run-exit.txt` — event `unpinned: typed`; event `unpinned: traceback` or `unpinned: waits` (whichever happens).
2. `uvx --from freecad-mcp python -c "import importlib.metadata as m; print(m.version('freecad-mcp'), m.version('mcp'))" |& tee out/fx4/F4/unpinned-versions.txt` (which freecad-mcp and which mcp the unpinned line resolved today).
3. For the record, the unpinned line in the July state: `timeout 8 uvx --exclude-newer 2026-07-27T00:00:00Z freecad-mcp |& tee out/fx4/F4/unpinned-july.txt; echo "exit=${PIPESTATUS[0]}" | tee out/fx4/F4/unpinned-july-exit.txt`; `uvx --exclude-newer 2026-07-27T00:00:00Z --from freecad-mcp python -c "import importlib.metadata as m; print(m.version('freecad-mcp'), m.version('mcp'))" |& tee out/fx4/F4/unpinned-july-versions.txt` (expected 0.1.19 and a 1.x: the July user of the unpinned line ran 0.1.19).

(c) Events: `unpinned: typed`, `unpinned: traceback` or `unpinned: waits`.

(d) Capture: out/fx4/F4/rec.mkv, events.tsv, cache-clean.txt, cache-after-clean.txt, unpinned-run.txt, unpinned-run-exit.txt, unpinned-versions.txt, unpinned-july.txt, unpinned-july-exit.txt, unpinned-july-versions.txt.

(e) EXPECTED: measure. By PLAN §4.1's PyPI metadata an unpinned run today resolves freecad-mcp 0.1.28, which has the rewritten import and starts; so the expected outcome is "starts", i.e. NOT a trigger, and the test is kept because Q8 asks for it and because the answer is the F13 lesson ("Lesson one pins the plug's version for exactly this reason" is then qualified in rev 4: the unpinned user got the fix for free, the pinned user did not).

(f) PASS-trigger: the traceback prints (then the unpinned line resolved a freecad-mcp older than 0.1.20, which unpinned-versions.txt shows; name "an unpinned uvx line after the cache is gone" in F4). PASS-not-a-trigger: it starts with 0.1.28: not named in F4; rev 4 is told, with the versions file, so the F14 clause about pinning is checked against it. FAIL: the unpinned run resolves 0.1.28 and still prints a traceback: stop rule 6.2.

### 3.R1 is section 4.

## 4. The Claude run R1 (pre-registered)

Prompt, one wording: the verbatim contents of out/fx4/A/traceback-0.1.19.txt (the full traceback as printed by take A, hint and all, nothing removed), then one blank line, then exactly:

```
what do I change?
```

No other text, no file attached, no system prompt, no CLAUDE.md in the folder. The prompt is prepared as out/fx4/runs/R1/prompt.txt before the run (`cat out/fx4/A/traceback-0.1.19.txt | tee out/fx4/runs/R1/prompt.txt; printf '\nwhat do I change?\n' | tee -a out/fx4/runs/R1/prompt.txt`) and pasted into Claude Code from that file so the wording cannot drift.

State before the run: a fresh container from the lesson 7 image with Claude Code signed in as lesson 7; NO plug connected (`claude mcp list | tee out/fx4/runs/R1/mcp-list-before.txt`: "No MCP servers configured. Use `claude mcp add` to add a server."; if take C's user-scope entry is present in this home, `claude mcp remove --scope user freecad` first and list again); working folder /home/maker/r1, empty (`ls -la ~/r1 | tee out/fx4/runs/R1/ls-before.txt`); auto mode as lesson 7 (the same permission setting lesson 7's R1 used, written into out/fx4/runs/R1/mode.txt from the lab's lesson 7 record); `claude --version | tee out/fx4/runs/R1/claude-version.txt`; uv 0.13.6 on PATH (Claude Code may run `uvx` itself in auto mode; that is allowed and recorded, not prevented). Recording out/fx4/runs/R1/rec.mkv starts before `claude` is typed.

Events: `claude: typed`, `prompt: traceback pasted` (the paste is complete and Enter is pressed), `turn 1: reply done` (the reply has finished and the greyed suggested next prompt is visible). If Claude Code runs tools before replying, each tool call is an extra event `turn 1: tool N` (N = 1, 2, ...), named for the cut.

Outcome classes, exactly PLAN §4.7, scored on the reply text of turn 1 only:
- A: the reply names the mcp 2 rename (FastMCP to MCPServer, or "mcp 2" / "mcp.server.mcpserver", or the migration page) AND gives the pin (mcp[cli] below 2, in any spelling) or the update (run a newer freecad-mcp / 0.1.20 or later / 0.1.28). Storyboard: F11 narration "[lab: the rename and the pin ...]" reads "the rename and the pin" or "the rename and the update" as applicable; label "matches".
- B: the reply says reinstall or `pip install mcp` (or `pip install --upgrade mcp`, `uv pip install mcp`, reinstall freecad-mcp without a version) and does not give the pin or a versioned update. Storyboard: F11 reads "a reinstall"; label "half"; the clause "If it said pip install mcp, that is half: it installs version 2 again" is spoken.
- C: the reply says edit the server's import to `mcp.server.mcpserver` (or to MCPServer) as the fix, and does not give the pin or the update. Storyboard: F11 reads "edit the import"; label "half"; the clause "[lab: if it said edit the import: half, that fixes the code you do not run; you run the published plug]" is spoken.
- Mixed replies: if the reply contains an A element (pin or versioned update together with the rename), it is A even if it also mentions B or C options. If it gives the pin or the update WITHOUT naming the rename: A with the note "pin without the cause"; F11's "[lab: the rename and the pin ...]" reads "the pin, but not why" and the label stays "matches" (the pin matches the evidence line). If the reply contains none of A, B, C (for example it blames FreeCAD, the PATH, or asks a question back): class "none"; label "does not match"; stop rule 6.9 (report before the storyboard reads it).

Evidence frame: take B `metadata: 2.x printed` (F5, the installed-version line showing mcp 2.x in the 0.1.19 set of parts). "Matches" means the reply's diagnosis agrees with that line: the installed mcp is a 2.x and the fix is to go below 2 or to a rewritten plug.

Record: out/fx4/runs/R1/prompt.txt; session.jsonl (copied from Claude Code's session folder after the run: the model name, every tool call and its input/output, the reply verbatim); reply.txt (the reply verbatim, copied from session.jsonl, not retyped); cost.txt (`/cost` output pasted, or the cost line from the session; "n = 1"); model.txt (from session.jsonl); tools.txt (the list of tool calls in order, or "none"); claude-version.txt; mode.txt; outcome.txt (one of A, B, C, none, plus the mixed-reply note); label.txt ("matches", "half" or "does not match"); screenshot suggested-prompt-crop.png showing where the greyed suggested next prompt sits so the editor crops it (SCRIPT-L7 §0 R1: "cropped out"); ls-before.txt, mcp-list-before.txt.

Rule: one run, scored before it runs (this section is the score sheet), no second try. If the run is interrupted by an error outside the reply (sign-in, network, a crash before `turn 1: reply done`), the run is recorded as "no result" in outcome.txt with the error text, and rev 4 decides; it is not re-run inside this lab without a new prereg commit. No message 2.

## 5. Measurements table

| value | where it is used (frame / description line) | how measured | expected | source |
|---|---|---|---|---|
| `sys.version` of the FreeCAD 1.1.4 AppImage's Python | F8 label "this FreeCAD: Python 3.11.x", F9 card-engines-1, F8/F9/F12 narration digits, Short fx4-02 S1; SCRIPT §0 pins | take E2, console `import sys; print(sys.version)` | starts with 3.11 | PLAN §4.1 (Linux AppImage read in the console; "never a universal"); ACCURACY E row 11 |
| mcp version `uvx freecad-mcp@0.1.19` resolves on the take day | SCRIPT §0 pins; description "Tested: ... mcp [lab]"; F5 "version 2 point [lab]"; S1 | take B step 1 | 2.3.0 | PLAN §4.1, Q8 |
| Claude Code exact build | SCRIPT §0 pins | `claude --version` at run start, out/fx4/pins.txt and runs/R1/claude-version.txt | 2.1.31x | SCRIPT §0 |
| R1 model | SCRIPT §0 pins; F11 chip | session.jsonl | claude-sonnet-5-5 | SCRIPT §0 (as lesson 7) |
| FULL last line of the 0.1.19 traceback, and its form (long stub / bare) | F0 (zoom on the first clause, the rest wrapped), F5's 4 s return with "pin 'mcp' below 2" lit, S0; thumbnail; the stub-vs-bare rule | take A steps 1-2, last-line.txt, last-line-chars.txt, last-line-form.txt | long form, about 330 characters, beginning with the bare clause; form = 1 | ACCURACY E rows 4-5; PLAN §4.1, Q8; SCRIPT §0 take A |
| 0.1.19 fails, 0.1.20 starts and waits on stdin | F6 "0.1.20: rewritten for the new name", §4.1 "0.1.19 is the last failing version" | take A steps 1, 3, 4 | fails / waits | PLAN §4.1; ACCURACY E row 6; SCRIPT §0 take A "[lab: confirm]" |
| mcp version in the 0.1.19 set of parts (the metadata line) | F5 "what it got", S1, F11 evidence frame | take B step 1 | 2.x (2.3.0) | SCRIPT §0 take B |
| mcp version with the pin | F5 "pinned", "1 point [lab]" | take B step 2 | 1.x (1.30.0) | SCRIPT §0 take B; PLAN Q8 |
| 0.1.28's declared bound | F6 "below 3 [lab: confirm the bound]", F13 question, description | take B step 3, `m.requires('freecad-mcp')` | mcp[cli] at least 1.28.1 and below 3 (real signs in the fence in 3.B) | PLAN §4.1; ACCURACY E row 6 |
| Does `uvx` accept `python` with `--from`; the working line | description "the working `uvx --from ... python -c` form"; §4.6 step 4 | take B steps 1 and 4, working-form.txt | measure | PLAN Q8, §4.3; SCRIPT §0 take B |
| `uvx --with` the pin `freecad-mcp@0.1.19` starts and waits | F6 "workaround", S2 | take C steps 1-2 | waits | PLAN §4.6 step 2, issue #98; SCRIPT §0 take C |
| "Added ..." text of the add line | F1, F6 (0.1.28 lit) | take C step 3 | "Added stdio MCP server freecad with command: uvx freecad-mcp@0.1.28 to user config" | SCRIPT-L7 §0 take A wording; SCRIPT §0 take C "[as printed, lab]" |
| `claude mcp list` Connected line | F1, F6, F14, S2, S3 | take C steps 4 and 6 | contains "Connected" (lesson 7: "✔ Connected") | SCRIPT §0 take C "[lab: exact line]" |
| `claude mcp get freecad` output | F13 your-turn | take C step 5 | measure; shows freecad-mcp@0.1.28 | SCRIPT §0 take C "[lab]" |
| PyPI 0.1.19 JSON readable in Firefox (else issue #98) | F3 | take D steps 2-3, readable.txt | measure | PLAN Q8; SCRIPT §0 take D |
| Does the image already have a 3.12 | SCRIPT §0 take E "[lab: ... then build a 3.11-only image]" | take E0 | measure | PLAN Q8 |
| pip's exact text under 3.11 | F8 (lit lines), S0 of fx4-02 | take E1 step 1, E1-pip-lit-lines.txt | Requires-Python at least 3.12 and "No matching distribution found" (real sign in the fence in 3.E1) | PLAN Q8, F8; ACCURACY E row 9 |
| uv's CPython 3.12 download line | F10 (lit), fx4-02 S2, narration "[lab: the line it prints]" | take E1 step 3, E1-download-line.txt | measure | PLAN Q8, F10; ACCURACY E row 13 |
| The confirmed fresh-install triggers | F4 card-bound-4 and clause, §4.5 "[lab: the confirmed triggers]", F14 pin clause check | takes F1-F4, one PASS-trigger / PASS-not-a-trigger each | measure (expected by metadata: F1 trigger, F2 trigger, F3 depends on the lock, F4 not a trigger) | PLAN §4.1 last bullet, Q8; ACCURACY E row 12 |
| R1 outcome A/B/C, reply, cost, n = 1 | F11 narration and type-on | section 4 | measure | PLAN §4.7, Q11; SCRIPT §0 R1 |
| R1 label matches / half / does not match | F11 label | section 4, label.txt | measure | SCRIPT §0 R1 |
| Status-bar text after Start RPC Server (0.1.28 add-on) | description only | take E2 step 4 | "RPC Server started at 127.0.0.1:9875" | PLAN Q10 (lesson 7) |
| Take folder names | SCRIPT header "[lab: folder]" | this file | out/fx4/A..F4, out/fx4/runs/R1 | SCRIPT header |
| The take day (DATE) | description "Tested: ... Linux (Docker), DATE" | pins.txt | measure | PLAN §4.3 |

## 6. Stop rules

6.1 `uvx freecad-mcp@0.1.19` starts, or take B step 1 prints a 1.x, or the PyPI JSON shows a bound on 0.1.19's mcp line: the video's premise (an unbounded list resolving 2.x today) does not hold on the take day. Stop; report the resolved version and the JSON line; no take is re-done. Fallback named by the plan: none for this case (Open 8 lets the owner choose to film 2.0.0 via `--with "mcp[cli]==2.0.0"`, but that is an owner decision, not a lab fallback).

6.2 `uvx freecad-mcp@0.1.20` prints a traceback (or F4's unpinned 0.1.28 does): "0.1.19 is the last failing version" and "0.1.20 rewritten for the new name" are not confirmed. Stop; report the traceback; the do-not-say rule (ACCURACY E: no version named "the last failing one" before the lab confirms) holds and rev 4 reworks F6.

6.3 The pin does not help (take B step 2 prints 2.x after `--refresh`, or take C step 1 prints the traceback): stop; report both outputs and the uv version; the workaround clauses (F5, F6, F7, F12, S2) cannot be filmed as written.

6.4 `claude mcp list` prints a failure other than lesson 7's ENOENT after one login-shell retry: stop; copy the full line; F1/F6/F14 are blocked.

6.5 Firefox or the FreeCAD AppImage does not start in Xvfb (take D or E2): record the error text (`|& tee`), try once with Mesa's software renderer env as the lesson 7 image notes, then stop and report. Fallbacks: for D, none in the plan (the JSON text is kept as pypi-0.1.19-json.txt and rev 4 decides whether a typed card replaces F3; the plan's own fallback, issue #98, also needs Firefox); for E2, the F8 label "this FreeCAD: 3.11.x" cannot be filled and is removed until measured (PLAN §4.1: never "FreeCAD ships 3.11" as a universal); Q10 falls back to lesson 7's text.

6.6 pip installs freecad-mcp under 3.11, or uvx in `fx4-py311` prints no download line after one image rebuild: the cousin does not reproduce. Stop; report; Open 4 (cut F8-F10 to the fx4-02 Short or drop them) goes to the producer; retime.py is rerun by rev 4.

6.7 The AppImage's Python is 3.12 or later: the "two engines" half (F8-F10, fx4-02) loses its premise on Linux. Stop; report the version; Open 4 decides.

6.8 The July state cannot be built (`--exclude-newer` not accepted by uvx or `uv lock` in 0.13.6, or no 1.x satisfies 0.1.19 at that date): takes F1 and F3 cannot show "ran last month"; record the error; takes F2 and F4 still run; F4's card names only F2's trigger (if PASS) and the F4 clause is shortened; rev 4 is told to rerun retime.py.

6.9 R1 returns class "none" or "no result": stop before F11 is written; report the reply verbatim; rev 4 decides the F11 wording (the plan's F11 has no text for a reply outside A/B/C).

6.10 Any dialog, prompt or line whose text differs from the expected quote (the release page wording, the "Added ..." line, the Connected line, pip's lines, uv's lines): not a stop; record the actual text and use it as the lit words; list every such difference in the deliverables.

6.11 Windows-only steps: none in fx4 (PLAN §4.8 "Cannot reproduce: nothing Windows-specific here").

6.12 Any spoken addition the lab's values would force before F10 (for example a longer trigger list in F4) is not made by the lab: the values are reported and rev 4 reruns retime.py (SCRIPT §4: the pitch sits at 66%, the top of the window).

## 7. Deliverables back to Cowork

Files (all under out/fx4/ in freecad-course-lab, committed after the runs; this file's commit hash is in pins.txt):
- pins.txt, pins-mcp-resolved.txt
- A/: rec.mkv, events.tsv, traceback-0.1.19.txt, last-line.txt, last-line-chars.txt, last-line-form.txt, traceback-full.png, 0.1.20.txt, 0.1.20-exit.txt, test-0.1.20.txt, test-0.1.19.txt, uv-install.txt, uv-cache-dir.txt, cache-before.txt, cache-after.txt
- B/: rec.mkv, events.tsv, metadata-0.1.19.txt, metadata-pinned.txt, metadata-0.1.28.txt, working-form.txt, python-form-N.txt (if any)
- C/: rec.mkv, events.tsv, mcp-list-before.txt, pinned-0.1.19.txt, pinned-0.1.19-exit.txt, test-pinned.txt, add-0.1.28.txt, list.txt, list-2.txt, get-freecad.txt, user-config-mcp.txt
- D/: rec.mkv, events.tsv, release-v2.0.0.png, pypi-0.1.19-json.png, pypi-0.1.19-json.txt, readable.txt, issue-98.png (if any), pypi-0.1.28.png
- E/: Dockerfile-py311.txt, E0-*.txt, rec-E1.mkv, events-E1.tsv, E1-*.txt, E1-image-inspect.json, rec-E2.mkv, events-E2.tsv, E2-*.txt, E2-*.png
- F1/, F2/, F3/, F4/: rec.mkv, events.tsv and the files listed in 3.F1-3.F4 (F3 also the three .lock copies)
- runs/R1/: rec.mkv, events.tsv, prompt.txt, session.jsonl, reply.txt, cost.txt, model.txt, tools.txt, claude-version.txt, mode.txt, outcome.txt, label.txt, suggested-prompt-crop.png, ls-before.txt, mcp-list-before.txt
- tools/test_mcp.py (in the repo root tools folder)
- out/fx4/ANSWERS.md: the one-line answers below, filled

One-line answers to section 2, to be filled (the lab writes the measured value after the colon; the frame it feeds is in section 5):
- 8a: 0.1.19 traceback yes/no; 0.1.20 waits yes/no (exit code, test_mcp reply).
- 8b: mcp version resolved by 0.1.19 on the take day: [value].
- 8c: the full last line verbatim (pasted from last-line.txt), its character count, form = long stub / bare; the stub-vs-bare rule applied: keep / cut F0 label, F2 stub clause, F5 clause (+ retime.py rerun).
- 8d: metadata 0.1.19: [2.x]; with the pin: [1.x]; 0.1.28 requires line: [verbatim].
- 8e: `python` accepted with `--from`: yes/no; the working line: [verbatim command].
- 8f: pinned 0.1.19 waits: yes/no.
- 8g: triggers: F1 cleared cache: trigger / not (baseline used: uvx env / installed tool; installed tool survives clean: yes/no); F2 new machine: trigger / not; F3 re-synced clone: (i) lock committed: trigger / not; (ii) upgrade: trigger / not; (iii) no lock: trigger / not; (iv) old uv run form: trigger / not; chosen F4 wording: [one of the allowed wordings]; F4 unpinned: trigger / not, resolved freecad-mcp [version] and mcp [version].
- 8h: pip's lines verbatim: [Requires-Python line], [No matching distribution line], pip version [value].
- 8i: uv's download line verbatim: [value]; the plug then waits: yes/no.
- 8j: the lesson 7 image has a 3.12: yes/no (system / uv-managed); E1 ran in fx4-py311: yes/no.
- 8k: sys.version: [verbatim]; the label reads "this FreeCAD: Python [3 fields]".
- 8l: PyPI JSON readable in Firefox: yes/no; F3 films: JSON / issue #98.
- 10: status-bar text: [verbatim] (same as lesson 7: yes/no).
- 11: R1 outcome: A / B / C / none; label: matches / half / does not match; model [value]; cost [value]; tool calls [list or none]; Claude Code build [value]; the reply verbatim is in runs/R1/reply.txt; suggested prompt cropped: yes.
- Deviations list (every actual text that differed from an expected quote, stop rule 6.10) and every stop rule that fired, with the file that shows it.
