import csv
import os
from itertools import product, chain
from pandas import DataFrame

import pandas as pd
from pgmpy.models import BayesianModel

from Discretizer import DiscretizerFactory
from Discretizer.AbstractSupervisedDiscretizer import AbstractSupervisedDiscretizer
from typing import NewType, Dict, List, Tuple

HyperParameter = NewType("HyperParameter", int)
Grid = NewType("Grid", Dict[str, List[HyperParameter]])


class SRAD_Discretizer(AbstractSupervisedDiscretizer):

    def __init__(self, parent_limit=6, alpha=10,
                 grid={'EWD': [2, 3, 10], 'EFD': [2, 3, 10], 'IQR': [0], 'Median': [0]}):
        self.parent_limit = parent_limit
        self.alpha = alpha
        self.grid = grid

    @staticmethod
    def unfold_grid(grid: object) -> List[Tuple[str, int]]:
        return [*chain(*[product([method], grid[method]) for method in grid])]

    def create_constraints(self, discretization_vars: List[str], grid: Grid, objective: str) -> List[str]:
        constraints = []
        for var in discretization_vars:
            d_var = [self.create_strategy_name(var, method, hp) for (method, hp) in self.unfold_grid(grid)]
            constraints += [f'~{x}<-{y}' for (x, y) in product(d_var, d_var)]
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

    def get_discretization_graph(self, df: DataFrame, discretization_var: str, grid: Grid) -> BayesianModel:
        ddf = self.create_discretization_dataframe(df, discretization_var, grid)
        constraints = self.create_constraints([discretization_var], grid)
        G = self.structure_learn(self.discr_df_to_dat(ddf), self.get_discretization_settings(), constraints)
        return G

    @classmethod
    def get_discretization_strategy(cls, df: DataFrame, discretization_var: str, objective: str, grid: Grid) -> List[
        str]:
        G = cls.get_discretization_graph(df, discretization_var, grid)
        selected_nodes = [cls.from_strategy_name(x) for (x, y) in G.edges if
                          y == objective and discretization_var in x]
        return selected_nodes

    # should we not kick this out since it has no buckets? it violates the interface..
    @classmethod
    def create_discretization_dataframe(cls, df: DataFrame, discretization_var: str, grid: Grid) -> DataFrame:
        ddf = df.copy()
        ddf = ddf.drop(discretization_var, axis=1)

        strategies = []
        for method in grid:
            for hp in grid[method]:
                strategies.append((discretization_var, method, hp))

        return cls.discretize_from_strategies(ddf, strategies)

    @classmethod
    def get_raw_bins(cls, column: pd.Series, target: str, df: DataFrame) -> List[int]:
        selected_nodes = cls.get_discretization_strategy(df, column.name, target, cls.grid)

        # In this version we're going to always select the first strategy, and we assume only one exists..
        discretization_var, method, hp = selected_nodes[0]
        discretizer = DiscretizerFactory.get_discretizer(method)

        if isinstance(discretizer, AbstractSupervisedDiscretizer):
            raise ValueError("Using supervised discretizers has not yet been implemented for SRAD")

        return discretizer.get_bins(hp)
        
    @classmethod
    def get_name(cls):
        return "SRAD"

    @staticmethod
    def structure_learn(dat, settings, constraints):

        if os.path.exists('sol.dot'):
            os.remove('sol.dot')
