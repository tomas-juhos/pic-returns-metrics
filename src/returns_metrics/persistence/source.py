"""Source."""

from typing import List, Tuple

import psycopg2
import psycopg2.extensions


class Source:
    """Source class."""

    def __init__(self, connection_string: str) -> None:
        self._connection_string = connection_string
        self._connection = psycopg2.connect(connection_string)
        self._connection.autocommit = False
        self._tx_cursor = None

    @property
    def cursor(self) -> psycopg2.extensions.cursor:
        """Generate cursor.

        Returns:
            Cursor.
        """
        if self._tx_cursor is not None:
            cursor = self._tx_cursor
        else:
            cursor = self._connection.cursor()

        return cursor

    def disconnect(self) -> None:
        """Disconnect from database."""
        self._connection.close()

    def fetch_keys(self):
        """Fetches U.S. gvkeys."""
        cursor = self.cursor
        query = "SELECT DISTINCT factor, timeframe, mkt_cap_class, top " "FROM factor_returns; "
        cursor.execute(query)
        keys = cursor.fetchall()

        return keys if keys else None

    def fetch_returns(self, key) -> List[Tuple]:
        """Fetch records with the provided keys.

        Args:
            key: key of portfolio.

        Returns:
            List of records with matching keys.
        """
        cursor = self.cursor
        query = (
            "SELECT * "
            "FROM factor_returns "
            "WHERE factor = %s "
            "AND timeframe = %s "
            "AND mkt_cap_class = %s "
            "AND top = %s "
            "AND datadate <= '2019-12-31' "
            "ORDER BY datadate; "
        )

        cursor.execute(query, (key[0], key[1], key[2], key[3]))
        res = cursor.fetchall()

        return res if res else None
