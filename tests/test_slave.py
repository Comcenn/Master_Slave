from unittest import TestCase, main
from unittest.mock import Mock, patch
from requests.exceptions import RequestException
from slave.slave import get_status_code, exit_with_code


# Mocking a response object
class ResponseObj:
    def __init__(self, status_code: int) -> None:
        self.status_code = status_code


# Function to raise an error
def raise_error(*args, **kwargs) -> None:
    raise RequestException


class TestSlave(TestCase):
    @patch("slave.slave.get", spec=True)
    def test_get_status_code_sends_correct_url(self, mock_get: Mock) -> None:
        expected_pattern = r"https://postman-echo.com/delay/[1-5]"

        get_status_code()

        self.assertRegex(
            mock_get.call_args[0][0],
            expected_pattern,
            msg="URL to requests.get() did not return expected"
            f"pattern: {expected_pattern} != {mock_get.call_args[0][0]}(URL).",
        )

    @patch("slave.slave.get")
    def test_get_status_code_returns_correct_code(self, mock_get: Mock) -> None:
        expected_code = 200
        mock_get.return_value = ResponseObj(200)

        ret_status_code = get_status_code()

        self.assertTrue(
            (expected_code == ret_status_code),
            msg="Returned Status Code not as expected: "
            f"{expected_code} != {ret_status_code}",
        )

    @patch("slave.slave.get")
    def test_get_status_code_returns_none_on_an_error(self, mock_get: Mock) -> None:

        expected_code = None
        mock_get.side_effect = raise_error

        ret_status_code = get_status_code()

        self.assertTrue(
            (expected_code == ret_status_code),
            msg=f"Returned code != None; Returned code = {ret_status_code}",
        )

    @patch("slave.slave.get")
    def test_exit_with_code_exits_with_exit_code_0_when_status_code_is_200(
        self, mock_get: Mock
    ) -> None:
        exp_exit_code = 0
        mock_get.return_value = ResponseObj(200)

        with self.assertRaises(SystemExit) as exit_obj:
            exit_with_code()
        self.assertEqual(
            exit_obj.exception.code,
            exp_exit_code,
            msg=f"Exit code != 0; code = {exit_obj.exception.code}",
        )

    @patch("slave.slave.get")
    def test_exit_with_code_exits_with_exit_code_1_when_status_code_is_not_equal_to_200(
        self, mock_get: Mock
    ) -> None:
        exp_exit_code = 1
        mock_get.return_value = ResponseObj(404)

        with self.assertRaises(SystemExit) as exit_obj:
            exit_with_code()
        self.assertEqual(
            exit_obj.exception.code,
            exp_exit_code,
            msg=f"Exit code != 1; code = {exit_obj.exception.code}",
        )

    @patch("slave.slave.get")
    def test_exit_with_code_exits_with_exit_code_2_when_get_status_code_returns_none(
        self, mock_get: Mock
    ) -> None:
        exp_exit_code = 2
        mock_get.side_effect = raise_error

        with self.assertRaises(SystemExit) as exit_obj:
            exit_with_code()
        self.assertEqual(
            exit_obj.exception.code,
            exp_exit_code,
            msg=f"Exit code != 2; code = {exit_obj.exception.code}",
        )


if __name__ == "__main__":
    main()
