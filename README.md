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

## Lesson 3 (30 Oct 2026): named sizes in a spreadsheet, by hand and by Claude

Lesson 2's hook (its by-hand file, the course's start file) gets a spreadsheet with five named sizes (aliases):
`hook_depth` 25 mm, `thickness` 5 mm, `lip_height` 10 mm, `plate_height` 60 mm, `width` 20 mm. Its six sizes and the
pad's length are written from them (expressions): bottom = `Spreadsheet.hook_depth`, lip = `Spreadsheet.lip_height`,
lip width = `Spreadsheet.thickness`, the drop inside the lip = `Spreadsheet.lip_height - Spreadsheet.thickness`,
back plate = `Spreadsheet.plate_height`, back plate thickness = `Spreadsheet.thickness`, Pad Length =
`Spreadsheet.width`. Expected without CAD (`checker/outline.py`, tested): 8,500 mm³; hook_depth 40: 10,000 mm³,
40 x 20 x 60; then thickness 8: 752 mm², 15,040 mm³. Same pins as lessons 1-2. Ledger: lesson 3's own GO line in
`../freecad-course-BUDGET.tsv`. Messages and scoring were committed before the first run (`out/l3/prereg.json`,
`out/l3/messages/`, `checker/score_l3.py`).

| Q | What happened (file) |
|---|---|
| Q1 by hand | File > Open; workbench list > Spreadsheet; **New Spreadsheet** opens a tab with Content and Alias boxes; names in A1-A5, values with mm in B1-B5, each B cell's Alias box. In the Sketcher: double-click a size → Insert Length → `=` opens the Expression Editor → `Spreadsheet.hook_depth` (Enter picks it from the list; "Result 25.00 mm"), Enter, Enter → "25 mm (ƒ𝑥)" (our container's label font lacks the 𝑥 glyph). All six, still "Fully constrained"; Pad Length `=` `Spreadsheet.width`; Windows > Tile puts the sheet beside the hook (`hand/`) |
| Q2 numbers | after binding 8500.0 (7 expressions); hook_depth 40 mm: **10000.0**, 40 x 20 x 60, X 0..40, the part followed with no click; thickness 8 mm: **15040.0**; back to 5 mm: 10000.0; fully constrained throughout (`hand/measure-*.json`) |
| Q3 plain | lesson 2's hook with plain sizes, its 25 set to 40 directly: **10000.0**, 40 x 20 x 60, still fully constrained: the arm's top has no size of its own, so it follows (`plain/`) |
| Q4 Claude B1 (asked) | Claude Code 2.1.308, Sonnet 5.5, auto mode. Its first call failed (`Support`: AttributeError; 1.x calls it AttachmentSupport), the retry worked. A new document "Hook": a spreadsheet named **Params** with the five names (with mm), a Body, a sketch on XZ, 8 lines, all **7** lengths written from names, a Pad named Extrude from `Params.width`; fully constrained; 8,500. "40 deep": one call, `Params.set("B4", "40 mm")`: 10,000. "8 thick": `set("B3", "8 mm")`: 15,040 (it noted the lip now stands 2 above the arm). $0.164 (`runs/B1/`) |
| Q4 Claude A1 (not asked) | No names. One call per message: 8,500 first (sketch with 8 joins only, as in lesson 2); "40 deep": deleted every line and drew 8 new corners: 10,000; "8 thick": drew new corners with the plate and the arm 8 thick but the **lip kept 5 wide and raised to 13**: **15,220**, a different hook from the named reading; its reply said so and offered to change it. $0.127 (`runs/A1/`) |
| Q4 Claude B2 (asked) | Two failed calls, then the build: 5 names, 6 sketch sizes + the pad from names, 8,500; each edit one cell: 10,000, 15,040. $0.205 (`runs/B2/`) |
| Q5 scored | B1 and B2: names, first build right, both edits followed and by one cell. A1: first build right, 40 followed by redrawing (not one cell), 8 thick read differently (15,220) (`compare.json`, `runs/*/score.json`) |
| Q6 replay | B1's and A1's logged calls replayed per message in a fresh FreeCAD with no AI: the same 8,500 / 10,000 / 15,040 (B1) and 8,500 / 10,000 / 15,220 (A1) (`replay-*/`) |

