# LAB-fx20: FreeCAD, a size that fights the others ("Value Error" / over-constrained) — pre-registration v1.1, 2026-11-14 (PLAN rev 2) (before any run)

v1.1 = plan gate round 1 applied (accuracy MUST 1-3, 8): the Insert Length dialog is predicted to refuse and undo a
clashing size, so G0-20 has three pre-registered rungs; the reference path is the dialog's "Reference" box; the
your-turn uses a different value (41) on a rectangle tied to the origin.

Lab repo: freecad-course-lab. Folder: out/fx20/ (G0, P, A, B, C, D, E; run runs/R1). Committed into
out/fx20/LAB-fx20.md before the first container (hash into PREREG.txt); `| tee` on every command; deviations in
DEVIATIONS.md; nothing re-scored. Runs after the fx19 lab (one lab at a time; G0s together), on the PC
(HANDOVER-lab.md). Never pushed.

## 0. Pins
As LAB-fx19 section 0. Start file: `out/l2/hand/hand.FCStd` copied to P/hook.FCStd (fully constrained, 6 sizes, Pad
20, 8,500.0). Outline: (0,0) right 25, up 10, left 5, down 5, left 15, up 55, left 5, back. The arm's top is the
line (20, 5)-(5, 5), 15 long, no size of its own (25 - 5 - 5). Geometry indices are found by end points and logged,
never assumed.

## 1. PROBE FIRST: gate G0-20 (no filming, no AI, minutes)
G0a (headless freecadcmd; out/fx20/G0/g0a.py, g0a.txt):
1. Open P/hook.FCStd; log constraint count, `solve()` code, DoF if exposed, the arm-top line's index.
2. setDatum path (what the dialog does): add a driving Distance on the arm-top line at its current length (15), then
   `setDatum(index, 17 mm)` inside try/except (then reopen P/hook.FCStd before the next step): log the exception type and text verbatim, the constraint count after,
   the sketch's solve code. Prediction: ValueError "Negative datum values are not valid for the constraint with index
   N" (-4), the value restored. Repeat with 15 (Q12): prediction ValueError "Datum ... is invalid" (-2). Reopen P/hook.FCStd before step 3.
3. addConstraint path (rung c): `addConstraint(Sketcher.Constraint('Distance', g, 17))`; `solve()`; recompute; log the
   code, `ConflictingConstraints`, `RedundantConstraints`, `getStatusString()`, the Pad's validity. Prediction: -4,
   "Over-constrained sketch" + "Remove at least one of the following conflicting constraints: ...". Undo.
4. Control (the fix): bottom 25 to 27 by setDatum: code 0, Pad valid, 8700.0; a non-driving (reference) Distance on
   the arm top reads 17.0.

G0b (GUI, one container, stills only; out/fx20/G0/g0b-*.png). Rungs in this order, no others:
- Rung a: open P/hook.FCStd; double-click the sketch; Dimension tool (record its shortcut) on the arm-top line; type
  17; OK. Stills: the refusal message (popup, then the notification list opened; caption, sender label, full text
  verbatim; its expiry), the sketch after it (is the size kept? colour), Solver messages panel. env.txt gets the
  NonIntrusiveNotificationsEnabled value; never change that preference. Then the same with 15 (Q12). Then the same with the Insert Length dialog's "Reference" box
  ticked (Q13): size kept, blue, reads 15.00.
- Rung b (only if a shows no refusal AND the size stays driving): stills of Solver messages "Over-constrained:" and,
  after Close, the Report view and tree marks. If a showed a refusal, rung b is NOT run.
- Rung c (always): open G0a step 3's saved over-constrained copy: stills of the red sketch, Solver messages
  "Over-constrained:" with numbers, a click on the numbers (what it selects), the Report view line after Close.
**G0-20 pass = rung a shows the refusal text (popup, notification list or modal box) and the size not kept (the predicted case), OR rung b
shows a lasting red "Over-constrained" state.** Rung c is evidence for F4/take D, not a pass on its own. A fail = stop:
fx20 dropped, RESULTS-fx20.md, the planner swaps in fx21 (G0-21 ran in the same slot, LAB-fx19 section 1).
After G0: report to the planner (verbatim texts); PLAN rev 3 picks the title from 2.3; wait before take A.

## 2. Common to every take
As LAB-fx19 section 2.

