from typing import List

from mdlp.discretization import MDLP
from pandas import DataFrame

from Discretizer.AbstractSupervisedDiscretizer import AbstractSupervisedDiscretizer


class MDLP_Discretizer(AbstractSupervisedDiscretizer):
    @classmethod
    def get_name(cls):
        return "MDLP"

    def get_raw_bins(self, variables: List[str], df: DataFrame, target: str, number_of_bins=None) -> List[int]:
        column = df[variables]
        transformer = MDLP()
        transformer = transformer.fit(column, df[target])
        return list(transformer.cut_points_[0])
