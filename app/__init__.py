from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from decouple import Config, RepositoryEnv
from datetime import timedelta
from werkzeug.middleware.proxy_fix import ProxyFix
from flask_cors import CORS

import os

from app.utils.debugging_utils import printn

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    
    CORS(app, supports_credentials=True, origins=["https://nulldaan.netlify.app"])
    
    app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

    env = os.environ.get("ENVIRONMENT", "development")
    env_file = f".env.{env}"
    config_env = Config(RepositoryEnv(env_file))

    app.config['SECRET_KEY'] = config_env('SECRET_KEY')
    app.config['SQLALCHEMY_DATABASE_URI'] = config_env('SQLALCHEMY_DATABASE_URI')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = config_env('SQLALCHEMY_TRACK_MODIFICATIONS', cast=bool)
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=7)
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_pre_ping': True, 'pool_recycle': 250}

    print("DB URI:", app.config["SQLALCHEMY_DATABASE_URI"])

    if env == "production":
        printn("-------------- MODO PRODUCCIÓN. NO EJECUTAR TESTS!! --------------")

    db.init_app(app)
    Migrate(app, db)

    from . import models
    from .routes import register_routes

    register_routes(app)
  
    return app
