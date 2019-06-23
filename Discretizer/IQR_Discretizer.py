from Discretizer.AbstractUnsupervisedDiscretizer import AbstractUnsupervisedDiscretizer


class IQR_Discretizer(AbstractUnsupervisedDiscretizer):
    @staticmethod
    def get_raw_bins(column, _):
        q2 = column.quantile(0.25)
        q4 = column.quantile(0.75)
        return [None, q2, q4, None]

    @classmethod
    def get_name(self):
        return 'IRQ'