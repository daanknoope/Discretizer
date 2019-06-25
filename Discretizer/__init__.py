from typing import Tuple

from Discretizer.DiscretizerFactory import DiscretizerFactory

name = 'Discretizer'


class Discretizer(object):
    sep = '|'

    @staticmethod
    def discretize_from_object(df, column, discretizer):
        return discretizer.apply(column)

    @staticmethod
    def discretize(df, variable, method, hp=None):
        print(df)
        print(variable)
        return DiscretizerFactory.get_discretizer(method).fit_apply(variable, df, hp)

    @classmethod
    def create_strategy_name(cls, discretization_var: str, method: str, hyperparameter: int) -> str:
        return f'{discretization_var}{cls.sep}{method}{cls.sep}{hyperparameter}'

    @classmethod
    def from_strategy_name(cls, input: str) -> Tuple[str, str, int]:
        split = input.split(cls.sep)
        discretization_var = split[0]
        method = split[1]
        hyperparameter = int(split[2])
        return (discretization_var, method, hyperparameter)

    @classmethod
    def discretize_from_strategies(cls, df, strategies):
        ddf = df.copy()
        for (discretization_var, method, hp) in strategies:
            ddf[cls.create_strategy_name(discretization_var, method, hp)] = cls.discretize(df, discretization_var,
                                                                                           method, hp)
        discretization_vars = set([x for (x, y, z) in strategies])
        for discretization_var in discretization_vars:
            ddf = ddf.drop(discretization_var, axis=1)
        return ddf

    @classmethod
    def fit_apply_from_strategies(cls, df, strategies):
        ddf = df.copy()
        discretizers = {}
        for (discretization_var, method, hp) in strategies:
            name = cls.create_strategy_name(discretization_var, method, hp)
            discretizers[name] = DiscretizerFactory.get_discretizer(method).fit(df[discretization_var], hp)
            ddf[discretization_var] = discretizers[name].apply(df[discretization_var])
        # this needs to change for the different versions of discretizatoin
        #         for var in set([x for (x,_,_) in strategies]):
        #             ddf = ddf.drop(var, axis=1)
        return (ddf, discretizers)

    @staticmethod
    def from_strategy_name(name):
        split = name.split('|')
        discretization_var = split[0]
        method = split[1]
        hp = int(split[2])
        return (discretization_var, method, hp)
