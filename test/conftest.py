# type: ignore
# flake8: noqa ANN201

__copyright__ = "Copyright 2020-2021, Gispo Ltd"
__license__ = "GPL version 3"
__email__ = "info@gispo.fi"
__revision__ = "$Format:%H$"

from typing import Tuple

import pytest
from PyQt5.QtWidgets import QWidget
from qgis.core import QgsApplication
from qgis.gui import QgsMapCanvas

from ..testing.qgis_interface import QgisInterface
from ..testing.utilities import get_qgis_app
from ..tools.custom_logging import setup_logger
from ..tools.resources import plugin_name


@pytest.fixture(autouse=True, scope="session")
def initialize_qgis() -> Tuple[QgsApplication, QgsMapCanvas, QgisInterface, QWidget]:
    """Initializes qgis session for all tests"""
    yield get_qgis_app()


@pytest.fixture(scope="session")
def qgis_app(initialize_qgis) -> QgsApplication:
    return initialize_qgis[0]


@pytest.fixture(scope="session")
def canvas(initialize_qgis) -> QgsMapCanvas:
    return initialize_qgis[1]


@pytest.fixture(scope="session")
def iface(initialize_qgis) -> QgisInterface:
    return initialize_qgis[2]


@pytest.fixture(scope="session")
def qgis_parent(initialize_qgis) -> QWidget:
    return initialize_qgis[3]


@pytest.fixture(scope="function")
def new_project(iface) -> None:
    """
    Initializes new QGIS project by removing layers and relations etc.
    """
    yield iface.newProject()


@pytest.fixture(scope="session")
def initialize_logger(iface):
    setup_logger(plugin_name(), iface)
