import pandas as pd

from Discretizer.AbstractUnsupervisedDiscretizer import AbstractUnsupervisedDiscretizer


class EFD_Discretizer(AbstractUnsupervisedDiscretizer):
    @staticmethod
    def get_raw_bins(self, variables, df, target=None, number_of_bins=3):
        _, bins = pd.qcut(df[variables[0]], q=number_of_bins, retbins=True, duplicates='drop')
        return bins

    @classmethod
    def get_name(self):
        return "EFD"