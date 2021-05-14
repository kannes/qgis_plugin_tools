import os  # noqa F401

from qgis.gui import QgisInterface

# <commented_out>from .qgis_plugin_tools.infrastructure.debugging import (
# <commented_out>    setup_pydevd,
# <commented_out>    setup_ptvsd,
# <commented_out>    setup_debugpy,
# <commented_out>)
# <commented_out>debugger = os.environ.get("QGIS_PLUGIN_USE_DEBUGGER")
# <commented_out>if debugger:
# <commented_out>    if (
# <commented_out>        os.environ.get("IN_TESTS", "0") != "1"
# <commented_out>        and os.environ.get("QGIS_PLUGIN_IN_CI", "0") != "1"
# <commented_out>    ):
# <commented_out>        locals()["setup_" + debugger]()


def classFactory(iface: QgisInterface):  # noqa N802
    from .plugin import Plugin

    return Plugin(iface)
