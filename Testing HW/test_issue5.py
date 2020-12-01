import re

import pytest
from unittest.mock import MagicMock, patch
import urllib.request

from what_is_year_now import what_is_year_now, API_URL


@pytest.fixture
def json_file_dmy_datetime_format(tmpdir):

    json_file = tmpdir.join("dmy.json")
    json_file.write('{"currentDateTime": "01.12.2020T09:22Z"}')
    return json_file


@pytest.fixture
def json_file_ymd_datetime_format(tmpdir):

    json_file = tmpdir.join("ymd.json")
    json_file.write('{"currentDateTime": "2020-12-01T09:22Z"}')
    return json_file


@pytest.fixture
def json_file_invalid_datetime_format(tmpdir):

    json_file = tmpdir.join("invalid.json")
    json_file.write('{"currentDateTime": "wrongformat"}')
    return json_file


@pytest.fixture
def datetime_format_files(
    json_file_dmy_datetime_format,
    json_file_ymd_datetime_format,
    json_file_invalid_datetime_format,
):
    return {
        "json_file_dmy_datetime_format": json_file_dmy_datetime_format,
        "json_file_ymd_datetime_format": json_file_ymd_datetime_format,
        "json_file_invalid_datetime_format": json_file_invalid_datetime_format,
    }


@patch.object(urllib.request, "urlopen")
@pytest.mark.parametrize(
    ("json_filename", "expected"),
    [
        pytest.param("json_file_dmy_datetime_format", 2020, id="dmy"),
        pytest.param("json_file_ymd_datetime_format", 2020, id="ymd"),
        pytest.param("json_file_invalid_datetime_format", 2020, id="invalid"),
    ],
)
def test_current_year_getting(
    mock_api, json_filename, expected, datetime_format_files, request
):

    json_file = datetime_format_files[json_filename]
    context_manager_mock = MagicMock()
    context_manager_mock.__enter__ = MagicMock(return_value=json_file)
    context_manager_mock.__exit__ = MagicMock(return_value=None)
    mock_api.return_value = context_manager_mock

    param_id = re.search(r"\[(?:[a-zA-z ])+\]", string=request.node.name).group(0)[1:-1]

    if param_id == "invalid":
        with pytest.raises(ValueError):
            what_is_year_now()
    else:
        assert expected == what_is_year_now()
