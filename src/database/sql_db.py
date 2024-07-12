from langchain_community.utilities.sql_database import SQLDatabase
from urllib.parse import quote_plus

def bigquery(project, dataset, service_account_key_path, include_tables=None):
    return SQLDatabase.from_uri(f"bigquery://{project}/{dataset}?credentials_path={service_account_key_path}", include_tables=include_tables)


def mysql(db_host, db_user, db_password, db_name, include_tables=None):
    return SQLDatabase.from_uri(f"mysql+pymysql://{db_user}:{quote_plus(db_password)}@{db_host}/{db_name}", include_tables=include_tables)


def postgres(db_host, db_user, db_password, db_name, schema="public", include_tables=None):
    return SQLDatabase.from_uri(f"postgresql://{db_user}:{quote_plus(db_password)}@{db_host}/{db_name}", schema=schema, include_tables=include_tables)
