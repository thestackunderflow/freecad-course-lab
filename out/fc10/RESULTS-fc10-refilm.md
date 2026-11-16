# RESULTS: fc10 re-film (16 Nov 2026)

Why: the first recordings (`screen.mp4`, git-ignored) were lost when the lab worktree was removed; only stills and logs
had been committed (c88f393). Re-filmed in the main checkout with the same scripts (`lab/fc10_take.sh`,
`claude-run/fc10run.sh` -> `lab/fc10_R.sh`), image `fcc-app:1.1.4-0.1.28` (FreeCAD 1.1.4, freecad-mcp 0.1.28), Claude
Code 2.1.308, `claude-sonnet-5-5`, `--strict-mcp-config` (FreeCAD plug only). Start files rebuilt from scratch
(`fc10parts.py` build, 60 mm states identical; its own resize legs vary, see `P/build-refilm.json`; the original
`P/build.json` is kept). Every take's `events.jsonl`, `check.json`, `take.log` and stills now belong to the new
`screen.mp4` (the old ones are in git at c88f393). NUMBERS.json was NOT regenerated (it still holds the first run).

## 1. Takes: every on-screen number reproduced exactly
| Take | GUI Measure (Position Z) | Code check (new) | Script value | Same? |
|---|---|---|---|---|
| T slip | top 50.85, bottom -9.15, X 1.98 | -9.14988 / 50.85012 / hole 5.85012, xmin 1.97571, DoF 2 | -9.15 / 50.85 / 5.85 / 1.98 | yes |
| TB pinned slip | top 60.00, bottom 0.00 | 0 / 60 / 15.0, DoF 0 | 0.00 / 60.00 / 15.0 | yes |
| P pickup | (none) | 0 / 60 / 15.0, DoF 2; solver "Under-constrained: " + "2 Degrees of Freedom"; link selects all corners | same | yes |
| A trap | top 78.68, bottom -1.32 | -1.320832 / 78.679168 / 13.679168, 10,420.48 | -1.32 / 78.68 / 13.68 / 18.68 up | yes |
| B pinned | top 80.00, bottom 0.00 | 0 / 80 / 15.0, DoF 0, "Fully constrained" | same | yes |
| C fix | top 80.00, bottom 0.00 | box selects Vertex1 + RootPoint; 2 -> 0 DoF; 0 / 80 / 15.0 | same | yes |
| D proof | top 100.00, bottom 0.00 | drag moves nothing; 0 / 100 / 15.0, 12,420.48 | same | yes |

## 2. Controls by code (not filmed; F13 second line)
- Take A's new file 80 -> 100, 3 tries: -2.64 / hole 12.36 (1 try, = script), -11.71 / hole 3.29 (2 tries). The committed
  `controls/takeA-80-to-100.json` (-2.64) stays a real try; F13 "unpinned copy at 100: bottom -2.64 · hole 12.36" is
  still true of one try but the main session may want "for example" or the drop range (it varies like F8).
- Take T's new file 60 -> 80, 3 tries: -10.47 / hole 4.53 every time (= committed control).
- Build legs: unpinned 60 -> 80 now -1.32 (was -6.97); 60 -> 100 now -19.23, hole above the plate (was -3.07).

## 3. Claude runs (cap $0.50 for both; spent $0.2530; ledger total for the GO now $0.5052 of $0.90)
| Run | Cost | Calls (new / old) | Class | Its claim (new) | Our check (new) | Old check |
|---|---|---|---|---|---|---|
| A1 not asked | $0.1291 (was $0.1272) | list_documents, get_objects, 1 execute_code (Params B1 = 80) / same | moved | "it stays 15 mm below the top"; NEW: "the plate is now 80 mm tall (bounding box height 80)" | DoF 2, bottom **-10.39**, top **69.61**, hole **4.61** below the top | -1.32 / 78.68 / 13.68 |
| B1 asked | $0.1239 (was $0.1250) | list_documents + **4** execute_code / list_documents + 5 execute_code | right + pinned | "Before: 2" -> one Coincident (start of the first line / origin, same constraint as before) -> "After: 0" -> 80; "HoleSketch was already at 0 DoF" | DoF 0, 0.00 / 80.00 / 15.0 | same |
- A1: the claim about the hole is still wrong, and more wrong: hole 4.61 from the top (moved 10.39). Its height claim is
  true as a size (69.61 - (-10.39) = 80). Its file dropped like GUI run 1 in G0 (10.39), the third known value.
