# LAB-fc8 v1 (FreeCAD course lesson 8, assembly): pre-registration, 14 Nov 2026

Plan: `Refream-Canvas/inputs/video-plans/2026-11-14-cad-lessons/PLAN.md` 4.B2; twin of sc8 (`RESULTS-sc8.md`).
Image `fcc-app:1.1.4-0.1.28` (FreeCAD 1.1.4 AppImage, freecad-mcp 0.1.28 add-on + plug as filmed in fc1-fc7).

## Parts (same hook and rail as sc8, `solidcraft-course-lab/lab/sc8parts.py`)
Hook: lesson 3 profile (plate x 0..5, arm to x 25, lip, y -20..0, z 0..60) + a block x -10+gap..0 with a T-slot along Z.
Rail: base 24 x 4 (x -14..-10), T-rib stem 6 x 3, head 12 x 3, z 0..80. Spreadsheet `Params` (lesson 3): rib_stem 6,
rib_head 12, gap, slot_stem = rib_stem + 2 * gap, slot_head = rib_head + 2 * gap. Built from Part Design boxes driven by
the spreadsheet, so `gap` 0 -> 0.4 + Recompute moves every slot face.
Cases: typo (gap 0, slot_head typed 11.6), touch (gap 0), gap01 (0.1), gap04 (0.4).
Expected by arithmetic (to be measured, never copied): typo Common 72 mm3; hook 17,260 mm3 at gap 0, rail 12,000.

## G0 ($0) questions
G0a (headless): build the 4 files; Common volume, per-side gaps by code; Assembly by Python (links, ground, slider with
whole-body references, solve); a hook moved into the rail: does the solver object?
G0b (GUI, stills): the Assembly workbench's toolbars; Create Assembly, Insert, Ground, Slider (which picks keep the gap
centred), drag the hook: does anything stop it at the rail? Part > Common: what a person sees for overlap / empty;
where a person reads the Common's volume; Measure between slot and rib walls.
Stop: plan 4.B2.4 rules 1, 2 (no fc8 / RETHINK). Rule 7 (no collision stop) is a planned branch, not a stop.

## Takes (after G0), Claude runs, numbers
Takes A (typo Common lit red + volume), B (assembly, ground, slider, drag), C (gap 0: Common), D (spreadsheet gap 0.4,
Recompute, Measure), E (drag the whole rail). Claude A1 (not asked) and B1 (asked), sentences from sc8's runner,
`--strict-mcp-config`, freecad server only, live cost guard, $0.60 total. Every number -> out/fc8/NUMBERS.json by
`lab/fc8numbers.py`.
