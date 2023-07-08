CREATE TABLE regression_portfolio_results
(
    universe_constr             VARCHAR(50),
    model_type                  VARCHAR(20),
    val_criterion               VARCHAR(20),
    rtn_type                    VARCHAR(20),
    side                        VARCHAR(10),

    cumulative_rtn              DECIMAL(10,4),
    cumulative_net_rtn          DECIMAL(10,4),
    ann_rtn                     DECIMAL(10,4),
    ann_vol                     DECIMAL(10,4),
    ann_sharpe                  DECIMAL(10,4),
    max_drawdown                DECIMAL(10,4),

    PRIMARY KEY (universe_constr, model_type, val_criterion, rtn_type, side)
);