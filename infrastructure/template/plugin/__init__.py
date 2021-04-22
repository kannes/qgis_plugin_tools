import os  # noqa F401

# <commented_out>from .qgis_plugin_tools.infrastructure.debugging import setup_pydevd

# <commented_out>if os.environ.get("QGIS_PLUGIN_USE_DEBUGGER") == "pydevd":
# <commented_out>    if (
# <commented_out>        os.environ.get("IN_TESTS", "0") != "1"
# <commented_out>        and os.environ.get("QGIS_PLUGIN_IN_CI", "0") != "1"
# <commented_out>    ):
# <commented_out>        setup_pydevd()


def classFactory(iface):  # noqa N802
    from .plugin import Plugin

    return Plugin(iface)
