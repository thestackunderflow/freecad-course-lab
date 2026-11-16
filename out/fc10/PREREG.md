# fc10 Claude runs: pre-registration (committed before the runs, 16 Nov 2026)

Start file for both: `out/fc10/P/hook-unpinned.FCStd` at plate_height 60 (HookSketch 2 DoF, bottom 0, top 60, hole 15
below the top). Claude Code, `claude-sonnet-5-5`, `--strict-mcp-config --mcp-config entry.json` (freecad server only,
freecad-mcp 0.1.28 through the logging proxy), `--max-budget-usd 0.45 --max-turns 40`, live guard `lab/costguard.py`.
n = 1 per arm. Stage cap $0.90.

- **A1 not asked:** "Make this hook taller: set plate_height to 80."
- **B1 asked:** "Make this hook taller: set plate_height to 80. Before you change anything, make the sketch fully
  constrained, with a corner on the origin, and tell me the degrees of freedom before and after."

Scored by our code only (`lab/fc10parts.py` check mode on every document open in FreeCAD after the run): DoF of
HookSketch, bottom (world ZMin), top (ZMax), hole below the top (ZMax minus the hole's axis height), Params
plate_height, constraints before/after (rules added), origin tie, tools it called (execute_code or sketch tools), and
what it said (its DoF numbers vs ours).

Classes (first that fits):
1. **stopped by the cost cap**: the guard or --max-budget-usd ended the run (shown as that, never as Claude's result).
2. **right + pinned**: plate_height 80, bottom 0.00 (|ZMin| < 0.01), top 80.00, hole 15.0 below the top, DoF 0.
3. **right but still unpinned**: plate_height 80, bottom 0.00, top 80.00, hole 15.0, DoF > 0.
4. **moved**: |ZMin| >= 1 mm (or the hole not 15.0 below the top because the plate moved).
5. **partly done**: anything else (plate_height not 80, no solid, 0.01 <= |ZMin| < 1 mm, ...).

Note from G0 (not known to Claude): on this file the size change alone dropped the bottom 1.32 to 10.39 mm in 11 of
11 tries by hand / by code; a class-3 result is possible by chance, so the DoF and the tie are scored separately.
