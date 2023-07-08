"""Portfolio Metrics queries."""


class Queries:
    """Portfolio Metrics queries class."""

    UPSERT = (
        "INSERT INTO factor_portfolio_results ("
        "       factor, "
        "       timeframe, "
        "       mkt_cap_class, "
        "       top, "
        "       side, "
        "       cumulative_rtn, "
        "       cumulative_net_rtn, "
        "       ann_rtn, "
        "       ann_vol, "
        "       ann_sharpe, "
        "       max_drawdown "
        ") VALUES %s "
        "ON CONFLICT (factor, timeframe, mkt_cap_class, top, side) DO "
        "UPDATE SET "
        "       factor=EXCLUDED.factor, "
        "       timeframe=EXCLUDED.timeframe, "
        "       mkt_cap_class=EXCLUDED.mkt_cap_class, "
        "       top=EXCLUDED.top, "
        "       side=EXCLUDED.side, "
        "       cumulative_rtn=EXCLUDED.cumulative_rtn, "
        "       cumulative_net_rtn=EXCLUDED.cumulative_net_rtn, "
        "       ann_rtn=EXCLUDED.ann_rtn, "
        "       ann_vol=EXCLUDED.ann_vol, "
        "       ann_sharpe=EXCLUDED.ann_sharpe, "
        "       max_drawdown=EXCLUDED.max_drawdown; "
    )
