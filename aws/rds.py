import logging
import sys

import pandas as pd
import psycopg2
from sqlalchemy import URL, create_engine
from sqlalchemy.orm import sessionmaker

# Initialising the logger
LOGGER = logging.getLogger(__name__)


def connect_to_rds_with_sqlalchemy(rds_host: str, rds_port: str, rds_username: str, rds_user_pwd: str,
                                   rds_db_name: str):
    """
    Connecting to RDS with SQLAlchemy. This creates a connection engine.
    :param rds_host:
    :param rds_port:
    :param rds_username:
    :param rds_user_pwd:
    :param rds_db_name:
    :return:
    """

    try:
        url_object = URL.create(
            "postgresql+psycopg2",
            username=rds_username,
            password=rds_user_pwd,  # plain (unescaped) text
            host=rds_host,
            database=rds_db_name,
            port=int(rds_port)
        )
        engine = create_engine(url_object, echo=False)

        # Create connection to DB using engine
        conn = engine.connect()

        # Create session
        session = sessionmaker(bind=engine)
        session = session()

        return conn, engine, session

    except Exception as e:
        LOGGER.error(f"ERROR: Could not connect to Postgres instance. \n {e}",
                     exc_info=True, stack_info=True)
        sys.exit(1)


def connect_to_rds(rds_host: str, rds_port: str, rds_username: str, rds_user_pwd: str, rds_db_name: str):
    """
    Establish connection with RDS

    :param rds_host: name of DB host
    :param rds_port: port number
    :param rds_username: DB username
    :param rds_user_pwd: DB password
    :param rds_db_name: Name of the database
    :return: cursor or pointer to DB
    :rtype: psycopg2.extensions.connection
    """
    try:
        conn_string = (f"host={rds_host} user={rds_username} password={rds_user_pwd} dbname={rds_db_name} "
                       f"port={rds_port}")
        connection = psycopg2.connect(conn_string)
        cursor = connection.cursor()
        LOGGER.debug("SUCCESS: Connection to RDS Postgres instance succeeded")
        return connection, cursor

    except Exception as e:
        LOGGER.error(f"ERROR: Could not connect to Postgres instance. \n {e}",
                     exc_info=True, stack_info=True)
        sys.exit(1)


def read_data_from_rds(cursor, query):
    """
    Read table from database

    :param cursor: DB pointer
    :type: psycopg2.extensions.connection
    :param query: SQL query to be executed
    :type query: str
    :return: fetched values from DB
    :rtype: list
    """
    cursor.execute(query)
    vals = cursor.fetchall()
    return vals


def read_table_from_rds(query, engine):
    return pd.read_sql_query(query, con=engine)
