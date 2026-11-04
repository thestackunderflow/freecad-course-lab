const { spawn } = require('child_process');
const cmd = process.argv[2];
const p = spawn(cmd, ['freecad-mcp@0.1.28'], { stdio: ['pipe', 'inherit', 'inherit'] });
p.on('error', function (e) { console.log(e.message); process.exit(1); });
p.on('spawn', function () { console.log('started: ' + cmd + ' (pid ' + p.pid + ')'); setTimeout(function () { p.kill(); }, 5000); });
