# fx19 deviations (LAB-fx19 v1.1)

1. G0a step 1: FreeCAD 1.1.4's Python has no `SketchObject.movePoint`; the same call is `moveGeometry(GeoId, PointPos,
   Vector, relative)` (its own docstring: "Move a given point (or curve) to another location."). Used with the same
   arguments; the first g0a run stopped at that line before saving anything. The solver's DoF read from the
   sketch's `DoF` property after `solve()`.
2. G0b first container: the env line called the FreeCAD GUI binary with --version, which never returned; the
   container was killed with no stills. Fix 1: env from `freecadcmd --version` (env.txt).
3. G0b run 2 (G0/run2): the reader sent socket queries while the modal "Input error" box was up; they waited, then
   ran and printed their code in red into the Report view, and the box closed out of order. Fix 2 (the clean
   run, G0/g0b-*): the box closed by its own OK at the place run 1's still shows it, no query while it is up. Rule for
   the takes: no socket query while a modal box is open; every socket query adds "Python code executed
   successfully." to the Report view.
4. G0b: Validate Sketch started by its command (Sketcher_ValidateSketch) after the still of the open Sketch menu, not
   by clicking the menu item (an open menu blocks the socket). The takes click the item (offset from g0b-7).
5. G0b: the tree tooltip was not recorded (hover gave no popup on Xvfb; ToolTipRole empty). The tree icon's error mark is.
6. PLAN rev 3 lab fills (DECISIONS.md, 14 Nov, after G0): take A ends with the box's OK, then Cancel (the Pad is
   removed); take B = Validate, rejoin the gap in the sketch, close it, Pad again (20, OK). Validate labels as found
   (no count text); DoF 2; tree tooltip dropped.
7. Take A first container (A/attempt1, kept): the Sketch row was under a closed Body, the lookup returned "none", the
   script stopped about 10 s into the recording (3 s open + isometric + front only). Fix 1: the tree opened before
   the recording (lab/fx19_lib.sh row_open). Take A then ran once in full (A/).
8. Take A: "slow orbit" filmed as key 0 (isometric), hold, key 1 (front), not a mouse orbit.
9. Take B order: Validate + Highlight before entering the sketch (Validate Sketch is in Part Design's Sketch menu;
   G0 showed it there), and Validate again after closing the sketch, BEFORE the second Pad (the sketch row is
   then still on top). The sketch was left with Esc (selection cleared, then FreeCAD left the sketch on the same
   Esc); the script's "Close" lookup found nothing, harmless. Zoom on the corner: 12 wheel steps (gap 15 -> 90 px).
10. Take B's console step missed: the Python console docked as a hidden tab beside the Report view, so the click had
   no target (its typed line went nowhere; the read after: Pad valid, 8500.0). Re-filmed as pickup take B2 on B's own
   saved document (B/B-fixed.FCStd): Pad clicked, View > Panels > Python console, the "Python Console" tab, the line:
   8500.0 on screen (B2/volume.png). The console helper now clicks the tab (lab/fx19_lib.sh console_line).
11. Takes A and B: the lab's socket queries (row lookups, sketch points) each add "Python code executed
   successfully." to the visible Report view during B. C, E, B2 and R1 close the Report dock before recording.
12. Take C: the last click was aimed 2 mm above the first point; it landed at (0.039, 2.419) mm (2.42 mm gap, the
   LAB said 1-2 mm). The second outline was drawn in a second sketch (Sketch001) after hiding the first (Space), not
   in the same sketch. Q4's hook-touch file was opened over the socket, not by File > Open.
13. Take E: attempt 1 (E/attempt1): the second size's place click landed on the task panel, the sketch was then left
   by Esc and the corner click + Delete deleted the whole sketch. Fix 1: the size placed inside the rectangle, and a
   guard stops the take if the sketch is not in edit with both sizes. Attempt 2 (E/attempt2): the Delete removed
   only the corner's Coincident, but the drag did not move the end (no preselection: the cursor had not moved since
   the click), so there was no gap; joined nothing, Pad 10 built 6000.0 (touching ends). Fix 2: the cursor moved away
   and back before the drag. E (final) ran once: gap 0.915 mm, the join added Coincident (3,1,2,2), Pad 10 = 6000.0.
   Both earlier attempts are kept.
14. Take D: the plug's packages came from a uv cache warmed in a separate container with network
   (out/scratch/uvcache-fx19, not committed); the take ran with --network none and UV_OFFLINE=1.
15. R1: Claude Code was started inside its tmux pane before the recording, so its start banner (version, model,
   plan name, folder; no e-mail) is on screen in the first seconds of runs/R1/screen.mp4. The cut starts after it or
   crops it. `claude mcp list` (mcp-list.txt) printed only "Checking MCP server health…" (claude.ai lines filtered;
   the strict config is not read by `mcp list`).
16. R1 session.jsonl: 16 context lines dropped before commit (skill listing, session context, prompt snapshots, API
   request shapes/blobs: they named the account's connectors and the account e-mail) by lab/fx19redact.py (tested);
   the turn's 66 lines kept. tools.txt was rebuilt on the host from transcript.jsonl (the in-container parser hit a
   non-dict proxy line).
