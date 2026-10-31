"""Flatten three of PrusaSlicer's own bundled system presets into one config file for the CLI (lesson 5).
PrusaSlicer 2.9.2's --printer-profile left the printer at "- default FFF -" in our container (probed 31 Oct 2026), so
the stock presets are resolved here exactly as the bundle writes them: a preset's `inherits = A; B` applies A, then B,
then its own keys; abstract presets are the `*name*` sections.
    python3 slicer/flatten.py /usr/share/PrusaSlicer/profiles/PrusaResearch.ini OUT.ini
Stock = printer "Original Prusa MK4S 0.4 nozzle", its default print "0.20mm SPEED @MK4S 0.4" and its default filament
"Prusament PLA @MK4S"."""
import sys

PRINTER = 'Original Prusa MK4S 0.4 nozzle'
PRINT = '0.20mm SPEED @MK4S 0.4'
FILAMENT = 'Prusament PLA @MK4S'


def parse(text):
    secs, cur = {}, None
    for ln in text.splitlines():
        s = ln.strip()
        if not s or s.startswith('#'):
            continue
        if s.startswith('[') and s.endswith(']'):
            cur = secs.setdefault(s[1:-1], {})
            continue
        if cur is not None and '=' in ln:
            k, v = ln.split('=', 1)
            cur[k.strip()] = v.strip()
    return secs


def resolve(secs, kind, name, seen=()):
    key = f'{kind}:{name}'
    if key not in secs:
        raise KeyError(key)
    if key in seen:
        raise ValueError('inherit loop ' + key)
    own = secs[key]
    out = {}
    for parent in [p.strip().strip('"') for p in own.get('inherits', '').split(';') if p.strip()]:
        out.update(resolve(secs, kind, parent, seen + (key,)))
    out.update({k: v for k, v in own.items() if k != 'inherits'})
    return out


def flatten(text, printer=PRINTER, prnt=PRINT, filament=FILAMENT):
    secs = parse(text)
    cfg = {}
    cfg.update(resolve(secs, 'printer', printer))
    cfg.update(resolve(secs, 'print', prnt))
    cfg.update(resolve(secs, 'filament', filament))
    for k in ('compatible_printers', 'compatible_printers_condition', 'compatible_prints',
              'compatible_prints_condition', 'renamed_from', 'alias'):
        cfg.pop(k, None)
    cfg['printer_settings_id'] = printer
    cfg['print_settings_id'] = prnt
    cfg['filament_settings_id'] = '"' + filament + '"'
    return cfg


def write(cfg, path):
    with open(path, 'w', encoding='utf-8', newline='\n') as f:
        f.write(f'# {PRINTER} + {PRINT} + {FILAMENT}, flattened from PrusaSlicer 2.9.2\'s PrusaResearch.ini\n')
        for k in sorted(cfg):
            f.write(f'{k} = {cfg[k]}\n')


USER = {'printer': 'MK4S 0.4 nozzle (stock)', 'print': '0.20mm SPEED (stock)', 'filament': 'Prusament PLA (stock)'}
DROP = ('compatible_printers', 'compatible_printers_condition', 'compatible_prints', 'compatible_prints_condition',
        'renamed_from', 'alias', 'inherits')


def datadir(text, d):
    """The GUI (2.9.2 offline, no profile repository) shows the same three presets as user presets, named "(stock)",
    each one resolved from the bundle unchanged; PrusaSlicer.ini selects them."""
    import os
    secs = parse(text)
    for kind, name in (('printer', PRINTER), ('print', PRINT), ('filament', FILAMENT)):
        cfg = {k: v for k, v in resolve(secs, kind, name).items() if k not in DROP}
        os.makedirs(os.path.join(d, kind), exist_ok=True)
        with open(os.path.join(d, kind, USER[kind] + '.ini'), 'w', encoding='utf-8', newline='\n') as f:
            f.write(f'# "{name}" from PrusaSlicer 2.9.2\'s bundled PrusaResearch.ini, resolved unchanged\n')
            for k in sorted(cfg):
                f.write(f'{k} = {cfg[k]}\n')
    with open(os.path.join(d, 'PrusaSlicer.ini'), 'w', encoding='utf-8', newline='\n') as f:
        f.write('[app]\nversion_check = 0\npreset_update = 0\nshow_splash_screen = 0\nno_defaults = 1\nshow_hints = 0\n'
                'show_drop_project_dialog = 0\nnotify_release = none\nview_mode = simple\nuse_perspective_camera = 1\n\n'
                f'[presets]\nprinter = {USER["printer"]}\nprint = {USER["print"]}\nfilament = {USER["filament"]}\n'
                'physical_printer = \nsla_print = \nsla_material = \n')


if __name__ == '__main__':
    if sys.argv[2] == '--datadir':
        datadir(open(sys.argv[1], encoding='utf-8').read(), sys.argv[3])
    else:
        write(flatten(open(sys.argv[1], encoding='utf-8').read()), sys.argv[2])
