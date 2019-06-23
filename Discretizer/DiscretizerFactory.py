from Discretizer.EFD_Discretizer import EFD_Discretizer
from Discretizer.EWD_Discretizer import EWD_Discretizer
from Discretizer.IQR_Discretizer import IQR_Discretizer
from Discretizer.Median_Discretizer import Median_Discretizer


class DiscretizerFactory:
    @staticmethod
    def get_discretizer(method):
        if method == 'EWD':
            return EWD_Discretizer()
        elif method == 'EFD':
            return EFD_Discretizer()
        elif method == 'IQR':
            return IQR_Discretizer()
        elif method == 'Median':
            return Median_Discretizer()
        else:
            raise ValueError(f'Discretization method "{method} is not implemented."')