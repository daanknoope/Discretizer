from mdlp.discretization import MDLP

from Discretizer.AbstractSupervisedDiscretizer import AbstractSupervisedDiscretizer


class MDLP_Discretizer(AbstractSupervisedDiscretizer):
    @classmethod
    def get_name(cls):
        return "MDLP"

    @staticmethod
    def get_raw_bins(column, target):
        transformer = MDLP()
        transformer = transformer.fit(column, target)
        return list(transformer.cut_points_[0])