# LAB-fc9 (FreeCAD course lesson 9, LinearPattern coat rack), 15-16 Nov 2026

Plan: `Refream-Canvas/inputs/video-plans/2026-11-15-cad-lesson-9/PLAN.md` section 4 (fc9). Image `fcc-app:1.1.4-0.1.28`.
Results: `RESULTS-fc9.md` in that plan folder. Every number: `out/fc9/NUMBERS.json` (`lab/fc9numbers.py`).

- `lab/fc9parts.py` (freecadcmd): build = `P/rack-start.FCStd` (body Rack: Strip Pad 180 x 5 x 60 from a sketch whose
  width is `Params.rack_width`, Hook Pad = lesson 3 profile on the YZ plane, offset `Params.margin`, length
  `Params.width`; spreadsheet Params rack_width 180, width 20, margin 20, hooks 5) + one file per case (trap, fix,
  proof, control, yourturn, trap_nocompound) -> `P/build.json`; check = hooks, end gaps, air, solids of any saved file.
- G0: `G0/VERDICT.txt` (probe container `lab/fc9_up.sh` + `lab/fc9x.sh`, queries `lab/fc9q.py`).
- Takes (`lab/fc9_take.sh A|B|C`, by hand, no AI, 2880x1800, events + cursor logs): A trap, B fix, C proof.
- Claude runs (`claude-run/fc9run.sh A1|B1` -> `lab/fc9_R.sh`): claude-sonnet-5-5, --strict-mcp-config, freecad
  server only, cap $0.45 each, $0.90 stage. Plan name covered in the recordings and stills (`lab/fc9redact.sh`),
  checked by OCR (`lab/fc9ocr.sh` -> `OCR-plan.txt`, 0 hits).
- Tests: `tests/test_fc9.py` (red first, then green).
