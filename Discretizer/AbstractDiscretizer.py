from abc import ABC, abstractmethod
from typing import Tuple

import numpy as np


class AbstractDiscretizer(ABC):
    min_int = int(np.iinfo(np.int32).min)
    max_int = int(np.iinfo(np.int32).max)
    bins = []
    sep = '|'

    @classmethod
    @abstractmethod
    def get_name(cls):
        ...

    @classmethod
    def get_bins(cls, *args):
        bins = cls.get_raw_bins(*args)
        bins[0] = cls.min_int
        bins[-1] = cls.max_int
        return bins

    @classmethod
    def create_strategy_name(cls, discretization_var: str, method: str, hyperparameter: int) -> str:
        return f'{discretization_var}{cls.sep}{method}{cls.sep}{hyperparameter}'

    @classmethod
    def from_strategy_name(cls, input : str) -> Tuple[str,str,int]:
        split = input.split(cls.sep)
        discretization_var = split[0]
        method = split[1]
        hyperparameter = int(split[2])
        return (discretization_var, method, hyperparameter)