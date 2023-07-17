import helpers.plotting as plt
from helpers.dataframes import Dataframes


dfs = Dataframes()
plt.portfolio_returns(
    portfolio=dfs.regr_portfolio_cumreturns,
    benchmark=dfs.regr_benchmark_cumreturns,
    file_name='regr_top_strat'
)
plt.portfolio_returns(
    portfolio=dfs.gbm_portfolio_cumreturns,
    benchmark=dfs.gbm_benchmark_cumreturns,
    file_name='gbm_top_strat'
)

plt.average_daily_return(
    df=dfs.regr_portfolio_returns,
    file_name='regr_daily_rtn'
)
plt.average_daily_return(
    df=dfs.gbm_portfolio_returns,
    file_name='gbm_daily_rtn'
)

print(dfs.regr_portfolio_returns)
print(dfs.regr_benchmark_returns)
plt.histogram(
    portfolio=dfs.regr_portfolio_returns,
    benchmark=dfs.regr_benchmark_returns,
    file_name='regr_top_strat_dist',
    strat_bins=20
)
print(dfs.gbm_portfolio_returns)
print(dfs.gbm_benchmark_returns)
plt.histogram(
    portfolio=dfs.gbm_portfolio_returns,
    benchmark=dfs.gbm_benchmark_returns,
    file_name='gbm_top_strat_dist',
    strat_bins=40
)

plt.calendar_returns(
    df=dfs.regr_calendar_returns,
    file_name='regr_top_strat_calendar'
)
plt.calendar_returns(
    df=dfs.gbm_calendar_returns,
    file_name='gbm_top_strat_calendar'
)
