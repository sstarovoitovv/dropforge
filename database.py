import psycopg


def get_connection():
    return psycopg.connect()