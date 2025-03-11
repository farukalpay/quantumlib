import pytest
import subprocess

def test_cli_help():
    proc = subprocess.run(["run_circuit", "--help"], capture_output=True, text=True)
    assert proc.returncode == 0
    assert "usage" in proc.stdout.lower()
