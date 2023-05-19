from math import sqrt
from scipy.stats import norm
from ab_testing.testers.tester import Tester


class SampleTester(Tester):
    def __init__(self, 
                 convert_ctrl: int,
                 convert_expr: int,
                 total_ctrl: int,
                 total_expr: int) -> None:
        self.convert_ctrl = convert_ctrl
        self.convert_expr = convert_expr
        self.total_ctrl = total_ctrl
        self.total_expr = total_expr

        self.prob_ctrl = self.convert_ctrl / self.total_ctrl 
        self.prob_expr = self.convert_expr / self.total_expr
        
        self._calculate()
    
    def _calculate(self) -> None:
        difference = self.prob_expr - self.prob_ctrl
        prob_pooled = (
            (self.convert_ctrl + self.convert_expr)
            / (self.total_ctrl + self.total_expr)
        )
        std_err_pooled = sqrt(
            prob_pooled
            * (1 - prob_pooled)
            * (1 / self.total_ctrl + 1 / self.total_expr))

        # create distributions
        # null
        self.mean_null = 0
        self.stdev_null = std_err_pooled
        self.distribution_null = norm(self.mean_null, self.stdev_null)
        # alternative
        self.mean_alt = difference
        self.stdev_alt = std_err_pooled
        self.distribution_alt = norm(self.mean_alt, self.stdev_alt)
