"""Returns model."""

import logging
from typing import Optional, Tuple

from returns_metrics.model.metrics import Metrics
from returns_metrics.model.base import Modeling

logger = logging.getLogger(__name__)


class PortfolioMetrics(Modeling):
    """Returns record object class."""

    factor: str
    timeframe: str
    mkt_cap_class: str
    top: int
    side: str

    metrics: Optional[Metrics] = None

    @classmethod
    def build_record(cls, key,  returns) -> "PortfolioMetrics":
        """Builds Returns record object.

        Args:
            key: portfolio key.
            returns: portfolio returns.
        Returns:
            Returns record object.
        """
        res = cls()

        res.factor = key[0]
        res.timeframe = key[1]
        res.mkt_cap_class = key[2]
        res.top = key[3]
        res.side = key[4]
        res.metrics = Metrics(returns, res.timeframe)

        return res

    def as_tuple(self) -> Tuple:
        """Get tuple with object attributes.

        Returns:
            Tuple with object attributes.
        """
        return (
            self.factor,
            self.timeframe,
            self.mkt_cap_class,
            self.top,
            self.side,
            self.metrics.cumulative_rtn,
            self.metrics.cumulative_net_rtn,
            self.metrics.ann_rtn,
            self.metrics.ann_vol,
            self.metrics.sharpe,
            self.metrics.ann_sharpe,
            self.metrics.max_drawdown
        )