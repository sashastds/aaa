import re

import pytest

from morse import decode


@pytest.mark.parametrize(
    "input_sequence, expected",
    [
        pytest.param("... --- ...", "SOS", id="SOS"),
        pytest.param("", "", id="empty"),
        pytest.param("." * 5, "5", id="five"),
        pytest.param("symbolsnotfromvocab", "", id="keyerror"),
    ],
)
def test_decode(expected, input_sequence, request):
    """
    this test checks not only asserts expected equals actual,
    but also exception raising on unknown characters
    using parameter's id
    this is possible due to pytest's 'request' fixture
    """
    current_test_name = request.node.name
    param_id = re.search(r"\[(?:[a-zA-z ])+\]", string=current_test_name).group(0)[1:-1]

    if param_id == "keyerror":
        with pytest.raises(KeyError):
            decode(input_sequence)
    else:
        actual = decode(input_sequence)
        assert expected == actual, "actual decoded result doesn't match expected"
