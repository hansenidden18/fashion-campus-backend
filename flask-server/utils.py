from sqlalchemy import create_engine, text


def get_engine():
    """Creating MySQL Engine to interact"""
    return create_engine("postgresql+psycopg2://posgres:user@postgres:5432/python_docker", future=True)


def run_query(query, commit: bool = False):
    """Runs a query against the given MySQL database.

    Args:
        commit: if True, commit any data-modification query (INSERT, UPDATE, DELETE)
    """
    engine = get_engine()
    if isinstance(query, str):
        query = text(query)

    with engine.connect() as conn:
        if commit:
            conn.execute(query)
            conn.commit()
        else:
            return [dict(row) for row in conn.execute(query)]