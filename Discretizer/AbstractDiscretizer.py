from abc import ABC, abstractmethod
from typing import Tuple, List

import numpy as np
import pandas as pd
from pandas import DataFrame


class AbstractDiscretizer(ABC):
    min_int = int(np.iinfo(np.int32).min)
    max_int = int(np.iinfo(np.int32).max)
    bins = []
    sep = '|'

    @abstractmethod
    def get_name(cls):
        ...

    def get_bins(self, variables: List[str], df: DataFrame, target=None, number_of_bins=0):
        bins = self.get_raw_bins(variables, df, target, number_of_bins)
        bins[0] = self.min_int
        bins[-1] = self.max_int
        return bins

    @classmethod
    def create_strategy_name(cls, discretization_var: str, method: str, hyperparameter: int) -> str:
        return f'{discretization_var}{cls.sep}{method}{cls.sep}{hyperparameter}'

    @classmethod
    def from_strategy_name(cls, input: str) -> Tuple[str, str, int]:
        split = input.split(cls.sep)
        discretization_var = split[0]
        method = split[1]
        hyperparameter = int(split[2].split('_')[0])
        return (discretization_var, method, hyperparameter)

    @abstractmethod
    def get_raw_bins(self, variables: List[str], df: DataFrame, target: str, number_of_bins: int) -> List[int]:
        ...

    def apply(self, column):
        if not len(self.bins):
            raise ValueError('Discretizer has not been fitted yet or has created empty bins')
        # print(type(self))
        return pd.cut(column, bins=self.bins, retbins=False, labels=range(0, len(self.bins) - 1))