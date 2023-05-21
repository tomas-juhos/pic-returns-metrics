from math import sqrt
from typing import List, Optional, Tuple

import numpy as np


class Metrics:
    # PER YEAR
    TIME_PERIODS = {
        'DAILY': 252,
        'WEEKLY': 52,
        'MONTHLY': 12,
    }

    def __init__(self, portfolio_returns: Tuple[set, List], timeframe: str):
        self.periods_per_year = self.TIME_PERIODS[timeframe]

        self.portfolio_returns = portfolio_returns
        self.returns_list = np.array([r[1] for r in portfolio_returns if r[1] is not None])
        self.net_returns_list = self.net_returns()

        self.cumulative_rtn = self.cumulative_returns(self.returns_list)[-1]
        self.cumulative_net_rtn = self.cumulative_returns(self.net_returns_list)[-1]

        self.ann_rtn = self.annualized_return()
        self.ann_vol = self.annualized_volatility()

        self.sharpe = self.sharpe_ratio()
        self.ann_sharpe = self.ann_sharpe_ratio()

        self.max_drawdown = self.maximum_drawdown()

    @staticmethod
    def cumulative_returns(rtn_list) -> List:
        res = []
        temp_rtn = 1
        for rtn in rtn_list:
            temp_rtn = temp_rtn * (1 + rtn)
            res.append(temp_rtn - 1)
        return res

    def net_returns(self):
        fee = 0.0005  # 5 basis pts fee
        prev_long = None
        prev_short = None

        res = []
        for portfolio_rtn in self.portfolio_returns:
            long = portfolio_rtn[0]['LONG']
            short = portfolio_rtn[0]['SHORT']
            rtn = portfolio_rtn[1] if portfolio_rtn[1] else 0

            if not prev_long and long:
                turnover_long = 1
            elif prev_long and not long:
                turnover_long = 1
            elif prev_long and long:
                turnover_long = len(set(long).symmetric_difference(prev_long)) / len(long)
            else:
                turnover_long = 0

            if not prev_short and short:
                turnover_short = 1
            elif prev_short and not short:
                turnover_short = 1
            elif prev_short and short:
                turnover_short = len(set(short).symmetric_difference(prev_short)) / len(short)
            else:
                turnover_short = 0

            rtn = float(rtn) - ((turnover_long+turnover_short) * fee)

            res.append(rtn)

            prev_long = long
            prev_short = short

        return np.array(res)

    def annualized_return(self):
        compounded_growth = self.cumulative_net_rtn + 1
        n_periods = self.net_returns_list.shape[0]
        if compounded_growth < 0:
            return -(abs(compounded_growth) ** (self.periods_per_year / n_periods) - 1)
        else:
            return (compounded_growth ** (self.periods_per_year / n_periods)) - 1

    def annualized_volatility(self):
        return self.net_returns_list.std() * sqrt(self.periods_per_year)

    def sharpe_ratio(self):
        rtn = self.net_returns_list.mean()
        vol = self.net_returns_list.std()

        return rtn / vol

    def ann_sharpe_ratio(self):
        rtn = self.ann_rtn
        vol = self.ann_vol

        return rtn / vol

    def maximum_drawdown(self):
        peak = 0
        mdd = 0
        returns = self.cumulative_returns(self.net_returns_list)
        for rtn in returns:
            rtn += 1
            if rtn > peak:
                peak = rtn

            if rtn < peak:
                drawdown = (rtn - peak) / peak
                if drawdown < mdd:
                    mdd = drawdown
        return mdd

    def as_tuple(self) -> Tuple:
        """Get tuple with object attributes.

        Returns:
            Tuple with object attributes.
        """
        return (
            self.cumulative_rtn,
            self.cumulative_net_rtn,
            self.ann_rtn,
            self.ann_vol,
            self.ann_sharpe,
            self.max_drawdown
        )

