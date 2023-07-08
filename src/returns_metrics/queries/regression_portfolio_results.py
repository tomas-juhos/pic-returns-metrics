"""Portfolio Metrics queries."""


class Queries:
    """Regression Portfolio Metrics queries class."""

    UPSERT = (
        "INSERT INTO regression_portfolio_results ("
        "       universe_constr, "
        "       model_type, "
        "       val_criterion, "
        "       rtn_type, "
        "       side, "
        "       cumulative_rtn, "
        "       cumulative_net_rtn, "
        "       ann_rtn, "
        "       ann_vol, "
        "       ann_sharpe, "
        "       max_drawdown "
        ") VALUES %s "
        "ON CONFLICT (universe_constr, model_type, val_criterion, rtn_type, side) DO "
        "UPDATE SET "
        "       universe_constr=EXCLUDED.universe_constr, "
        "       model_type=EXCLUDED.model_type, "
        "       val_criterion=EXCLUDED.val_criterion, "
        "       rtn_type=EXCLUDED.rtn_type, "
        "       side=EXCLUDED.side, "
        "       cumulative_rtn=EXCLUDED.cumulative_rtn, "
        "       cumulative_net_rtn=EXCLUDED.cumulative_net_rtn, "
        "       ann_rtn=EXCLUDED.ann_rtn, "
        "       ann_vol=EXCLUDED.ann_vol, "
        "       ann_sharpe=EXCLUDED.ann_sharpe, "
        "       max_drawdown=EXCLUDED.max_drawdown; "
    )
