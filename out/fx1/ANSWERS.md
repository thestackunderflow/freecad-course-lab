# fx1 lab answers (take day 2026-11-04 UTC; FreeCAD 1.1.4, freecad-mcp 0.1.28, Linux AppImage in Docker)

Prereg commit: see PREREG.txt (LAB-fx1.md committed before the first take). Take scripts: lab/fx1take.sh. Recordings are screen.mp4 + events.jsonl (+ events.tsv converted) instead of take.mkv: same content, the screen-lab kit's format.

## Findings that change the plan (read first)
1. **A2 needs an old CONFIG folder too.** With only `~/.local/share/FreeCAD/Mod/FreeCADMCP` present on a fresh home (no `~/.config/FreeCAD`), FreeCAD 1.1.4 showed NO Welcome dialog (first probe, not kept). The dialog appeared only after the home also had unversioned `~/.config/FreeCAD/user.cfg + system.cfg` (what a machine that ran an older FreeCAD has). The A2 takes use that state (old_machine() in fx1take.sh: FreeCAD run once, its cfg files moved up one level, v1-1 folders removed, add-on put in the old Mod). SCRIPT §3 "whenever an unversioned folder exists without v1-1" needs "an unversioned config folder" in the wording.
2. **Status bar text has a PID:** "RPC Server started at 127.0.0.1:9875 (PID 1383)." (C-drag) and "(PID 4398)." (C-terminal). The plan's "RPC Server started at 127.0.0.1:9875" is incomplete; the PID differs per run.
3. **Half-flattened case DOES print:** D-half Report view: `04:17:36 [MCP] Auto-start failed: No module named 'rpc_server'` (red), and MCP Addon IS in the workbench list (InitGui.py alone is enough to list it). Candidate extra beat (not an ImportError text, but a message the viewer would see).
4. **R1 used a tool call:** the lab image has FreeCAD installed, so Claude ran `freecadcmd` to ask for the data dir (see runs/R1/score.md). Outcome A.
5. A clean first start shows an in-tab "Welcome to FreeCAD" first-run panel (language, unit system, theme) on the Start page: it is NOT a dialog window (wmctrl lists only the main window). Do not confuse with the migration dialog.
6. No mkdir needed? No: `v1-1/Mod` is NOT created by FreeCAD's first start, so `mkdir -p` is needed (F4 crop stays). Reset for C-terminal removed the empty Mod that C-drag's new-folder step created (so the take starts from A's state).

## Q1 (a)
v1-1 created on first start: **yes**; console prints: **/home/maker/.local/share/FreeCAD/v1-1/**; v1-1/Mod created: **no** (v1-1 holds Macro, SavedPreferencePacks; config in ~/.config/FreeCAD/v1-1: system.cfg, user.cfg); dialog on clean home: **none** (only the in-tab first-run panel); no unversioned `$FC/Mod` created by FreeCAD (A0/ls-FreeCAD.txt shows only v1-1).

## Q1 (b)
add-on in old Mod, list without MCP Addon: **yes** (A/workbench-list.png); Report view: **empty** (A/report-view.png).

## Q1 (c)
dialog title: **"Welcome to FreeCAD 1.1"**; text: "Configuration data and addons from a previous program version were found. Migrate the configuration to a new directory for this version? ... Estimated size of data to copy: 99.75 KiB" (A2-copy/dialog.png); buttons: **"Help"** and the split button **"Copy Configuration (Recommended)"** whose arrow menu holds **"Share configuration with previous version"** and **"Use a new default configuration"** (A2-share/dialog-menu.png). Copy progress text: the migration is so quick that only a small window titled "Restarting" with **"Migration complete → Restarting..."** was seen (frames 11.8-12.1 s of A2-copy/screen.mp4); "Migrating configuration data and addons…" was NOT seen on screen. FreeCAD restarts itself (yes). After Copy console: **/home/maker/.local/share/FreeCAD/v1-1/**; add-on shows: **yes**; old folder present: **yes** (Mod/FreeCADMCP still there; a Macro folder also appeared beside Mod); "Migrating config from" line: **not printed** (Report view empty after the restart); second add-on in old Mod shows: **no** (SecondAddon absent from the list, A2-copy/workbench-list-2.png); diff -r old Mod vs v1-1/Mod: differs only by __pycache__ .pyc files (exit 1; sources identical). Share marker path: **~/.local/share/FreeCAD/v1-1.do_not_migrate AND ~/.config/FreeCAD/v1-1.do_not_migrate** (both); Share console: **/home/maker/.local/share/FreeCAD/** ; Share add-on shows: **yes**; no v1-1 data folder created. New default creates v1-1: **yes**, empty: **yes** (Macro, SavedPreferencePacks only, no Mod/FreeCADMCP); console ends in v1-1; MCP Addon **not** listed.

## Q2
star copy listing (`ls ~/.local/share/FreeCAD/v1-1/Mod`): **Init.py  InitGui.py  package.xml  rpc_server** (loose); MCP Addon: **no**; Report view: **empty**; half-flattened (Mod/FreeCADMCP with only InitGui.py) Report view: **"04:17:36 [MCP] Auto-start failed: No module named 'rpc_server'"**, ImportError: **no ImportError text, but that message**; MCP Addon listed: **yes**. (D used `mkdir -p v1-1/Mod` unfilmed first because FreeCAD does not create it.) E fix: `mkdir ~/.local/share/FreeCAD/v1-1/Mod/FreeCADMCP` then `cd ~/.local/share/FreeCAD/v1-1/Mod && mv Init.py InitGui.py package.xml rpc_server FreeCADMCP/` (E/notes.md); after restart MCP Addon listed (E/workbench-list.png).

## Q3
Addon Manager (version 2026.2.19) search "MCP" on **2026-11-04**: one hit, **"MCP Bridge" v0.1.26 by CREATeNG, repository https://github.com/CREATeNG/freecad-mcp-bridge** (F/search-MCP.png, F/hit-1.png; the maintainer line shows an email address: crop it out of any video frame). neka-nat listed: **no**. So the description line is "FreeCAD MCP by neka-nat is not listed in FreeCAD's Addon manager (checked 2026-11-04)" but the F5 typed label must NOT say "not in the Addon manager" alone: a different MCP add-on (MCP Bridge by CREATeNG) IS listed, per SCRIPT §0 Take F. The manager first shows an "Addon Manager Warning" (Continue / Cancel; F/warning.png); the index loaded within ~50 s (network reachable).

## Q4
R1 outcome: **A**. Reply path: **/home/maker/.local/share/FreeCAD/v1-1/Mod/FreeCADMCP** (reply.txt). Label: **matches**. cost: **$0.0535** (cost.txt, ledger ../fx1-BUDGET.tsv); model: **claude-sonnet-5-5** (model.txt); Claude Code **2.1.308** (version.txt; not 2.1.31x). tool calls: **2 Bash calls** (tool-calls.txt): file search and `freecadcmd` getUserAppDataDir. Events: `turn 1: Enter` = claude: typed (12.2 s), `turn 1: reply done` (28.0 s).

## Q10
status-bar text: **"RPC Server started at 127.0.0.1:9875 (PID 1383)."** (C-drag; PID 4398 in C-terminal).

## Q11
prereg commit before the run: **yes** (PREREG.txt); one run: **yes**; auto mode command: **`claude`** (command.txt, no flags; auto mode on per the screen); suggested prompt cropped: **yes** (reply.png; the greyed "create that Mod directory for me" is only in reply-full.png).

## Script-level
C filmed as drag and terminal: **both**; mkdir -p needed: **yes**. The drag works with PCManFM (two windows side by side, drag icon from left to right window; first attempt with the pointer under the icon label failed, then pressed on the icon itself). C-drag restart-to-list took ~26 s of real time (chip "sped up"). C-drag also films the new-folder step (Ctrl+Shift+N, typed "Mod") because v1-1/Mod does not exist.

## Deviations from LAB-fx1.md
- A0, A, B ran in one container; C-drag and C-terminal were re-run in fresh containers whose state was rebuilt (A0 unfilmed, add-on in old Mod) because PCManFM tabs/ids failed in the first pass; C-terminal's state reset removes the empty v1-1/Mod (so mkdir -p is a real step).
- A2 uses the old-config precondition (finding 1). A2-copy-2 is the recorded second start (SecondAddon test). A2-copy console typed after the restart; the Report view is read from its tab.
- Take F: one hit only; hit detail captured (hit-1.png); no further scroll needed.
- `workbench list: MCP Addon` in the brief is `workbench list: MCP Addon chosen` in C-drag/C-terminal/E events (E also has `workbench list: MCP Addon`); `console: print typed` etc. as brief. D `cd` step added (`terminal: cd typed`).
- E's last command is `ls -R ~/.local/share/FreeCAD/v1-1/Mod | head -8` (event `terminal: ls -R typed`).
- Zoomed clips: clips/*.mp4 (lab/fx1clips.py, 1920x1080, click rings, no chips); the FreeCAD crops are fixed boxes, the build stage may re-cut.
