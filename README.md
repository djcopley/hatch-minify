# Hatch Minify Build Hook

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
