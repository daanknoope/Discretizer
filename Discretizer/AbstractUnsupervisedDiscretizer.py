import pandas as pd

from Discretizer.AbstractDiscretizer import AbstractDiscretizer


class AbstractUnsupervisedDiscretizer(AbstractDiscretizer):

    def fit(self, variable, df, number_of_bins):
        self.bins = self.get_bins([variable], df, number_of_bins=number_of_bins)
        return self

    def apply(self, column):
        if not len(self.bins):
            raise ValueError('Discretizer has not been fitted yet or has created empty bins')
        return pd.cut(column, bins=self.bins, retbins=False, labels=range(0, len(self.bins) - 1))

    def fit_apply(self, variable, df, number_of_bins):
        column = df[variable]
        self.fit(variable, df, number_of_bins)
        discretized = self.apply(column)
        return discretized

    #     @classmethod
    #     def discretize(cls, column, number_of_bins):
    #         bins = cls.get_bins(column, number_of_bins)
    #         return pd.cut(column, bins=bins, retbins=False, labels=range(0,len(bins)-1))