# freecad-course-lab

The lab behind the **FreeCAD + Claude Course** by The Stack Underflow. Lesson 1: connect Claude to FreeCAD with the
FreeCAD MCP add-on, then make a first part (a 5 x 20 x 60 mm block, the back plate of the course's wall hook) by hand
and by Claude, and measure both with FreeCAD's own numbers.

Everything runs in Docker on a virtual screen (Xvfb): the real FreeCAD window, a real terminal with Claude Code in it,
a real web browser and a real file manager, driven by a script at a person's pace (xdotool) and recorded at 30 fps
with a cursor log and an event log, so the video can be cut by event and zoomed onto what is clicked. Nothing in the
footage is staged or drawn; sped-up parts are labelled in the video.

## Pinned versions (lab day: 28 Oct 2026)

| what | version | how it is checked |
|---|---|---|
| FreeCAD | 1.1.4 (official AppImage, extracted) | SHA-256 against the release's own file (base image `screen-lab-freecad:1.1.4`) |
| FreeCAD MCP add-on + server | neka-nat/freecad-mcp **0.1.28** (git tag v0.1.28, commit 8babe99; PyPI 0.1.28) | the tag ZIP's SHA-256 in the Dockerfile; the server is started as `uvx freecad-mcp@0.1.28` |
| Claude Code | 2.1.308 (the "stable" channel on the lab day), auto-updater off | `claude --version` in every run folder |
| uv | 0.13.6 | SHA-256 of the release tarball |
| Firefox | 158.0.1 (Mozilla's APT repository) | apt pin |

Images, built in this order (the first two are the screen-lab kit's own Dockerfiles, vendored unchanged in
`vendor/screenlab-docker/`):
```
docker build -t screen-lab-base:1 -f vendor/screenlab-docker/base.Dockerfile vendor/screenlab-docker
docker build -t screen-lab-freecad:1.1.4 -f vendor/screenlab-docker/freecad.Dockerfile vendor/screenlab-docker
docker build -t fcc-app:1.1.4-0.1.28 -f docker/fcc.Dockerfile docker
```
The kit's recording library is vendored in `vendor/screenlab-lib/` (kit commit 2855535, unchanged).

## Lesson 1 questions and where the answers are

| # | Question | Answer file |
|---|---|---|
| Q0 | Without the plug, what does Claude do with the block request? | `out/l1/runs/no-plug/` |
| Q1 | Can the browser on the virtual screen film freecad.org's download page and the GitHub tag page? | `out/l1/web/` |
| Q2 | The ZIP's folder nesting; where the add-on goes in a fresh 1.1.4 profile | `out/l1/addon/` |
| Q3 | Start RPC Server: the status-bar text, the toolbar, Stop | `out/l1/addon/`, `out/l1/hand/` |
| Q4 | uv's install; is a new terminal needed before `uvx` works? | `out/l1/install/` |
| Q5 | `claude mcp add` + `claude mcp list` with a cold uv cache (timed); the `/mcp` tools screen; the tools/list count | `out/l1/connect/` |
| Q6 | The first question ("What documents are open in FreeCAD?"): which call, what reply | `out/l1/runs/connect/` |
| Q7 | The by-hand block: menu path, Property view names, the console line | `out/l1/hand/` |
| Q8 | Claude's block: calls, replies (a picture of the 3D view?), permission prompts | `out/l1/runs/claude-1/` |
| Q9 | Is Claude's block real? A no-AI read over the same plug, and a replay of Claude's calls in a fresh FreeCAD | `out/l1/compare.json`, `out/l1/replay/` |
| Q10 | The failures: the socket off ("Connected", then what?); the next real beginner failure | `out/l1/runs/fail/`, `out/l1/fail/` |
| Q11 | Does the window repaint with no input when the plug changes the document? | `out/l1/replay/repaint.json` |
| Q12 | The real permission prompt for execute code, in the mode a fresh install uses | `out/l1/runs/` (the run that shows it) |
| Q14 | Which document Claude's block lands in, and where | `out/l1/compare.json` |

## How the unattended Claude runs answer permission prompts (Q13; written before any run)

Each Claude run is one Claude Code session in its real terminal (xterm + tmux) beside FreeCAD's window, launched as a
viewer would start it: `claude` with no permission flags (Claude Code's own default mode on a fresh install), a fresh
home folder, no CLAUDE.md, auto memory off, one fixed model. The script types each message one character at a time,
presses Enter and then only waits. If Claude Code shows a permission prompt, the script waits 1.5 s (so it is
filmed) and answers with the prompt's own **"1. Yes"** option, never a "don't ask again" option and never "No". The
prompt's text is saved (`approval-N-M.txt`). The script never types anything else into a running turn.

Every MCP JSON-RPC line between Claude Code and the plug is logged by `proxy/mcp_log_proxy.py` (wrapped around
`uvx freecad-mcp@0.1.28` in the session's config); images in replies are saved as PNG files and shortened in the log.

## Lesson 1 results (28 Oct 2026)

| Q | What happened (file) |
|---|---|
| Q0 no plug | Claude ran `which freecadcmd`, wrote a script and ran `freecadcmd` in its own terminal, saved `block.FCStd` in the project folder and said 6,000 mm³. Nothing appeared in the open FreeCAD window (`runs/no-plug/tool-uses.json`, `pane-full-after.txt`) |
| Q1 web | Firefox films freecad.org ("Current stable version: 1.1.4") and the GitHub tag page; Download ZIP gives the same file as the pinned ZIP (SHA-256 matches, `web/zip-sha256.txt`). Playwright 1.63's browser is now Chrome for Testing (a testing banner), so Firefox from Mozilla's APT repository is used |
| Q2 folders | Extract Here (file manager) gives `freecad-mcp-0.1.28/addon/FreeCADMCP/` (Init.py, InitGui.py, package.xml, rpc_server). `print(App.getUserAppDataDir())` = `/home/maker/.local/share/FreeCAD/v1-1/`, which holds Macro and SavedPreferencePacks only: no Mod (`addon/profile-before.txt`) |
| Q3 socket | Workbench "MCP Addon", toolbar Start RPC Server / Stop RPC Server / Auto-Start Server / Remote Connections / Configure Allowed IPs / Set Auth Token. Start: status bar "RPC Server started at 127.0.0.1:9875 (PID n)." Stop: the status message is cleared at once (it never stays on screen); the console echoes the command |
| Q4 installers | Claude Code's installer ends with a setup note (~/.local/bin not in PATH, run the echo line); after it and a new terminal, `claude --version` = 2.1.308. uv 0.13.6 installs into the same ~/.local/bin, so `uvx` is found at once: the planned "uvx not found in an old terminal" failure did not happen (`install/q4-*.txt`) |
| Q5 connect | `claude mcp list` with an empty uv cache: Connected after 5.6 s. `/mcp`: freecad, 17 tools (`runs/connect/tools-list.json`). The server detail screen shows the logging wrapper's command line (the video skips it) |
| Q6 first call | `list_documents` → `["Unnamed"]` in 11 ms; no permission prompt (Claude Code 2.1.308's default is auto mode) |
| Q7 by hand | File > New Document, Part, Cube (Name Box, Label Cube), Property view Length 5 / Width 20 / Height 60, console `Gui.Selection.getSelection()[0].Shape.Volume` = 6000.0; freecadcmd: 6000.0, 5 x 20 x 60, Z 0..60 (`hand/measure.json`) |
| Q8 Claude | create_document "Block" (Claude ignored the empty document we opened), create_object Part::Box 5/20/60, execute_code → "Output: 6000.0"; 12 s; "Allowed by auto mode classifier" under each call; no prompt. The new document's 3D view stayed an unfitted TOP view, so the block was not visible there (only the tree changed) (`runs/claude-1/`) |
| Q9 proof | `compare.json`: hand vs Claude same volume, size, corner, height, validity. No-AI read of Claude's saved document over the plug: 6000.0, 5 x 20 x 60. Replay of Claude's 4 calls in a fresh FreeCAD: 0 errors, 6000.0 (`replay/`) |
| Q10a socket off | `claude mcp list`: Connected. create_document / execute_code / get_rpc_status: "Error executing tool ..." (the plug's log: "Failed to connect to FreeCAD ([Errno 111] Connection refused)"). Claude then used execute_code_headless and said nothing would show in the window. After Start RPC Server and "Try again.": the block in the window, 6000.0; that create_object reply carried a picture of the 3D view (`runs/fail-2/`) |
| Q10b already open | Claude Code started before the plug was added: `/mcp` → "No MCP servers configured."; `/exit`, `claude`: freecad, 17 tools (`fail-open/`) |
| Q11 repaint | The window redraws with no input when the plug changes the document (`replay/repaint.json`) |
| Q12 execute code | No prompt in auto mode; `/mcp` > View tools > execute_code: "Execute arbitrary Python code in FreeCAD." |
| Q14 where | Claude's block: its own new document "Block", object Box at 0,0,0 |

Cost: five Claude Code runs, $0.383 (`../freecad-course-BUDGET.tsv`, from each run's /cost).

## Lesson 2 (29 Oct 2026): sketch, pin, pad in Part Design, by hand and by Claude

The course's wall hook (side view on the XZ plane, from 0,0: right 25, up 10, left 5, down 5, left 15, up 55, left 5,
back to the start; padded 20). Expected without CAD (`checker/outline.py`): 425 mm², **8,500 mm³**, 25 x 20 x 60,
6 free sizes once every line is level or upright. Same pins as lesson 1 (FreeCAD 26.3 is still a release candidate).
Ledger: lesson 2's own GO line in `../freecad-course-BUDGET.tsv` (`LESSON=l2 BUDGET_MARK=...`).

| Q | What happened (file) |
|---|---|
| Q1 by hand | Part Design; New Body; New Sketch → "Select attachment": XY-plane, XZ-plane, YZ-plane (Base plane); XZ, OK → the Sketcher facing FRONT. Polyline by clicks (FreeCAD 1.1.4's Polyline has no typed lengths), closed on the first point: "Under-constrained: 6 Degrees of Freedom"; a corner drags. Dimension (D): six sizes typed in "Insert Length" (25, 10, 5, 5, 60, 5), the count to 0, "Fully constrained" in green; the corner no longer drags. Close; Pad (Length 10.00 mm by default) 20; OK. Tree: Body > Origin, Pad > Sketch (`hand/`, stills s1-s12) |
| Q2 hand numbers | 8500.0, 25 x 20 x 60, X 0..25, Y -20..0 (the pad goes along the XZ plane's normal, -Y), Z 0..60; 23 constraints (9 joined ends, 7 level/upright, 1 corner on an axis, 6 sizes), fully constrained (`hand/measure.json`) |
| Q3 Claude run 1 | Claude Code 2.1.308, claude-sonnet-5-5, auto mode, no prompt. Message 1 = SolidCraft lesson 2's message with one word changed (`message-diff.txt`). One execute_code: a PartDesign Body, a sketch attached to XZ_Plane (FlatFace), 8 lines, **8 Coincident constraints only**, a Pad of 20. Its reply: "The sketch is closed but has no dimensional constraints, only coincident points." Message 2: the tree, and an offer to add the sizes. $0.099 (`runs/claude-1/`) |
| Q4 which way up | **Upright**: X 0..25, Y -20..0, Z 0..60, the same as the hand part (`compare-1.json`: same: true; upright: both) |
| Q5 run 2 | The same: one execute_code, attached to XZ_Plane, 8 joins only, upright, 8,500. $0.098 (`compare-2.json`) |
| Q6 replay | Run 1's 2 calls replayed in a fresh FreeCAD with no AI: 0 errors, 8,500, same as the hand part; its sketch again 8 joins (`replay/`) |
| Q7 inside the sketch | Hand: fully constrained. Claude's (run 1's saved document, opened again with no AI): "Under-constrained: 16 Degrees of Freedom"; its back plate's corner drags and the plate leans over; Ctrl+Z (`inspect/`) |
| Q8 the view | Claude's create step returned a picture of the 3D view and the window showed the part upright with no input. Run 1's own viewer steps after the turn were spoiled by our lab query (a Qt tree item error shown by the add-on), so `take_inspect2.sh` films them on run 1's saved document |

Gotchas: in the Sketcher, the key V starts the Vertical constraint (use the Fit all button, not V, F); with a document
open, View > Panels lists Python Console above Report View; `lab.fcrpc row` can hit "Internal C++ object already
deleted" when the tree is rebuilt (the takes use fixed rows); `lab.drive`'s end-of-turn check misses the second
message after Ctrl+O (it waits for its time limit, then goes on).

## Tests

`tools/test.sh` runs every test in the lab image (unit tests, plus real Xvfb/tmux checks). The leak scan before any
commit: the screen-lab kit's `tools/leakscan.sh` with a patterns file kept outside this folder.

## Licence

Apache-2.0 (see LICENSE). FreeCAD, freecad-mcp, Claude Code, uv and Firefox are their owners' software, downloaded
at build time and not redistributed here.
