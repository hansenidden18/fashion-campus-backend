from sqlalchemy import create_engine, text
from datetime import datetime, timedelta
from flask import request
import jwt

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

def generate_jwt(payload: dict) -> str:
    expired = datetime.now() + timedelta(days=1)
    payload['exp'] = expired
    return jwt.encode(payload, 'doaibu', algorithm='HS256')

# def generate_admin_jwt(payload: dict) -> str:
#     expired = datetime.now() + timedelta(days=1)
#     payload['exp'] = expired
#     return jwt.encode(payload, 'doaibu', algorithm='HS256')


def jwt_verification(token: str) -> dict:
    decode_token = jwt.decode(token, 'doaibu', algorithms='HS256')
    return decode_token

def admin_token_checker(token):
    verif = jwt_verification(token)
    usercheck = run_query(f"SELECT * FROM users WHERE token='{token}' and admin=True")
    if "message" in verif:
        return {"error": "User token expired, please re-login"}, 403
    elif not usercheck:
        return {"error": "Unauthorized User"}, 401   

    
    
def user_token_checker(token):
    verif = jwt_verification(token)
    usercheck = run_query(f"SELECT * FROM users WHERE token='{token}' and admin=False")
    if "message" in verif:
        return {"error": "User token expired, please re-login"}, 403
    elif not usercheck:
        return {"error": "Unauthorized User"}, 401   
