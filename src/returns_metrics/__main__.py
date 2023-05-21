import logging
from sys import stdout
import os
from typing import Dict, List, Union

import returns_metrics.model as model
import returns_metrics.queries as queries
from returns_metrics.persistence import source, target

logging.basicConfig(
    level=os.environ.get("LOG_LEVEL", "INFO").upper(),
    format="%(asctime)s %(levelname)s [%(filename)s:%(lineno)d]: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    stream=stdout,
)

logger = logging.getLogger(__name__)


class Loader:
    """Loader class for portfolio metrics."""

    def __init__(self) -> None:
        self.source = source.Source(os.environ.get("SOURCE"))
        self.target = target.Target(os.environ.get("TARGET"))

    def run(self):
        portfolio_keys = self.source.fetch_keys()
        records = []
        for portfolio_key in portfolio_keys:
            portfolio_key = list(portfolio_key)
            raw_records = self.source.fetch_returns(portfolio_key)
            portfolio_returns: Dict[str, List] = {
                "LONG": [({'LONG': r[9]['LONG'], 'SHORT': None}, r[5]) for r in raw_records],
                "SHORT": [({'LONG': None, 'SHORT': r[9]['SHORT']}, r[6]) for r in raw_records],
                "NEUTRAL": [(r[9], r[7]) for r in raw_records]
            }

            for k, v in portfolio_returns.items():
                key = portfolio_key + [k]
                record = model.PortfolioMetrics.build_record(key, v).as_tuple()
                records.append(record)

        self.target.execute(queries.PortfolioMetricsQueries.UPSERT, records)
        self.target.commit_transaction()


loader = Loader()
loader.run()
