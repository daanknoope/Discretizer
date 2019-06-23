from unittest import TestCase

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