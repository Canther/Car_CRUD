import os
import click
from dotenv import load_dotenv
from flask import Flask
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_smorest import Api

import app.routes.homepage_route

import app.routes.car_route
from app.database import db
import app.database

from app.routes.car_route import cars_bp
from app.routes.homepage_route import home_bp

load_dotenv()

app = Flask(__name__)
db_path = os.path.join(os.path.dirname(__file__), os.environ['DATABASE_URL'])
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['API_TITLE'] = 'Cars API'
app.config['API_VERSION'] = 'v1'
app.config['OPENAPI_VERSION'] = '3.1.0'
app.config['OPENAPI_URL_PREFIX'] = '/docs'
app.config['OPENAPI_SWAGGER_UI_PATH'] = '/swagger-ui'
app.config['OPENAPI_REDOC_PATH'] = '/redoc'
app.config['OPENAPI_SWAGGER_UI_URL'] = 'https://cdn.jsdelivr.net/npm/swagger-ui-dist/'

api = Api(app)

limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["200 per day", "50 per hour"],
    storage_uri="memory://",
    headers_enabled=True
)

db.init_app(app)

api.register_blueprint(cars_bp)
api.register_blueprint(home_bp)


@app.cli.command("init_db")
@click.argument('num_entries', default=20)
def init_db_command(num_entries):
    print(f"Initializing the database at {app.config['SQLALCHEMY_DATABASE_URI']}")
    with app.app_context():
        db.drop_all()
        db.create_all()
    from .database import init_db_with_example_data
    init_db_with_example_data(num_entries)
    print(f"Database has been initialized with {num_entries} example cars.")
