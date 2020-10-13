from flask import Flask
from flask_cors import CORS
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_limiter import Limiter
from flask_limiter.util import get_ipaddr as get_remote_address
from pathlib import Path
from dotenv import load_dotenv
import os

class LimitConfig:
    # RATELIMIT_DEFAULT = "1/3second"
    RATELIMIT_DEFAULT = "50/minute"
    RATELIMIT_HEADERS_ENABLED = True
    RATELIMIT_IN_MEMORY_FALLBACK = "1/2second"
    RATELIMIT_KEY_PREFIX = "test-limiter"
    RATELIMIT_SWALLOW_ERRORS = True

app = Flask(__name__)
app.config.from_object(LimitConfig)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
CORS(app)
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)
SERVER = os.getenv("DB_SERVER")
DB_NAME = os.getenv("DB_NAME")
USER = os.getenv("DB_USER")
PASS = os.getenv("DB_PASS")
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://"+USER+":"+PASS+"@"+SERVER+"/"+DB_NAME
sql = SQLAlchemy(app)
ma = Marshmallow(app)
api = Api(app)
limiter = Limiter(app, key_func=get_remote_address)
