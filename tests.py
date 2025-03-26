import os


def test_replicate__success(create_temporary_dirs, run_cli_app) -> None:
    reference_dir, target_dir = create_temporary_dirs
    result = run_cli_app(reference_dir, target_dir)

    assert result.returncode == 0
    assert os.path.exists(target_dir / "file1.txt")
    assert (target_dir / "file1.txt").read_text() == "First text file"
    assert os.path.exists(target_dir / "file2.txt")
    assert os.path.exists(target_dir / "nested_dir" / "nested_file.txt")
    assert f"{reference_dir} directory has been successfully replicated to {target_dir}" in result.stderr


def test_replicate__source_not_found(create_temporary_dirs, run_cli_app) -> None:
    result = run_cli_app()
    assert f"Error: Source directory not found" in result.stderr


def test_replicate__overwrite(create_temporary_dirs, run_cli_app) -> None:
    reference_dir, target_dir = create_temporary_dirs
    run_cli_app(reference_dir, target_dir)
    assert (reference_dir / "file1.txt").read_text() == (target_dir / "file1.txt").read_text()
    assert (reference_dir / "file2.txt").read_text() == (target_dir / "file2.txt").read_text()

    new_subdir = reference_dir / "new_subdir"
    new_subdir.mkdir()
    (new_subdir / "new_file.txt").write_text("New file in new subdir")
    (reference_dir / "file3.txt").write_text("Third text file")
    (reference_dir / "file1.txt").unlink()

    result = run_cli_app(reference_dir, target_dir)
    assert result.returncode == 0
    assert (target_dir / "file3.txt").read_text() == "Third text file"
    assert (target_dir / new_subdir / "new_file.txt").read_text() == "New file in new subdir"
    assert not (target_dir / "file1.txt").exists()
    assert f"{reference_dir} directory has been successfully replicated to {target_dir}" in result.stderr
    assert f"Replication completed!" in result.stderr
