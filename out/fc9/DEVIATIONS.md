# fc9 lab: deviations from PLAN 4.2 (15 Nov 2026)

1. **Hooks stand out toward -Y** (strip y 0..5, hook plate y -5..0) so FreeCAD's isometric view (key 0) shows them in
   front of the strip. G0 (out/fc9/G0/b) ran on a first file with the hooks toward +Y; the pattern behaviour is the
   same (headless build of both). All takes and runs use `out/fc9/P/rack-start.FCStd`.
2. **The trap does not drop the 5th hook** (PLAN §2/§4.2 Q1, ACCURACY P11 said "dropped, 4 hooks"). In FreeCAD 1.1.4 a
   Body has `AllowCompound = True` by default (a new GUI body too, G0), so Length 180 / 5 keeps the 5th hook as a
   second solid floating at x 200..220, 20 mm past the strip's end; a warning toast says "One transformed shape does
   not intersect the support (3 times)"; OK accepts it. With AllowCompound off it IS dropped (build case
   `trap_nocompound`: 4 hooks, 88,000 mm3). PLAN 4.3 stop rule (2) branch: F0/F9/F10/S0/S1 rewritten from the frame,
   thumbnail falls back to "5 HOOKS, EVEN" (or a new "ONE HOOK FELL OFF"), re-gate teacher + producer.
3. **Direction default is "Horizontal sketch axis"** for this hook (sketch on the YZ plane = global Y): the copy goes
   out from the strip, not along it. The takes pick **Base X-axis** from the Direction list (one more step in F6).
4. **Right-end GUI Measure failed in takes B and C** (the Measurement task panel sits over the rack's right end and
   takes the wheel and clicks; try 1: wheel zoom over the panel; try 2: a middle-button pan did not move the CAD-style
   view). Two fix attempts used, stopped. The right end gaps of B (20.0) and C (20.0) are by code only
   (`check.json`); take A's right-end Measures worked (5.00 and 20.00, zoom point left of the panel). Take B's
   footage ends on an empty Measure panel: trim at the script gate. Logs of the failed tries: `B-try1`, `C-try1`.
5. **Q4 (STL + PrusaSlicer) not run** (PLAN: "cut first if the take fails"; kept the lab lean). The 220 x 60 rack's
   size is in `P/build.json` (proof bbox); no slicer claim.
6. Take A needed 3 starts before the kept take: a CRLF line-ending error in the script, then the tree row for Hook
   not found until the Body row is opened (now opened before recording). No footage from those starts is kept.
7. sc9 was not touched by this stage. The search check (growth rule G) was **not checkable** from the Studio files on
   disk (no search-term table); fc9 is built either way (DECISIONS.md).
