import pytest
from flask import Flask

from app.database import db
from app.routes.car_route import cars_bp


@pytest.fixture
def app():
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    db.init_app(app)
    app.register_blueprint(cars_bp)
    return app


@pytest.fixture
def client(app):
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            yield client
