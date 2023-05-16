from typing import Optional

import numpy as np


# PER YEAR
TIME_PERIODS = {
    'DAILY': 252,
    'WEEKLY': 52,
    'MONTHLY': 12,
}

# r is always a np array


def cumulative_return(r):
    return (1+r).prod()


def annualized_return(r, periods_per_year):
    compounded_growth = (1+r).prod()
    n_periods = r.shape[0]
    return compounded_growth**(periods_per_year/n_periods)-1


def annualized_volatility(r, periods_per_year):
    return r.std()*(periods_per_year**0.5)


def sharpe_ratio(r, annualized: bool = False, periods_per_year: Optional[int] = None):
    s_r = r.mean() / r.std()
    if annualized:
        ann_sharpe_ratio = s_r * np.sqrt(periods_per_year)
        return ann_sharpe_ratio
    else:
        return s_r


def run_stats(r, periods_per_year: int):
    return {
        'cumulative_return': cumulative_return(r),
        'ann_return': annualized_return(r, periods_per_year),
        'ann_volatility': annualized_volatility(r, periods_per_year),
        'ann_sharpe': sharpe_ratio(r, True, periods_per_year)
    }
