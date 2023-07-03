"""Returns model."""

import logging
from typing import Dict, List, Optional, Tuple

from returns_metrics.model.metrics import Metrics
from returns_metrics.model.base import Modeling

logger = logging.getLogger(__name__)


class RegressionPortfolioMetrics(Modeling):
    """Returns record object class."""

    TIMEFRAME = "DAILY"

    model_type: str
    val_criterion: str
    rtn_type: str
    side: str

    metrics: Optional[Metrics] = None

    @classmethod
    def build_record(
        cls, key, returns: List[Tuple[Dict, float]]
    ) -> "RegressionPortfolioMetrics":
        """Builds Returns record object.

        Args:
            key: portfolio key.
            returns: portfolio returns.
        Returns:
            Returns record object.
        """
        res = cls()

        res.model_type = key[0]
        res.val_criterion = key[1]
        res.rtn_type = key[2]
        res.side = key[3]
        res.metrics = Metrics(returns, cls.TIMEFRAME)

        return res

    def as_tuple(self) -> Tuple:
        """Get tuple with object attributes.

        Returns:
            Tuple with object attributes.
        """
        return (
            self.model_type,
            self.val_criterion,
            self.rtn_type,
            self.side,
            self.metrics.cumulative_rtn,
            self.metrics.cumulative_net_rtn,
            self.metrics.ann_rtn,
            self.metrics.ann_vol,
            self.metrics.ann_sharpe,
            self.metrics.max_drawdown,
        )