Lesson 2's error dialog, found: the take's tree lookup used PySide's `findItems`, whose item wrappers for a second
document's rows come back "Internal C++ object (QTreeWidgetItem) already deleted"; the exception reached FreeCAD and
the add-on showed it. `lab/fcrpc.py` now walks the tree's model indexes (no item wrappers), only takes rows under the
asked document, and runs every query inside try/except so nothing is raised in FreeCAD (`tests/test_l3.py`). In run
B1 the old lookup missed Claude's part, so its viewer steps were refilmed on B1's own saved copies
(`lab/take_inspect3.sh`, "opened again"). `lab/drive.py` now ends a turn on a new end-of-turn line (Claude Code can
re-draw its transcript, so a count of such lines can fall).

## Lesson 4 (30 Oct 2026): screw holes from named sizes, a fillet, and one change (width 20 to 30)

Start file: lesson 3's by-hand hook as lesson 3 leaves it (`out/l3/hand/back5.FCStd`, hook_depth 40: 10,000 mm3).
Pre-registration and scoring (`checker/score_l4.py`, `out/l4/prereg.json`) committed before any Claude run (696b5fa).
Numbers worked out without CAD in `checker/holes.py` (tests/test_l4.py): two 4 mm holes through the 5 mm plate
remove 125.66 mm3, a 2 mm fillet along the lip removes (4 - pi) x width; **9,857.168** at width 20, **14,848.584**
at width 30.

| # | Question | Answer | Files |
|---|---|---|---|
| L4-Q1 | The by-hand path in FreeCAD 1.1.4 | the sheet's rows 6-7 (hole_d 4 mm, hole_spacing 30 mm); key 6; the back face; Create sketch (straight onto the face); G C, two circles, 4; each centre: L / I, `=`, `Spreadsheet.width / 2`, `(Spreadsheet.plate_height -+ Spreadsheet.hole_spacing) / 2`; Hole, Diameter `= Spreadsheet.hole_d`, Through all; the lip edge, Fillet (Edge10), 2 | `out/l4/hand/` (rules.txt, sketch-check.txt) |
| L4-Q2 | The numbers | holes + fillet **9857.168146928205**; width 30 **14848.584073464102**; holes 10 / 10 from the sides, then **15 / 15**; the hole sketch reads 15 mm (f) | `out/l4/hand/check-*.json` |
| L4-Q3 | Plain numbers (watch only, built headless by `lab/build4.py PLAIN=1`) | width 30: holes **10 / 20** from the sides, its sketch still 10 mm; the same volume | `out/l4/plain/` |
| L4-Q4 | Claude B1 (with the sentence) | names in B6/B7; a sketch on the body's YZ plane, every hole size from names; a Pocket, through all; a 2 mm fillet on Edge10; 9,857.17; "30 wide": one call `ss.set('B5','30 mm')`: 15 / 15, fillet kept. $0.148 | `out/l4/runs/B1/` |
| L4-Q4 | Claude A1 (without) | no names; plain centres; right first build; "30 wide": changed the width **and** tied the across distance to `-Spreadsheet.width / 2` in the same call ("they would have stayed 10 mm from the edge and ended up off-centre"): 15 / 15, not by one cell. $0.163 | `out/l4/runs/A1/` |
| L4-Q4 | Claude B2 (with the sentence) | a failed first call, then names, YZ plane, Pocket, fillet; one cell; 15 / 15. $0.138 | `out/l4/runs/B2/` |
| L4-Q5 | Scored | B1, B2: every check passes, the edit by one cell; A1: right, centred, fillet kept, not by one cell | `out/l4/runs/*/score.json`, `out/l4/compare.json` |
| L4-Q6 | Real? | no-AI replays of B1 and A1: 9,857.17, then 15 / 15 and 14,848.58 | `out/l4/replay-B1/`, `out/l4/replay-A1/` |
| L4-Q7 | Does the fillet survive? | yes at width 30, at width 30 + thickness 8, and back (from back5, sketch on the face); the saved files keep a history name beside Edge10 | `out/l4/fillet-tests.json` |

All runs: Claude Code 2.1.308, Sonnet 5.5, auto mode, no permission prompt. Lab gotchas found: a circle's size label
(placed where the cursor was) takes the click meant for the centre, so the take moves the cursor away before typing
the size; an open menu blocks the add-on's socket, so menu items are clicked at offsets from the menu title
(`lab/button.py menu`); the Windows menu moves with the workbench; tiled windows put the sheet left or right, so
cells are found by `lab/button.py cell`; a file saved headless opens with every object hidden.

## Lesson 5 (31 Oct 2026): export an STL, check the mesh, and the slicer's estimate

