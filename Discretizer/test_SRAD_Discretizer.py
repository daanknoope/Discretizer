import unittest
from unittest import TestCase

import os
import pandas as pd

from Discretizer.SRAD_Discretizer import SRAD_Discretizer


class TestSRAD_Discretizer(TestCase):
    def test_unfold_grid(self):
        grid = {'EWD': [1, 2, 3], 'MDLP': [0], 'EFD': [1, 2, 10]}
        expectedResult = [('EWD', 1), ('EWD', 2), ('EWD', 3), ('MDLP', 0), ('EFD', 1), ('EFD', 2), ('EFD', 10)]
        print(SRAD_Discretizer.unfold_grid(grid))
        self.assertEqual(expectedResult, SRAD_Discretizer.unfold_grid(grid))


class TestSRAD_Discretizer(TestCase):
    def test_create_constraints(self):
        discretization_vars = ['pulse', 'speed']
        grid = {'EWD' : [2,10], 'MDLP': [0]}
        objective = 'y'
        d = SRAD_Discretizer()
        output = d.create_constraints(discretization_vars, grid, objective)
        test_constraint = f'~{d.create_strategy_name("speed", "EWD", 10)}<-{d.create_strategy_name("speed", "MDLP", 0)}'
        self.assertTrue(test_constraint in output)

    def test_create_constraints_simple(self):
        discretization_vars = ['x']
        objective = 'y'
        grid = {'EWD' : [2,10]}

        d = SRAD_Discretizer()
        output = d.create_constraints(discretization_vars, grid, objective)
        self.assertEqual(6, len(set(output)))

    @unittest.skipIf("TRAVIS" in os.environ and os.environ['TRAVIS'] == "true", "Skipping on travis due to gobnilp dependency.")
    def test_get_raw_bins_srad(self):
        df = pd.DataFrame(data={'x': [1, 2, 3, 4, 5], 'y': [0, 0, 0, 1, 1]})
        discretizer = SRAD_Discretizer(grid={'EWD' : [2]})
        res = discretizer.get_raw_bins(df[['x']], 'y', df)
        self.assertEqual(len(res), 1+2)
        self.assertEqual(3, res[1])

    def test_get_bins(self):
        df = pd.DataFrame(data={'x': [1, 2, 3, 4, 5], 'y': [1, 0, 0, 1, 1]})
        discretizer = SRAD_Discretizer(grid = {'EWD' : [2,3,10]})
        res = discretizer.get_bins(discretizer, df[['x']], 'y', df)
        self.assertEqual(len(res), 2 + 2)

    def test_bins_2(self):
        df = pd.DataFrame(data={'x': [1, 2, 3, 4, 5], 'y': [1, 0, 0, 1, 1]})
        discretizer = SRAD_Discretizer(grid = {'EWD' : [2,3,10], 'MDLP': [0]})
        res = discretizer.get_bins(discretizer, df[['x']], 'y',df)
        print(res)