"""Reading Claude Code's terminal screen (the text of `tmux capture-pane -p`), so a lab script knows when a reply is still
running and when Claude Code shows a permission prompt. Nothing here types for Claude: the script only waits, and
answers a permission prompt with the prompt's own plain "Yes" option (never "don't ask again"), as the README says.
Ported from the SolidCraft course lab (lesson 2), checked against Claude Code 2.1.308's screens."""
import re

BUSY = re.compile(r'esc to interrupt', re.IGNORECASE)
ASK = re.compile(r'Do you want to (proceed|allow|make this)', re.IGNORECASE)
DONE = re.compile(r'[A-Z][^\W\d_]+ for [0-9hms ]+· done [0-9]')    # "Worked for 9s · done", "Sautéed for 12s · done"
YES = re.compile(r'^\s*[❯>]?\s*(\d)\.\s+Yes\s*$', re.MULTILINE)  # the plain "1. Yes", not "Yes, and don't ask again"
TOOL = re.compile(r'^\s*(\S+ - \S+) \(MCP\)', re.MULTILINE)


def busy(text):
    return bool(BUSY.search(text or ''))


def approval(text):
    return bool(ASK.search(text or '')) and bool(YES.search(text or ''))


def approval_key(text):
    m = YES.search(text or '')
    return m.group(1) if m else None


def approval_tool(text):
    m = TOOL.search(text or '')
    return m.group(1) if m else None


def turns_done(text):
    """How many end-of-turn lines the screen shows (a turn is over when this count goes up)."""
    return len(DONE.findall(text or ''))
