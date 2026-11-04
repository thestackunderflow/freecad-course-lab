#!/bin/bash
# fx3 takes A, B, C (LAB-fx3 sections 3.A-3.C): one fresh home, one filmed terminal (46 columns), three recordings.
#   tools/run_fx4.sh fx3ABC lab/fx3_ABC.sh fx3-lab:1        (PREREG env is set by run_fx4.sh)
set -u
. /lab/lab/fx3_lib.sh
mkdir -p $X/A $X/B $X/C
cd ~
# ---- state building (not filmed): short prompt appended BEFORE the "before" copies; no ~/.local, no uv cache
echo "PS1='\$ '" >> ~/.bashrc
cp ~/.bashrc $X/A/bashrc-before.txt; cp ~/.profile $X/A/profile-before.txt
claude_home /home/maker
ls -d ~/.local ~/.cache/uv 2>&1 > $X/A/fresh-check.txt
{ claude --version; node --version; echo "prereg commit $PREREG"; cat /etc/os-release | head -4; date -u; } > $X/pins.txt 2>&1
claude mcp list > $X/A/mcp-list-before.txt 2>&1
curl -LsSf https://astral.sh/uv/0.13.6/install.sh | sh > $X/A/uv-install.txt 2>&1
mkdir -p ~/fx3 && cp /lab/lab/fx3/launcher.js ~/fx3/launcher.js
sl_display $W $H
term_start
# ================= take A
O=$X/A
sl_record "$O" nomouse; sl_mark "recording started: a new login shell, uv installed"; sl_nap 1.5
run_wait 'uvx --version' "uvx --version: typed" "uvx --version: printed" $O/uvx-version.txt 60
sl_nap 3
typ 'echo $PATH' "echo PATH: typed"; wait_prompt 20; sl_mark "echo PATH: printed"; save_out $O/echo-path.txt; sl_nap 3
typ 'which uvx' "which uvx: typed"; wait_prompt 20; save_out $O/which-uvx.txt; sl_nap 3
typ 'grep -n local/bin ~/.bashrc ~/.profile' "grep startup: typed"; wait_prompt 20; save_out $O/grep-startup.txt; sl_nap 3
if grep -q 'local/bin/env' ~/.bashrc ~/.profile; then
  typ 'cat "$HOME/.local/bin/env"' "env file: typed"; wait_prompt 20; save_out $O/startup-env-file.txt; sl_nap 3
fi
typ 'cat /etc/environment' "etc-environment: typed"; wait_prompt 20; sl_mark "short list: shown"; save_out $O/short-list-etc-environment.txt; sl_nap 3
typ 'systemctl --user show-environment' "systemd-user: typed"; wait_prompt 20; save_out $O/short-list-systemd-user.txt; sl_nap 3
grep -n '^ENV_PATH\|^ENV_SUPATH' /etc/login.defs | tee $O/short-list-login-defs.txt
typ 'which uvx' "which uvx again: typed"; wait_prompt 20; sl_nap 20
sl_mark "recording stopped"; stamp $O
diff $O/bashrc-before.txt ~/.bashrc | tee $O/bashrc-diff.txt
diff $O/profile-before.txt ~/.profile | tee $O/profile-diff.txt
ls -l ~/.local/bin | tee $O/ls-local-bin.txt
grep -n local/bin ~/.bash_profile ~/.bash_login ~/.zshrc 2>&1 | tee $O/grep-startup-wide.txt
# ================= take B
O=$X/B
fresh; typ 'which node' "which node: typed"; wait_prompt 20; save_out $O/which-node.txt; sl_nap 1   # pre-check, outside the recording
NODE=$(which node)
sl_record "$O" nomouse; sl_mark "recording started: same terminal, nothing installed since take A"; sl_nap 2
typ 'env -i HOME=/home/maker PATH=/usr/bin:/bin $(which node) /home/maker/fx3/launcher.js uvx' "launcher short: typed"
end=$(( $(date +%s) + 30 )); until tmux capture-pane -p -t cc | grep -q 'ENOENT'; do [ "$(date +%s)" -ge "$end" ] && break; sleep 0.2; done
sl_mark "launcher short: ENOENT"; wait_prompt 30; save_out $O/launcher-short.txt; sl_nap 6
typ 'env -i HOME=/home/maker PATH=/usr/bin:/bin $(which node) /home/maker/fx3/launcher.js /home/maker/.local/bin/uvx' "launcher full: typed"
end=$(( $(date +%s) + 30 )); until tmux capture-pane -p -t cc | grep -q 'started:'; do [ "$(date +%s)" -ge "$end" ] && break; sleep 0.2; done
sl_mark "launcher full: starts"; wait_prompt 40 || sl_mark "TIMEOUT: launcher full did not return"; save_out $O/launcher-full.txt; sl_nap 5
sl_mark "recording stopped"; stamp $O
cp ~/fx3/launcher.js $O/launcher.js; sha256sum $O/launcher.js | tee $O/launcher.sha256
{ node --version; } > $O/node-version.txt
# ================= take C
O=$X/C
mkdir -p ~/.config/Claude   # not filmed: the lab's own copy of the config file (written with printf; the take films the cat)
printf '{\n  "mcpServers": {\n    "freecad": {\n      "command": "/home/maker/.local/bin/uvx",\n      "args": ["freecad-mcp@0.1.28"]\n    }\n  }\n}\n' > ~/.config/Claude/claude_desktop_config.json
claude mcp list > $O/mcp-list-before.txt 2>&1
sl_record "$O" nomouse; sl_mark "recording started: same terminal"; sl_nap 2
typ 'cat ~/.config/Claude/claude_desktop_config.json' "config: full path"; wait_prompt 20; save_out $O/claude_desktop_config.txt; sl_nap 12
typ 'claude mcp add --scope user freecad -- /home/maker/.local/bin/uvx freecad-mcp@0.1.28' "add full path: typed"; wait_prompt 60; save_out $O/mcp-add.txt; sl_nap 2
typ 'claude mcp list' "list: typed"
end=$(( $(date +%s) + 120 )); until tmux capture-pane -p -t cc | grep -qE 'Connected|Failed'; do [ "$(date +%s)" -ge "$end" ] && break; sleep 0.3; done
sl_mark "list: Connected"; wait_prompt 60; save_out $O/mcp-list.txt; sl_nap 15
sl_mark "recording stopped"; stamp $O
cp ~/.config/Claude/claude_desktop_config.json $O/claude_desktop_config.json
ls -l ~/.config/Claude | tee $O/ls-config-dir.txt
tmux kill-server 2>/dev/null; sl_display_stop
echo "ABC done"
