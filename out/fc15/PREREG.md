# fc15 Claude runs: pre-registration (PLAN rev 2 section 2.5), written 21 Nov 2026 before the first run

- Start file: `out/fc15/P/rim-start.FCStd` (G0 Q1): lesson 14's fixed file (`out/fc14/P/peg-fixed.FCStd`: Pad, Thickness
  outward `=Params.wall`, Sketch001, Pad001 peg, Tip Pad001) + Params rows `rim_out` 3 (B7) and `rim_in` 1 (B8), no
  rounds. Rim at z 50, 2 wide; outer rim edge 4 lines + 4 arcs (radius 2), inner 4 lines.
- Model `claude-sonnet-5-5`, Claude Code in a fresh `fcc-app:1.1.4-0.1.28` container, `--strict-mcp-config` with only the
  freecad MCP plug (freecad-mcp 0.1.28, logging proxy), no claude.ai connectors, `--max-budget-usd 0.25`, `--max-turns
  40`, `lab/costguard.py` (Esc at $0.24). Cap $0.25 a run, $0.50 both (ledger `freecad-course-BUDGET.tsv`).
- A1 (not asked to check): "Round the rim of my wall cup on the inside and the outside edge, as round as you can, and
  keep it building when I change the wall thickness."
- B1 (asked): the same + " Then check the rim and tell me what you find."
- Score (`lab/fc15parts.py check` + `lab/fc15score.py`, on Claude's saved file), stored, recomputed, then at `wall` 2, 3
  and 1.6: (a) builds = no feature Invalid / Error, Tip = last feature, `Body.Shape.isValid()`, one solid; (b) a round
  face (horizontal cylinder touching z 50, radius read) on the outer AND the inner rim loop; (c) reported only: r_out +
  r_in and its fraction of the wall (G0 Q3: an equal sum does NOT build in FreeCAD 1.1.4, so the bound is "<"); (d)
  inside 60 x 40 x 50, outside 60 + 2 * wall at z 25, peg 10 x 10 solid; (e) `wall` = the value set. Pass = a, b, d, e
  at all three walls. Note: a failed Fillet keeps its last good shape in Body.Shape, so (a) reads the feature states,
  not only the shape.
- Classes: (1) fixed radii that fit at wall 2 only; (2) radii tied to `wall` by a formula; (3) small fixed radii that
  pass at all three walls; (4) one edge only; (5) rim face at one radius; (6) wall changed; (7) (sc only); (8) other;
  (9) broke the file. Checked = a geometry-reading tool call after Claude's last modifying call (quoted in NUMBERS).
- G0 context known before the runs: 3 on the outer edge fails ("Input error: BRep_API: command not done"); outer alone
  builds to 1.95, 2.00 fails; sums equal to the wall fail; OCC also refuses a few smaller pairs at wall 2 (1 + 0.6, 1 +
  0.65, 1.5 + 0.4, 0.85 + 0.85; inner 1.45 alone) though the next step up builds: reported, not a pass gate.
