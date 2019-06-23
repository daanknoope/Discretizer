from abc import abstractmethod
from typing import List

from pandas import Series, DataFrame

from Discretizer.AbstractDiscretizer import AbstractDiscretizer


class AbstractSupervisedDiscretizer(AbstractDiscretizer):
    @staticmethod
    @abstractmethod
    def get_raw_bins(column: Series, target: str, df: DataFrame) -> List[int]:
        ...
