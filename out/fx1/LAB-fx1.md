# LAB-fx1: FreeCAD MCP Not Working in FreeCAD 1.1? Addon Not Showing: the Mod Folder Moved to v1-1 — pre-registration v1, 2026-11-01 (before any run)

Lab repo: freecad-course-lab. Folder: out/fx1/ (takes out/fx1/A0, A, A2-copy, A2-share, A2-new, B, C-drag, C-terminal, D, D-half, E, F; run out/fx1/runs/R1). Pins: FreeCAD 1.1.4 AppImage (Linux), freecad-mcp 0.1.28 (the add-on folder addon/FreeCADMCP from the v0.1.28 download, lesson 1), Claude Code 2.1.31x (exact build written to out/fx1/runs/R1/version.txt at run start), uv 0.13.6 (lesson 1's pin; present, not used: no plug is connected in fx1), model claude-sonnet-5-5 (confirmed from session.jsonl after R1). SolidCraft 0.28.0 and PrusaSlicer 2.9.2 are series pins not used in fx1. Docker image: the lab's FreeCAD image that lesson 7 (out/l7) ran in; Xvfb display, xdotool, ffmpeg x11grab, the terminal and file manager lesson 1 filmed, Mesa (llvmpipe) only if FreeCAD's 3D view does not render; XDG_DATA_HOME unset in every container (check: `env | grep -c XDG_DATA_HOME` prints 0); no 3.11-only image needed for fx1. Every take starts from a new container of that image (fresh home) unless the take says "continues from"; the home user is the image's user (lesson 7: /home/maker), written below as $HOME.

Sources for this file: PLAN.md rev 3 section 1, §0.3 rows 1-3, §0.4 Q1-Q4, Q10, Q11; ACCURACY.md block B; SCRIPT-fx1.md §0 and §1; SCRIPT-L7.md §0 (lab conventions). Every expected value below is a quote with its source, or "measure".

Variables used in the commands (filled at run start, written to out/fx1/env.txt): `$FREECAD` = absolute path of the FreeCAD 1.1.4 AppImage in the image (`$FREECAD --version` output copied to env.txt); `$ADDON_SRC` = absolute path of the extracted v0.1.28 download so that `$ADDON_SRC/addon/FreeCADMCP/InitGui.py` exists (`ls -l $ADDON_SRC/addon/FreeCADMCP` copied to env.txt); `$FC` = `$HOME/.local/share/FreeCAD`.

Conventions (from SCRIPT-L7 §0): prereg committed to the lab repo before the first container starts (commit hash written into out/fx1/PREREG.txt); every take is one recording `take.mkv` (x11grab of the Xvfb display) plus `events.tsv` (one line per event: seconds since recording start, TAB, event name exactly as written below; the take script writes the line at the moment it sends the xdotool action or the terminal keystrokes); all clicks and typing by xdotool at a person's pace (type delay 80 ms, 1 s pause before each click); screenshots as PNG by `import -window root` (ImageMagick) or `xwd`; terminal text also saved as plain text (`script -q` typescript or `tee`) so the cut can be checked against text, not only pixels; a restart is "quit FreeCAD (File, Exit via xdotool), wait for the process to end, start again" and is one event `FreeCAD: restarting`. No AI in any take except R1. No no-AI test script is needed in fx1 (no plug is started; the Report view and the console are read on screen and transcribed into notes.md of the take by hand, verbatim).

## 2. Questions this lab answers (PLAN §0.4 numbering)

- Q1 (a): On a clean home, after FreeCAD 1.1.4 is started once and quit, does `$FC/v1-1/` exist, does `print(App.getUserAppDataDir())` print a path ending in `/v1-1/`, and is `v1-1/Mod` created or only `v1-1`?
- Q1 (b): With the add-on in the OLD drawer `$FC/Mod/FreeCADMCP` (folder created by the lab) and v1-1 already existing, does the restarted FreeCAD show no MCP Addon in the workbench list, and does the Report view print nothing about it?
- Q1 (c): On a fresh home where `$FC/Mod/FreeCADMCP` exists BEFORE the first start, does FreeCAD 1.1.4 show the dialog titled "Welcome to FreeCAD 1.1" with the three buttons; after Copy Configuration, is v1-1 a copy of the old folder (add-on shows, console ends in v1-1, old folder still there, "Migrating config from ... to ..." printed or not), and does a second add-on put into the old Mod only then stay hidden; after Share, is `v1-1.do_not_migrate` written, does the console print the old path, does the add-on show; does New default create an empty v1-1?
- Q2: Does `cp -r addon/FreeCADMCP/* v1-1/Mod/` (files loose in Mod) give no MCP Addon, and what does the Report view print; what does the Report view print for a `Mod/FreeCADMCP` that holds only InitGui.py (no rpc_server/)?
- Q3: On the take day, what does the Addon Manager (Tools, Addon manager) list for the search "MCP", with each hit's author line; is "FreeCAD MCP by neka-nat" among them?
- Q4: With no plug connected and `claude` in an empty folder, does the one pre-registered run answer A (a v1-1 path), B (the old FreeCAD/Mod path) or C (run the console line / getUserAppDataDir), and does it match the F2 console line?
- Q10: What is the exact status-bar text after Start RPC Server with the 0.1.28 add-on?
- Q11: Was the R1 prompt and its A/B/C scoring committed before the run, was there one run only, in auto mode, and is the greyed suggested prompt cropped out?

## 3. Takes, in run order

Take-level file set, every take: `take.mkv`, `events.tsv`, `notes.md` (verbatim transcriptions, pass/fail line per rule), the screenshots and text files named per take. Frame names in "used in" are SCRIPT-fx1 §1 rows.

### A0 (clean home, Q1 a; evidence only, no frame)

(a) State: new container, home fresh, `ls $FC` fails ("No such file or directory"), XDG_DATA_HOME unset.
(b) Commands:
```
env | grep XDG_DATA_HOME ; echo "exit=$?"            # expected: exit=1
ls -la $HOME/.local/share/ |& tee out/fx1/A0/ls-before.txt
$FREECAD &                                           # event: FreeCAD: starting
# wait for the main window (xdotool search --name FreeCAD); screenshot A0/first-start.png
# if a dialog is on top: screenshot A0/dialog.png and STOP (stop rule 1)
# xdotool: View, Panels, Python console                event: console: opened
# xdotool type: print(App.getUserAppDataDir())  Return  event: console: print typed
# screenshot A0/console.png                            event: console: path printed
# xdotool: File, Exit; wait for the process to end
ls -la $FC |& tee out/fx1/A0/ls-FreeCAD.txt
ls -la $FC/v1-1 |& tee out/fx1/A0/ls-v1-1.txt
find $FC -maxdepth 3 | tee out/fx1/A0/find.txt
ls -la $HOME/.config/FreeCAD |& tee out/fx1/A0/ls-config.txt
```
(c) Events: `FreeCAD: starting`, `console: opened`, `console: print typed`, `console: path printed`.
(d) Capture: A0/first-start.png, A0/console.png, A0/ls-before.txt, A0/ls-FreeCAD.txt, A0/ls-v1-1.txt, A0/find.txt, A0/ls-config.txt; notes.md: the printed path verbatim.
(e) Expected: `$FC/v1-1/` exists after the first quit (ACCURACY B: "the version folder is appended when the FreeCAD folder does not exist yet", ApplicationDirectories.cpp 163-192, tag 1.1.4); no Welcome dialog (ACCURACY B: "on a clean home it never asks"); printed path ends in `/v1-1/`: measure (PLAN Q1 a); `v1-1/Mod` created or only `v1-1`: measure (PLAN Q1 a); whether 1.1.4 creates an unversioned `$FC/Mod` itself: measure (PLAN §1.8).
(f) PASS: v1-1 exists, no dialog, path ends in v1-1. FAIL: v1-1 absent or a dialog appears: stop rule 1 (the A, B, C storyboard rests on this; report before any other take). If `v1-1/Mod` already exists: SCRIPT §4 rule, the F4 label "the Mod folder may not exist yet" stays, the `mkdir -p` crop may be dropped, retime.py rerun.

### A (the symptom, trap 1, Q1 b; continues from A0's container)

(a) State: A0 done, FreeCAD closed, `$FC/v1-1` exists, `$FC/Mod` absent or empty (A0/ls-FreeCAD.txt says which).
(b) Commands:
```
mkdir -p $FC/Mod
cp -r $ADDON_SRC/addon/FreeCADMCP $FC/Mod/
ls -la $FC/Mod/FreeCADMCP | tee out/fx1/A/ls-old-Mod.txt     # InitGui.py must be listed
# file manager opened at $FC/Mod/FreeCADMCP (address bar), window on the right half
#                                                      event: file manager: old Mod/FreeCADMCP
# screenshot A/filemanager-old-Mod.png
$FREECAD &                                             # event: FreeCAD: starting
# wait for the main window; xdotool: open the workbench selector list
#                                                      event: workbench list: opened (no MCP Addon)
# hold 6 s; screenshot A/workbench-list.png
# xdotool: View, Panels, Report view                   event: report view: shown
# hold 5 s; screenshot A/report-view.png
# xdotool: File, Exit
```
(c) Events: `FreeCAD: starting`, `workbench list: opened (no MCP Addon)`, `report view: shown`, `file manager: old Mod/FreeCADMCP`.
(d) Capture: A/ls-old-Mod.txt, A/filemanager-old-Mod.png, A/workbench-list.png (the whole list; every entry readable), A/report-view.png; notes.md: the Report view text transcribed verbatim (or "empty"). Used in F0 (both halves) and Short S0.
(e) Expected: no "MCP Addon" entry (PLAN §1.1: "the workbench list has no MCP Addon after the add-on was copied"; issue #146 "the workbench silently does not appear", ACCURACY B); Report view: "expected: nothing; confirm, do not assume" (SCRIPT §0 Take A).
(f) PASS: no MCP Addon in the list; F0 stands. Report view empty: F0 stands as written. Report view not empty: F0 stands, the text goes to notes.md and the description; no narration says "FreeCAD prints nothing" (SCRIPT §3). FAIL: MCP Addon IS listed: the premise is wrong; stop rule 2, report; no further take.

### B (the console line, Q1 a again on A's state; continues from A)

(a) State: A's state, FreeCAD closed, add-on in the old drawer.
(b) Commands:
```
$FREECAD &                                             # event: FreeCAD: starting
# xdotool: View, Panels, Python console                event: console: opened
# screenshot B/console-empty.png
# xdotool type (80 ms/char): print(App.getUserAppDataDir())   then Return
#                                                      event: console: print typed
# wait 1 s                                             event: console: path printed
# hold 6 s; screenshot B/console-path.png (the console crop must hold the typed line and the answer, 3 lines)
# leave FreeCAD open for take C-drag
```
(c) Events: `console: opened`, `console: print typed`, `console: path printed`.
(d) Capture: B/console-empty.png, B/console-path.png; notes.md: the exact printed path. Used in F2, F10 (right half), F12 (banner over it), Short S1.
(e) Expected: a path ending in `/v1-1/` (PLAN §1.6 step 1: "on 1.1 it ends in v1-1 once that folder exists"); the exact string: measure (`[lab: exact path]`, F2 and S1). Lesson 1's recorded Linux AppImage path for reference: `~/.local/share/FreeCAD/v1-1/Mod` (ACCURACY B, PUBLISH/70 youtube-metadata.txt).
(f) PASS: the printed path equals `$FC/v1-1/` (trailing slash or not, recorded as printed). FAIL: it prints the old `$FC/` or anything else: stop rule 1 (F1, F2, F10 clause "the answer ends in v1-1" cannot be said); report.

### C-drag (the fix for trap 1, file manager; continues from B)

(a) State: B's FreeCAD open with the console; file manager open; add-on at `$FC/Mod/FreeCADMCP`; `$FC/v1-1/Mod` exists or not per A0 (if not: create it in the file manager first, filmed, event `file manager: new folder Mod` — extra event, not in SCRIPT §1, kept for the cut).
(b) Commands:
```
# xdotool: File, Exit (FreeCAD closed before the move)
# file manager: two panes or two windows: left $FC/Mod, right $FC/v1-1/Mod
# xdotool drag (mousedown on FreeCADMCP, move at a person's pace, mouseup on the right pane)
#                                                      event: file manager: drag FreeCADMCP to v1-1/Mod
ls -R $FC | tee out/fx1/C-drag/ls-after-drag.txt      # $FC/v1-1/Mod/FreeCADMCP/InitGui.py must be listed, $FC/Mod empty
$FREECAD &                                             # event: FreeCAD: restarting
# xdotool: open the workbench list                     event: workbench list: MCP Addon
# hold 5 s; screenshot C-drag/workbench-list.png
# xdotool: select MCP Addon; click Start RPC Server (toolbar)   event: FreeCAD: Start RPC Server
# wait 1 s                                             event: status bar: started
# hold 5 s; screenshot C-drag/status-bar.png (status bar crop at 1:1 pixels)
# screenshot C-drag/window-mcp-active.png (whole window, for F13)
# xdotool: File, Exit
```
(c) Events: `file manager: drag FreeCADMCP to v1-1/Mod`, `FreeCAD: restarting`, `workbench list: MCP Addon`, `FreeCAD: Start RPC Server`, `status bar: started`.
(d) Capture: C-drag/ls-after-drag.txt, C-drag/workbench-list.png, C-drag/status-bar.png, C-drag/window-mcp-active.png; notes.md: the status-bar text verbatim. Used in F1, F5, F13, Short S2.
(e) Expected: "MCP Addon" in the list (PLAN §1.6 step 5); status bar "RPC Server started at 127.0.0.1:9875" (PLAN §0.4 Q10: "lesson 7 recorded 'RPC Server started at 127.0.0.1:9875'; reuse"), exact text: measure.
(f) PASS: MCP Addon listed and the socket starts; F1/F5/F13/S2 stand; the status-bar text, whatever it reads, replaces the F5 `[lab: exact text]`. FAIL: no MCP Addon after the move: stop rule 3 (check ls-after-drag.txt for the three levels first; if the drag copied instead of moved, or dropped into the wrong pane, redo the drag once, same event names, take folder C-drag-2; if the three levels are right and it still does not show, report).

### C-terminal (the fix for trap 1, terminal; reset first, then continues on A's state)

(a) State: reset to A's state in the same container: FreeCAD closed; `mv $FC/v1-1/Mod/FreeCADMCP $FC/Mod/` (not filmed); `ls -R $FC` saved as C-terminal/ls-reset.txt showing `$FC/Mod/FreeCADMCP/InitGui.py` and no FreeCADMCP under v1-1. If `$FC/v1-1/Mod` was created by C-drag or by A0 it stays (the `mkdir -p` line is then a no-op; noted).
(b) Commands (typed in the lab terminal, 80 ms/char, window wrapped at 44 columns so each crop is 3 lines):
```
ls ~/.local/share/FreeCAD                              # event: terminal: ls FreeCAD typed
mkdir -p ~/.local/share/FreeCAD/v1-1/Mod               # event: terminal: mkdir -p typed
mv ~/.local/share/FreeCAD/Mod/FreeCADMCP ~/.local/share/FreeCAD/v1-1/Mod/
                                                       # event: terminal: mv typed
ls ~/.local/share/FreeCAD/v1-1/Mod/FreeCADMCP          # event: terminal: ls InitGui shown
# then FreeCAD start, list, Start RPC Server, status bar exactly as in C-drag:
#   events: FreeCAD: restarting, workbench list: MCP Addon, FreeCAD: Start RPC Server, status bar: started
```
(c) Events: `terminal: ls FreeCAD typed`, `terminal: mkdir -p typed`, `terminal: mv typed`, `terminal: ls InitGui shown`, `FreeCAD: restarting`, `workbench list: MCP Addon`, `FreeCAD: Start RPC Server`, `status bar: started`.
(d) Capture: C-terminal/terminal.txt (typescript of the four commands and their output), one screenshot per command after its output (C-terminal/01-ls.png, 02-mkdir.png, 03-mv.png, 04-ls-InitGui.png), C-terminal/workbench-list.png, C-terminal/status-bar.png. Used in F4 (left half), F5.
(e) Expected: `ls` shows `Mod` and `v1-1` (SCRIPT §0 Take C `[lab]`); `mkdir -p` needed or not: measure (Q1 a); the last `ls` shows `InitGui.py`: measure (the add-on's file list from `$ADDON_SRC`); MCP Addon listed; status bar as in C-drag.
(f) PASS: the four crops exist with the lit words present (v1-1, -p, FreeCADMCP, InitGui.py) and MCP Addon shows; F4 stands. If only one of C-drag / C-terminal is usable: SCRIPT §4 rule, F4's left half becomes the drag and the lit-word notes fall away. FAIL on the list: as C-drag.

### D (trap 2, the flattened copy, Q2; new container, A0 repeated unfilmed first)

(a) State: new container; run A0's commands once without recording (FreeCAD started once, quit) so `$FC/v1-1` exists; `ls -R $FC` saved as D/ls-start.txt; `$FC/Mod` absent; `mkdir -p $FC/v1-1/Mod` only if A0 showed v1-1/Mod is not created (noted in D/notes.md; the star copy into a missing Mod would fail with "No such file or directory" and that is not the beat).
(b) Commands (terminal, 44 columns):
```
cd $ADDON_SRC
cp -r addon/FreeCADMCP/* ~/.local/share/FreeCAD/v1-1/Mod/     # event: terminal: cp star typed
ls ~/.local/share/FreeCAD/v1-1/Mod                           # event: terminal: ls Mod loose
ls -R ~/.local/share/FreeCAD/v1-1/Mod | tee out/fx1/D/ls-R-loose.txt
$FREECAD &                                                   # event: FreeCAD: restarting
# xdotool: open the workbench list                           event: workbench list: opened (no MCP Addon)
# hold 6 s; screenshot D/workbench-list.png
# xdotool: View, Panels, Report view                         event: report view: shown
# hold 5 s; screenshot D/report-view.png
# xdotool: File, Exit
```
(c) Events: `terminal: cp star typed`, `terminal: ls Mod loose`, `FreeCAD: restarting`, `workbench list: opened (no MCP Addon)`, `report view: shown`.
(d) Capture: D/terminal.txt, D/01-cp.png, D/02-ls-loose.png, D/ls-R-loose.txt, D/workbench-list.png, D/report-view.png; notes.md: the exact `ls` listing and the Report view text verbatim. Used in F7.
(e) Expected: the listing shows the add-on's files loose in Mod, "expected InitGui.py, Init.py, rpc_server/ and the rest" (SCRIPT §0 Take D); exact listing: measure; no MCP Addon: "lab: measure (Q1, Q2)" (ACCURACY B row "cp -r ... leaves the files loose and no workbench appears; Report view empty or not"); Report view: measure.
(f) PASS: no MCP Addon; F7 stands with the listing filled in. Report view text, if any, goes to notes.md and the description (F7 narration does not quote it). FAIL: MCP Addon appears with loose files: F7, F8, F9 and F6's "Trap 2" are cut; stop rule 4, report (the storyboard's second trap is then not reproducible on Linux).

### D-half (the half-flattened case, Q2; evidence only, candidate extra beat; new container, A0 repeated unfilmed)

(a) State: as D (a), v1-1 exists, `$FC/v1-1/Mod` exists (create if needed, noted).
(b) Commands:
```
mkdir -p $FC/v1-1/Mod/FreeCADMCP
cp $ADDON_SRC/addon/FreeCADMCP/InitGui.py $FC/v1-1/Mod/FreeCADMCP/
ls -R $FC/v1-1/Mod | tee out/fx1/D-half/ls-R.txt                 # only InitGui.py under FreeCADMCP
$FREECAD &                                                   # event: FreeCAD: starting
# xdotool: View, Panels, Report view                         event: report view: shown
# hold 5 s; screenshot D-half/report-view.png
# xdotool: open the workbench list; screenshot D-half/workbench-list.png
# xdotool: File, Exit
```
(c) Events: `FreeCAD: starting`, `report view: shown`, `workbench list: opened (no MCP Addon)` or `workbench list: MCP Addon` (whichever is true; both names exist in SCRIPT §1).
(d) Capture: D-half/ls-R.txt, D-half/report-view.png, D-half/workbench-list.png; notes.md: Report view text verbatim, whether an ImportError (or any traceback) is printed, whether MCP Addon is listed.
(e) Expected: measure (PLAN Q2: "what does the Report view say? Candidate extra beat if it prints an ImportError").
(f) PASS/FAIL: no storyboard clause depends on it. If an ImportError is printed: report it as a candidate extra beat (not in SCRIPT v1). Otherwise record and move on.

### E (the fix for trap 2; continues from D's container)

(a) State: D's state, FreeCAD closed, the add-on's files loose in `$FC/v1-1/Mod`, no FreeCADMCP folder.
(b) Commands (terminal, 44 columns; the mv line is chosen at the take from D/ls-R-loose.txt so that it names every loose entry and nothing else; the exact line used is the `[lab]` value):
```
mkdir ~/.local/share/FreeCAD/v1-1/Mod/FreeCADMCP             # event: terminal: mkdir FreeCADMCP typed
cd ~/.local/share/FreeCAD/v1-1/Mod && mv Init.py InitGui.py rpc_server FreeCADMCP/   # plus any other loose entry from D/ls-R-loose.txt
                                                             # event: terminal: mv loose typed
ls ~/.local/share/FreeCAD/v1-1/Mod | tee out/fx1/E/ls-Mod-after-mv.txt   # expected: FreeCADMCP only
$FREECAD &                                                   # event: FreeCAD: restarting
# xdotool: open the workbench list                           event: workbench list: MCP Addon
# hold 5 s; screenshot E/workbench-list.png
# xdotool: File, Exit
ls -R ~/.local/share/FreeCAD/v1-1/Mod                        # event: terminal: ls -R typed
# hold 5 s; screenshot E/04-ls-R.png
```
(c) Events: `terminal: mkdir FreeCADMCP typed`, `terminal: mv loose typed`, `FreeCAD: restarting`, `workbench list: MCP Addon`, `terminal: ls -R typed`.
(d) Capture: E/terminal.txt, E/01-mkdir.png, E/02-mv.png, E/ls-Mod-after-mv.txt, E/workbench-list.png, E/04-ls-R.png; notes.md: the exact mv line used. Used in F8.
(e) Expected: MCP Addon listed after the restart (PLAN F8 narration); `ls -R` shows `Mod/FreeCADMCP/InitGui.py` (PLAN F8); the mv line: measure.
(f) PASS: MCP Addon listed; F8 stands with the mv line as typed. FAIL: not listed: compare E/ls-Mod-after-mv.txt with A0/C's working layout; if an entry was left loose, redo the mv once (take folder E-2); if the layout is identical to C's and it still does not show, stop rule 3, report.

### F (Addon manager search "MCP", Q3; evidence only, not a frame; continues from E)

(a) State: E's state (add-on working) or any state with FreeCAD open; network must be reachable from the container (the Addon Manager fetches its index); if the container has no network, stop rule 5.
(b) Commands:
```
$FREECAD &                                                   # event: FreeCAD: starting
# xdotool: Tools, Addon manager                              event: addon manager: opened
# wait for the list to load (up to 120 s); screenshot F/addon-manager-loaded.png
# if an update/index dialog appears first: screenshot F/dialog.png, accept the default, note its text
# xdotool: click the search box; type: MCP                   event: addon manager: search MCP typed
# hold 6 s; screenshot F/search-MCP.png (every hit and its author line readable; scroll and take F/search-MCP-2.png if the list is longer than the window)
# for each hit: click it; screenshot F/hit-N.png (the detail pane with author, repository URL, version)
date -u +%Y-%m-%d | tee out/fx1/F/date.txt
# xdotool: close the Addon manager; File, Exit
```
(c) Events: `FreeCAD: starting`, `addon manager: opened`, `addon manager: search MCP typed` (take-F events are not cut into any frame; the names are for the record).
(d) Capture: F/addon-manager-loaded.png, F/search-MCP.png (and -2), F/hit-N.png per hit, F/date.txt; notes.md: every hit verbatim as "name - author line - repository URL" and the line "FreeCAD MCP by neka-nat: listed / not listed".
(e) Expected: measure (ACCURACY B: "Whether the Addon Manager lists anything for 'MCP' on take day, and whose: lab: measure (Q3; the only evidence for the description line)"). For reading the author line: FreeCAD/Addons #189 "MCP+" (Connor9220/freecad-mcp-plus) and #70 "freecad-mcp-bridge" (CREATeNG) are different projects, not neka-nat's (ACCURACY B).
(f) PASS/FAIL (description and the F5 typed label only): if the search shows no entry whose author/repository is neka-nat: the description line "FreeCAD MCP by neka-nat is not listed in FreeCAD's Addon manager (checked DATE)" and the F5 label "not in the Addon manager: the folder is the way" are used, DATE = F/date.txt. If a different MCP add-on appears: the label and the line name the author shown (SCRIPT §0 Take F). If neka-nat's is listed: the line and the label are cut, reported as a finding (PLAN §1.5 and §1.3 change). Never written: "the index has not taken it", "will have it soon" (SCRIPT §3).

### A2-copy (the upgraded machine, Copy; Q1 c; new container)

(a) State: new container, fresh home; BEFORE the first start:
```
mkdir -p $FC/Mod
cp -r $ADDON_SRC/addon/FreeCADMCP $FC/Mod/
ls -R $FC | tee out/fx1/A2-copy/ls-before.txt            # $FC/Mod/FreeCADMCP/InitGui.py, no v1-1
ls -la $HOME/.config/FreeCAD |& tee out/fx1/A2-copy/ls-config-before.txt   # expected absent
```
(b) Commands:
```
$FREECAD &                                           # event: FreeCAD: starting
# wait; the dialog is expected on top               event: welcome dialog: shown
# hold 8 s; screenshot A2-copy/dialog.png (whole dialog, title bar readable); if the title bar is clipped, also xdotool getwindowname of the active window to A2-copy/dialog-title.txt
# xdotool: click "Copy Configuration (Recommended)"  event: welcome dialog: Copy clicked
# screenshot A2-copy/progress.png as soon as the progress text appears (capture every 0.5 s for 10 s into A2-copy/progress-NN.png; keep the first that shows text)
# FreeCAD restarts itself (expected); wait for the main window   event: FreeCAD: restarting
# xdotool: View, Panels, Report view; hold 5 s; screenshot A2-copy/report-view.png
# xdotool: View, Panels, Python console; type print(App.getUserAppDataDir()) Return; screenshot A2-copy/console-path.png
#                                                    events: console: opened, console: print typed, console: path printed
# xdotool: open the workbench list; hold 5 s; screenshot A2-copy/workbench-list-1.png   event: workbench list: MCP Addon
# xdotool: File, Exit
ls -R $FC | tee out/fx1/A2-copy/ls-after-copy.txt        # v1-1/Mod/FreeCADMCP present AND Mod/FreeCADMCP still present
diff -r $FC/Mod $FC/v1-1/Mod |& tee out/fx1/A2-copy/diff-Mod.txt ; echo "diff exit=${PIPESTATUS[0]}" | tee -a out/fx1/A2-copy/diff-Mod.txt   # expected 0 (bash; |& = stderr too)
ls -la $FC |& tee -a out/fx1/A2-copy/ls-after-copy.txt      # any v1-1.do_not_migrate marker? expected none
# the trap on an upgraded machine: a second add-on into the OLD Mod only
mkdir -p $FC/Mod/SecondAddon
printf 'import FreeCADGui\nclass SecondAddonWorkbench(FreeCADGui.Workbench):\n    MenuText = "SecondAddon"\n    ToolTip = "lab marker"\n    def Initialize(self):\n        pass\nFreeCADGui.addWorkbench(SecondAddonWorkbench())\n' | tee $FC/Mod/SecondAddon/InitGui.py
$FREECAD &                                           # event: FreeCAD: restarting
# xdotool: open the workbench list; hold 5 s; screenshot A2-copy/workbench-list-2.png   event: workbench list: opened (no SecondAddon)
# xdotool: File, Exit
```
(c) Events: `FreeCAD: starting`, `welcome dialog: shown`, `welcome dialog: Copy clicked`, `FreeCAD: restarting`, `console: opened`, `console: print typed`, `console: path printed`, `workbench list: MCP Addon`, `workbench list: opened (no SecondAddon)` (A2 events are for the record and the description; no frame cuts them; F3's small label is typed, not footage).
(d) Capture: A2-copy/ls-before.txt, dialog.png, dialog-title.txt, progress-NN.png, report-view.png, console-path.png, workbench-list-1.png, ls-after-copy.txt, diff-Mod.txt, workbench-list-2.png; notes.md: the dialog title verbatim, the three button texts verbatim, the progress text verbatim, the console path verbatim, whether "Migrating config from ... to ..." is in the Report view, whether SecondAddon shows.
(e) Expected: dialog title "Welcome to FreeCAD 1.1" (ACCURACY B: title format "Welcome to %1 %2.%3", DlgVersionMigrator.cpp line 140, tag 1.1.4); buttons "Copy Configuration (Recommended)" (line 161), "Share configuration with previous version" (171), "Use a new default configuration" (172) (same source); progress text "Migrating configuration data and addons…" (line 451, same source); restart after Copy (same source: "and restarts"); v1-1 is a recursive copy of the old folder and the Report view line "Migrating config from ... to ..." (ACCURACY B: ApplicationDirectories.cpp 572-615, 635-637) — whether the line is printed on screen: measure; console path ends in v1-1: measure (exact); old folder still exists (PLAN §0.3 row 3: "the old drawer stays behind"); SecondAddon not listed (PLAN Q1 c: "it does not show, which is the trap on a real upgraded machine").
(f) PASS: dialog with that title and those three buttons, Copy produces v1-1 with the add-on listed, SecondAddon in the old Mod stays hidden; F3's clause "1.1 asked at its first start whether to copy your old settings into the new drawer; the old one stays behind" and the description's "Upgrading from an older FreeCAD?" line stand. If the title or a button text differs: the recorded text replaces the plan's wording in the description; the F3 small label "first start of 1.1: Welcome dialog, Copy Configuration" keeps "Welcome dialog" only if the title starts with "Welcome" (else it uses the recorded title). FAIL: no dialog at the first start: stop rule 1 (F3's dialog clause and label are cut, retime.py rerun; report).

### A2-share (the upgraded machine, Share; Q1 c; new container)

(a) State: as A2-copy (a), fresh home with `$FC/Mod/FreeCADMCP` before the first start; `ls -R $FC` to A2-share/ls-before.txt.
(b) Commands:
```
$FREECAD &                                           # event: FreeCAD: starting
# dialog expected                                    event: welcome dialog: shown
# screenshot A2-share/dialog.png
# xdotool: click "Share configuration with previous version"   event: welcome dialog: Share clicked
# if FreeCAD restarts or continues: note which; wait for the main window
# Python console: print(App.getUserAppDataDir()); screenshot A2-share/console-path.png   events: console: opened, console: print typed, console: path printed
# workbench list; screenshot A2-share/workbench-list.png     event: workbench list: MCP Addon
# File, Exit
ls -la $FC | tee out/fx1/A2-share/ls-after-share.txt     # expected: a v1-1.do_not_migrate marker, no v1-1 folder
ls -la $HOME/.config/FreeCAD |& tee -a out/fx1/A2-share/ls-after-share.txt 2@1
find $HOME -name 'v1-1.do_not_migrate' | tee out/fx1/A2-share/marker.txt
```
(c) Events: `FreeCAD: starting`, `welcome dialog: shown`, `welcome dialog: Share clicked`, `console: opened`, `console: print typed`, `console: path printed`, `workbench list: MCP Addon`.
(d) Capture: A2-share/ls-before.txt, dialog.png, console-path.png, workbench-list.png, ls-after-share.txt, marker.txt; notes.md: marker path, console path verbatim, add-on listed or not.
(e) Expected: marker file `v1-1.do_not_migrate` written (ACCURACY B: "Share writes the marker and FreeCAD keeps reading the old folder", DlgVersionMigrator.cpp 60-81, 180-190); where it is written: measure (marker.txt); console prints the old path `$FC/` (PLAN Q1 c: "the console line prints the old path"), exact: measure; the add-on shows (PLAN Q1 c).
(f) PASS: marker exists, console prints the unversioned path, MCP Addon listed; the description's Share sentence and SCRIPT §3 "Share keeps it that way" stand. FAIL: no marker or v1-1 created anyway: record; the description's Share sentence is rewritten from the recording; no frame changes.

### A2-new (the upgraded machine, New default; Q1 c; new container; evidence only)

(a) State: as A2-copy (a).
(b) Commands: start FreeCAD (`FreeCAD: starting`), dialog (`welcome dialog: shown`, screenshot A2-new/dialog.png), click "Use a new default configuration" (`welcome dialog: New clicked`), wait for the main window, Python console line (console events, screenshot A2-new/console-path.png), workbench list (screenshot A2-new/workbench-list.png), File, Exit; then `ls -R $FC | tee out/fx1/A2-new/ls-after-new.txt` and `ls -la $FC |& tee -a out/fx1/A2-new/ls-after-new.txt`.
(c) Events: as named in (b).
(d) Capture: A2-new/dialog.png, console-path.png, workbench-list.png, ls-after-new.txt; notes.md: is `v1-1` created, is it empty (no Mod/FreeCADMCP), does the console end in v1-1, is MCP Addon listed (expected not, since the add-on is only in the old Mod).
(e) Expected: measure (PLAN Q1 c: "whether the New-default choice creates an empty v1-1").
(f) PASS/FAIL: no storyboard clause depends on it; the answer goes to the description only.

### Take order as run

A0 → A → B → C-drag → C-terminal (same container); D → E → F (second container; D-half in a third); A2-copy, A2-share, A2-new (one container each); R1 last (section 4). Any take that stops the lab (section 6) is reported before the next container starts.

## 4. The Claude run R1 (pre-registered)

- Prompt, one wording, verbatim (PLAN §0.4 Q4, SCRIPT §0): "Where exactly does the FreeCADMCP add-on folder go for FreeCAD 1.1 on this Linux computer? Give the full path."
- State before the run: a container in which take B's console path is known (B/notes.md); no plug connected: `claude mcp list` is run first and its output saved to runs/R1/mcp-list.txt, expected "No MCP servers configured. Use `claude mcp add` to add a server." (SCRIPT-L7 §0 Take A, lesson 7's recorded text); if any server is listed, remove it (`claude mcp remove NAME`) and rerun the list before R1. Folder: `mkdir -p $HOME/r1-empty && cd $HOME/r1-empty && ls -la` (empty; the `ls` output saved to runs/R1/ls-empty.txt). FreeCAD may be installed in the container but is not running and nothing tells Claude where it is. `claude --version` to runs/R1/version.txt. Auto mode: `claude` launched with the same command line lesson 7's R1 used (copied from out/l7/runs/R1; written to runs/R1/command.txt). The terminal recorded by x11grab; the prompt typed by xdotool at 80 ms/char.
- Events: `claude: typed` (at the Return after the prompt), `turn 1: reply done` (when the reply's last line is on screen and the input line is back). No second prompt is typed. No follow-up question is answered; if Claude asks a question instead of answering, the run ends there and that reply is the scored reply.
- Outcome classes (PLAN §0.4 Q4 and §1.7, SCRIPT §0 R1), scored on the reply's text as a whole:
  - A: the reply names a path containing `v1-1` as the place for the folder (for example `~/.local/share/FreeCAD/v1-1/Mod/FreeCADMCP`). Storyboard: F10 label "matches"; narration "[lab: its answer]" reads the path it gave; "Beside it, our console line: matches."
  - B: the reply names the old unversioned path (`~/.local/share/FreeCAD/Mod/...` or `~/.FreeCAD/Mod/...`) and no v1-1 path. Storyboard: F10 label "does not match"; narration "does not match"; PLAN §1.7: "this is why you check with the console line".
  - C: the reply gives no path of its own but tells us to run the console line / `getUserAppDataDir` (or to look it up on the machine). Storyboard: F10 label "half"; narration "half, it gave the check, not the answer".
  - Mixed replies: a reply that names both the old and the v1-1 path is scored by the path it recommends as the answer to "give the full path"; if it recommends both without choosing, score B (it did not give the one path) and note "both". A reply that names a v1-1 path AND says to check with the console line is A (the check is a bonus; notes.md records it). The scoring sentence is written in runs/R1/score.md with the quoted clause that decided it.
- Evidence frame: F2 (take B, `console: path printed`, B/console-path.png); the split screen's right half is that crop; the label is set by comparing the reply's path to B/notes.md's printed path plus `Mod/FreeCADMCP`.
- Record: runs/R1/session.jsonl (copy of the session file from `$HOME/.claude/projects/`), runs/R1/cost.txt (`/cost` output or the session's usage fields), runs/R1/model.txt (the model field from session.jsonl; expected claude-sonnet-5-5, SCRIPT §0 pins), runs/R1/tool-calls.txt (every tool call in the session, expected none: an empty folder, no plug; any Bash or file read is listed verbatim), runs/R1/reply.txt (the reply verbatim), runs/R1/reply.png (the crop with the greyed suggested prompt cut out; the uncropped runs/R1/reply-full.png kept), runs/R1/version.txt, runs/R1/command.txt, runs/R1/mcp-list.txt, runs/R1/score.md.
- Rule: one run, scored before it runs, no second try. If the run fails for a reason outside the prompt (no network, auth, Claude Code crash before the prompt is sent), the failure is recorded in runs/R1/failed-1.md and one retry is allowed only if `claude: typed` was never reached; once the prompt is sent, the reply (or the absence of one) is the result.

## 5. Measurements table (every [lab] mark of SCRIPT-fx1 §0 once)

| value | where it is used (frame / description line) | how measured | expected | source |
|---|---|---|---|---|
| Claude Code exact build | SCRIPT §0 pins; description "Tested:" | `claude --version` at R1 start, runs/R1/version.txt | 2.1.31x | SCRIPT §0 pins |
| R1 model | SCRIPT §0 pins, F10 chip | model field in runs/R1/session.jsonl | claude-sonnet-5-5 | SCRIPT §0 pins; SCRIPT-L7 §0 (lesson 7 saw it in session.jsonl) |
| Take DATE | description "Tested: ... DATE", "checked DATE" (Q3) | `date -u +%Y-%m-%d` at A0 start and F | measure | SCRIPT §0 pins |
| A0: `$FC/v1-1/` appears after the first start and quit | F1 narration "once FreeCAD 1.1 has made its new drawer"; Q1 a | A0/ls-FreeCAD.txt | yes | ACCURACY B, ApplicationDirectories.cpp 163-192 (tag 1.1.4) |
| A0: exact printed `getUserAppDataDir()` | Q1 a; F2 cross-check | A0/console.png, A0/notes.md | ends in `/v1-1/` | PLAN §1.6 step 1 |
| A0: `v1-1/Mod` created or only `v1-1` | F4 label "the Mod folder may not exist yet", the `mkdir -p` crop (SCRIPT §4) | A0/ls-v1-1.txt, A0/find.txt | measure | PLAN Q1 a |
| A0: no Welcome dialog on a clean home | SCRIPT §3 "on a clean home it never asks" | A0/first-start.png, no dialog window in xdotool search | none | ACCURACY B (DlgVersionMigrator.cpp exec(), marker/versioned-dir condition) |
| A0: does 1.1.4 create an unversioned `$FC/Mod` itself | §1.8 measured values; A (a) | A0/ls-FreeCAD.txt | measure | PLAN §1.8 |
| A: workbench list without MCP Addon | F0, S0 | A/workbench-list.png | no MCP Addon | PLAN §1.1; issue #146 (ACCURACY B) |
| A: Report view contents | F0 (nothing spoken), description | A/report-view.png, A/notes.md verbatim | "expected nothing; confirm, do not assume" | SCRIPT §0 Take A |
| A2: dialog exact title | F3 small label, description | A2-copy/dialog.png, dialog-title.txt | "Welcome to FreeCAD 1.1" | ACCURACY B, DlgVersionMigrator.cpp 140 |
| A2: exact button texts | description | A2-copy/dialog.png | "Copy Configuration (Recommended)", "Share configuration with previous version", "Use a new default configuration" | ACCURACY B, DlgVersionMigrator.cpp 161, 171, 172 |
| A2 Copy: progress text | description | A2-copy/progress-NN.png | "Migrating configuration data and addons…" | ACCURACY B, DlgVersionMigrator.cpp 451 |
| A2 Copy: v1-1 created as a copy, add-on shows | F3 clause, description | A2-copy/diff-Mod.txt (exit 0), workbench-list-1.png | copy; MCP Addon listed | ACCURACY B, ApplicationDirectories.cpp 572-615; PLAN Q1 c |
| A2 Copy: console path | description | A2-copy/console-path.png | ends in v1-1, exact: measure | PLAN Q1 c |
| A2 Copy: old folder still exists | F3 "the old one stays behind" | A2-copy/ls-after-copy.txt | `$FC/Mod/FreeCADMCP` present | PLAN §0.3 row 3 |
| A2 Copy: Report view "Migrating config from ... to ..." printed or not | description | A2-copy/report-view.png | measure | ACCURACY B, ApplicationDirectories.cpp 635-637 |
| A2 Copy: second add-on in the old Mod only, not shown | description "Upgrading from an older FreeCAD?" | A2-copy/workbench-list-2.png | not shown | PLAN Q1 c |
| A2 Share: `v1-1.do_not_migrate` written | description; SCRIPT §3 | A2-share/marker.txt | written | ACCURACY B, DlgVersionMigrator.cpp 60-81, 180-190 |
| A2 Share: console prints the old path (exact) | description | A2-share/console-path.png | `$FC/` (unversioned), exact: measure | PLAN Q1 c |
| A2 Share: the add-on shows | description | A2-share/workbench-list.png | shows | PLAN Q1 c |
| A2 New default: empty v1-1 created or not | description | A2-new/ls-after-new.txt | measure | PLAN Q1 c |
| B: exact console output | F2, F10 right half, F12, S1 (`[lab: exact path]`) | B/console-path.png, B/notes.md | `$FC/v1-1/` | PLAN §1.6; lesson 1's recorded path (ACCURACY B) |
| C-terminal: `ls ~/.local/share/FreeCAD` shows Mod and v1-1 | F4 first crop (lit: v1-1) | C-terminal/terminal.txt, 01-ls.png | Mod, v1-1 | SCRIPT §0 Take C |
| C-terminal: `mkdir -p` needed or not | F4 second crop, label | A0/ls-v1-1.txt, C-terminal/terminal.txt | measure | PLAN Q1 a; SCRIPT §4 |
| C: workbench list with MCP Addon after the move | F1, F5, F13, S2 | C-drag/workbench-list.png, C-terminal/workbench-list.png | MCP Addon | PLAN §1.6 step 5 |
| C: status-bar text after Start RPC Server | F5 (`[lab: exact text]`) | C-drag/status-bar.png, C-terminal/status-bar.png | "RPC Server started at 127.0.0.1:9875" | PLAN §0.4 Q10 (lesson 7 recorded) |
| D: exact `ls v1-1/Mod` listing after the star copy | F7 (`[lab: exact listing]`) | D/terminal.txt, 02-ls-loose.png, ls-R-loose.txt | "InitGui.py, Init.py, rpc_server/ and the rest" | SCRIPT §0 Take D |
| D: no MCP Addon | F7, F6 "Trap 2" | D/workbench-list.png | no MCP Addon | ACCURACY B row "cp -r ... no workbench appears" (lab: measure) |
| D: Report view contents | description | D/report-view.png, D/notes.md | measure | PLAN Q2 |
| D-half: Report view text (ImportError or not) | candidate extra beat (not in the storyboard) | D-half/report-view.png, notes.md | measure | PLAN Q2 |
| E: the exact mv line used | F8 second crop (lit: mv) | E/terminal.txt, 02-mv.png | measure | SCRIPT §0 Take E |
| E: MCP Addon in the list | F8 | E/workbench-list.png | MCP Addon | PLAN F8 |
| F: every "MCP" hit with its author line | description "not listed (checked DATE)" line; F5 typed label | F/search-MCP.png, F/hit-N.png, F/notes.md | measure | ACCURACY B (lab row, Q3) |
| F: the author named on the label/line if a different add-on appears | F5 label, description | F/notes.md | measure | SCRIPT §0 Take F |
| R1: outcome A / B / C | F10 label and narration | runs/R1/score.md | measure | PLAN Q4 |
| R1: the reply's words | F10 type-on, narration "[lab: its answer]" | runs/R1/reply.txt | measure | SCRIPT §0 R1 |
| R1: cost | SCRIPT §0 R1 | runs/R1/cost.txt | measure | SCRIPT §0 R1 |
| R1: label matches / does not match / half | F10 | reply path vs B/notes.md | measure | SCRIPT §0 R1 |
| R1: tool calls (expected none) | F10 chip "one run" | runs/R1/tool-calls.txt | none | PLAN §1.7 (no plug) |

## 6. Stop rules

1. A0 shows no `v1-1` after the first start, or a dialog appears on a clean home, or B prints a path not ending in v1-1: stop; report with A0/find.txt and the screenshot. The storyboard's F1, F2, F3, F10 rest on this; no fallback is named in the plan, rev 4 must be written first. Same rule for A2-copy if the Welcome dialog does not appear: stop the A2 takes, report; the plan's fallback is to cut F3's dialog clause and small label and rerun retime.py (PLAN §0.3 row 3 says the dialog is deterministic; a miss is a finding).
2. Take A shows MCP Addon in the list with the add-on in the old drawer: stop; the premise is false on 1.1.4 Linux; report (no fallback in the plan).
3. After a correct three-level layout (`v1-1/Mod/FreeCADMCP/InitGui.py`, verified by ls) MCP Addon is not listed: stop; report with the Report view screenshot; check first that `$ADDON_SRC` is the v0.1.28 download (`ls -l`, package.xml version line) and that the AppImage is 1.1.4 (`$FREECAD --version`).
4. Take D shows MCP Addon with loose files: stop the trap-2 takes (E unchanged can still be filmed for the record); report; plan fallback: F6's trap-2 card, F7, F8, F9 are cut and retime.py rerun (not pre-approved; rev 4 decides).
5. Addon Manager cannot load its index in the container (no network, or an error dialog): report the dialog text verbatim (F/dialog.png); the description's "not listed" line and the F5 typed label are NOT used (SCRIPT §0 Take F: used ONLY if the filmed search shows it).
6. A dialog with different text than expected (Welcome dialog title, button texts, progress text; any confirmation dialog on Exit or at first start): screenshot, transcribe verbatim, continue with the button that matches the intended choice by meaning, and flag the difference in notes.md; the recorded text replaces the plan's text everywhere.
7. FreeCAD 1.1.4 AppImage does not start or does not render in Xvfb (blank window, GL error): try with Mesa llvmpipe (`LIBGL_ALWAYS_SOFTWARE=1`); if it still fails, stop; report the stderr (saved as out/fx1/freecad-stderr.txt). No fx1 take can be filmed without it.
8. Windows-only steps (PowerShell `Copy-Item -Recurse`, `%APPDATA%`, the macOS path): never attempted in the lab; the plan's fallback is the typed note on F7 plus issue 116 in the description, and the path cards labelled "from the project's docs" (PLAN §0.3 rows 1-2; Owner 5 default).
9. The file manager in the image cannot show a drag (no drag support under xdotool, or no file manager present): film C-terminal only; SCRIPT §4 rule: F4's left half becomes the drag is NOT possible, so F1 and S2 use the terminal `mv` crop instead and the "file-manager drag" clause is flagged for rev 4; report.
10. R1: Claude Code cannot start or authenticate: record runs/R1/failed-1.md, one retry allowed only before `claude: typed`; otherwise the run is over. A plug found connected (`claude mcp list` not empty) is removed before the run, never after.
11. Any expected screen absent (no Report view panel, no workbench selector, the status bar hidden): screenshot, note, stop that take, report; do not improvise an alternative view.

## 7. Deliverables back to Cowork

Files (all under freecad-course-lab/out/fx1/): PREREG.txt (this file's commit hash), env.txt (FreeCAD and add-on paths, versions, date), per take A0, A, B, C-drag, C-terminal, D, D-half, E, F, A2-copy, A2-share, A2-new: take.mkv, events.tsv, notes.md and the screenshots and text files named in section 3; runs/R1: session.jsonl, cost.txt, model.txt, tool-calls.txt, reply.txt, reply.png, reply-full.png, version.txt, command.txt, mcp-list.txt, ls-empty.txt, score.md; ANSWERS.md with the one-line answers below.

One-line answers to fill (ANSWERS.md, one line each, verbatim values from notes.md):
- Q1 (a): v1-1 created on first start: yes/no; console prints: PATH; v1-1/Mod created: yes/no; dialog on clean home: none/TEXT.
- Q1 (b): add-on in old Mod, list without MCP Addon: yes/no; Report view: "empty" or the text.
- Q1 (c): dialog title: TEXT; buttons: TEXT, TEXT, TEXT; Copy progress text: TEXT; after Copy console: PATH; add-on shows: yes/no; old folder present: yes/no; "Migrating config from" line: printed/not; second add-on in old Mod shows: yes/no; Share marker path: PATH or none; Share console: PATH; Share add-on shows: yes/no; New default creates v1-1: yes/no, empty: yes/no.
- Q2: star copy listing: LIST; MCP Addon: yes/no; Report view: "empty" or the text; half-flattened Report view: "empty" or the text (ImportError: yes/no).
- Q3: hits for "MCP" on DATE: NAME by AUTHOR (each); neka-nat listed: yes/no.
- Q4: R1 outcome A/B/C; the reply's path or sentence; label matches / does not match / half; cost; model; tool calls: none or the list.
- Q10: status-bar text: TEXT.
- Q11: prereg commit HASH before the run: yes; one run: yes; auto mode command: TEXT; suggested prompt cropped: yes.
- Script-level: C filmed as drag and terminal: both/one; mkdir -p needed: yes/no (drives the F4 crop and retime.py).

These fill PLAN rev 4 §0 "lab fills" and SCRIPT-fx1 v2 §0; the description's DATE lines take F/date.txt and env.txt.
