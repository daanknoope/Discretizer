from unittest import TestCase

import pandas as pd

from Discretizer.MDLP_Discretizer import *


class TestMDLP_Discretizer(TestCase):
    def test_get_raw_bins(self):
        df = pd.DataFrame({'x': [1, 2, 3, 4, 5], 'y': [0, 0, 0, 1, 1]})
        res = MDLP_Discretizer().get_raw_bins(['x'], df, 'y', None)
        self.assertEqual(len(res), 1)
        self.assertEqual(3.5, res[0])
