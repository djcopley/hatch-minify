from __future__ import annotations

from typing import Any, Callable
from unittest.mock import MagicMock

import pytest

from hatch_minify.plugin import MinifyBuildHook


@pytest.fixture
def mock_builder():
    builder = MagicMock()
    mock_files = [MagicMock(path="test.js"), MagicMock(path="test.css"), MagicMock(path="test.html")]
    builder.recurse_included_files.return_value = mock_files
    builder.target_dir = "/mock/target/dir"
    builder.source_dir = "/mock/source/dir"
    return builder


@pytest.fixture
def mock_app():
    app = MagicMock()
    app.env_vars = {}
    app.verbosity = 0
    return app


@pytest.fixture
def mock_hook(mock_builder, mock_app):
    return MinifyBuildHook(mock_builder, mock_app)


@pytest.fixture
def mock_build_config(mock_builder):
    config = MagicMock()
    config.builder = mock_builder
    return config


@pytest.fixture
def build_hook(mock_build_config, mock_app):
    root = "/mock/root"
    config = {"key": "value"}
    metadata = MagicMock()
    directory = "/mock/directory"
    target_name = "mock_target"
    return MinifyBuildHook(root, config, mock_build_config, metadata, directory, target_name, app=mock_app)


@pytest.fixture
def build_hook_factory(tmp_path_factory) -> Callable:
    def _create_build_hook(
        root: str = "/mock/root",
        config: dict[str, Any] | None = None,
        build_config: Any = None,
        metadata: Any = None,
        directory: str = "/mock/directory",
        target_name: str = "mock_target",
        app: Any = None,
    ) -> MinifyBuildHook:
        if config is None:
            config = {"key": "value"}
        if build_config is None:
            build_config = MagicMock()
        if metadata is None:
            metadata = MagicMock()
        if app is None:
            app = MagicMock()

        # Create a new temporary directory for each invocation
        tmp_path_factory.mktemp("build_hook")

        return MinifyBuildHook(root, config, build_config, metadata, directory, target_name, app=app)

    return _create_build_hook
