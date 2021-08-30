# coding=utf-8
"""Common functionality used by regression tests."""

import os
import warnings

from ..tools.exceptions import QgsPluginNotImplementedException


# noinspection PyUnresolvedReferences
def get_qgis_app():  # noqa
    warnings.warn(
        "get_qgis_app() is deprecated. Use library pytest-qgis instead.",
        DeprecationWarning,
    )
    raise QgsPluginNotImplementedException(
        "get_qgis_app() is deprecated. Use library pytest-qgis instead."
    )


def is_running_inside_ci() -> bool:
    """Tells whether the plugin is running in CI environment"""
    return int(os.environ.get("QGIS_PLUGIN_IN_CI", "0")) == 1


def is_running_in_tools_module_ci() -> bool:
    return (
        is_running_inside_ci()
        and int(os.environ.get("QGIS_PLUGIN_TOOLS_IN_CI", "0")) == 1
    )


def qgis_supports_temporal() -> bool:
    try:
        from qgis.core import QgsRasterLayerTemporalProperties  # noqa F401

        return True
    except ImportError:
        return False
