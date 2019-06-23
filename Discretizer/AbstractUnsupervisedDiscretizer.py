from Discretizer.AbstractSupervisedDiscretizer import AbstractSupervisedDiscretizer


class SRAD_Discretizer(AbstractSupervisedDiscretizer):
    @classmethod
    def get_name(cls):
        return "SRAD"

    @staticmethod
    def get_raw_bins(column, number_of_bins):
        pass


