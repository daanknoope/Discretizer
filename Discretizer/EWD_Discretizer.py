import pandas as pd

from Discretizer.AbstractUnsupervisedDiscretizer import AbstractUnsupervisedDiscretizer


class EWD_Discretizer(AbstractUnsupervisedDiscretizer):

    @staticmethod
    def get_raw_bins(column, number_of_bins):
        _, bins = pd.cut(column, bins=number_of_bins, retbins=True)
        return bins

    @classmethod
    def get_name(self):
        return "EWD"