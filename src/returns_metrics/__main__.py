from datetime import datetime
import logging
from sys import stdout
import os
from typing import Dict, List, Tuple

import returns_metrics.model as model
import returns_metrics.queries as queries
from returns_metrics.persistence import source, target

import pandas as pd

logging.basicConfig(
    level="INFO",
    format="%(asctime)s %(levelname)s [%(filename)s:%(lineno)d]: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    stream=stdout,
)

logger = logging.getLogger(__name__)


class FactorPortfolioLoader:
    """Loader class for portfolio metrics."""

    def __init__(self) -> None:
        self.source = source.Source(os.environ.get("SOURCE"))
        self.target = target.Target(os.environ.get("TARGET"))

    def run(self):
        portfolio_keys = self.source.fetch_factor_keys()
        records = []
        for portfolio_key in portfolio_keys:
            portfolio_key = list(portfolio_key)
            raw_records = self.source.fetch_factor_returns(portfolio_key)
            portfolio_returns: Dict[str, List[Tuple[Dict, float]]] = {
                "LONG": [
                    ({"LONG": r[9]["LONG"], "SHORT": None}, r[5]) for r in raw_records
                ],
                "SHORT": [
                    ({"LONG": None, "SHORT": r[9]["SHORT"]}, r[6]) for r in raw_records
                ],
                "NEUTRAL": [(r[9], r[7]) for r in raw_records],
            }

            for k, v in portfolio_returns.items():
                key = portfolio_key + [k]
                record = model.FactorPortfolioResults.build_record(key, v).as_tuple()
                records.append(record)

        self.target.execute(queries.PortfolioMetricsQueries.UPSERT, records)
        self.target.commit_transaction()


class RegressionPortfolioLoader:
    """Loader class for portfolio metrics."""

    MODEL_TYPES = ["REGRESSION", "GBM"]
    UNIVERSE_CONSTRAINTS = ["LOAN_RATE_AVG", "SHORT_INTEREST"]
    VALIDATION_CRITERIA = ["MSE", "DIR_ACC", "RTN_BOTTOM", "RTN_WEIGHTED"]
    RTN_TYPES = ["BOTTOM", "WEIGHTED", "RANDOM", "BENCHMARK"]

    def __init__(self) -> None:
        self.source = source.Source(os.environ.get("SOURCE"))
        self.target = target.Target(os.environ.get("TARGET"))

    def run_all(self):
        for model_type in self.MODEL_TYPES:
            self.run(model_type)

    def run(self, model_type, save_best_strats_csv=False):
        res = []
        for universe_constr in self.UNIVERSE_CONSTRAINTS:
            for val_criterion in self.VALIDATION_CRITERIA:
                for rtn_type in self.RTN_TYPES:
                    raw_records = self.source.fetch_model_returns(
                        model=model_type.lower(),
                        universe_constr=universe_constr.upper(),
                        val_criterion=val_criterion.upper(),
                    )
                    if not raw_records:
                        logger.info(f"No available records for {universe_constr}|{val_criterion}|{rtn_type}")
                    if model_type == "REGRESSION":
                        records = [
                            model.RegressionMetrics.build_record(r) for r in raw_records
                        ]
                    elif model_type == "GBM":
                        records = [
                            model.GBMMetrics.build_record(r) for r in raw_records
                        ]
                    else:
                        logger.warning("No valid model type provided (regression/gbm).")
                        return
                    if rtn_type == "benchmark":
                        raw_gvkeys = self.source.fetch_chosen_gvkeys(
                            model=model_type.lower(),
                            universe_constr=universe_constr.upper(),
                            val_criterion=val_criterion.upper(),
                        )
                    else:
                        raw_gvkeys = self.source.fetch_chosen_gvkeys(
                            model=model_type.lower(),
                            universe_constr=universe_constr.upper(),
                            val_criterion=val_criterion.upper(),
                        )

                    gvkeys_dict = self.group_gvkeys_by_date(raw_gvkeys)
                    key = [
                        universe_constr.upper(),
                        model_type.upper(),
                        val_criterion.upper(),
                        rtn_type.upper(),
                        "SHORT",
                    ]
                    portfolio_rtn: List[Tuple[Dict, float]] = []
                    for r in records:
                        portfolio = self.get_porfolio_gvkeys(
                            r.testing_start, gvkeys_dict
                        )
                        # GVKEYS, RETURN
                        # SYMMETRIC RETURNS BECAUSE ALWAYS SHORT
                        portfolio_rtn.append(
                            (portfolio, -float(getattr(r, f"rtn_{rtn_type.lower()}")))
                        )
                    record = model.RegressionPortfolioResults.build_record(
                            key, portfolio_rtn
                        )

                    if save_best_strats_csv:
                        self.save_best_strats_data(key, record)

                    res.append(record.as_tuple())

            self.target.execute(queries.RegressionPortfolioMetricsQueries.UPSERT, res)
            self.target.commit_transaction()

    @staticmethod
    def save_best_strats_data(key, record):
        # SAVES CSV WITH THE BEST STRATEGIES BOTTOM AND BENCHMARK NET RETURN
        if key[0] == 'SHORT_INTEREST' and key[2] == 'DIR_ACC' and key[3] in ['BOTTOM', 'BENCHMARK']:
            net_rtn = record.metrics.net_returns_list
            net_rtn_df = pd.DataFrame(net_rtn, columns=['Net_Rtn'])
            net_rtn_df.to_csv(f'{key[1].lower()}_{key[3].lower()}_net.csv', index=False)

    @staticmethod
    def get_porfolio_gvkeys(d, gvkeys_dict):
        if d in gvkeys_dict.keys():
            res = {"LONG": [], "SHORT": gvkeys_dict[d]}
        else:
            res = {"LONG": [], "SHORT": []}
        return res

    @staticmethod
    def group_gvkeys_by_date(raw_keys: List[Tuple[datetime, int]]):
        gvkeys_dict = {}
        for k in raw_keys:
            if k[0].date() in gvkeys_dict.keys():
                gvkeys_dict[k[0].date()].append(k[1])
            else:
                gvkeys_dict[k[0].date()] = [k[1]]
        return gvkeys_dict


class PortfolioResultsLoader:
    factor_portofolio_loader = FactorPortfolioLoader()
    regression_portfolio_loader = RegressionPortfolioLoader()

    def factor(self):
        self.factor_portofolio_loader.run()

    def regression(self, model_type):
        self.regression_portfolio_loader.run(model_type)

    def all_regression(self):
        self.regression_portfolio_loader.run_all()


portfolio_results = PortfolioResultsLoader()
portfolio_results.all_regression()
