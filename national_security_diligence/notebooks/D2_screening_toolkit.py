#!/usr/bin/env python3
from pathlib import Path
import subprocess
import sys
import os

ROOT = Path(__file__).resolve().parents[1]
OUTDIR = Path('/tmp/ns-diligence-lab-notebooks')
OUTDIR.mkdir(parents=True, exist_ok=True)
env = {**os.environ, 'PYTHONPATH': str(ROOT / 'src')}
commands = [
    [sys.executable, str(ROOT / 'ns_screen.py'), str(ROOT / 'data/synthetic/d2_counterparties.csv'), str(ROOT / 'data/sample/d2_fixture_screening_list.csv'), str(OUTDIR / 'd2_ns_screen_sample.csv'), '--threshold', '0.80'],
    [sys.executable, '-m', 'ns_diligence.export_list_screen', str(ROOT / 'data/synthetic/d2_counterparties.csv'), str(ROOT / 'data/sample/d2_fixture_screening_list.csv'), str(OUTDIR / 'd2_export_screen_sample.csv'), '--threshold', '0.80'],
    [sys.executable, '-m', 'ns_diligence.ownership_graph', str(ROOT / 'data/synthetic/d2_ownership_edges.csv'), str(OUTDIR / 'd2_ownership_graph_sample.csv')],
]
for cmd in commands:
    subprocess.run(cmd, check=True, cwd=ROOT, env=env)
print('Wrote D2 outputs to', OUTDIR)

