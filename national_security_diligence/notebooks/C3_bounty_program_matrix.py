#!/usr/bin/env python3
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
OUT = Path('/tmp/ns-diligence-lab-notebooks/c3_bounty_program_matrix.csv')
OUT.parent.mkdir(parents=True, exist_ok=True)
cmd = [
    sys.executable, '-m', 'ns_diligence.award_matrix',
    str(ROOT / 'data/sample/c3_whistleblower_programs.csv'),
    str(OUT),
]
subprocess.run(cmd, check=True, cwd=ROOT, env={**__import__('os').environ, 'PYTHONPATH': str(ROOT / 'src')})
print('Wrote', OUT)