- B1: same outcome and numbers; one call fewer (it read the spreadsheet and the DoF in one call); its own "before" print
  returned None (code slip) but it had read DoF 2 in call 2. Reply wording changed (below).
- Masks: plan name covered by `lab/fc10redact.sh` (fixed box); B1's header did NOT scroll into the open this time (top
  strip checked at 1 fps: the header leaves the screen at about 21 s in one jump), so no second cover box was needed.
  OCR of all 9 recordings for Ultra/@gmail/sk-ant/plan words: 0 hits (`OCR-refilm.txt`). Session logs (account e-mail)
  were moved out of the repo. Model lines in the session log: 1-2 `claude-opus-5-5` (Claude Code's own side calls, the
  original A1 had 1 too) besides the Sonnet turns.

## 4. Script lines that must change (SCRIPT-fc10.md; the Short needs no change)
1. F15 narration (line 126): "bottom minus 1.32, hole 13.68 from the top" -> "bottom minus 10.39, hole 4.61 from the top".
2. F15 On screen (line 93) + §3 code panels (lines 160-161): "2 degrees of freedom · bottom -1.32" / "top 78.68 · hole
   13.68 from top" -> "bottom -10.39" / "top 69.61 · hole 4.61 from top"; chip "said 15 · checked by code 13.68" (line 166)
   -> "... 4.61". Handover §4 item 4 the same.
3. F16 On screen (line 94): "five tool calls" stays true only counting list_documents (now 1 + 4 execute_code; was
   1 + 5); the handover's "5 execute_code 19.3-32.7" -> "4 execute_code 19.2-35.9". The quoted line "I set plate_height to 80"
   -> new text "I set Params.plate_height (cell B1) from 60 to 80"; "Before: 2." / "After: 0" / "I added one constraint"
   still appear. Drop "the second cover box at 28-34 s kept" (not needed now).
4. F16 chip (line 166) "run 2 · asked · $0.13" -> "$0.12" ($0.1239); run 1 stays $0.13 ($0.1291).
5. Facts block lines 61-64 and the description lines 200-202 + numbers table rows 228-229: A1 $0.1291, -10.39 / 69.61 /
   4.61; B1 $0.1239, 4 execute_code.
6. Optional: F8 "11 tries" — A1's file is one more unpinned 60 -> 80 try (10.39, already one of the three values).
   F13 "-2.64 · 12.36": see §2.
7. Every time range in the footage map (HANDOVER-fc10-render §1) and in the On screen cells moves by -3.9 to +7.8 s:
   use §5 below (new key ranges) or the full mark table (§6).

## 5. Footage map, re-filmed (new seconds)
| Take | Key ranges (s) |
|---|---|
| T | sketch 4.6-9.2; **drag 15.1-16.4**; Close 21.9, iso 25.8; front view set 33.1; Measure top 46.4 (Z 50.85); **bottom 65.2-74.1 "Z: -9.15 mm"**; right view 78.5-85.4 |
| TB | sketch 4.5, **"Fully constrained" 9.0-15.1**; **drag 15.1-16.4**; front 33.6; top 46.7 (60.00); **bottom 66.3-75.8 "Z: 0.00 mm"** |
| P | Params 4.3, rows 8.3-18.7; sketch 28.6; rule marks 35.0; **message 40.2-46.4**; link 46.4; origin 53.3-58.4 |
| A | Params 4.3, 80 typed 12.9, Recompute 18.4; front 39.1; top 52.0 (78.68); **bottom 70.4-79.1 "Z: -1.32 mm"**; right view 87.6-94.4 |
| B | iso 119.6-121.1; message 109.4-115.9 |
| C | sketch 4.6-9.0; **box 14.7-16.0**; hover Coincident Constraint 18.9, click 22.4; **"Fully constrained" 24.8-32.1**; 80 typed 45.4, Recompute 50.8; front 66.4; **top 78.5-86.8**; **bottom 96.2-104.8**; right 109.2; iso 115.8-117.0 |
| D | sketch 4.3; **drag 13.5-15.2**; 100 typed 33.2, Recompute 38.6; front 54.1-61.1 |
| A1 | prompt 2.2-5.2; tool calls 7.4-13.7; reply done 19.0; end 25.0 |
| B1 | prompt 2.1-12.1; 4 execute_code 19.2-35.9; reply done 41.4; end 47.4 |

