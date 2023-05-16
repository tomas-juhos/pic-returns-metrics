CREATE TABLE portfolio_metrics
(
    factor              VARCHAR(100),
    timeframe           VARCHAR(20),
    mkt_cap_class       VARCHAR(20),
    top                 INTEGER,
    side                VARCHAR(10),

    cumulative_rtn      DECIMAL(25,15),
    ann_rtn             DECIMAL(25,15),
    ann_volatility      DECIMAL(25,15),
    ann_sharpe          DECIMAL(25,15),

    PRIMARY KEY (factor, timeframe, mkt_cap_class, top, side)
);