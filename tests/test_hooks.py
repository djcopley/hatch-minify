from hatch_minify.hooks import hatch_register_build_hook
from hatch_minify.plugin import MinifyBuildHook


def test_minify_build_hook():
    assert hatch_register_build_hook() == MinifyBuildHook
