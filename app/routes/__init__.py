from .auth_routes import auth_bp
from .debug_routes import debug_bp


def register_routes(app):    
    app.register_blueprint(auth_bp, url_prefix='')
    app.register_blueprint(debug_bp, url_prefix='')
    