from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from decouple import Config, RepositoryEnv
from datetime import timedelta
from werkzeug.middleware.proxy_fix import ProxyFix
from flask_cors import CORS
from flask_jwt_extended import JWTManager

import os

from app.utils.debugging_utils import printn

db = SQLAlchemy()
jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    
    env = os.environ.get("ENVIRONMENT", "development")
    env_file = f".env.{env}"
    config_env = Config(RepositoryEnv(env_file))

    if env == 'development':

        CORS(app, origins="http://localhost:4321", supports_credentials=True)
        app.debug=True

    else:
        CORS(app, 
            origins=[
            "https://nulldaan.netlify.app", 
            "https://nulldaanfix.netlify.app", 
            "http://localhost:4321"
            ],
            supports_credentials=True,
            methods=["GET","POST","OPTIONS"],
            allow_headers=["Content-Type","Authorization"])
        app.debug=False
        
    app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

    app.config['SECRET_KEY'] = config_env('SECRET_KEY')
    app.config['SQLALCHEMY_DATABASE_URI'] = config_env('SQLALCHEMY_DATABASE_URI')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = config_env('SQLALCHEMY_TRACK_MODIFICATIONS', cast=bool)
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_pre_ping': True, 'pool_recycle': 250}

    app.config["JWT_SECRET_KEY"] = config_env("JWT_SECRET_KEY")
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(minutes=15)
    app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=7)

    print("DB URI:", app.config["SQLALCHEMY_DATABASE_URI"])

    if env == "production":
        printn("-------------- MODO PRODUCCIÓN. NO EJECUTAR TESTS!! --------------")

    db.init_app(app)
    Migrate(app, db)

    from .routes import register_routes

    register_routes(app)
    
    jwt.init_app(app)

    return app
