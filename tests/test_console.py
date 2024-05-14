# tests/test_console.py
from unittest.mock import Mock

import pytest
import requests
from click.testing import CliRunner
from pytest_mock import MockFixture

from sixth import console, wikipedia


@pytest.fixture
def runner() -> CliRunner:
    return CliRunner()


# def test_main_succeeds(runner):
#     result = runner.invoke(console.main)
#     assert result.exit_code == 0
@pytest.mark.e2e
def test_main_succeeds_in_production_env(runner: CliRunner) -> None:
    result = runner.invoke(console.main)
    assert result.exit_code == 0


def test_main_succeeds(runner: CliRunner, mock_requests_get: Mock) -> None:
    result = runner.invoke(console.main)
    assert result.exit_code == 0


def test_main_prints_title(runner: CliRunner, mock_requests_get: Mock) -> None:
    result = runner.invoke(console.main)
    assert "Lorem Ipsum" in result.output


def test_main_invokes_requests_get(runner: CliRunner, mock_requests_get: Mock) -> None:
    runner.invoke(console.main)
    assert mock_requests_get.called


def test_main_uses_correct_url(runner: CliRunner, mock_requests_get: Mock) -> None:
    runner.invoke(console.main)
    assert mock_requests_get.call_args[0] == (wikipedia.API_URL.format(language="en"),)


def test_main_fails_on_request_error(
    runner: CliRunner, mock_requests_get: Mock
) -> None:
    mock_requests_get.side_effect = Exception("Boom")
    result = runner.invoke(console.main)
    assert result.exit_code == 1


def test_main_prints_message_on_request_error(
    runner: CliRunner, mock_requests_get: Mock
) -> None:
    mock_requests_get.side_effect = requests.RequestException
    result = runner.invoke(console.main)
    assert "Error" in result.output


@pytest.fixture
def mock_wikipedia_random_page(mocker: MockFixture) -> Mock:
    return mocker.patch("sixth.wikipedia.random_page")


def test_main_uses_specified_language(
    runner: CliRunner, mock_wikipedia_random_page: Mock
) -> None:
    runner.invoke(console.main, ["--language=pl"])
    mock_wikipedia_random_page.assert_called_with(language="pl")
