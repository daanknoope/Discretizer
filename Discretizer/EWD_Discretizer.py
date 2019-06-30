import pandas as pd

from Discretizer.AbstractUnsupervisedDiscretizer import AbstractUnsupervisedDiscretizer


class EWD_Discretizer(AbstractUnsupervisedDiscretizer):

    def get_raw_bins(self, variables, df, target=None, number_of_bins=3):
        _, bins = pd.cut(df[variables[0]], bins=number_of_bins, retbins=True, duplicates='drop')
        return bins

    @classmethod
    def get_name(self):
        return "EWD"