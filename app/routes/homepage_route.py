from flask import render_template
from flask.views import MethodView
from flask_smorest import Blueprint

from app.database import Car

home_bp = Blueprint('home', 'home', url_prefix='/', description='Home page')


@home_bp.route('/')
class HomeResource(MethodView):
    def get(self):
        """Home page"""
        cars = Car.query.all()
        return render_template('index.html', cars=cars)
