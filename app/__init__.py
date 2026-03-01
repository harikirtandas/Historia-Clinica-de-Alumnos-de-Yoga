from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config

db = SQLAlchemy()

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(Config)

    db.init_app(app)

    with app.app_context():
        from .models import alumno
        db.create_all()

    from .controllers.alumnos import alumnos_bp
    app.register_blueprint(alumnos_bp)

    return app
