from sqlalchemy import create_engine, text
from datetime import datetime, timedelta
import jwt

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

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

def find(statement, params = None):
    engine = get_engine()
    with engine.connect() as conn:
        return [dict(row) for row in conn.execute(text(statement), params)]

def first(statement, params = None):
    row = find(statement, params)
    if len(row) == 0:
        return None
    return row[0]

def generate_jwt(payload: dict) -> str:
    expired = datetime.now() + timedelta(days=1)
    payload['exp'] = expired
    return jwt.encode(payload, 'doaibu', algorithm='HS256')

def jwt_verification(token: str) -> dict:
    try:
        decode_token = jwt.decode(token, 'doaibu', algorithm='HS256')
        if decode_token['exp'] < datetime.now():
            return {"message":"Token expired"}
        return decode_token
    except jwt.ExpiredSignatureError:
        return {"message":"Token expired"}
    except jwt.InvalidTokenError:
        raise Exception("Invalid Token")