from contextlib import contextmanager
from psycopg2.pool import SimpleConnectionPool

env = 'development'
database_host = 'localhost'
database = 'horserankerlocal'
database_user = 'claytonwinterbotham'
database_password = 'claytonwinterbotham'
production_database_host = ''
production_database = ''
production_database_user = ''
production_database_password = ''

database_host = production_database_host if env == 'production' \
    else database_host
database = production_database if env == 'production' \
    else database
database_user = production_database_user if env == 'production' \
    else database_user
database_password = production_database_password if env == 'production' \
    else database_password

pool = SimpleConnectionPool(
    minconn=1,
    maxconn=20,
    host=database_host,
    database=database,
    user=database_user,
    password=database_password
)


@contextmanager
def get_connection():
    connection = pool.getconn()

    try:
        yield connection
    finally:
        pool.putconn(connection)
