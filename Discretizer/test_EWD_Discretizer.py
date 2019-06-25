from unittest import TestCase

from pandas import DataFrame

from Discretizer.EWD_Discretizer import EWD_Discretizer


class TestEWD_Discretizer(TestCase):
    def test_get_raw_bins(self):
        variables = ['x']
        df = DataFrame({'x': [0, 1, 2, 3], 'y': [1, 2, 3, 4]})
        result = EWD_Discretizer().get_raw_bins(variables, df, number_of_bins=4)
        self.assertEqual(5, len(result))
