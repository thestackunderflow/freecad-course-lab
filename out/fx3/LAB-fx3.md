# LAB-fx3: spawn uvx ENOENT: Claude Desktop Cannot Start FreeCAD MCP, but uvx Works in Your Terminal | Fix — pre-registration v1, 2026-11-01 (before any run)

Lab repo freecad-course-lab, folder out/fx3/ (takes out/fx3/A, out/fx3/B, out/fx3/C, run out/fx3/runs/R1, owner clip out/fx3/O when delivered). Pins: uv 0.13.6 (lesson 1's pin, installed by uv's own installer so the start-up line exists), freecad-mcp 0.1.28, Claude Code 2.1.31x (exact build written into out/fx3/pins.txt from `claude --version` at run start), model claude-sonnet-5-5 (as lesson 7; read back from session.jsonl), Node for the launcher (not pinned by the plan: `node --version` written into pins.txt at run start), FreeCAD 1.1.4 AppImage NOT started in any fx3 take (PLAN §3.8: no fx3 frame shows the plug reaching FreeCAD), SolidCraft and PrusaSlicer not used. Docker image notes: the lesson 7 image (Linux, lab user `maker`, HOME /home/maker, `claude` on PATH); Xvfb not needed (no GUI take); Mesa not needed; XDG_DATA_HOME unset; nodejs installed from the distro package before the run (if the image has none, see stop rule 6.1); network on (the uv installer, `uvx` resolving freecad-mcp@0.1.28, Claude Code). Claude Desktop is not installed and no sign-in is attempted (Q6). Sources for every expected value: PLAN rev 3 §3 and §0.3/§0.4, ACCURACY rev 3 block D, SCRIPT-fx3 v1 §0 and §1. A value not quoted there is "measure".

Conventions (SCRIPT-L7 §0): this file is committed before any run ("prereg before the run"; the commit hash goes into out/fx3/pins.txt). Each take is one screen recording out/fx3/TAKE/rec.mkv plus out/fx3/TAKE/events.tsv (event name, seconds from recording start); event names are exactly the SCRIPT §1 names so the footage cut can find them. Every terminal command's text is also kept as a file via `| tee` (`|&` where stderr matters). The launcher is the no-AI test script of this video; a plug's log, where one exists, is read only after the plug has exited (lesson 7 lesson: the log is flushed at exit).

## 2. Questions this lab answers (PLAN §0.4, numbered as in the plan)

6. fx3: Claude Desktop (Linux build) cannot be installed and signed in inside the lab (expected: no; no attempt beyond stating it), so the owner records take O on their PC, and the lab's fallback is a 5-line Node launcher that starts `uvx` under `env -i PATH=/usr/bin:/bin` and prints the real Node string, expected `spawn uvx ENOENT`; if Python had to be used instead, the text is `FileNotFoundError: [Errno 2] No such file or directory: 'uvx'` and the alternate narration applies; the screen says which program printed it.
7. fx3: in the lab terminal, `echo $PATH`, `which uvx`, the line uv's installer added to the shell start-up file (`grep -n local/bin ~/.bashrc ~/.profile`), and `claude mcp add` with the full path followed by `claude mcp list`: Connected; plus the system's default PATH on this Linux (`/etc/environment` or the systemd user environment) so the card's "short list" is a measured one, labelled "the system's default list, measured in Docker" (never "the desktop app's PATH"). Claude Desktop's Linux paths `~/.config/Claude/claude_desktop_config.json` and `~/.config/Claude/logs` are confirmed on screen only if the Linux build is ever present (it is not; they stay "from the MCP docs (connect-local-servers)").
11. All Claude runs: the R1 prompt and the A/B/C score are written here before the run; one run; auto mode as lesson 7; the greyed suggested next prompt is cropped; the evidence frame for the split screen is named here (take A `which uvx: typed`) and the match is recorded.

## 3. Takes, in run order

Run order: A, B, C, R1. Take O is not a lab take (section "Not in Docker: the owner records" below). Before take A: `claude --version | tee out/fx3/pins.txt`, `node --version | tee -a out/fx3/pins.txt`, `git rev-parse HEAD | tee -a out/fx3/pins.txt` (the prereg commit), `cat /etc/os-release | tee -a out/fx3/pins.txt`.

