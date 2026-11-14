# LAB-fx19: FreeCAD Pad: "Wire is not closed." — pre-registration v1.1, 2026-11-14 (PLAN rev 2; plan gate round 1 applied) (before any run)

Lab repo: freecad-course-lab. Folder: out/fx19/ (G0, P, A, B, C, D, E; run runs/R1). This file is committed into
out/fx19/LAB-fx19.md before the first container starts (hash into out/fx19/PREREG.txt); `| tee` on every command;
deviations in out/fx19/DEVIATIONS.md; nothing re-scored. Runs only after the plan gate (DECISIONS.md) and on the PC
(HANDOVER-lab.md). Never pushed.

## 0. Pins
FreeCAD 1.1.4 AppImage in `fcc-app:1.1.4-0.1.28` (image ID 8e44e83ab6ce into env.txt with `FreeCAD --version`
output, Xvfb size, Qt scale); freecad-mcp 0.1.28 (`uvx freecad-mcp@0.1.28`, takes D and R1 only); Claude Code version
and model id for R1 from the run itself. All takes `--network none`. Start file: lesson 2's by-hand hook
`out/l2/hand/hand.FCStd` (8,500.0 mm3; sketch on XZ, 8 lines, fully constrained, Pad 20), copied, never edited.

## 1. PROBE FIRST: gate G0-19 (no filming, no AI, minutes)
Purpose: stop rule S1, "the line must reproduce", before any take. Two steps, one container each, stills only.

G0a (headless, `freecadcmd` in the image; out/fx19/G0/g0a.py, output g0a.txt):
1. Open a copy of hand.FCStd; delete the Pad. Find (by end points, logged) the closing line (0, 60)-(0, 0) and every
   constraint on it. Log which point at (0, 0) carries the tie to the origin (root Coincident or point-on-axis) and whether the
   closing line has a Vertical rule. Delete ONLY: the Coincident joining the closing line's end to the first line's
   start at (0, 0), and any length size on the closing line (if one of the six sizes sits there, log which). Then
   move the end that is NOT tied to the origin with `movePoint`: the closing line's end to (0, 0.5), or, if that end
   carries the origin tie, line 1's start to (0.5, 0). No other branch. Recompute TWICE. Save as P/hook-gap.FCStd. Log: the measured distance between the two ends (pass needs
   0.50 +- 0.01 after both recomputes; the vertical rule and the 60 size must not pull it shut), the sketch's wires and
   `isClosed()` per wire, the solver's DoF text (expected 1 or more: F1/F6 never say Fully constrained).
1b. On a copy: re-add the Coincident, recompute, Pad 20 = 8500.0 within 0.1% (the join moves the free end back,
   not the plate; log DoF: if 1, F2/F5 never say Fully constrained). Discard the copy.
2. Add PartDesign::Pad on the sketch, Length 20; recompute. Log `pad.isValid()`, `pad.getStatusString()`,
   the document's recompute messages, `pad.Shape.isNull()`.
   Prediction: invalid; status contains "Wire is not closed." (FaceMakerBullseye.cpp 83).
3. Rung 2 (pre-registered, only if step 2 builds or shows another line): the same with a 2.0 mm gap. No third rung.
4. Control: hand.FCStd unchanged, recompute: valid, 8500.0.

G0-21 (spare) runs in the same G0 slot, after G0-20, from PLAN section 3 (headless Pocket preview and one GUI still;
pass = the "Resulting shape is empty ..." text visible in the Pocket task panel); recorded only, used on a swap.

G0b (GUI, one container, Xvfb, stills only; out/fx19/G0/g0b-*.png):
1. Open P/hook-gap.FCStd (the gap that showed the line in G0a); select the sketch; Part Design, Pad; Length 20; OK.
2. Stills of: the task panel, any dialog (its title and text), the Report view (View, Panels, Report view), the tree
   icon and its tooltip. Record the exact words and their place. Close any dialog with its own button.
3. Validate sketch (Sketch menu): stills of the dialog (predicted "Sketch Validation"); section "Open and Non-Manifold
   Vertices"; button "Highlight Troublesome Vertices": record the number of marks (predicted 2), colour and shape
   (predicted orange/yellow plus marks), and any count text. Names recorded exactly as shown.
**G0-19 pass = the words "Wire is not closed." visible somewhere in the window (task panel, dialog, Report view or
tree tooltip) after step 1 AND the gap measured 0.50 mm in G0a (2.00 mm if rung 2 ran; the narration's "half a millimetre"
follows the rung).** A fail (another line, or the Pad builds) = stop: fx19 dropped, RESULTS-fx19.md written,
the planner swaps in fx21 (spare). Exception, pre-registered: if the window shows a different refusal whose fix is the
same (join the gap), record it verbatim and stop for the planner; the planner and the accuracy reviewer decide at the
script gate, not the lab.
After G0: report to the planner, wait for PLAN rev 3 "lab fills" before take A.

## 2. Common to every take
As the course lab (`lab/common.sh`): full-window recording of the whole display, TAKE/screen.mp4 x11grab 30 fps +
cursor log, events.jsonl, 3 s full-window open, 4 s holds on every line to read, stills at every event.