Start file: lesson 4's by-hand hook as lesson 4 leaves it (`out/l4/hand/width30.FCStd`: 30 wide, two 4 mm holes, a
2 mm fillet; the solid 14,848.584 mm3). Pre-registration and scoring (`checker/score_l5.py`, `out/l5/prereg.json`)
committed before any Claude run (693672b). STL files are measured with no CAD by `checker/mesh5.py` (tests/test_l5.py).
The slicer: PrusaSlicer 2.9.2 (Debian trixie's 2.9.2+dfsg-1) in `docker/fcc-slicer.Dockerfile`, no network, with the
stock "Original Prusa MK4S 0.4 nozzle" + its default "0.20mm SPEED" + "Prusament PLA" presets resolved from the bundle
by `slicer/flatten.py` (offline 2.9.2 can't install system presets, so the window shows them as user presets named
"(stock)"); the command-line estimates by `slicer/estimate5.sh`.

| # | Question | Answer | Files |
|---|---|---|---|
| L5-Q1 | The by-hand path in FreeCAD 1.1.4 | the Body row; File > Export; type list "STL Mesh (*.stl *.ast)" (3MF is first in the list); `hook.stl`; Save. Mesh workbench; File > Import; Mesh Info "Number of facets 272"; Evaluate and repair mesh, All above tests together, Analyze: "No flipped normals ... No self-intersections"; Check solid mesh: "The mesh 'hook' is a solid." | `out/l5/hand/` |
| L5-Q2 | The wrong row (the Pad) | 28 triangles, **15,000.0 mm3**, no holes, and "The mesh 'hook-pad' is a solid."; the Body's mesh volume line: 14849.0185546875 | `out/l5/hand/mesh-*.json`, `s7-s9` |
| L5-Q3 | Maximum mesh deviation (Preferences > Import-Export > Mesh Formats, 0.10 mm by default; the page appears once the Mesh workbench has loaded) | default: 272 triangles, each 4 mm hole **26 sides** (flats 3.971 mm); 0.01: **2,100**, 229 sides (flats 3.9996). Window, coarse to fine: 0.1 and 0.08 give 272; 0.06-0.02 give 1,172 (126 sides); 0.01 gives 2,100. A coarser number after a finer one keeps the finer mesh in that window. Headless (freecadcmd) the default gives 1,172 | `out/l5/hand/`, probe notes in the lesson plan |
| L5-Q4 | Every STL measured | Body 272 / 14,849.015, closed, one part; Pad 28 / 15,000; fine 2,100 / 14,848.588 | `out/l5/hand/mesh-*.json` |
| L5-Q5 | The slicer, filmed | the Body's file: back view with both holes; Slice now: 36m, 9.09 g; Rotate X 90 (Size 40 / 60 / 30): 22m, 9.19 g, 150 layers, the middle layer (75, 15 mm up) is the J outline with the two holes cut through it; the Pad's file: no holes from the back, 36m, 9.08 g | `out/l5/slicer/` |
| L5-Q6 | The slicer's command-line estimates | Body: standing 35m 56s / 9.09 g / 300 layers; side 21m 55s / 9.19 g / 150; back 29m 16s / 9.40 g ("Detected print stability issues"); Pad: 35m 53s / 21m 18s / 27m 52s; Claude's file = the Body's | `out/l5/estimates/estimates.json` |
| L5-Q7 | Claude B1 (asked to check) | exported the Body with `Mesh.export` (272 triangles, 13,684 bytes), read the file back with `Mesh.Mesh` and tested isSolid, components, non-manifolds, self-intersections; reported 272 triangles and 14,849.0 mm3 (and the solid's 14,848.58), said it used the Python mesh API instead of the workbench's dialogs. Message 2: "Lie it on its side", with a strength reason. $0.081 | `out/l5/runs/B1/` |
| L5-Q7 | Claude A1 (not asked) | exported the Body (the same 272-triangle file), checked the shape before export, said it had not checked the mesh itself. Message 2: "on its side", with a strength reason. $0.112 | `out/l5/runs/A1/` |
| L5-Q8 | Scored | B1: right part, clean, checked, numbers true (both sources named); A1: right part, clean, not checked (none reported); both picked side (the slicer's lower time estimate), both made a strength claim (recorded) | `out/l5/runs/*/score.json`, `out/l5/compare.json` |
| L5-Q9 | Real? | no-AI replay of B1's calls: the same 272 triangles, 14,849.015 mm3, the same verdicts: pass | `out/l5/replay-B1/compare.json` |

Runs: Claude Code 2.1.308, Sonnet 5.5, auto mode, no permission prompt; the live cost guard (`lab/costguard.py`)
never fired (estimates $0.108 and $0.146 against $0.30). Found after the pre-registration: Claude's numbers came in a
markdown table, so the parser now strips bold and table pipes (the rule unchanged; a test added). Lab gotchas: in the
slicer, keys reach the 3D view only after a click in it, Tab switches to the preview (and slices), "Slice now" becomes
"Export G-code" in the same place after slicing, Rotate (relative) applies on Enter and resets to 0; the first run
shows a "Send system info" dialog and a hint popup. In FreeCAD, the Export dialog proposes 3MF; the Evaluate panel
docks cut off at the right edge (widened before its button is clicked).

## Lesson 6 (31 Oct 2026): change one thing, keep the rest, check it (the opening 30 to 45 mm for a backpack strap)

Start file: lesson 5's hook (= lesson 4's `out/l4/hand/width30.FCStd`, opened as `hook-lesson5.FCStd`): hook_depth 40,
width 30, the opening (back plate to lip) 30 mm, 14,848.584 mm3. Pre-registration (`out/l6/prereg.json`, messages,
`checker/l6read.py`, `checker/score_l6.py`, `tests/test_l6.py`) committed before any Claude run (710c967). The
must-stay-true list is read by a script from the saved file (no recompute, the part's Placement undone): the opening 45
+-0.05; one solid, no errors, FreeCAD's STL closed; plate 60 x 30; walls 5; lip 10; two 4 mm holes centred at 15/45;
the 2 mm lip fillet; the names still drive it (the 12 bindings, hook_depth = the depth, two drive tests); volume
17,098.584 +-1. FreeCAD's own tape measure (Tools > Measure) is driven like a person by `lab/l6common.sh`.

| # | Question | Answer | Files |
|---|---|---|---|
| L6-Q1 | The by-hand path | Tools > Measure, Mode **Distance** (Auto gives 90.00 deg for these picks), the plate's inside face, **Ctrl** + the lip's inside top edge (without Ctrl the second click replaces the first): **30.00 mm**; the sheet's B1 hook_depth 45: **35.00**; 55: **45.00**; Radius on a hole's rim **2.00**, on the small curve at the lip's end **2.00**; the volume line 17098.58 | `out/l6/hand/` |
| L6-Q2 | Read by the script | 40: fails only C and V (30.0, 14,848.584); 45: fails only C and V (35.0, 15,598.584); 55: passes every line (17,098.584) | `out/l6/hand/score-*.json` |
| L6-Q3 | Claude (2.1.308, Sonnet 5.5, auto mode, no prompt) | B1, B2: one cell, `set("B1", "=55 mm")`, then a table of every line with numbers; B3: a new name `opening` = 45 mm and `hook_depth = 2 * thickness + opening`; A1 (no list): one cell (55 mm), reported the opening, box and volume, said the other sizes were "unchanged", nothing about the names. ~30 s each from Enter to the reply; $0.113 / $0.098 / $0.093 / $0.129; the guard never fired, no "Your choice." needed | `out/l6/runs/*/` |
| L6-Q4 | Scored | **B: 3 of 3 passed; A1 passed** (one run). Lines Claude said with a number: 6 of 7 in every B run (the names line said without a number), 5 in A1 (the fillet without a number, the names not mentioned) | `out/l6/compare.json` |
| L6-Q5 | Real? | no-AI replays of all four runs' logged calls on a fresh hook: the same verdict on every line, 17,098.584 mm3: **4 of 4 matched** | `out/l6/replay-*/compare.json` |

Gotchas: `lab.fcrpc vp` points are ~60 px off at Qt scale 1.5 in the side-by-side layout, so B1's in-run filmed
Measure picked the fillet's edge and read 48.00 (a lab error, not the part: the script read 45.0); `m6_aim` now moves
the cursor until FreeCAD preselects the wanted face or edge (`lab.l6pick hit`), and B1's check was re-filmed on its saved
copy (`lab/take_inspect6.sh`, `out/l6/inspect-B1/`: 45.00). Any socket query clears the Measurement panel's Result, so
it is read once after the last pick. The Show Delta box can't be unticked through Qt before the panel opens (it stays on).

## Tests

`tools/test.sh` runs every test in the lab image (unit tests, plus real Xvfb/tmux checks). The leak scan before any
commit: the screen-lab kit's `tools/leakscan.sh` with a patterns file kept outside this folder.

## Licence

Apache-2.0 (see LICENSE). FreeCAD, freecad-mcp, Claude Code, uv and Firefox are their owners' software, downloaded
at build time and not redistributed here.