## 3. Takes (run order; written for the rung a outcome; on rung b the planner rewrites A/B)
### Take P: start files (not filmed)
out/fx20/P/make.py: P/hook.FCStd (copy); P/hook-red.FCStd (G0a step 3's over-constrained copy, rung c);
P/check.txt (DoF 0 and 8500.0 for hook.FCStd).
### Take A: the refusal (F0, F1, F4 left fallback; Short S0)
Open hook.FCStd; 3 s full window; double-click the sketch; "Fully constrained" held 4 s; drag a corner: nothing moves
(F1); Dimension on the arm's top, 17, OK; film the popup, then open the notification list and hold it 8 s
(A/refusal.png); close the list; the sketch unchanged held 4 s.
### Take B: the fix (F2, F5, F7 right; Short S1, S2)
Continue from A: double-click the bottom size 25, type 27, OK; "Fully constrained" (B/green.png); Close; the Pad
rebuilds; View, Panels, Python console; the lesson-1 volume line with the Pad selected: expected 8700.0 (Q14);
Solver messages and DoF text (Q15).
### Take C: a reading, not an order (F6)
B's result: Dimension on the arm's top; in Insert Length tick "Reference" (locator; Q13) and do NOT type a value (it is
ignored, EditDatumDialog.cpp 231); OK: blue, expected 17.00
(C/ref.png); bottom to 30: the blue reads 20.00; still fully constrained; Ctrl+Z back to 27. If the dialog has no
Reference box, use the Toggle Driving/Reference Constraints mode before the click and record the path.
### Take D: MCP, no AI (F9 left; F4 left; Q17)
out/fx20/D/noai.py through `execute_code`: (1) setDatum 17 on a new arm-top size, print the exception text; (2) open
hook-red.FCStd and print the solve code and conflicts. Tee D/reply.txt; film the terminal full window, then the
window showing hook-red.FCStd's red sketch and "Over-constrained:" (F4 left). Record what each reply carries without
and with prints.
### Take E: your turn (F10)
By hand: new document, Body, sketch on XY, Rectangle tool from the origin, sizes 40 and 20 (record DoF: expected 0
with the corner on the origin); Dimension on the far side, 41, OK: the refusal text (Q16; predicted -4 "Negative datum values
are not valid ..." if DoF is 0, else -3 "Cannot set the datum ..."); again with Reference ticked:
reads 40.00; Close; Pad 10; console 8000.0. Q12 still for the pinned comment: the hook's arm top sized 15 (from G0b).

## 4. The Claude run R1 (pre-registered; PC only)
Prompt, first and only message: `Make the top of the hook's arm 17 mm long.`
State: P/hook.FCStd open (fully constrained, Pad 20, 8,500); plug socket started; Claude Code with
`--strict-mcp-config --mcp-config` naming only the freecad server; auto mode; Sonnet; cap $0.25; one try. Files as
LAB-fx19 section 4; read-after.json (no AI): the arm-top length, solve code, conflicts, redundancies, DoF, the Pad's
validity and volume.
Classes:
- A: arm top 17.00, solve code 0 with no conflicts or redundancies, volume 8,700 within 0.1%, and the reply says
  which size it changed.
- B: arm top 17.00 another way (lip or back plate changed, a redrawn sketch), sketch solves, volume as read-after
  shows, and the reply says so.
- C: the reply says the arm is 17 while the sketch fails to solve, or the arm is not 17.
- D: anything else, incl. a cap kill.
Prediction: a setDatum on a new driving size meets the "Negative datum ..." ValueError; an addConstraint leaves the
sketch over-constrained until Claude acts; a direct edit of the bottom never meets either. F9 says which happened.

## 5. Measurements (predicted BEFORE the lab)
| value | used in | how | expected | source |
|---|---|---|---|---|
| rung a refusal text (G0-20) | F0, F4, S0, title | G0b, A | "Negative datum values are not valid for the constraint with index N" | ACCURACY C.3b |
| same value (15) | question card | G0a 2, G0b | "Datum ... is invalid" refusal | C.3b |
| rung c panel + Report line | F4 left, F9 | G0, D | "Over-constrained:" / "Over-constrained sketch ..." | C.1 |
| fixed volume (bottom 27) | F5 | B | 8700.0 mm3 | C.5 |
| reference reading | F6 | C | 17.00, then 20.00 | arithmetic |
| your-turn: 41 refused; reference 40.00; Pad | F10 | E | refusal text; 40.00; 8000.0 mm3 | 40 x 20 x 10 |
| MCP replies | F9 | D | measure | |

## 6. Stop rules
- S1 (G0-20): section 1. No improvised rungs.
- P0: hook.FCStd not DoF 0 or not 8,500 within 0.1%: stop.
- B1: after bottom 27 the sketch does not solve or the Pad is not 8,700 within 0.1%: type what shows; stop.
- R1 as LAB-fx19.

## 7. Deliverables
As LAB-fx19 section 7, folder out/fx20, RESULTS-fx20.md, marker out/fx20/fx20-lab.DONE.