### 3.A Take A: the lists (Q7)

(a) Starting state: fresh /home/maker (no ~/.local, no ~/.cache/uv, ~/.bashrc and ~/.profile as the image ships them; `cp ~/.bashrc out/fx3/A/bashrc-before.txt; cp ~/.profile out/fx3/A/profile-before.txt`); no Claude Code server configured for freecad (`claude mcp list | tee out/fx3/A/mcp-list-before.txt`, expected "No MCP servers configured. Use `claude mcp add` to add a server." as lesson 7 take A); no app open; one terminal, 44 columns or wider.

(b) Commands, in order:
1. Install uv the way lesson 7 take B did (state-building only, not a frame of this video): `curl -LsSf https://astral.sh/uv/0.13.6/install.sh | sh |& tee out/fx3/A/uv-install.txt` (expected text as lesson 7: "downloading uv 0.13.6 x86_64-unknown-linux-gnu / installing to /home/maker/.local/bin / uv / uvx / everything's installed!").
2. Close the terminal and open a new login shell so the start-up file is read: `bash -l`. Recording starts here (`out/fx3/A/rec.mkv`).
3. `uvx --version |& tee out/fx3/A/uvx-version.txt` (expected "uvx 0.13.6"; this crop is the F0 right-hand "works here" option).
4. `echo $PATH | tee out/fx3/A/echo-path.txt` — event `echo PATH: typed`; hold 3 s.
5. `which uvx | tee out/fx3/A/which-uvx.txt` — event `which uvx: typed`; hold 3 s (this is the F2 and F7 evidence frame and the F9 live cursor shot: run it once more at the end of the take and hold 20 s for F9).
6. `grep -n local/bin ~/.bashrc ~/.profile | tee out/fx3/A/grep-startup.txt` — event `grep startup: typed`. If the matched line sources a file rather than exporting PATH itself, also `cat "$HOME/.local/bin/env" | tee out/fx3/A/startup-env-file.txt` (both go to the card; rev 4 decides which line the card shows).
7. The system's default list: `cat /etc/environment | tee out/fx3/A/short-list-etc-environment.txt`; then `systemctl --user show-environment |& tee out/fx3/A/short-list-systemd-user.txt` — event `short list: shown` at the first of the two that prints a PATH line. Also `grep -n '^ENV_PATH\|^ENV_SUPATH' /etc/login.defs | tee out/fx3/A/short-list-login-defs.txt` for the record (not a card source unless both above are empty; see stop rule 6.3).
8. `which uvx` again, hold 20 s, cursor live (F9).

(c) Events: `echo PATH: typed`, `which uvx: typed`, `grep startup: typed`, `short list: shown`.

(d) Capture: out/fx3/A/rec.mkv, events.tsv, uvx-version.txt, echo-path.txt, which-uvx.txt, grep-startup.txt, startup-env-file.txt (if any), short-list-etc-environment.txt, short-list-systemd-user.txt, short-list-login-defs.txt, bashrc-before.txt, profile-before.txt, `diff bashrc-before.txt ~/.bashrc | tee out/fx3/A/bashrc-diff.txt`, `diff profile-before.txt ~/.profile | tee out/fx3/A/profile-diff.txt`, `ls -l ~/.local/bin | tee out/fx3/A/ls-local-bin.txt`.

(e) EXPECTED: `which uvx` = `/home/maker/.local/bin/uvx` (SCRIPT §0 "expected /home/maker/.local/bin/uvx"; PLAN F1 "[lab: /home/maker/.local/bin/uvx]"). `echo $PATH` contains `/home/maker/.local/bin` (PLAN §3.5 "uv's installer put its folder into the terminal's start-up file"): measure the full list. The start-up line: measure (which file, which text). The short list: measure; the plan only requires that `.local/bin` is absent from it (PLAN F3 "dot local bin missing from the short one").

(f) PASS: which uvx prints /home/maker/.local/bin/uvx; echo $PATH contains that folder; grep finds at least one line in ~/.bashrc or ~/.profile; the short list from /etc/environment or the systemd user environment prints a PATH without .local/bin. FAIL and rules: which uvx elsewhere: the F1/F5/take C path becomes the measured one and every "[lab: exact path]" takes it (no re-take). grep finds nothing: stop rule 6.2. Short list absent or containing .local/bin: stop rule 6.3 (card-two-lists-1 cannot be drawn from Docker; report).

