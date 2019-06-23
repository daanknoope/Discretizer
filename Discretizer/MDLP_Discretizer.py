from typing import List

from mdlp.discretization import MDLP
from pandas import DataFrame, Series

from Discretizer.AbstractSupervisedDiscretizer import AbstractSupervisedDiscretizer


class MDLP_Discretizer(AbstractSupervisedDiscretizer):
    @classmethod
    def get_name(cls):
        return "MDLP"

    @staticmethod
    def get_raw_bins(column: Series, target: str, df: DataFrame) -> List[int]:
        transformer = MDLP()
        transformer = transformer.fit(column, target)
        return list(transformer.cut_points_[0])
