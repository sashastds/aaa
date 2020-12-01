import pytest

from one_hot_encoder import fit_transform


def test_single_repeated():

    expected = [("8", [1]), ("8", [1]), ("8", [1])]
    input_sequence = ["8"] * 3
    actual = fit_transform(input_sequence)

    assert (
        expected == actual
    ), "multiple entrances of same string give different encodings"


def test_empty_str():

    expected = [("", [1])]
    actual = fit_transform([""])

    assert expected == actual


def test_single_arg_equal_calls():

    input_single = ""
    input_sequence = [""]

    assert fit_transform(input_single) == fit_transform(
        input_sequence
    ), "same single argument in iterable and as is yields different results"


def test_raises_exception_empty_args():

    with pytest.raises(TypeError):
        fit_transform()


@pytest.mark.parametrize(
    "input_sequence, expected",
    [
        pytest.param(list("abcd"), [0, 0, 1, 0], id="four elements"),
        pytest.param(list("ab"), [1, 0], id="two elements"),
    ],
)
def test_sequential_numeration_existence(input_sequence, expected):

    actual = [t[1] for t in fit_transform(input_sequence)]
    assert expected in actual


@pytest.mark.parametrize(
    "input_sequence, not_expected",
    [
        pytest.param(list("abcd"), [1, 0, 0, 0, 0], id="four elements"),
        pytest.param(list("ab"), [0, 1, 0], id="two elements"),
    ],
)
def test_sequential_numeration_absence(input_sequence, not_expected):

    actual = [t[1] for t in fit_transform(input_sequence)]
    assert not_expected not in actual
