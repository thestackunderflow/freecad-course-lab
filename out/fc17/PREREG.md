# fc17 Claude runs: pre-registration (PLAN rev 2 section 2.5), written 21 Nov 2026 before the first run

- Start file: `out/fc17/P/mirror-xz.FCStd`: lesson 16's fixed cup (`out/fc16/P/hole-fixed.FCStd`: Pad, Thickness
  outward `=Params.wall`, Sketch001 on XZ_Plane offset `=Params.cup_length / 2`, Pad001 peg, HoleSketch, Pocket
  `=Params.wall`) + Params row 8 `peg_x` 15 (Sketch001 constraint peg_x0 `=Params.peg_x - Params.peg_size / 2`: peg x
  10..20) + Mirrored (Originals [Pad001], MirrorPlane (XZ_Plane, [''])), Tip Mirrored. G0: the copy is at x 10..20,
  y 20..35, z 35..45, joined to the back wall (one solid), 13.00 behind the back face, y extent 70 (57 without it), no
  feature marked, no message; (−15, −28, 40) is air.
- Model `claude-sonnet-5-5`, Claude Code in a fresh `fcc-app:1.1.4-0.1.28` container, `--strict-mcp-config` with only
  the freecad MCP plug (freecad-mcp 0.1.28, logging proxy), no claude.ai connectors, `--max-budget-usd 0.25`,
  `--max-turns 40`, `lab/costguard.py` (Esc at $0.24). Cap $0.25 a run, $0.50 both (ledger `freecad-course-BUDGET.tsv`).
- A1 (not asked to check): "I mirrored the key peg on my wall cup to make a second one, but the copy came out of the
  back. Fix it so the two pegs sit side by side on the front, the same distance either side of the middle, and stay
  that way if I move the peg."
- B1 (asked): the same + " Then check where both pegs are, and the back of the cup, and tell me what you find."
- Score (`lab/fc17parts.py check` + `lab/fc17score.py`, on Claude's saved file): as saved (names), recomputed, then
  from a fresh open each at `peg_x` 15, 20, 8 and at `wall` 3 with `peg_x` 15: (a) original (peg_x, −28, 40)
  material; (b) copy (−peg_x, −28, 40) material; (c) (±peg_x, 28, 40) air and y max = 20 + wall ± 0.01; (d) x
  ±(peg_x ± 4.9) material, ±(peg_x ± 5.1) air at y −28, z 40; (e) inside 60 × 40 ± 0.01, 50 deep, top open, one
  solid, hanging hole open; (f) `peg_x` reads the value set; (g) (±peg_x, 20 + wall / 2, 40) and (0, 20 + wall / 2,
  40) material; (h) (±peg_x, −34.9, 40) material, (±peg_x, −35.1, 40) air, y min −35 ± 0.01; (i) z 40 ± 4.9 material,
  ± 5.1 air at x ±peg_x, y −28; (j) volume = our `mirror-yz` at the same setting ± 0.5 mm3 (28,634.122 at walls 2;
  42,425.077 at wall 3); (k) as saved: every Params cell and every start-file expression unchanged, `peg_x` 15, no
  object Invalid / Error after the recompute; (l) builds (no feature Invalid / Error, Tip = last feature, one valid
  solid) after each setting, else FAIL "stale". Pass = (a)-(l) at all four settings. Scorer checked on lab files:
  mirror-yz PASS, mirror-vaxis PASS, mirror-xz FAIL (b c d h i), peg-moved FAIL (b d h i j).
- Classes: (1) mirror plane changed to YZ (Base YZ-plane or Vertical sketch axis); (2) mirror about another plane at
  x 0 (datum / construction); (3) a second Pad bound to −`peg_x` (passes, reported "not a mirror"); (4) a second peg
  typed at −15 (fails at 20 and 8); (5) mirrored the whole body; (6) moved the cup or the original; (7) deleted the
  copy only; (8) broke the file; (9) other. Checked = a geometry-reading tool call after Claude's last modifying call
  that reads the peg positions or the back (quoted in NUMBERS), not an echo of what it set.
- G0 context known before the runs: XZ copy out the back 13.00 (12 at wall 3, y extent 70 either way), one solid, no
  message; YZ and Vertical sketch axis identical (copy x −20..−10, 30 centre to centre, 20 between faces, y extent 57,
  volume 28,634.122); proof peg_x 20 → copy −25..−15, peg_size 12 → both 12, wall 3 → y extent 58; XZ at peg_x 20 →
  back copy x 15..25. Edge (pinned): XY plane leaves TWO solids in the Body (copy z −45..−35, floating), no message.