## 6. Every mark, old (c88f393) vs new

**T** (marks old 20 / new 20)

| # | mark | old s | new s | shift |
|---|---|---|---|---|
| 1 | recording started: FreeCAD 1.1.4, hook.FCStd open (T) | 0.0 | 0.0 | +0.0 |
| 2 | double-click: HookSketch (edit) | 4.5 | 4.6 | +0.2 |
| 3 | (sketch view set) | 8.9 | 9.2 | +0.3 |
| 4 | drag: the back line (a slip) | 14.8 | 15.1 | +0.3 |
| 5 | drag: released | 16.0 | 16.4 | +0.3 |
| 6 | sketch: Close | 21.5 | 21.9 | +0.4 |
| 7 | key 0: isometric | 25.4 | 25.8 | +0.4 |
| 8 | (view fitted) | 26.7 | 27.1 | +0.4 |
| 9 | key 1: Front view | 31.4 | 31.8 | +0.4 |
| 10 | (view set: Front centred 12 0 30, 110 mm tall) | 32.7 | 33.1 | +0.4 |
| 11 | Measure | 40.3 | 41.2 | +0.9 |
| 12 | top: corner | 45.5 | 46.4 | +0.9 |
| 13 | Measure: Close | 54.1 | 55.2 | +1.1 |
| 14 | Measure | 58.8 | 60.0 | +1.3 |
| 15 | bottom: corner | 64.0 | 65.2 | +1.2 |
| 16 | Measure: Close | 72.9 | 74.1 | +1.2 |
| 17 | key 3: Right view | 76.1 | 77.1 | +1.0 |
| 18 | (view set: Right centred 0 -10 30, 90 mm tall) | 77.7 | 78.5 | +0.9 |
| 19 | key 0: isometric | 84.8 | 85.4 | +0.5 |
| 20 | (view fitted) | 86.5 | 86.7 | +0.3 |

**TB** (marks old 20 / new 20)

| # | mark | old s | new s | shift |
|---|---|---|---|---|
| 1 | recording started: FreeCAD 1.1.4, hook.FCStd open (TB) | 0.1 | 0.1 | -0.0 |
| 2 | double-click: HookSketch (edit) | 4.4 | 4.5 | +0.2 |
| 3 | (sketch view set) | 8.7 | 9.0 | +0.3 |
| 4 | drag: the back line (a slip) | 14.4 | 15.1 | +0.7 |
| 5 | drag: released | 15.6 | 16.4 | +0.8 |
| 6 | sketch: Close | 20.8 | 22.2 | +1.4 |
| 7 | key 0: isometric | 24.6 | 26.1 | +1.5 |
| 8 | (view fitted) | 25.9 | 27.4 | +1.6 |
| 9 | key 1: Front view | 30.5 | 32.2 | +1.8 |
| 10 | (view set: Front centred 12 0 30, 110 mm tall) | 31.7 | 33.6 | +1.9 |
| 11 | Measure | 38.8 | 41.7 | +2.8 |
| 12 | top: corner | 43.8 | 46.7 | +2.9 |
| 13 | Measure: Close | 52.3 | 55.6 | +3.3 |
| 14 | Measure | 56.7 | 61.0 | +4.3 |
| 15 | bottom: corner | 61.7 | 66.3 | +4.7 |
| 16 | Measure: Close | 70.0 | 75.8 | +5.8 |
| 17 | key 3: Right view | 72.9 | 79.0 | +6.1 |
| 18 | (view set: Right centred 0 -10 30, 90 mm tall) | 74.3 | 80.6 | +6.3 |
| 19 | key 0: isometric | 80.9 | 87.8 | +6.9 |
| 20 | (view fitted) | 82.2 | 89.3 | +7.1 |

**P** (marks old 15 / new 15)

