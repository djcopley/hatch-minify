import os
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import MagicMock


def test_initialization(build_hook):
    assert build_hook.PLUGIN_NAME == "minify"
    assert build_hook.builder is not None
    assert isinstance(build_hook.minified_directory, TemporaryDirectory)


def test_minify_included_files_empty(build_hook):
    build_data = {"force_include": {}}
    build_hook.minify_included_files(build_data)
    build_hook.app.display_waiting.assert_called_once_with("Minifying python source...")
    assert build_data["force_include"] == {}


def test_minify_included_files(build_hook, tmp_path):
    test_file = tmp_path / "test.py"
    test_file.write_text("def hello():\n    print('Hello, World!')", encoding="utf-8")

    mock_included_file = MagicMock()
    mock_included_file.path = str(test_file)
    mock_included_file.distribution_path = "test.py"
    build_hook.builder.recurse_included_files.return_value = [mock_included_file]

    build_data = {"force_include": {}}
    build_hook.minify_included_files(build_data)

    assert len(build_data["force_include"]) == 1
    minified_path = next(iter(build_data["force_include"].keys()))
    assert Path(minified_path).exists()
    minified_content = Path(minified_path).read_text(encoding="utf-8")
    assert "def hello" in minified_content
    assert len(minified_content) < len(test_file.read_text(encoding="utf-8"))


def test_initialize_standard_version(build_hook):
    build_data = {"force_include": {}}
    build_hook.initialize("standard", build_data)
    build_hook.app.display_waiting.assert_called_once_with("Minifying python source...")


def test_initialize_non_standard_version(build_hook):
    build_data = {"force_include": {}}
    build_hook.initialize("other", build_data)
    build_hook.app.display_waiting.assert_not_called()


def test_finalize_standard_version(build_hook):
    build_data = {}
    temp_dir = build_hook.minified_directory
    build_hook.finalize("standard", build_data, "artifact.whl")
    assert not os.path.exists(temp_dir.name)


def test_finalize_non_standard_version(build_hook):
    build_data = {}
    temp_dir = build_hook.minified_directory
    build_hook.finalize("other", build_data, "artifact.whl")
    assert os.path.exists(temp_dir.name)
    temp_dir.cleanup()  # Clean up after test


def test_non_python_files_not_minified(build_hook, tmp_path):
    test_file = tmp_path / "test.txt"
    test_file.write_text("Hello, World!", encoding="utf-8")

    mock_included_file = MagicMock()
    mock_included_file.path = str(test_file)
    mock_included_file.distribution_path = "test.txt"
    build_hook.builder.recurse_included_files.return_value = [mock_included_file]

    build_data = {"force_include": {}}
    build_hook.minify_included_files(build_data)

    assert build_data["force_include"] == {}
    build_hook.app.display_debug.assert_called_once()
