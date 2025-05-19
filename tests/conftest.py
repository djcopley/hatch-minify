import textwrap
from unittest.mock import MagicMock

import pytest
from hatchling.builders.plugin.interface import IncludedFile

from hatch_minify.plugin import MinifyBuildHook


@pytest.fixture
def mock_app():
    app = MagicMock()
    app.display_waiting = MagicMock()
    app.display_debug = MagicMock()
    return app


@pytest.fixture
def mock_builder():
    return MagicMock()


@pytest.fixture
def mock_build_config(mock_builder):
    build_config = MagicMock()
    build_config.builder = mock_builder
    return build_config


@pytest.fixture
def mock_config():
    return {}


@pytest.fixture
def mock_metadata():
    return MagicMock()


@pytest.fixture
def build_data():
    return {"force_include": {}}


@pytest.fixture
def sample_py_file(tmp_path):
    file_path = tmp_path / "sample.py"
    contents = textwrap.dedent("""\
    def hello():
        print("Hello, World!")
    """)
    file_path.write_text(contents, encoding="utf-8")
    return IncludedFile(
        str(file_path),
        "package/sample.py",
        "package/sample.py",
    )


@pytest.fixture
def sample_txt_file(tmp_path):
    file_path = tmp_path / "sample.txt"
    contents = textwrap.dedent("""\
    This is a sample text file.
    """)
    file_path.write_text(contents, encoding="utf-8")
    return IncludedFile(
        str(file_path),
        "package/sample.txt",
        "package/sample.txt",
    )


@pytest.fixture
def minify_build_hook(
    tmp_path,
    mock_config,
    mock_build_config,
    mock_metadata,
    mock_app,
):
    root = str(tmp_path)
    dist_path = str(tmp_path / "dist")
    return MinifyBuildHook(
        root,
        mock_config,
        mock_build_config,
        mock_metadata,
        dist_path,
        "wheel",
        mock_app,
    )
