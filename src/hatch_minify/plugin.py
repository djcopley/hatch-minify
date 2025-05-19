from __future__ import annotations

from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any

from hatchling.builders.hooks.plugin.interface import BuildHookInterface
from python_minifier import minify


class MinifyBuildHook(BuildHookInterface):
    PLUGIN_NAME = "minify"

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.builder = self.build_config.builder
        self.minified_directory = TemporaryDirectory()

    def minify_included_files(self, build_data):
        self.app.display_waiting("Minifying python source...")
        for included_file in self.builder.recurse_included_files():
            if not included_file.path.endswith(".py") or not included_file.distribution_path:
                self.app.display_debug(f"Not minified: {included_file.path}")
                continue
            source_path = Path(included_file.path)
            minified_path = Path(self.minified_directory.name) / included_file.distribution_path
            minified_path.parent.mkdir(parents=True, exist_ok=True)
            minified = minify(source_path.read_text(encoding="utf-8"), source_path.name)
            minified_path.write_text(minified, encoding="utf-8")
            build_data["force_include"][minified_path] = included_file.distribution_path

    def initialize(self, version: str, build_data: dict[str, Any]) -> None:
        if version != "standard":
            return
        self.minify_included_files(build_data)

    def finalize(
        self,
        version: str,
        build_data: dict[str, Any],  # noqa: ARG002
        artifact_path: str,  # noqa: ARG002
    ) -> None:
        if version != "standard":
            return
        self.minified_directory.cleanup()