| # | mark | old s | new s | shift |
|---|---|---|---|---|
| 1 | recording started: FreeCAD 1.1.4, hook.FCStd open (P) | 0.1 | 0.1 | -0.0 |
| 2 | double-click: open Params | 4.3 | 4.3 | -0.0 |
| 3 | hover: Params row 1 | 8.4 | 8.3 | -0.0 |
| 4 | hover: Params row 2 | 11.0 | 10.9 | -0.1 |
| 5 | hover: Params row 3 | 13.6 | 13.5 | -0.1 |
| 6 | hover: Params row 4 | 16.1 | 16.1 | -0.0 |
| 7 | hover: Params row 5 | 18.7 | 18.7 | -0.0 |
| 8 | tab: back to the 3D view | 24.7 | 24.6 | -0.0 |
| 9 | double-click: HookSketch (edit) | 28.7 | 28.6 | -0.1 |
| 10 | (sketch view set) | 33.0 | 32.9 | -0.1 |
| 11 | hold: rule marks | 35.1 | 35.0 | -0.1 |
| 12 | hold: message | 40.3 | 40.2 | -0.1 |
| 13 | message link: 2 Degrees of Freedom | 46.5 | 46.4 | -0.1 |
| 14 | hover: near the origin | 53.4 | 53.3 | -0.1 |
| 15 | sketch: Close | 58.5 | 58.4 | -0.2 |

**A** (marks old 22 / new 22)

| # | mark | old s | new s | shift |
|---|---|---|---|---|
| 1 | recording started: FreeCAD 1.1.4, hook.FCStd open (A) | 0.1 | 0.1 | -0.0 |
| 2 | double-click: open Params | 4.5 | 4.3 | -0.1 |
| 3 | hover: plate_height | 8.5 | 8.4 | -0.1 |
| 4 | cell B1: plate_height | 10.7 | 11.1 | +0.5 |
| 5 | typed 80 | 12.4 | 12.9 | +0.5 |
| 6 | Enter | 13.2 | 13.7 | +0.5 |
| 7 | Recompute | 17.5 | 18.4 | +0.9 |
| 8 | tab: back to the 3D view | 23.5 | 24.2 | +0.7 |
| 9 | key 0: isometric | 26.4 | 27.1 | +0.7 |
| 10 | (view fitted) | 27.8 | 28.4 | +0.6 |
| 11 | key 1: Front view | 32.6 | 33.6 | +0.9 |
| 12 | (view set: Front centred 12 0 40, 130 mm tall) | 38.0 | 39.1 | +1.1 |
| 13 | Measure | 45.5 | 46.9 | +1.3 |
| 14 | top: corner | 50.8 | 52.0 | +1.2 |
| 15 | Measure: Close | 59.6 | 60.9 | +1.2 |
| 16 | Measure | 64.4 | 65.3 | +1.0 |
| 17 | bottom: corner | 69.6 | 70.4 | +0.8 |
| 18 | Measure: Close | 78.4 | 79.1 | +0.8 |
| 19 | key 3: Right view | 81.4 | 82.1 | +0.8 |
| 20 | (view set: Right centred 0 -10 40, 110 mm tall) | 86.8 | 87.6 | +0.8 |
| 21 | key 0: isometric | 93.7 | 94.4 | +0.8 |
| 22 | (view fitted) | 94.9 | 95.8 | +0.8 |

**B** (marks old 26 / new 26)

| # | mark | old s | new s | shift |
|---|---|---|---|---|
| 1 | recording started: FreeCAD 1.1.4, hook.FCStd open (B) | 0.1 | 0.1 | -0.0 |
| 2 | double-click: open Params | 4.5 | 4.6 | +0.1 |
| 3 | hover: plate_height | 8.7 | 9.2 | +0.5 |
| 4 | cell B1: plate_height | 10.9 | 11.4 | +0.5 |
| 5 | typed 80 | 12.6 | 13.1 | +0.5 |
| 6 | Enter | 13.5 | 14.0 | +0.5 |
| 7 | Recompute | 18.3 | 19.6 | +1.3 |
| 8 | tab: back to the 3D view | 24.2 | 25.7 | +1.4 |
| 9 | key 0: isometric | 27.2 | 28.6 | +1.4 |
| 10 | (view fitted) | 30.1 | 29.9 | -0.1 |
| 11 | key 1: Front view | 35.6 | 34.9 | -0.6 |
| 12 | (view set: Front centred 12 0 40, 130 mm tall) | 41.0 | 40.5 | -0.5 |
| 13 | Measure | 48.4 | 49.4 | +1.0 |
| 14 | top: corner | 53.4 | 54.8 | +1.4 |
| 15 | Measure: Close | 61.9 | 64.0 | +2.1 |
| 16 | Measure | 66.3 | 68.7 | +2.4 |
| 17 | bottom: corner | 71.3 | 74.0 | +2.7 |
| 18 | Measure: Close | 80.1 | 83.4 | +3.3 |
| 19 | key 3: Right view | 83.1 | 86.5 | +3.4 |
| 20 | (view set: Right centred 0 -10 40, 110 mm tall) | 88.5 | 92.2 | +3.7 |
| 21 | double-click: HookSketch (edit) | 96.7 | 101.1 | +4.4 |
| 22 | (sketch view set) | 101.1 | 105.8 | +4.6 |
| 23 | hold: message | 104.5 | 109.4 | +4.8 |
| 24 | sketch: Close | 110.7 | 115.9 | +5.2 |
| 25 | key 0: isometric | 114.4 | 119.6 | +5.2 |
| 26 | (view fitted) | 115.8 | 121.1 | +5.3 |

