#!/usr/bin/env python3
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
OUT = Path('/tmp/ns-diligence-lab-notebooks/a1_cfius_public_actions_sample.csv')
OUT.parent.mkdir(parents=True, exist_ok=True)
cmd = [
    sys.executable, '-m', 'ns_diligence.cfius_reports',
    str(ROOT / 'data/sample/cfius_annual_report_figures.csv'),
    str(OUT),
]
subprocess.run(cmd, check=True, cwd=ROOT, env={**__import__('os').environ, 'PYTHONPATH': str(ROOT / 'src')})
print('Wrote', OUT)

