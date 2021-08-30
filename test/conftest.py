# type: ignore
# flake8: noqa ANN201

__copyright__ = "Copyright 2020-2021, Gispo Ltd"
__license__ = "GPL version 3"
__email__ = "info@gispo.fi"
__revision__ = "$Format:%H$"

import pytest

from ..tools.custom_logging import setup_logger
from ..tools.resources import plugin_name


@pytest.fixture(scope="session")
def initialize_logger(qgis_iface):
    setup_logger(plugin_name(), qgis_iface)