**C** (marks old 30 / new 30)

| # | mark | old s | new s | shift |
|---|---|---|---|---|
| 1 | recording started: FreeCAD 1.1.4, hook.FCStd open (C) | 0.1 | 0.1 | +0.0 |
| 2 | double-click: HookSketch (edit) | 4.4 | 4.6 | +0.2 |
| 3 | (sketch view set) | 8.7 | 9.0 | +0.3 |
| 4 | box select: start up-left of the corner | 14.4 | 14.7 | +0.3 |
| 5 | box select: released (corner + origin) | 15.7 | 16.0 | +0.3 |
| 6 | hover: Coincident Constraint | 18.4 | 18.9 | +0.6 |
| 7 | Coincident Constraint | 21.7 | 22.4 | +0.7 |
| 8 | hold: Fully constrained | 24.0 | 24.8 | +0.7 |
| 9 | sketch: Close | 31.1 | 32.1 | +0.9 |
| 10 | double-click: open Params | 36.1 | 37.3 | +1.1 |
| 11 | hover: plate_height | 40.2 | 41.5 | +1.3 |
| 12 | cell B1: plate_height | 42.3 | 43.6 | +1.3 |
| 13 | typed 80 | 44.0 | 45.4 | +1.3 |
| 14 | Enter | 44.9 | 46.2 | +1.3 |
| 15 | Recompute | 49.2 | 50.8 | +1.7 |
| 16 | tab: back to the 3D view | 54.8 | 56.6 | +1.7 |
| 17 | key 0: isometric | 57.7 | 59.4 | +1.7 |
| 18 | (view fitted) | 59.1 | 60.6 | +1.5 |
| 19 | key 1: Front view | 63.7 | 65.2 | +1.5 |
| 20 | (view set: Front centred 12 0 40, 130 mm tall) | 65.0 | 66.4 | +1.4 |
| 21 | Measure | 72.2 | 73.4 | +1.2 |
| 22 | top: corner | 77.2 | 78.5 | +1.3 |
| 23 | Measure: Close | 85.6 | 86.8 | +1.2 |
| 24 | Measure | 90.2 | 91.2 | +1.0 |
| 25 | bottom: corner | 95.3 | 96.2 | +0.9 |
| 26 | Measure: Close | 104.0 | 104.8 | +0.8 |
| 27 | key 3: Right view | 106.8 | 107.8 | +1.0 |
| 28 | (view set: Right centred 0 -10 40, 110 mm tall) | 108.0 | 109.2 | +1.1 |
| 29 | key 0: isometric | 115.1 | 115.8 | +0.7 |
| 30 | (view fitted) | 116.5 | 117.0 | +0.6 |

**D** (marks old 27 / new 27)

