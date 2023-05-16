"""Portfolio Metrics queries."""


class Queries:
    """Portfolio Metrics queries class."""

    UPSERT = (
        "INSERT INTO portfolio_metrics ("
        "       factor, "
        "       timeframe, "
        "       mkt_cap_class, "
        "       top, "
        "       side, "
        "       cumulative_rtn, "
        "       ann_rtn, "
        "       ann_volatility, "
        "       ann_sharpe "
        ") VALUES %s "
        "ON CONFLICT (factor, timeframe, mkt_cap_class, top, side) DO "
        "UPDATE SET "
        "       factor=EXCLUDED.factor, "
        "       timeframe=EXCLUDED.timeframe, "
        "       mkt_cap_class=EXCLUDED.mkt_cap_class, "
        "       top=EXCLUDED.top, "
        "       side=EXCLUDED.side, "
        "       cumulative_rtn=EXCLUDED.cumulative_rtn, "
        "       ann_rtn=EXCLUDED.ann_rtn, "
        "       ann_volatility=EXCLUDED.ann_volatility, "
        "       ann_sharpe=EXCLUDED.ann_sharpe; "
    )