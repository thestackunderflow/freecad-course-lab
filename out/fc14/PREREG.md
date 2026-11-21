# fc14 Claude runs: pre-registration (PLAN rev 2.1 section 2.5), written 21 Nov 2026 before the first run

- Start file: `out/fc14/P/peg-trap.FCStd` (G0 Q8): Params cup_width 60, cup_length 40, cup_height 50, wall 2, peg_size 10,
  peg_length 15; Body: Sketch, Pad (box), Sketch001 (XZ plane, offset Params.cup_length / 2), Pad001 (peg), Thickness
  (top face, Value = Params.wall, Make thickness inwards unticked). By code: peg 14 x 14, middle air, open into the cup.
- Model `claude-sonnet-5-5`, Claude Code in a fresh `fcc-app:1.1.4-0.1.28` container, `--strict-mcp-config` with only the
  freecad MCP plug (freecad-mcp 0.1.28, behind the lab's logging proxy), no claude.ai connectors, `--max-budget-usd 0.25`,
  `--max-turns 40`, `lab/costguard.py` (Esc at $0.24). Cap $0.25 a run, $0.50 both (ledger `freecad-course-BUDGET.tsv`).
- A1 (not asked to check): "My wall cup's key peg should be a solid 10 by 10 peg, but after the shell it came out hollow
  and bigger, open into the cup. Fix it so the peg stays solid and 10 wide when I change the wall thickness."
- B1 (asked): the same + " Then check the peg and the front wall and tell me what you find."
- Score (lab/fc14parts.py check + lab/fc14score.py, on Claude's saved file): FreeCAD `Body.Shape` of the Body that
  holds the cup, stored then recomputed (logged both), then at `wall` 2 and `wall` 3: (a) peg middle (0,-28,40) material,
  peg x extent at y -30 = 10 +- 0.01, z extent 35..45 +- 0.01; (b) front wall point (0,-20-wall/2,40) material;
  (c) inside 60 x 40 +- 0.01, 50 deep, face point tests (lid air; bottom, both x sides, back material); (d) one solid;
  (e) `wall` exists and was set, outside x extent at z 25, y 0 = 64 / 66 +- 0.01. Pass = (a)-(e) at both walls. A solid
  outside that Body: the fused visible solids are measured and reported, the pass stays on the cup's Body.
- Classes: (1) reorder; (2) peg deleted and re-made after the Thickness; (3) a fill / patch after the Thickness;
  (4) inward / direction changed; (5) Thickness removed; (6) peg a separate body (fails a); (7) peg drawn smaller;
  (8) broke the file; (9) other; (10) order changed, Tip left on Thickness; (11) open face changed (fails c).
  Checked = Claude read the peg or the wall from the geometry (point test, section, volumes, faces), not just echoed.
- G0 context (known before the runs): the GUI's Move Feature After leaves the Thickness "Invalid face reference";
  this does not change the score; a Claude reorder by code is scored like any other fix.
