from Discretizer.SRAD_Discretizer import AbstractUnsupervisedDiscretizer


class Median_Discretizer(AbstractUnsupervisedDiscretizer):
    @staticmethod
    def get_raw_bins(column, _):
        return [None, column.median(), None]

    @classmethod
    def get_name(self):
        return 'Median'