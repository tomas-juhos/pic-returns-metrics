from pathlib import Path
import os
import pandas as pd


class Dataframes:
    def __init__(self):
        self.regr_portfolio_returns = self.get_pit_rtn('regr_strat', 'regression_bottom_net')
        self.regr_portfolio_cumreturns = self.get_cum_rtn('regr_strat', 'regression_bottom_net')

        self.regr_benchmark_returns = self.get_pit_rtn('regr_bench', 'regression_benchmark_net')
        self.regr_benchmark_cumreturns = self.get_cum_rtn('regr_bench', 'regression_benchmark_net')

        self.gbm_portfolio_returns = self.get_pit_rtn('gbm_strat', 'gbm_bottom_net')
        self.gbm_portfolio_cumreturns = self.get_cum_rtn('gbm_strat', 'gbm_bottom_net')

        self.gbm_benchmark_returns = self.get_pit_rtn('gbm_bench', 'gbm_benchmark_net')
        self.gbm_benchmark_cumreturns = self.get_cum_rtn('gbm_bench', 'gbm_benchmark_net')

        self.regr_calendar_returns = self.read_file('regr_calendar')[
            ['year', 'strategy', 'benchmark']]
        self.regr_calendar_returns.columns = ['Year', 'Strategy (%)', 'Benchmark (%)']
        self.gbm_calendar_returns = self.read_file('gbm_calendar')[
            ['year', 'strategy', 'benchmark']]
        self.gbm_calendar_returns.columns = ['Year', 'Strategy (%)', 'Benchmark (%)']

    def get_pit_rtn(self, rtn_file, net_file):
        returns = self.read_file(rtn_file)
        returns.columns = ['Date', 'Rtn']
        returns['Date'] = pd.to_datetime(returns['Date'])
        returns.set_index('Date', inplace=True)
        net = self.read_file(net_file)
        returns.insert(1, 'Net_Rtn', list(net['Net_Rtn'])[1:])

        return returns

    def get_cum_rtn(self, rtn_file, net_file):
        returns = self.read_file(rtn_file)
        returns.columns = ['Date', 'Rtn']
        returns['Date'] = pd.to_datetime(returns['Date'])
        returns.set_index('Date', inplace=True)
        cumreturns = (1 + returns).cumprod() - 1
        net = self.read_file(net_file)
        cumnet = (1 + net).cumprod() - 1
        cumnet.columns = ['Net_Rtn']
        cumreturns.insert(1, 'Net_Rtn', list(cumnet['Net_Rtn'])[1:])

        return cumreturns

    @staticmethod
    def read_file(file_name: str) -> pd.DataFrame:
        """Returns dataframe with data from file with the provided file name."""
        local_data_path = os.path.join(Path(os.path.abspath(os.curdir)), 'data')
        df = pd.read_csv(os.path.join(local_data_path, f'{file_name}.csv'), low_memory=False)
        return df
