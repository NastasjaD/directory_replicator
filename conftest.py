import subprocess
from pathlib import Path

import pytest


@pytest.fixture
def create_temporary_dirs(tmp_path) -> Path:
    reference = tmp_path / "reference"
    target = tmp_path / "target"

    reference.mkdir()
    target.mkdir()

    (reference / "file1.txt").write_text("First text file")
    (reference / "file2.txt").write_text("Second text file")
    (reference / "nested_dir").mkdir()
    (reference / "nested_dir" / "nested_file.txt").write_text("Nested text file")

    return reference, target


@pytest.fixture
def run_cli_app():
    def _run_cli_app(
            reference_dir: Path | None = None,
            target_dir: Path | None = None
    ):
        result = subprocess.run(
            ["python", "main.py", str(reference_dir), str(target_dir)],
            capture_output=True,
            text=True
        )
        return result

    return _run_cli_app