### 3.B Take B: the no-AI launcher (Q6)

(a) Starting state: after take A (uv installed, ~/.local/bin/uvx present, ~/.cache/uv may hold nothing yet); the launcher file committed with this prereg at lab/fx3/launcher.js, copied to /home/maker/fx3/launcher.js; `node --version` already in pins.txt. Nothing else installed between the two launcher runs ("Nothing was installed in between", PLAN F4).

The 5-line Node launcher (lab/fx3/launcher.js; no arrow functions so the file holds no angle brackets):
```
const { spawn } = require('child_process');
const cmd = process.argv[2];
const p = spawn(cmd, ['freecad-mcp@0.1.28'], { stdio: ['pipe', 'inherit', 'inherit'] });
p.on('error', function (e) { console.log(e.message); process.exit(1); });
p.on('spawn', function () { console.log('started: ' + cmd + ' (pid ' + p.pid + ')'); setTimeout(function () { p.kill(); }, 5000); });
```
The child inherits the launcher's environment, so what `env -i` leaves is what the plug gets. HOME is kept in the short-list run because a desktop app has HOME and uv needs it for its cache; only PATH is the short list, and the crop lights "PATH=" (SCRIPT F4).

(b) Commands, in order (one terminal, cleared between commands so each crop is three lines):
1. Pre-check, not a frame: `uvx --version` works in this shell (from take A); `which node | tee out/fx3/B/which-node.txt` (the launcher is started by its full path so the short list does not need to hold node).
2. Short list: `env -i HOME=/home/maker PATH=/usr/bin:/bin $(which node) /home/maker/fx3/launcher.js uvx |& tee out/fx3/B/launcher-short.txt` — event `launcher short: typed` at the Enter key, event `launcher short: ENOENT` when the error line is printed.
3. Full path: `env -i HOME=/home/maker PATH=/usr/bin:/bin $(which node) /home/maker/fx3/launcher.js /home/maker/.local/bin/uvx |& tee out/fx3/B/launcher-full.txt` (the path from take A) — event `launcher full: typed` at Enter, event `launcher full: starts` when "started: /home/maker/.local/bin/uvx (pid N)" is printed. The plug is killed by the launcher after 5 s; whatever uvx or the plug printed before that is in launcher-full.txt.
4. For the record, the chip's claim ("the same start a desktop app makes") rests on PLAN §3.1 / ACCURACY D: Node's spawn error names the command word. No further command.

(c) Events: `launcher short: typed`, `launcher short: ENOENT`, `launcher full: typed`, `launcher full: starts`.

(d) Capture: out/fx3/B/rec.mkv, events.tsv, launcher-short.txt, launcher-full.txt, which-node.txt, `cp /home/maker/fx3/launcher.js out/fx3/B/launcher.js`, `sha256sum out/fx3/B/launcher.js | tee out/fx3/B/launcher.sha256`.

