import unittest

from one_hot_encoder import fit_transform


class TestFitTransform(unittest.TestCase):
    def test_single_repeated(self):

        expected = [("8", [1]), ("8", [1]), ("8", [1])]
        input_sequence = ["8"] * 3

        self.assertEqual(expected, fit_transform(input_sequence))

    def test_empty_str(self):

        expected = [("", [1])]
        input_sequence = [""]

        self.assertEqual(expected, fit_transform(input_sequence))

    def test_single_arg_equal_calls(self):

        input_single = ""
        input_sequence = [""]

        self.assertEqual(fit_transform(input_single), fit_transform(input_sequence))

    def test_raises_exception_empty_args(self):

        with self.assertRaises(TypeError):
            fit_transform()

    def test_sequential_numeration(self):

        input_sequence = list("abcd")
        actual = [t[1] for t in fit_transform(input_sequence)]

        self.assertIn([0, 0, 1, 0], actual)
        self.assertNotIn([1, 0, 0, 0, 0], actual)


if __name__ == "__main__":
    unittest.main()
