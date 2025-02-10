# Hatch Minify Build Hook

<div>
<a href="https://github.com/djcopley/hatch-minify/actions/workflows/tests.yml"><img src="https://github.com/djcopley/hatch-minify/actions/workflows/tests.yml/badge.svg?branch=main" alt="Tests" /></a> <a href="https://badge.fury.io/py/hatch-minify"><img src="https://badge.fury.io/py/hatch-minify.svg" alt="PyPI version" /></a> <a href="https://pypi.python.org/pypi/hatch-minify/"><img src="https://img.shields.io/pypi/pyversions/hatch-minify.svg" alt="PyPI Supported Python Versions" /></a> <a href="https://pepy.tech/project/hatch-minify"><img src="https://static.pepy.tech/badge/hatch-minify" alt="Downloads" /></a>
</div>

This [Hatch](https://hatch.pypa.io/latest/) plugin provides a build hook for 
[minifying](https://en.wikipedia.org/wiki/Minification_(programming)) python source code. 
This is useful for keeping distributions lean.

## Global dependency

Ensure `hatch-minify` is defined within the `build-system.requires` field in your `pyproject.toml` file.

```toml
[build-system]
requires = ["hatchling", "hatch-minify"]
build-backend = "hatchling.build"
```

## Build hook

The [build hook plugin](https://hatch.pypa.io/latest/plugins/build-hook/reference/) name is `minify`.

- ***pyproject.toml***

    ```toml
    [tool.hatch.build.targets.wheel.hooks.minify]
    ```

- ***hatch.toml***

    ```toml
    [build.targets.wheel.hooks.minify]
    ```

> **Note:** It is not recommended to minify source distributions.

### Editable installs

This build hook does not support editable installations.
