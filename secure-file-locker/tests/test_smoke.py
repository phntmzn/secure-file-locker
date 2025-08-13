from pathlib import Path
from subprocess import run, CalledProcessError, PIPE
import sys

def test_help_runs():
    r = run([sys.executable, "-m", "locker.cli", "--help"], stdout=PIPE, stderr=PIPE)
    assert r.returncode == 0
