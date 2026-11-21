# fc18 Claude runs: pre-registration (PLAN rev 2 section 2.5), written 21 Nov 2026 before the first run

- Start file: `out/fc18/P/round-start.FCStd` (opened as `cup.FCStd`): Params `cup_diameter` 60, `cup_height` 80,
  `wall` 2 (aliases B1..B3), an empty Body labelled Cup. No sketch, no feature.
- Model `claude-sonnet-5-5`, Claude Code in a fresh `fcc-app:1.1.4-0.1.28` container, `--strict-mcp-config` with only
  the freecad MCP plug (freecad-mcp 0.1.28, logging proxy), no claude.ai connectors, `--max-budget-usd 0.25`,
  `--max-turns 40`, `lab/costguard.py` (Esc at $0.24). Cap $0.25 a run, $0.50 both (ledger `freecad-course-BUDGET.tsv`).
- A1 (not asked to check): "Make a round pen cup in this file by drawing its cross-section and revolving it. Use the
  parameters already here: cup_diameter is the outside diameter, cup_height the height, wall the side wall and the
  floor. Stand it on the XY plane, base at z 0, open at the top. It should follow cup_diameter when I change it."
- B1 (asked): the same + " Then measure the cup's outside diameter and tell me what you find."
- Score (`lab/fc18parts.py check` + `lab/fc18score.py`, on the file our `lab_save` saves after the run): as saved,
  recomputed, then from a fresh open each at `cup_diameter` 60, 80, 45 (wall 2): (a) outside x and y extent =
  `cup_diameter` ± 0.01; (b) z 0..80 ± 0.01; (c) at z 40 in five directions radius r − 1.95 material, r − 2.05 air,
  r + 0.05 air, and (0, 0, 1) material, (0, 0, 3) air; (d) one solid, top open, builds (no object Invalid / Error).
  Shape = the Body's shape, else the largest visible solid (recorded as `src`). Pass = (a)-(d) at all three.
  Reported, not in pass: (e) a PartDesign::Revolution inside the Body (Part workbench Revolution = class 9); (f) the
  width reads `cup_diameter` (every expression naming it, directly or through a Params cell that names it). Bounding
  box from `Shape.BoundBox` (the solid is exact; G0 BoundBox = Measure-by-code 120.00 / 60.00).
- Classes (`lab/fc18score.py cls`): (1) pass + Revolution; (2) typed 30 (60 at every setting); (3) width =
  `cup_diameter` (120 at 60, 160 at 80); (4) pass, not a revolve; (5) full section across the axis (by hand);
  (6) upside down / off the floor; (7) parameters changed or added that break the link (by hand); (8) broke the file;
  (9) other. Checked = a geometry-reading tool call after Claude's last modifying call that reads the built solid's
  size (quoted in NUMBERS), not an echo of what it set.
- Scorer checked on lab files before the runs: round-fixed PASS class 1; round-name FAIL (a c at 60 / 80 / 45) class
  3; round-typed30 FAIL (a c at 80 and 45 only) class 2.
- G0 context known before the runs: trap 120.00 × 120.00, z 0..80, inside 116, volume 80,449.905, no message (every
  object Up-to-date / Valid); typed 60 the same volume; fixed 60.00, inside 56, 34,079.997; fixed at 80 → 80.00,
  inside 76, 48,279.996; trap at 80 → 160; typed 30 at 80 → 60; fixed at 45 → 45 (width 22.5), trap at 45 → 90,
  at 40 → 80.
