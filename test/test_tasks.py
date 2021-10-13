import time

from qgis.core import Qgis

from ..testing.utilities import TestTaskRunner
from ..tools.exceptions import QgsPluginException, TaskInterruptedException
from ..tools.tasks import BaseTask, FunctionTask


class TestTask(BaseTask):
    def __init__(self, will_fail: bool = False, error_to_raise=ValueError):
        super().__init__()
        self._will_fail = will_fail
        self._error_to_raise = error_to_raise

    def _run(self) -> bool:
        for i in range(10):
            self.setProgress(i * 10)
            if self._will_fail:
                raise self._error_to_raise("custom failure")
            self._check_if_canceled()
            time.sleep(0.01)
        return True


def fn(*args, **kwargs):
    for i in range(10):
        time.sleep(0.01)
    return args, kwargs


def test_run_simple_task(task_runner: TestTaskRunner):
    task = TestTask()
    success = task_runner.run_task(task)

    assert success
    assert task_runner.progress == 100


def test_run_simple_task_canceled(task_runner: TestTaskRunner, qgis_iface):
    task = TestTask()
    success = task_runner.run_task(task, cancel=True)
    messages = qgis_iface.messageBar().get_messages(Qgis.Warning)

    assert not success
    assert task_runner.fail
    assert (
        "Task TestTask was not successful:Task was cancelled by user or some dependency tasks failed"
        in messages
    )


def test_run_simple_task_canceled_after_a_while(
    task_runner: TestTaskRunner, qgis_iface
):
    task = TestTask()
    success = task_runner.run_task(task, cancel=True, sleep_before_cancel=0.01)
    messages = qgis_iface.messageBar().get_messages(Qgis.Critical)

    assert not success
    assert task_runner.fail
    assert isinstance(task.exception, TaskInterruptedException)
    assert "Task canceled!:" in messages


def test_run_simple_task_failed(task_runner: TestTaskRunner, qgis_iface):
    task = TestTask(True)
    success = task_runner.run_task(task)
    messages = qgis_iface.messageBar().get_messages(Qgis.Critical)

    assert not success
    assert task_runner.fail
    assert "Unhandled exception occurred:custom failure" in messages


def test_run_simple_task_failed_with_qgs_plugin_exception(
    task_runner: TestTaskRunner, qgis_iface
):
    task = TestTask(True, QgsPluginException)
    success = task_runner.run_task(task)
    messages = qgis_iface.messageBar().get_messages(Qgis.Critical)

    assert not success
    assert task_runner.fail
    assert "custom failure:" in messages


def test_function_task_without_params(task_runner: TestTaskRunner):
    task = FunctionTask(fn)
    success = task_runner.run_task(task)

    assert success
    assert task.result == ((), {})


def test_function_task_with_params(task_runner: TestTaskRunner):
    task = FunctionTask(lambda: fn(1, 2, a=1, b=2))
    success = task_runner.run_task(task)

    assert success
    assert task.result == ((1, 2), {"a": 1, "b": 2})
