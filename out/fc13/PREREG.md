# fc13 Claude runs: pre-registration (PLAN rev 2.1 section 2.5), written 18 Nov 2026 before the first run

- Start file: `out/fc13/P/cup-trap.FCStd` (G0 Q8): Params `cup_width` 60, `cup_length` 40, `cup_height` 50, `wall` 2;
  Body: Sketch (width = Params.cup_width, length = Params.cup_length), Pad = Params.cup_height, Thickness on the top face,
  Value = Params.wall, Make thickness inwards ticked (Reversed true). Inside by code 56 x 36, 48 deep.
- FreeCAD 1.1.4 + freecad-mcp 0.1.28 (`fcc-app:1.1.4-0.1.28`), fresh container, the file open in the GUI.
- `claude --model claude-sonnet-5-5 --strict-mcp-config --mcp-config entry.json` (only the freecad server, behind the
  logging proxy), `--max-budget-usd 0.25 --max-turns 40`, live guard `lab/costguard.py` (sonnet-5-5 estimate x 0.6).
- Cap: **$0.25 per run, $0.50 for the stage** (ledger `freecad-course-BUDGET.tsv`, mark "# --- GO 18 Nov 2026 fc13").
  A run that hits its cap stops and is kept as is; no rerun without the owner. n = 1 each, A1 then B1.

## Prompts (exact)
- **A1 (not asked to check):** My wall cup should be 60 by 40 inside, but after the shell it came out smaller. Fix it so
  the inside stays 60 by 40 when I change the wall thickness.
- **B1 (asked):** the same + " Then measure the inside and tell me the numbers."

## Score (by code: `lab/fc13parts.py` check on the document as Claude left it; `lab/fc13score.py`)
- The stored shape is logged, then the file is recomputed (Thickness touched; G0 Q3: not needed, harmless) and the
  recomputed shape is scored; if they differ, the beat says so.
- (a) inside **60 x 40 +- 0.01** at `wall` 2 (as left) and at `wall` 3 (fixed numbers), measured wall 2 / 3 +- 0.01;
  (b) the inside-width name set to 70 -> inside 70 +- 0.01. Pass = (a) and (b). Inside depth reported per class
  (class 1: 50; class 2: 50 with height + 1 wall, 52 with height + 2 walls).
- The `wall` cell changed for (a) is the alias the Thickness Value expression reads (`wall` unless Claude changed it).
- (b) target name = the Params alias reached by tracing the sketch constraints' expressions (through formula cells)
  whose value is 60 (`cup_width` first if it qualifies); logged. If the inside width is only a literal inside a formula
  (e.g. `cup_width = 60 + 2 * wall`), (b) edits that literal to 70 and the class is logged **2-literal** ("the inside is
  a number, not a name").
- Classes: (1) outward, thickness bound to `wall`; (2) inward + outside drawn from the inside by a names formula;
  (3) outward with a typed thickness; (4) typed outside sizes in the sketch; (5) both / centred walls; (6) one direction
  only / other; (7) removed or zeroed the shell; (8) broke the file; (9) name values changed to the outside sizes.
- **Checked** = Claude read the inner faces or the cavity from the geometry (transcript, by hand), not just echoed the
  values it set. Every number Claude reports is compared with ours. Told as it happened.
