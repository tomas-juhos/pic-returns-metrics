CREATE TABLE portfolio_metrics
(
    factor                      VARCHAR(100),
    timeframe                   VARCHAR(20),
    mkt_cap_class               VARCHAR(20),
    top                         INTEGER,
    side                        VARCHAR(10),

    cumulative_rtn              DECIMAL(10,4),
    cumulative_net_rtn          DECIMAL(10,4),
    ann_rtn                     DECIMAL(10,4),
    ann_vol                     DECIMAL(10,4),
    sharpe                      DECIMAL(10,4),
    ann_sharpe                  DECIMAL(10,4),
    max_drawdown                DECIMAL(10,4),

    PRIMARY KEY (factor, timeframe, mkt_cap_class, top, side)
);