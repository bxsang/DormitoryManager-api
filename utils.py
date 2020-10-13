from flask import request
import jwt
from config import db

def get_jwt():
    try:
        encoded_token = request.headers.get('Authorization', type=str).split(' ')[1]
        return jwt.decode(encoded_token, 'secret', algorithms=['HS256'])
    except Exception:
        return ''

def return_auth_err():
    return {
        'success': False,
        'message': 'Khong lay duoc role'
    }

def return_unauthorized():
    return {
        'success': False,
        'message': 'Ban ko co quyen thuc hien hanh dong nay'
    }

def insert_db(obj):
    db.session.add(obj)
    try:
        db.session.commit()
    except Exception:
        db.session.rollback()
        raise
