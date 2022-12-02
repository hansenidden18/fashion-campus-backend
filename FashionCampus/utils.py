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
    return jwt.encode(payload, 'doaibu', 'HS256')

def jwt_verification(token: str) -> dict:
    try:
        decode_token = jwt.decode(token, 'doaibu', algorithms='HS256')
        return decode_token
    except:
        return {"message":"Unauthorized user"}
    
def productid_checker(id):
    return run_query(f"SELECT * FROM product WHERE id={id}")

def admin_token_checker(token):
    try:
        verif = jwt_verification(token)
        usercheck = run_query(f"SELECT * FROM users WHERE email='{verif['email']}' and type='seller'")
        if not usercheck:
            return False
        return True
    except:
        return False

def user_token_checker(token):
    verif = jwt_verification(token)
    usercheck = run_query(f"SELECT * FROM users WHERE token='{token}' and type='buyer'")
    if "message" in verif:
        return {"error": "User token expired, please re-login"}, 403
    elif not usercheck:
        return {"error": "Unauthorized User"}, 401   