## 3. Takes (run order)
### Take P: start files (not filmed)
No-AI script out/fx19/P/make.py (from G0a): P/hook-gap.FCStd (the G0 gap), P/hook-touch.FCStd (Q4: the last end
placed ON (0, 0) exactly by script, no Coincident rule; source predicts the wire closes at 1e-7 mm and Pad builds). Each reopened; volumes and wire closure logged in P/check.txt.
### Take A: the refusal (F0, F1, F4 left; Short S0)
Open hook-gap.FCStd; 3 s full window; slow orbit; select the sketch; Pad, 20, OK; the line held 8 s (A/refusal.png).
### Take B: the fix (F2, F5, F7 right; Short S1)
Double-click the sketch; Validate sketch, Highlight Troublesome Vertices (B/validate.png); click the two end points, C; Close; the Pad
recomputes (Refresh if its mark stays; record which); Validate sketch again (none); View, Panels, Python console; the
lesson-1 line with the Pad selected: expected 8500.0 (B/volume.png). Q2, Q3.
### Take C: how the gap happens (F6; Short S2 background)
New sketch on XZ; Polyline the hook's eight corners by clicks; last click 1-2 mm off the first point (no highlight):
Esc; zoom in on the corner (C/apart.png). Then the same with the last click ON the first point: record whether a
highlight cue shows on Xvfb (Q5) and that it closes. Q4: open hook-touch.FCStd; Pad 20: built or refused (C/touch.png). Q5 also records whether the closing click on the
highlighted first point adds a Coincident itself (the constraint list before and after).
### Take D: MCP, no AI (F9 left; Q7)
out/fx19/D/noai.py through the plug (`execute_code`): open hook-gap.FCStd, add the Pad, recompute, print
`pad.isValid()` and `pad.getStatusString()`; tee to D/reply.txt; film the terminal full window. Record exactly what
the reply carries without the prints (a first call with no prints, then one with).
### Take E: your turn (F10)
By hand, as a viewer would: New document, Part Design, New Body, sketch on XY; Rectangle tool; sizes 30 and 20; delete
one corner's Coincident and drag that end about 1 mm apart; Validate, the two marks; join (C); Close; Pad 10; console
volume expected 6000.0 (Q6). Record each step's path for the description.

## 4. The Claude run R1 (pre-registered; PC only)
Prompt, first and only message: `Pad the sketch in this document 20 mm.`
State: hook-gap.FCStd open in FreeCAD 1.1.4 (no Pad); the plug's socket started; Claude Code started with
`--strict-mcp-config --mcp-config` naming only the freecad server (HANDOVER-lab.md), auto mode, Sonnet; cap $0.25; one
try; no message after the prompt. Files: reply.txt, tools.txt (FreeCAD calls only), transcript.jsonl (proxy),
read-after.json (no-AI: every Pad's isValid, status string, volume; the sketch's open vertices), after.png.
Classes:
- A: a Pad that is valid, volume 8,500 within 0.1%, the sketch's wire closed, and the reply says it found and closed
  a gap (or quotes the line).
- B: a valid solid of 8,500 within 0.1% made another way (redrawn sketch, Part Extrude, a new document) and says so.
- C: the reply says the Pad is done while read-after shows an invalid Pad or another volume.
- D: anything else, incl. a cap kill; F9 rewritten at the script gate.
Prediction: execute_code shows only printed Output, so if Claude does not check the Pad, class C is possible. Only
whole sentences of the reply are quoted.

## 5. Measurements (predicted BEFORE the lab)
| value | used in | how | expected | source |
|---|---|---|---|---|
| the line, where (G0-19) | F0, F4, S0 | G0b, A | "Wire is not closed." | ACCURACY B.1-B.2 |
| Validate sketch names, count | F2, F8 | G0b, B | measure | B.5 |
| fixed hook volume | F5 | B | 8500.0 mm3 | lesson 2 measure.json |
| Polyline highlight cue | F6 | C | measure | none |
| touching ends, no Coincident | question card | C | measure | B.7 |
| your-turn rectangle (by hand) | F10 | E | 6000.0 mm3 | 30 x 20 x 10 |
| MCP reply content | F9 | D | Output only unless printed | freecad-mcp execute_code |
| R1 class, cost | F9 | R1 | not predicted; cap $0.25 | |

## 6. Stop rules
- S1 (G0-19): see section 1. No improvised rungs.
- P0: a start file's check differs from the expected volume by over 0.1%: stop and report.
- B1: joining the gap does not make the Pad valid: type what shows; stop (F2 cannot be filmed).
- R1: no retry, max 2 fix attempts per lab step, unexpected dialogs closed with their own button and logged.

## 7. Deliverables
out/fx19/env.txt, PREREG.txt, G0/*, P/*, {A,B,C,D,E}/events.jsonl + screen.mp4 + stills, runs/R1/*, ANSWERS.md
(Q1-Q8), DEVIATIONS.md; RESULTS-fx19.md in the plan folder; marker out/fx19/fx19-lab.DONE.
