import pandas as pd

from Discretizer.SRAD_Discretizer import AbstractUnsupervisedDiscretizer


class EFD_Discretizer(AbstractUnsupervisedDiscretizer):
    @staticmethod
    def get_raw_bins(column, number_of_bins):
        _, bins = pd.qcut(column, q=number_of_bins, retbins=True, duplicates='drop')
        return bins

    @classmethod
    def get_name(self):
        return "EFD"