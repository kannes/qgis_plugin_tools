__copyright__ = "Copyright 2020-2021, Gispo Ltd"
__license__ = "GPL version 3"
__email__ = "info@gispo.fi"

import logging
from typing import Optional

from qgis.PyQt import uic
from qgis.PyQt.QtCore import pyqtSignal
from qgis.PyQt.QtWidgets import (
    QDialog,
    QHBoxLayout,
    QLabel,
    QProgressBar,
    QPushButton,
    QSizePolicy,
    QSpacerItem,
    QVBoxLayout,
    QWidget,
)

from ..tools.i18n import tr
from ..tools.resources import plugin_name, qgis_plugin_tools_resources

FORM_CLASS: QWidget
FORM_CLASS, _ = uic.loadUiType(qgis_plugin_tools_resources("ui", "progress_dialog.ui"))
LOGGER = logging.getLogger(plugin_name())


class ProgressDialog(QDialog, FORM_CLASS):
    """
    Dialog containing progress bar to show processes of long running tasks.
    """

    progress_bar: QProgressBar
    status_label: QLabel
    v_layout: QVBoxLayout

    aborted = pyqtSignal()

    def __init__(
        self,
        parent: Optional[QDialog] = None,
        show_abort_button: bool = False,
        abort_btn_text: Optional[str] = None,
    ) -> None:
        QDialog.__init__(self, parent)
        self.setupUi(self)
        if show_abort_button:
            self.push_btn = QPushButton()
            self.push_btn.setText(
                abort_btn_text if abort_btn_text is not None else tr("Abort")
            )
            layout = QHBoxLayout()
            spacer = QSpacerItem(
                100, 20, QSizePolicy.MinimumExpanding, QSizePolicy.Expanding
            )
            layout.addSpacerItem(spacer)
            layout.addWidget(self.push_btn)
            self.v_layout.addLayout(layout)
            self.push_btn.clicked.connect(self._aborted)

        self.update_progress_bar(0)

    def set_status(self, status_text: str) -> None:
        LOGGER.debug(f"Status:   {status_text}")
        self.status_label.setText(status_text)

    def update_progress_bar(self, progress: float) -> None:
        """ Update progress bar with a progress """
        LOGGER.debug(f"Progress {progress}")
        self.progress_bar.setValue(min(100.0, progress))

    def _aborted(self) -> None:
        LOGGER.warning("Aborted")
        self.aborted.emit()
