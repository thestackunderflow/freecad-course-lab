# fc11 Claude runs: pre-registration (committed before the runs, 17 Nov 2026, PLAN 4.2 rev 3.1)

Start file for both: `out/fc11/G0b/hook-orphan.FCStd` (made by hand in G0b: the `plate_height = 60 mm (f)` size on the
back line deleted, a driving 55 on the inner face, "Fully constrained", no error; `Params.plate_height` 60, read by no
size). Claude Code, `claude-sonnet-5-5`, `--strict-mcp-config --mcp-config entry.json` (freecad server only,
freecad-mcp 0.1.28 through the logging proxy), `--max-budget-usd 0.45 --max-turns 40`, live guard `lab/costguard.py`.
API key in the container env only. n = 1 per arm. Stage cap $0.90.

- **A1 not asked:** "Make this hook taller: set plate_height to 80."
- **B1 asked:** "Make this hook taller: set plate_height to 80. Before you change anything, check which sizes drive this
  sketch and which Params cells they use. After the change, measure the top height and tell me the number."

Scored by our code only (`lab/fc11parts.py` check mode on every document open in FreeCAD after the run): Params
plate_height, top (ZMax), the 8 line lengths (step height, hook_depth, lip_height), the inner size (driving / reference /
expression / gone, its value), `plate_height_users` (driving sizes whose expression reads Params.plate_height),
redundant / conflicting lists, HookSketch state, constraints vs the start file; tools called (execute_code or sketch
tools); what it said vs what we measured.

Classes (`lab/fc11score.py classify`, first that fits):
1. **stopped by the cost cap** (shown as that, never as Claude's result).
2. **partly done**: no solid read.
3. plate_height not 80: **asked a question or made no change** (sketch and sheet as the start file), else **partly done**.
4. **second driving size by code, kept (sketch invalid)**: redundant / conflicting constraints or HookSketch Invalid
   (top [lab]).
5. **stale**: top not 80.00 (said done / reported: told apart by hand from the reply).
6. **wrong part**: top 80.00 but a line length other than 80 / 75 changed (e.g. the 55 kept, another size bound).
7. **right, 55 bound to a formula**: the inner size driving with an expression of plate_height (and thickness).
8. **right now, trap kept**: top 80.00, right profile, but no size reads Params.plate_height (e.g. 55 edited to 75).
9. **right by re-linking plate_height**: the 55 deleted, a back-line size bound to plate_height.
10. **right + reference**: the 55 reference (75), back line bound to plate_height.
11. **partly done**: anything else.

"Added a second driving size in a way FreeCAD refused, then [what next]" is read by hand from tools.txt (a refused
`setDatum` / an error reply) and reported beside the class.
