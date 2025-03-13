# Hatch Minify Build Hook
 
[![Hatch](https://img.shields.io/badge/%F0%9F%A5%9A-Hatch-4051b5.svg)](https://github.com/pypa/hatch)
[![Tests](https://github.com/djcopley/hatch-minify/actions/workflows/tests.yml/badge.svg?branch=main)](https://github.com/djcopley/hatch-minify/actions/workflows/tests.yml)
[![PyPI version](https://badge.fury.io/py/hatch-minify.svg)](https://badge.fury.io/py/hatch-minify)
[![PyPI Supported Python Versions](https://img.shields.io/pypi/pyversions/hatch-minify.svg)](https://pypi.python.org/pypi/hatch-minify/)
[![Downloads](https://static.pepy.tech/badge/hatch-minify)](https://pepy.tech/project/hatch-minify)

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