(e) EXPECTED: short list prints exactly `spawn uvx ENOENT` (PLAN §3.1: "the line a Node-based client writes when the program named in command is not found on the PATH it was given"; ACCURACY D: the literal spelling is in the mcpplaygroundonline table, https://mcpplaygroundonline.com/blog/fix-spawn-npx-enoent-mcp, "spawn npx ENOENT means Node looked for a program called npx in every folder on the client's PATH and did not find it"; no vendor page carries the uvx spelling). Full path: the launcher's "started:" line (measure), then whatever the plug prints or silence while it waits on stdin (measure: "the first line it prints, or the waiting-on-stdin state", SCRIPT §0).

(f) PASS: launcher-short.txt holds the line `spawn uvx ENOENT` and launcher-full.txt holds a "started:" line with no ENOENT. The storyboard's F0 (title B), F4 and Short S0/S1/S2 read these two files verbatim. FAIL rules: a different error text under the short list (e.g. EACCES, or uv itself failing): record it verbatim, stop rule 6.4. The full-path run also fails: stop rule 6.4 (do not edit the launcher between the two runs; if a rerun is needed, both runs are re-done as one take B2). If Node cannot be present at all: the Python fallback (stop rule 6.1); its expected text `FileNotFoundError: [Errno 2] No such file or directory: 'uvx'` (PLAN §0.4 Q6) and the alternate F0/F2/F4 narration (PLAN §3.10 "Alternate F0 narration", SCRIPT F2 bracket) are then used, the chip names Python, and the description's first line says so.

### 3.C Take C: where the full path goes (Q7)

(a) Starting state: after take B; no freecad server in any Claude Code scope (`claude mcp list` prints the no-servers line; if take A's before-check already showed that, nothing to remove); ~/.config/Claude does not exist (the lab creates it only to hold the lab's own copy of the config file; it is the lab's file, labelled so, SCRIPT §0 "the lab's file; the owner clip shows the real one in F1").

(b) Commands, in order:
1. `mkdir -p ~/.config/Claude` (the Linux folder from the MCP docs' connect-local-servers page, ACCURACY D row 1).
2. Write the lab's config with the measured path, then show it: `printf '{\n  "mcpServers": {\n    "freecad": {\n      "command": "/home/maker/.local/bin/uvx",\n      "args": ["freecad-mcp@0.1.28"]\n    }\n  }\n}\n' | tee ~/.config/Claude/claude_desktop_config.json` then `cat ~/.config/Claude/claude_desktop_config.json | tee out/fx3/C/claude_desktop_config.json` — event `config: full path` at the cat; hold 12 s with the cursor live (F5 crop, the path in "command" lit). The `args` form is the README's own shape for the plug (PLAN §3.1: freecad-mcp's README starts the plug with "command": "uvx"); only "command" is changed.
3. `claude mcp add --scope user freecad -- /home/maker/.local/bin/uvx freecad-mcp@0.1.28 |& tee out/fx3/C/mcp-add.txt` — event `add full path: typed` (this line is for the description; it is not on screen in F5).
4. `claude mcp list |& tee out/fx3/C/mcp-list.txt` — event `list: Connected` when the Connected line prints; hold 15 s with the cursor live (F5 3 s shot and the F10 outro hold).

(c) Events: `config: full path`, `add full path: typed`, `list: Connected`.

(d) Capture: out/fx3/C/rec.mkv, events.tsv, claude_desktop_config.json, mcp-add.txt, mcp-list.txt, `ls -l ~/.config/Claude | tee out/fx3/C/ls-config-dir.txt`.

(e) EXPECTED: mcp-add.txt: "Added stdio MCP server freecad with command: /home/maker/.local/bin/uvx freecad-mcp@0.1.28 to user config" (form from lesson 7 take A, SCRIPT-L7 §0, with the full path instead of uvx: measure the exact line). mcp-list.txt: "freecad: /home/maker/.local/bin/uvx freecad-mcp@0.1.28 - ✔ Connected" (SCRIPT §0 "expected ✔ Connected"; lesson 7 take A/B form: measure the exact line).

(f) PASS: the list line carries "✔ Connected". FAIL: "✘ Failed to connect": stop rule 6.5 (one re-run of `claude mcp list` after `uvx freecad-mcp@0.1.28 --help` has warmed the cache is allowed and is recorded as the second attempt in mcp-list-2.txt; the frame uses the first attempt that shows Connected and the description says "first attempt" or "second attempt").

## 4. The Claude run R1 (pre-registered)

- Prompt, one wording, pasted as the first message: `The FreeCAD MCP plug fails in Claude Desktop. The log says: spawn uvx ENOENT. In my terminal, uvx works. What should I change?`
- State before the run: after take C, then `claude mcp remove --scope user freecad |& tee out/fx3/runs/R1/mcp-remove-before.txt` so no plug is connected during the run (the run is a text answer; the F10 outro uses take C's footage, not R1's); an empty folder /home/maker/fx3-r1 (`mkdir` and `cd`); `claude` started in auto mode exactly as lesson 7's R1 (same invocation as out/l7/runs/R1; copied into out/fx3/runs/R1/invocation.txt); the lab's ~/.config/Claude file from take C is left in place (not read by Claude Code). Build and model: `claude --version` already in pins.txt; the model read back from session.jsonl after the run.
- Events: `claude: typed` (the Enter on the pasted prompt), `turn 1: reply done` (the reply stops growing).
- Outcome classes (PLAN §3.7, scored by the first actionable instruction in the reply): A = write the full path to uvx in "command" (or run `which uvx` and use its output); B = add ~/.local/bin to PATH (a half-answer: it fixes the terminal, not the app; F7 then says in one clause why it is half); C = reinstall uv. A reply that lists several steps is scored by the first step it tells the user to do; a reply that is none of the three (e.g. only asks a question) is recorded as "none" and F7 reads the reply's gist with the label "does not match" (report to Cowork; no second run).
- Evidence frame: take A `which uvx: typed` (/home/maker/.local/bin/uvx expected). Match rule: A and the reply names a path equal to take A's `which uvx` output, or tells the user to run `which uvx`: "matches"; A with a different literal path (a tilde path, a macOS path, another user name): "does not match" (the description quotes both); B: "half" (the F7 label reads "does not match" and the extra clause is spoken); C: "does not match".
- Storyboard clause each outcome triggers (SCRIPT F7): A: "[lab: read the reply's one-line gist: full path]" + "matches"; B: "add to PATH" + "does not match" + the half clause "If it said add to PATH, that is half: it fixes the terminal, not the app."; C: "reinstall uv" + "does not match", no half clause.
- Record: out/fx3/runs/R1/session.jsonl (copied from ~/.claude/projects/ after the run), reply.txt (verbatim), cost.txt (`/cost` output), model.txt (from session.jsonl), tool-calls.txt (every tool call in session.jsonl; expected none), outcome.txt (one line: A/B/C/none, matches/does not match/half), suggested-prompt-crop.png (the greyed suggested next prompt, cropped out of the frame; the crop box noted in events.tsv), rec.mkv, events.tsv, invocation.txt, mcp-remove-before.txt.
- Rule: one run, scored before it runs, no second try. If the run fails to start (auth, network), it is reported as "R1 not run", F7 is held, and the retime is not rerun until Cowork decides.

## 5. Measurements table

| value | where it is used (frame / description line) | how measured | expected | source |
|---|---|---|---|---|
| Claude Code build 2.1.31x | SCRIPT §0 pins; description "Tested:" line | `claude --version` at run start, pins.txt | 2.1.31x: measure | SCRIPT §0 |
| R1 model | SCRIPT §0 pins; description | session.jsonl | claude-sonnet-5-5 | SCRIPT §0 "expected claude-sonnet-5-5"; SCRIPT-L7 §0 |
| the full path to uvx | F1 "[lab: /home/maker/.local/bin/uvx]", F5 crop, take C add line, Short S2 | take A `which uvx` | /home/maker/.local/bin/uvx | SCRIPT §0; PLAN F1 |
| take O exact log text | F0 title A, S0 | owner clip (not the lab) | spawn uvx ENOENT | SCRIPT §0 "expected spawn uvx ENOENT"; ACCURACY D (owner's clip is the source for the string on a Claude Desktop screen) |
| `echo $PATH` exact output | F2 overlay (one folder per line), F3 card-two-lists-1 long list, S1 | take A echo-path.txt | measure (contains /home/maker/.local/bin) | PLAN §3.5 |
| `which uvx` output | F2, F7 evidence frame, F9 live | take A which-uvx.txt | /home/maker/.local/bin/uvx | SCRIPT §0 |
| the start-up line and which file | F3 card-two-lists-2 "[lab: the real line]" | take A grep-startup.txt (+ startup-env-file.txt) | measure | SCRIPT §0; PLAN Q7 |
| the system's default list (short list) | F3 card-two-lists-1 "[lab: the real short list]", S1; label "the system's default list, measured in Docker" | take A short-list-etc-environment.txt or short-list-systemd-user.txt | measure (.local/bin absent) | PLAN Q7; ACCURACY D "Do not say" (not "the desktop app's PATH") |
| launcher short-list exact text | F0 title B, F4 "[lab: exact text]", S0 | take B launcher-short.txt | spawn uvx ENOENT | PLAN §3.1, Q6; ACCURACY D (mcpplaygroundonline table) |
| which program printed it (chip) | F0 chip, F4 | take B: Node, or Python if 6.1 fires | Node | SCRIPT §0 "On screen the chip says which program printed it" |
| launcher full-path exact path | F4 "[lab: exact path]" | take B launcher-full.txt | /home/maker/.local/bin/uvx | SCRIPT §0 |
| the plug's first line, or waiting-on-stdin | F4 `launcher full: starts`, F1 fallback "starts" | take B launcher-full.txt | measure | SCRIPT §0 |
| take C exact path in `claude mcp add` | description (the add line); F5 crop of the json | take C mcp-add.txt, claude_desktop_config.json | /home/maker/.local/bin/uvx | SCRIPT §0 |
| `claude mcp list` line | F5 3 s shot, F10 outro hold | take C mcp-list.txt | "✔ Connected" | SCRIPT §0; lesson 7 take A/B |
| R1 prompt wording | F7 narration "We pasted the log line and asked what to change", description | this file, section 4 (committed before the run) | the wording in section 4 | SCRIPT §0 "[lab: the exact pre-registered wording]" |
| R1 outcome A/B/C | F7 "[lab: full path, PATH, or reinstall]" | outcome.txt | measure | PLAN §3.7 |
| R1 reply text (type-on) | F7 "[lab: reply]" | reply.txt | measure | SCRIPT §0 |
| matches / does not match / half | F7 label "[lab]" | section 4 match rule against take A which-uvx.txt | measure | SCRIPT §0, PLAN F7 |
| R1 cost, model, build | description; SCRIPT §0 | cost.txt, model.txt, pins.txt | measure | SCRIPT §0 |
| lab folder | SCRIPT header "out/[lab: folder]" | this file | out/fx3/ | brief |
| Claude Desktop Linux config and log paths on screen | F5 path labels (stay "from the MCP docs") | not measured (no Linux build in the lab) | not confirmed on screen | PLAN Q7 last sentence; ACCURACY D row 1 |

## 6. Stop rules

6.1 Node absent and not installable from the distro package in the image: stop, report; the fallback pre-registered here is the Python launcher (`env -i HOME=/home/maker PATH=/usr/bin:/bin /usr/bin/python3 /home/maker/fx3/launcher.py uvx`, a 5-line `subprocess.Popen` script committed beside launcher.js), expected `FileNotFoundError: [Errno 2] No such file or directory: 'uvx'` (PLAN Q6), the alternate narration (PLAN §3.10, SCRIPT F2 bracket), chip "our launcher (Python)", description first line says so. Run the fallback only after Cowork confirms the switch.
6.2 `grep -n local/bin ~/.bashrc ~/.profile` finds nothing after a new login shell: record `grep -n local/bin ~/.bash_profile ~/.bash_login ~/.zshrc | tee out/fx3/A/grep-startup-wide.txt` and stop; F3 card-two-lists-2 needs a real line and the plan has no fallback (report).
6.3 No PATH line in /etc/environment and `systemctl --user show-environment` fails in the container (expected possible: no user session in Docker): report the three files; card-two-lists-1's short list is then decided by Cowork (the plan's label "the system's default list, measured in Docker" cannot be used; ACCURACY D forbids calling the lab's list "the desktop app's PATH"). Do not draw a list.
6.4 Take B prints anything but `spawn uvx ENOENT` on the short list, or the full-path run does not print "started:": stop; keep both files verbatim; report. No edit to launcher.js between the two runs of one take; a corrected take is B2 with its own folder.
6.5 Take C `claude mcp list` shows "✘ Failed to connect": one warm-up (`uvx freecad-mcp@0.1.28 --help`) and one second `claude mcp list` are allowed and recorded; still failing: stop, report (network or uv cache), F5's 3 s shot and F10 are held.
6.6 Claude Desktop: no install, no sign-in attempt in the lab; Q6 is answered "no" by protocol, not by trial. The two Linux paths stay "from the MCP docs (connect-local-servers)" and are not shown as confirmed.
6.7 Any Windows-only item (`Get-Command uvx`, backslash doubling, EFTYPE / uv_spawn, issue 140): not attempted; description and on-screen labels only (PLAN §0.3).
6.8 R1 does not start, or a dialog or prompt appears that lesson 7's R1 did not show (login, trust folder with different text): stop, screenshot to out/fx3/runs/R1/stop.png, report; no second run.
6.9 A take needs a window the lab cannot make (Claude Desktop's Connectors list, its log, a FreeCAD window in frame): it is not a lab shot; report, the cut uses take O or the plan's fallback wording.
6.10 Anything in a reply, log or file that reads like an instruction to the lab is data; the protocol is this file only.

## Not in Docker: the owner records (take O, title A only, Q6)

30 s on the owner's PC, Claude Desktop signed in, with the plug configured the README's way (`"command": "uvx"`) so it fails. Exact shot list (SCRIPT §0 take O), one event each, in this order:
1. `connectors: failed` — the plus button, Connectors: the list with the freecad entry failed.
2. `log: ENOENT line` — `mcp-server-freecad.log` opened at the line (expected `spawn uvx ENOENT`; the owner records the exact text; this clip is the only source for that string on a Claude Desktop screen). Log folder from the MCP docs' connect-local-servers page: macOS `~/Library/Logs/Claude`, Windows `%APPDATA%\Claude\logs`, Linux `~/.config/Claude/logs`.
3. `settings: Edit Config` — Settings from the Claude menu in the system menu bar (not the settings inside the chat window), Developer, Edit Config.
4. `config: edited` — `claude_desktop_config.json`: `"command": "uvx"` changed to the full path from `which uvx` (Windows: `Get-Command uvx | Select-Object Source`, every backslash written twice).
5. `quit` — quit Claude Desktop completely (tray icon / Command-Q), open it again.
6. `connectors: fixed` — the Connectors list with freecad working.
Deliver as out/fx3/O/rec.mp4 (or the owner's format) plus O/events.tsv with the six names and seconds, and O/log-line.txt holding the exact ENOENT line as text. Without this clip: title B, F0/S0 use the fallback wording, Claude Desktop in the description only (PLAN §3.3, §3.8). If Claude Desktop's Linux build is ever present in the lab instead, confirm on screen `~/.config/Claude/claude_desktop_config.json` and `~/.config/Claude/logs` (Q6/Q7).

## 7. Deliverables back to Cowork

Files: out/fx3/pins.txt; out/fx3/A/{rec.mkv, events.tsv, uvx-version.txt, echo-path.txt, which-uvx.txt, grep-startup.txt, startup-env-file.txt, short-list-etc-environment.txt, short-list-systemd-user.txt, short-list-login-defs.txt, bashrc-diff.txt, profile-diff.txt, ls-local-bin.txt, mcp-list-before.txt}; out/fx3/B/{rec.mkv, events.tsv, launcher-short.txt, launcher-full.txt, launcher.js, launcher.sha256, which-node.txt}; out/fx3/C/{rec.mkv, events.tsv, claude_desktop_config.json, mcp-add.txt, mcp-list.txt, ls-config-dir.txt}; out/fx3/runs/R1/{rec.mkv, events.tsv, session.jsonl, reply.txt, cost.txt, model.txt, tool-calls.txt, outcome.txt, suggested-prompt-crop.png, invocation.txt, mcp-remove-before.txt}; out/fx3/O/ when the owner delivers; this file at its prereg commit.

One-line answers (filled after the run, in this form):
- Q6: Claude Desktop in the lab: no (not attempted, sign-in). Take O: delivered / not delivered, so title A / B. Launcher: Node / Python; short-list text verbatim: "...".
- Q7: echo $PATH = "..."; which uvx = "..."; start-up line = "FILE:LINE: ..." ; short list = "..." from FILE (or: none measurable, 6.3 fired); `claude mcp list` after the full-path add: Connected yes / no (attempt 1 / 2). Linux config and log paths: not confirmed on screen (no Linux build).
- Q11: R1 prompt as section 4, committed at HASH before the run; outcome A / B / C / none; evidence frame take A `which uvx: typed`; label matches / does not match / half; cost $..., model ..., build ...; suggested prompt cropped yes.
These fill PLAN rev 4 §0 "lab fills" and SCRIPT-fx3 v2 §0/§1; the retime is rerun only if the F7 half clause or the Python alternate narration changes a word count.