| # | mark | old s | new s | shift |
|---|---|---|---|---|
| 1 | recording started: FreeCAD 1.1.4, hook.FCStd open (D) | 0.1 | 0.1 | +0.0 |
| 2 | double-click: HookSketch (edit) | 4.5 | 4.3 | -0.2 |
| 3 | (sketch view set) | 9.0 | 8.7 | -0.3 |
| 4 | drag: the back line | 14.0 | 13.5 | -0.4 |
| 5 | drag: released | 15.7 | 15.2 | -0.5 |
| 6 | sketch: Close | 21.3 | 20.4 | -0.9 |
| 7 | double-click: open Params | 26.5 | 25.3 | -1.1 |
| 8 | hover: plate_height | 30.6 | 29.4 | -1.2 |
| 9 | cell B1: plate_height | 32.8 | 31.5 | -1.2 |
| 10 | typed 100 | 34.5 | 33.2 | -1.2 |
| 11 | Enter | 35.5 | 34.2 | -1.2 |
| 12 | Recompute | 40.1 | 38.6 | -1.5 |
| 13 | tab: back to the 3D view | 45.8 | 44.2 | -1.6 |
| 14 | key 0: isometric | 48.8 | 47.0 | -1.7 |
| 15 | (view fitted) | 50.0 | 48.2 | -1.8 |
| 16 | key 1: Front view | 54.7 | 52.8 | -1.9 |
| 17 | (view set: Front centred 12 0 50, 150 mm tall) | 56.0 | 54.1 | -1.9 |
| 18 | Measure | 63.5 | 61.1 | -2.4 |
| 19 | top: corner | 68.5 | 66.1 | -2.5 |
| 20 | Measure: Close | 77.2 | 74.4 | -2.8 |
| 21 | Measure | 81.8 | 78.8 | -3.0 |
| 22 | bottom: corner | 86.8 | 83.8 | -3.1 |
| 23 | Measure: Close | 95.5 | 92.1 | -3.4 |
| 24 | key 3: Right view | 98.4 | 94.9 | -3.5 |
| 25 | (view set: Right centred 0 -10 50, 130 mm tall) | 99.7 | 96.2 | -3.5 |
| 26 | key 0: isometric | 106.6 | 102.7 | -3.9 |
| 27 | (view fitted) | 107.9 | 103.9 | -3.9 |

**A1** (marks old 12 / new 12)

| # | mark | old s | new s | shift |
|---|---|---|---|---|
| 1 | recording started: Claude Code (left, FreeCAD plug only), FreeCAD with | 0.0 | 0.1 | +0.0 |
| 2 | turn 1: typing | 2.2 | 2.2 | +0.0 |
| 3 | turn 1: Enter | 5.2 | 5.2 | -0.0 |
| 4 | tool call: list_documents | 9.2 | 7.4 | -1.7 |
| 5 | tool reply: list_documents | 9.2 | 7.4 | -1.7 |
| 6 | tool call: get_objects | 10.8 | 10.3 | -0.5 |
| 7 | tool reply: get_objects | 11.7 | 10.3 | -1.4 |
| 8 | tool call: execute_code | 13.9 | 12.8 | -1.1 |
| 9 | tool reply: execute_code | 14.7 | 13.7 | -1.0 |
| 10 | turn 1: end-of-turn line seen | 17.9 | 17.0 | -0.9 |
| 11 | turn 1: reply done | 19.9 | 19.0 | -0.9 |
| 12 | recording stopped | 25.9 | 25.0 | -0.9 |

**B1** (marks old 18 / new 16)

| # | mark | old s | new s | shift |
|---|---|---|---|---|
| 1 | recording started: Claude Code (left, FreeCAD plug only), FreeCAD with | 0.1 | 0.1 | +0.0 |
| 2 | turn 1: typing | 2.1 | 2.1 | -0.0 |
| 3 | turn 1: Enter | 12.4 | 12.1 | -0.3 |
| 4 | tool call: list_documents | 15.8 | 15.5 | -0.3 |
| 5 | tool reply: list_documents | 15.9 | 15.5 | -0.3 |
| 6 | tool call: execute_code | 19.3 | 19.2 | -0.1 |
| 7 | tool reply: execute_code | 19.3 | 19.2 | -0.1 |
| 8 | tool call: execute_code | 23.0 | 23.9 | +0.9 |
| 9 | tool reply: execute_code | 23.0 | 23.9 | +0.9 |
| 10 | tool call: execute_code | 25.5 | 29.6 | +4.0 |
| 11 | tool reply: execute_code | 25.6 | 29.6 | +4.0 |
| 12 | tool call: execute_code | 28.8 | 35.1 | +6.3 |
| 13 | tool reply: execute_code | 28.9 | 35.9 | +7.0 |
| 14 | old: tool call: execute_code / new: turn 1: end-of-turn line seen | 31.5 | 39.4 | +7.8 |
| 15 | old: tool reply: execute_code / new: turn 1: reply done | 32.7 | 41.4 | +8.7 |
| 16 | old: turn 1: end-of-turn line seen / new: recording stopped | 35.9 | 47.4 | +11.5 |
| 17 | turn 1: reply done | 37.9 | - | - |
| 18 | recording stopped | 44.0 | - | - |
