from unittest import TestCase, main
from unittest.mock import patch, Mock, MagicMock
from asyncio import run, gather, sleep, Future
from os.path import split, join
from contextlib import contextmanager
from io import StringIO
from subprocess import run as proc_run
import sys
from master.master import run_app, run_controller, return_slave_app_path, main as mn


# Async mock
def async_mock(*args, **kwargs):
    m = MagicMock(*args, **kwargs)

    async def mock_coro(*args, **kwargs):
        return await m(*args, **kwargs)

    mock_coro.mock = m

    return mock_coro


# Mock Process Inherits from Future inorder for tests to work
class MockProcess(Future):
    def __init__(self, return_code, pid, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.returncode = return_code
        self.pid = pid
        # Immediately setting future to done and returning self
        self.set_result(self)

    def wait(self) -> None:
        return self.result()


# To capture output
@contextmanager
def capture(func, *args, **kwargs):
    out, sys.stdout = sys.stdout, StringIO()
    try:
        func(*args, **kwargs)
        sys.stdout.seek(0)
        yield sys.stdout.read()
    finally:
        sys.stdout = out


class TestMaster(TestCase):
    @patch(
        "master.master.create_subprocess_shell",
        new=async_mock(return_value=MockProcess(0, 1234)),
    )
    def test_run_app_calls_create_sub_process_shell_with_correct_path_and_returns_correct_exit_code(
        self,
    ) -> None:
        # Importing mock to query it
        from master.master import create_subprocess_shell

        create_subprocess_shell.mock.asser_called_once(
            join(*split(split(split(__file__)[0])[0]), "slave", "slave.py"), 0
        )

    @patch(
        "master.master.create_subprocess_shell",
        new=async_mock(return_value=MockProcess(0, 1234)),
    )
    def test_run_app_returns_exit_code(self) -> None:
        async def runner():
            async def get_code():
                proc = await run_app(None)
                return proc.returncode

            return await gather(get_code())

        return_code = run(runner())

        self.assertEqual(
            return_code[0], 0, msg=f"Return code != 0; Return code: {return_code}"
        )

    @patch(
        "master.master.create_subprocess_shell",
        new=async_mock(return_value=MockProcess(0, 1234)),
    )
    def test_run_controller_prints_the_correct_text(self):
        async def runner():
            await gather(run_controller(None))

        with capture(run, runner()) as output:
            self.assertRegex(
                output,
                "; Slave App succesfully ran and exited; Return Code: ",
                msg=f"{output} does not match Regex",
            )

    @patch(
        "master.master.run_app",
        new=async_mock(
            side_effect=[
                MockProcess(1, 1234),
                MockProcess(1, 1234),
                MockProcess(0, 3456),
            ]
        ),
    )
    def test_run_controller_continues_running_until_zero_code(self):
        async def runner():
            await gather(run_controller(None))

        with capture(run, runner()) as output:
            self.assertRegex(
                output,
                "; Slave App succesfully ran and exited; Return Code: ",
                msg=f"{output} does not match Regex",
            )

    @patch("master.master.run_controller", new=async_mock())
    @patch("master.master.gather", new=async_mock(return_value=MockProcess(0, 1223)))
    def test_main_runs_and_calls_gather(self):
        run(mn(None))
        from master.master import gather

        call_cnt = gather.mock.call_count

        self.assertEqual(call_cnt, 1, msg="{call_cnt} != 1")

    @patch("master.master.run_controller", new=async_mock())
    @patch("master.master.gather", new=async_mock(return_value=MockProcess(0, 1223)))
    def test_main_runs_and_calls_gather_with_five_params(self):
        run(mn(None))

        from master.master import gather

        params_cnt = len([call for call in gather.mock.call_args[0]])

        self.assertEqual(params_cnt, 5, msg="{params_cnt} != 5")

    def test_return_slave_app_path_returns_correct_path(self) -> None:
        expected = join(*split(split(split(__file__)[0])[0]), "slave", "slave.py")
        actual_path = return_slave_app_path()

        self.assertEqual(
            actual_path, expected, msg=f"Paths do not match {expected} != {actual_path}"
        )

    def test_master_exits_with_return_code_2_when_bad_file_passed_in_error_when_bad_file_path_passed_in(
        self,
    ) -> None:
        # Please note seeing "ERROR: '--slavePath' parameter is not a file. Bad path: <path>"
        # means test is normal and test is passing.
        import master.master as master

        result = proc_run(
            ["python", master.__file__, "--slavePath", "badfilepath"]
        ).returncode

        self.assertEqual(result, 2, msg="returncode != 2; Return code: {result}")


if __name__ == "__main__":
    main()
