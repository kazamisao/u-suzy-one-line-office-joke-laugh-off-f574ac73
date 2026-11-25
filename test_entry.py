"""Tests for the One-Line Office Joke Laugh-Off entry.

Run: python3 test_entry.py
Checks that main.py writes exactly the intended line, deterministically,
inside the competition's 1-200 character window.
"""

import importlib.util
import os
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))


def load_line():
    spec = importlib.util.spec_from_file_location("entry_main", os.path.join(HERE, "main.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.LINE


def run_once(out_dir):
    env = dict(os.environ, MAKEFUN_OUTPUT_DIR=out_dir)
    proc = subprocess.run(
        [sys.executable, "-P", "-s", os.path.join(HERE, "main.py")],
        env=env, capture_output=True, text=True,
    )
    assert proc.returncode == 0, proc.stderr
    with open(os.path.join(out_dir, "entry.txt"), encoding="utf-8") as fh:
        return fh.read()


def main():
    line = load_line()
    assert 1 <= len(line) <= 200, f"line length {len(line)} outside 1-200"
    assert line.strip() == line and line.strip(), "line must be non-blank and trimmed"
    assert "\n" not in line, "entry must be a single line"
    with tempfile.TemporaryDirectory() as d1, tempfile.TemporaryDirectory() as d2:
        first = run_once(d1)
        second = run_once(d2)
    assert first == line, "output file must equal the LINE constant"
    assert first == second, "output must be deterministic"
    print(f"ok: {len(line)} chars, deterministic, matches LINE")


if __name__ == "__main__":
    main()
