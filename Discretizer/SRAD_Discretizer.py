import csv
import os
import subprocess
from itertools import product, chain
from shutil import which
from typing import NewType, Dict, List, Tuple

import pandas as pd
from gobnilp import parse_gobnilp_structure
from pandas import DataFrame
from pgmpy.models import BayesianModel

from Discretizer import DiscretizerFactory, Discretizer
from Discretizer.AbstractSupervisedDiscretizer import AbstractSupervisedDiscretizer
from Discretizer.DDBN import DDBN

HyperParameter = NewType("HyperParameter", int)
Grid = NewType("Grid", Dict[str, List[HyperParameter]])


class SRAD_Discretizer(AbstractSupervisedDiscretizer):
    grid = {'EWD': [2, 3, 10], 'EFD': [2, 3, 10], 'IQR': [0], 'Median': [0]}

    def __init__(self, parent_limit=4, alpha=10,
                 grid=None):
        self.parent_limit = parent_limit
        self.alpha = alpha
        if grid:
            self.grid = grid

    @staticmethod
    def unfold_grid(grid: object) -> List[Tuple[str, int]]:
        return [*chain(*[product([method], grid[method]) for method in grid])]

    def create_constraints(self, discretization_vars: List[str], grid: Grid, objective: str) -> List[str]:
        constraints = []
        for var in discretization_vars:
            d_var = [self.create_strategy_name(var, method, hp) for (method, hp) in self.unfold_grid(grid)]
            constraints += [f'~{x}<-{y}' for (x, y) in product(d_var, d_var)]
            constraints += [f'~{x}->{objective}<-{y}' for (x,y) in product(d_var, d_var) if x!=y]
            constraints += [f'~{x}<-{objective}' for x in d_var]
        return constraints

    def get_discretization_settings(self) -> str:
        return f'''gobnilp/outputfile/dot = "sol.dot"
                gobnilp/dagconstraintsfile = "constraints.con"
                gobnilp/scoring/palim = {self.parent_limit}
                gobnilp/scoring/alpha = {self.alpha}'''

    # TODO this should be moved to gobnilp package
    @staticmethod
    def discr_df_to_dat(df: DataFrame) -> str:
        dff = df.copy()
        dff.loc[-1] = [len(pd.Series(dff[x].unique())) for x in dff.columns]
        dff.index = dff.index + 1
        dff = dff.sort_index()
        return dff.to_csv(sep=' ', index=False, quoting=csv.QUOTE_NONE)

    def get_discretization_graph(self, df: DataFrame, discretization_var: str, grid: Grid,
                                 objective: str) -> BayesianModel:
        ddf = self.create_discretization_dataframe(df, discretization_var, grid)
        # constraints = self.create_constraints([discretization_var], grid, objective)
        G = DDBN.learn_discretization_DBN(ddf, objective, [x for x in ddf.columns if self.sep in x], self.get_discretization_settings())
        # G = self.structure_learn(self.discr_df_to_dat(ddf), self.get_discretization_settings(), constraints)
        return G

    def get_discretization_strategy(self, df: DataFrame, discretization_var: str, objective: str, grid: Grid) -> List[
        str]:
        G = self.get_discretization_graph(df, discretization_var, grid, objective)
        selected_nodes = [self.from_strategy_name(x) for (x, y) in G.edges() if
                          y == objective and discretization_var in x]
        return selected_nodes

    # should we not kick this out since it has no buckets? it violates the interface..
    @classmethod
    def create_discretization_dataframe(cls, df: DataFrame, discretization_var: str, grid: Grid) -> DataFrame:
        ddf = df.copy()
        # ddf = ddf.drop(discretization_var, axis=1)

        strategies = []
        for method in grid:
            for hp in grid[method]:
                strategies.append((discretization_var, method, hp))

        return Discretizer.discretize_from_strategies(ddf, strategies)

    def get_raw_bins(self, variables: List[str], df: DataFrame, target: str, number_of_bins=0) -> List[int]:
        selected_nodes = self.get_discretization_strategy(df, variables[0], target, self.grid)

        # In this version we're going to always select the first strategy, and we assume only one exists..
        discretization_var, method, hp = selected_nodes[0]
        discretizer = DiscretizerFactory.get_discretizer(method)

        if isinstance(discretizer, AbstractSupervisedDiscretizer):
            raise ValueError("Using supervised discretizers has not yet been implemented for SRAD")

        return discretizer.get_bins([discretization_var], df, target=None, number_of_bins=hp)

    @classmethod
    def get_name(cls):
        return "SRAD"

    @staticmethod
    def structure_learn(dat: str, settings: str, constraints: List[str]) -> object:
        if not which('gobnilp'):
            raise EnvironmentError("Could not find gobnilp on path; make sure it is installed.")

        if os.path.exists('sol.dot'):
            os.remove('sol.dot')

        with open('datafile.dat', 'w') as data_file, open('gobnilp.set', 'w') as settings_file, open('constraints.con',
                                                                                                     'w') as constraints_file:
            data_file.write(dat)
            settings_file.write(settings)
            constraints_file.write('\n'.join(constraints))

        proc = subprocess.Popen(['gobnilp', 'datafile.dat'], stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                   cwd='.')
        proc.wait()
        out, err = proc.communicate()

        if not os.path.exists('sol.dot'):
            raise RuntimeError(f'Could not learn model: no output generated by gobnilp. Err: {err}')

        solution = open('sol.dot', 'r')
        return parse_gobnilp_structure(solution)
