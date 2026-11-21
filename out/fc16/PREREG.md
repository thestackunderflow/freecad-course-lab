# fc16 Claude runs: pre-registration (PLAN rev 2 section 2.5), written 21 Nov 2026 before the first run

- Start file: `out/fc16/P/hole-typed-w3.FCStd`: lesson 14's fixed cup (`out/fc14/P/peg-fixed.FCStd`; G0 Q9 branch:
  lesson 15's `rim-both` does not build at wall 2, Fillet001 "BRep_API: command not done", so no rim) + Params row
  `hole_size` 5 (B7); HoleSketch attached (FlatFace) to Pad001 Face13 = the back outside face, circle diameter
  `=Params.hole_size`, centre x 0 z 30; Pocket Type Length (panel "Dimension"), Length 2 typed, not Reversed; saved at
  `wall` 3 (hole closed: 1.00 mm skin at y 20..21, pit 2 deep, no feature marked).
- Model `claude-sonnet-5-5`, Claude Code in a fresh `fcc-app:1.1.4-0.1.28` container, `--strict-mcp-config` with only the
  freecad MCP plug (freecad-mcp 0.1.28, logging proxy), no claude.ai connectors, `--max-budget-usd 0.25`, `--max-turns
  40`, `lab/costguard.py` (Esc at $0.24). Cap $0.25 a run, $0.50 both (ledger `freecad-course-BUDGET.tsv`).
- A1 (not asked to check): "My wall cup's hanging hole in the back wall closed up when I changed the wall to 3. Fix it
  so the hole goes through the back wall whatever the wall thickness."
- B1 (asked): the same + " Then check the back wall, the front wall and the peg and tell me what you find."
- Score (`lab/fc16parts.py check` + `lab/fc16score.py`, on Claude's saved file), stored, recomputed, then at `wall` 2,
  3 and 12: (a) back hole open: axis points (x 0, z 30) at y 20.05, 20 + wall / 2, 20 + wall - 0.05 are air; (b) front
  wall point (0, -20 - wall / 2, 30) is material; (c) hole 5 across at y 20 + wall / 2 (x +-2.4 air, +-2.6
  material); (d) builds (no feature Invalid / Error, Tip = last feature, valid, one solid), peg (0, -34, 40) and
  (0, -28, 40) material, inside 60 x 40 +-0.01, 50 deep, top open; (e) `wall` = the value set and outside x at z 25 =
  60 + 2 * wall; (f) the depth setting read by code follows the wall: the last Pocket / Hole's Type Length with an
  expression naming `wall`, or Type UpToFirst / UpToFace. Pass = (a)-(f) at all three walls.
- Classes: (1) depth bound to `wall` (or an expression >= wall that stops before the front wall); (2) Through all
  (fails b); (3) To first / Up to face; (4) a bigger typed number (fails f; number reported); (5) symmetric / two
  sides; (6) sketch moved or re-attached; (7) wall set back to 2 (fails e); (8) a second cut or a separate body;
  (9) broke the file; (10) other. Checked = a geometry-reading tool call after Claude's last modifying call that
  reads the hole or the walls (quoted in NUMBERS), not an echo of what it set.
- G0 context known before the runs: typed 2 open at wall 2, skin 1.00 at wall 3 and 2.00 at wall 4 (no message);
  Through all at wall 3 drills the front wall (hole 5.00 across, peg kept); `=Params.wall` open + front closed at
  walls 2, 3, 4 and hole_size 6; To first and Up to face (inside back face) open + front closed at 2, 3, 4.
