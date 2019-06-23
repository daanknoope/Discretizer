from abc import ABC, abstractmethod

import numpy as np


class AbstractDiscretizer(ABC):
    min_int = int(np.iinfo(np.int32).min)
    max_int = int(np.iinfo(np.int32).max)
    bins = []

    @classmethod
    @abstractmethod
    def get_name(cls):
        ...

    @classmethod
    def get_bins(cls, *args):
        bins = cls.get_raw_bins(*args)
        bins[0] = cls.min_int
        bins[-1] = cls.max_int
        return bins
