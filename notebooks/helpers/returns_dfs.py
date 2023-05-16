import psycopg2
import os
import pandas as pd
from dotenv import load_dotenv, find_dotenv


class DBConnector:

    def __init__(self):
        load_dotenv(r'/db_creds.env')
        connection_string = os.getenv("SOURCE")
        self._connection = psycopg2.connect(connection_string)
        self._connection.autocommit = False
        self._tx_cursor = None

    @property
    def cursor(self):
        if self._tx_cursor is not None:
            cursor = self._tx_cursor
        else:
            cursor = self._connection.cursor()
        return cursor


db_connector = DBConnector()
