from abc import abstractmethod

from Discretizer.AbstractDiscretizer import AbstractDiscretizer


class AbstractSupervisedDiscretizer(AbstractDiscretizer):
    @staticmethod
    @abstractmethod
    def get_raw_bins(column, target):
        ...