import os
from pathlib import Path
from unittest.mock import MagicMock

from python_minifier import minify


def test_minify_included_files_skips_non_py_files(minify_build_hook, build_data, sample_txt_file):
    minify_build_hook.builder.recurse_included_files.return_value = [sample_txt_file]
    minify_build_hook.minify_included_files(build_data)
    assert not build_data["force_include"]


def test_minify_included_files_skips_files_without_distribution_path(minify_build_hook, build_data, sample_py_file):
    sample_py_file.distribution_path = ""
    minify_build_hook.builder.recurse_included_files.return_value = [sample_py_file]
    minify_build_hook.minify_included_files(build_data)
    assert not build_data["force_include"]


def test_minify_included_files_processes_py_files(minify_build_hook, build_data, sample_py_file):
    minify_build_hook.builder.recurse_included_files.return_value = [sample_py_file]

    minify_build_hook.minify_included_files(build_data)
    assert len(build_data["force_include"]) == 1

    minified_file_path = next(iter(build_data["force_include"].keys()))
    assert os.path.exists(minified_file_path)
    assert build_data["force_include"][minified_file_path] == sample_py_file.distribution_path

    original_content = Path(sample_py_file.path).read_text(encoding="utf-8")
    minified_content = Path(minified_file_path).read_text(encoding="utf-8")
    expected_minified = minify(original_content, Path(sample_py_file.path).name)
    assert minified_content == expected_minified


def test_initialize_standard_version(minify_build_hook, build_data):
    minify_build_hook.minify_included_files = MagicMock()
    minify_build_hook.initialize("standard", build_data)
    minify_build_hook.minify_included_files.assert_called_once_with(build_data)


def test_initialize_non_standard_version(minify_build_hook, build_data):
    minify_build_hook.minify_included_files = MagicMock()
    minify_build_hook.initialize("non-standard", build_data)
    minify_build_hook.minify_included_files.assert_not_called()


def test_finalize_standard_version(minify_build_hook, build_data):
    minify_build_hook.minified_directory.cleanup = MagicMock()
    minify_build_hook.finalize("standard", build_data, "artifact_path")
    minify_build_hook.minified_directory.cleanup.assert_called_once()


def test_finalize_non_standard_version(minify_build_hook, build_data):
    minify_build_hook.minified_directory.cleanup = MagicMock()
    minify_build_hook.finalize("non-standard", build_data, "artifact_path")
    minify_build_hook.minified_directory.cleanup.assert_not_called()
