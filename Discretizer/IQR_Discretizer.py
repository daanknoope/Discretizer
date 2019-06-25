from Discretizer.AbstractUnsupervisedDiscretizer import AbstractUnsupervisedDiscretizer


class IQR_Discretizer(AbstractUnsupervisedDiscretizer):
    @staticmethod
    def get_raw_bins(self, variables, df, target=None, number_of_bins=None):
        column = df[variables[0]]
        q2 = column.quantile(0.25)
        q4 = column.quantile(0.75)
        return [None, q2, q4, None]

    @classmethod
    def get_name(self):
        return 'IRQ'