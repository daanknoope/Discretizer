from Discretizer.AbstractUnsupervisedDiscretizer import AbstractUnsupervisedDiscretizer


class Median_Discretizer(AbstractUnsupervisedDiscretizer):

    def get_raw_bins(self, variables, df, target=None, number_of_bins=None):
        column = df[variables[0]]
        return [None, column.median(), None]

    @classmethod
    def get_name(self):
        return 'Median'
