from Discretizer.AbstractDiscretizer import AbstractDiscretizer


class AbstractSupervisedDiscretizer(AbstractDiscretizer):

    def fit(self, variable, df, target):
        self.bins = self.get_bins([variable], df, target)
        return self

    def fit_apply(self, variable, df, target):
        ddf = df.copy()
        self.fit(variable, df, target)
        discretized = self.apply(df[variable])
        ddf[variable] = discretized
        return ddf
