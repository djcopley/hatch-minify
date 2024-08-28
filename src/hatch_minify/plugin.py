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
        self.original_recurse_included_files = self.builder.recurse_included_files

    def recurse_included_minified_py_files(self):
        for include_file in self.original_recurse_included_files():
            self.app.display_debug(f"file: {include_file.path}")
            if not include_file.path.endswith(".py") or not include_file.relative_path:
                yield include_file
                continue
            source_path = Path(include_file.path)
            minified = minify(source_path.read_text(encoding="utf-8"), source_path.name)
            minified_path = Path(self.minified_directory.name) / include_file.relative_path
            minified_path.parent.mkdir(parents=True, exist_ok=True)
            minified_path.write_text(minified, encoding="utf-8")
            include_file.path = str(minified_path)
            yield include_file

    def initialize(self, version: str, build_data: dict[str, Any]) -> None:
        if version != "standard":
            return
        self.builder.recurse_included_files = self.recurse_included_minified_py_files

    def finalize(self, version: str, build_data: dict[str, Any], artifact_path: str) -> None:
        if version != "standard":
            return
        self.minified_directory.cleanup()
        self.builder.recurse_included_files = self.original_recurse_included_files
