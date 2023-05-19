from math import sqrt
from scipy.stats import chi
from ab_testing.testers.tester import Tester


class ChiSquareTester(Tester):
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
        ...
