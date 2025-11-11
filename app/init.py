from flask import Flask
from .database import init_db

def create_app():
    app = Flask(__name__)
    app.config.from_mapping(
        DATABASE_URL='postgresql://user:password@db:5432/microservice'
    )
    
    init_db(app)
    
    from .routes import bp
    app.register_blueprint(bp)
    
    return app