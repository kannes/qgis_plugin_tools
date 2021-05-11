__copyright__ = "Copyright 2020-2021, Gispo Ltd"
__license__ = "GPL version 2"
__email__ = "info@gispo.fi"
__revision__ = "$Format:%H$"

from typing import Any, Dict, Optional


class QgsPluginException(Exception):
    """ Use this as a base exception class in custom exceptions """

    # Override default_msg to set default message in inherited classes
    default_msg = ""

    def __init__(
        self, message: Optional[str] = None, bar_msg: Optional[Dict[str, Any]] = None
    ) -> None:
        """
        Initializes the exception with custom bar_msg to be shown in message bar
        :param message: Title of the message
        :param bar_msg: dictionary formed by tools.custom_logging.bar_msg
        """
        if message is None:
            message = self.default_msg
        super().__init__(message)
        self.bar_msg: Dict[str, Any] = bar_msg if bar_msg is not None else {}


class QgsPluginNetworkException(QgsPluginException):
    pass


class QgsPluginNotImplementedException(QgsPluginException):
    pass


class QgsPluginVersionInInvalidFormat(QgsPluginException):
    pass


class QgsPluginInvalidProjectSetting(QgsPluginException):
    pass
