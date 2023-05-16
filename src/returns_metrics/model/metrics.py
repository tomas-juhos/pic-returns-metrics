from decimal import Decimal
from typing import List, Optional, Tuple

import numpy as np

# PER YEAR
TIME_PERIODS = {
    'DAILY': 252,
    'WEEKLY': 52,
    'MONTHLY': 12,
}


class Metrics:

    def __init__(self, returns: List, timeframe: str):
        periods_per_year = TIME_PERIODS[timeframe]

        self.returns = np.array(returns)
        self.cumulative_rtn = self.cumulative_return()
        self.ann_rtn = self.annualized_return(periods_per_year)
        self.ann_volatility = self.annualized_volatility(periods_per_year)
        self.ann_sharpe = self.sharpe_ratio(True, periods_per_year)

    def cumulative_return(self):
        rtn = (1 + self.returns).prod() - 1
        return rtn

    def annualized_return(self, periods_per_year):
        compounded_growth = self.cumulative_return()
        n_periods = self.returns.shape[0]
        if compounded_growth < 0:
            return -(abs(float(compounded_growth)) ** (periods_per_year / n_periods))
        else:
            return float(compounded_growth) ** (periods_per_year / n_periods)

    def annualized_volatility(self, periods_per_year):
        return self.returns.std() * (Decimal(periods_per_year) ** Decimal(0.5))

    def sharpe_ratio(self, annualized: bool = False, periods_per_year: Optional[int] = None):
        s_r = self.returns.mean() / self.returns.std()
        if annualized:
            ann_sharpe_ratio = s_r * Decimal(np.sqrt(periods_per_year))
            return ann_sharpe_ratio
        else:
            return s_r

    def as_tuple(self) -> Tuple:
        """Get tuple with object attributes.

        Returns:
            Tuple with object attributes.
        """
        return (
            self.cumulative_rtn,
            self.ann_rtn,
            self.ann_volatility,
            self.ann_sharpe,
        )

