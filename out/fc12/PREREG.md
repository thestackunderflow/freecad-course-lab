# fc12 Claude runs: pre-registration (PLAN rev 2.1 section 2.5), written 17 Nov 2026 before the first run

- Start file: `out/fc12/P/stand-trap.FCStd` (G0 Q8): Params `hooks` 4, `hook_gap` 60 deg; Body: Post pad, Hook pad,
  PolarPattern Mode Extent, Angle 240, Occurrences = `Params.hooks`; lips at 0 / 80 / 160 / 240 (one in the wall).
- FreeCAD 1.1.4 + freecad-mcp 0.1.28 (`fcc-app:1.1.4-0.1.28`), fresh container, the file open in the GUI.
- Claude Code as in the image, `claude --model claude-sonnet-5-5 --strict-mcp-config --mcp-config entry.json`
  (only the freecad server, behind the logging proxy), `--max-budget-usd 0.20 --max-turns 40`, live cost guard.
- Cap: **$0.20 per run, $0.40 for the stage** (ledger `freecad-course-BUDGET.tsv`, mark "# --- GO 17 Nov 2026 fc12").
  A run that hits its cap stops; no rerun without the owner.
- n = 1 each, run in this order: A1, then B1.

## Prompts (exact)
- **A1 (not asked to check):** My coat stand has 4 hooks that should be 60 degrees apart on the front half, but one
  points into the wall. Fix it so the gap stays 60 when I change the number of hooks.
- **B1 (asked):** the same + " Then check the angle between neighbouring hooks and tell me the numbers."

## Score (by code: `lab/fc12parts.py` check on the document as Claude left it, then at `hooks` 3 and 6; `lab/fc12score.py`)
- Pass = gaps 60 +- 0.01 at hooks 4, 3 and 6, and the count follows `hooks`. Side reported separately (every
  lip-centre angle in [-0.01, 180.01] from the first hook's original direction).
- Classes, first that fits: (5) count typed, not bound; (4) per-gap Spacings list typed; (1) gap formula / Spacing
  bound to names (passes at 3 and 6, an expression reads `hook_gap`); (3) Spacing (or any route) passing with a typed
  60, names unused; (2) typed 180 in Extent (fails at 3: 90); (6) other angle / centred or reversed; (7) moved the
  first hook only (by hand from the transcript); (8) broke the file / no hooks read.
- **Checked** = Claude read the copies' geometry or placements (not just echoed the value it set): read by hand from
  the MCP transcript. Every number Claude reports is compared with ours.
- Told as they happened; no invented contrast; never "Claude always".
