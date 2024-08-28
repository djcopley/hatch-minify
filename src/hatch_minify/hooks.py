from hatchling.plugin import hookimpl

from hatch_minify.plugin import MinifyBuildHook


@hookimpl
def hatch_register_build_hook():
    return MinifyBuildHook
