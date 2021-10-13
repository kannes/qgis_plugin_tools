import time

import pytest
from PyQt5.QtCore import QCoreApplication
from qgis.PyQt import QtCore

from ...testing.utilities import TestTask
from ...tools.exceptions import TaskInterruptedException
from ...widgets import progress_dialog


@pytest.mark.parametrize("show_abort_btn", [True, False])
def test_progress_bar_dialog(qtbot, show_abort_btn):
    aborted = False

    def abort():
        nonlocal aborted
        aborted = True

    p_dialog = progress_dialog.ProgressDialog(show_abort_button=show_abort_btn)
    p_dialog.show()
    qtbot.addWidget(p_dialog)

    p_dialog.set_status("Status")
    p_dialog.update_progress_bar(10.0)
    p_dialog.update_progress_bar(101.0)
    p_dialog.aborted.connect(abort)

    assert hasattr(p_dialog, "push_btn") is show_abort_btn
    if show_abort_btn:
        qtbot.mouseClick(p_dialog.push_btn, QtCore.Qt.LeftButton)
    else:
        p_dialog.close()

    assert p_dialog.progress_bar.value() == 100
    assert p_dialog.abort_btn_text == progress_dialog.ProgressDialog.abort_btn_text
    assert aborted


@pytest.mark.parametrize("show_abort_btn", [True, False])
def test_create_simple_continuous_progress_dialog(qtbot, show_abort_btn):
    p_dialog = progress_dialog.create_simple_continuous_progress_dialog(
        "Progressing", show_abort_button=show_abort_btn
    )
    p_dialog.show()
    qtbot.addWidget(p_dialog)

    if show_abort_btn:
        qtbot.mouseClick(p_dialog.push_btn, QtCore.Qt.LeftButton)
    else:
        p_dialog.close()


@pytest.mark.parametrize("show_abort_btn", [True, False])
@pytest.mark.parametrize("should_abort", [True, False])
def test_run_task_with_continuous_progress_dialog(
    qtbot, show_abort_btn, should_abort, mocker
):
    # setup
    aborted = False
    terminated = False
    completed = False

    p_dialog = progress_dialog.create_simple_continuous_progress_dialog(
        "Mocking", show_abort_button=show_abort_btn
    )

    def complete():
        nonlocal completed
        completed = True

    def abort():
        nonlocal aborted
        aborted = True
        if show_abort_btn:
            qtbot.mouseClick(p_dialog.push_btn, QtCore.Qt.LeftButton)
        else:
            p_dialog.close()

    def terminate():
        nonlocal terminated
        terminated = True

    m_progress_bar = mocker.patch.object(
        progress_dialog,
        "create_simple_continuous_progress_dialog",
        return_value=p_dialog,
        autospec=True,
    )

    if should_abort:
        QtCore.QTimer.singleShot(5, abort)

    task = TestTask(sleep_time=0.005)

    # test
    progress_dialog.run_task_with_continuous_progress_dialog(
        task,
        "Processing",
        show_abort_button=show_abort_btn,
        completed_callback=complete,
        terminated_callback=terminate,
    )

    while not aborted and not completed and not terminated:
        QCoreApplication.processEvents()

    m_progress_bar.assert_called_once()

    time.sleep(0.1)

    if should_abort:
        assert isinstance(task.exception, TaskInterruptedException)
    else:
        assert task.exception is None
    assert aborted == should_abort
    assert completed != should_abort
    assert not terminated


@pytest.mark.parametrize("show_abort_btn", [True, False])
@pytest.mark.parametrize("should_fail", [True, False])
def test_run_task_with_continuous_progress_dialog_failure(
    qtbot, show_abort_btn, should_fail
):
    # setup
    terminated = False
    completed = False

    def complete():
        nonlocal completed
        completed = True

    def terminate():
        nonlocal terminated
        terminated = True

    task = TestTask(will_fail=should_fail, sleep_time=0.005)

    # test
    progress_dialog.run_task_with_continuous_progress_dialog(
        task,
        "Processing",
        show_abort_button=show_abort_btn,
        completed_callback=complete,
        terminated_callback=terminate,
    )

    if should_fail:
        assert isinstance(task.exception, ValueError)
    else:
        assert task.exception is None
    assert completed != should_fail
    assert terminated == should_fail
