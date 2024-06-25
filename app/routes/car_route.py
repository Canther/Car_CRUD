from flask.views import MethodView
from flask_smorest import Blueprint
from webargs.flaskparser import abort

from app.database import db
from app.database import Car
from app.schemas import PaginationSchema, FilterSchema, CarSchema

cars_bp = Blueprint('cars', 'cars', url_prefix='/cars', description='Operations on cars')


@cars_bp.route('/')
class CarListResource(MethodView):
    @cars_bp.arguments(PaginationSchema, required=False, location='query')
    @cars_bp.arguments(FilterSchema, required=False, location='query')
    def get(self, pagination_args, filter_args):
        """List cars with pagination and filters"""
        query = Car.query

        for key, value in filter_args.items():
            if value:
                if key in ['min_price', 'max_price']:
                    filter_expr = Car.price >= value if key == 'min_price' else Car.price <= value
                    query = query.filter(filter_expr)
                else:
                    query = query.filter(getattr(Car, key) == value)

        pagination = query.paginate(page=pagination_args['page'], per_page=pagination_args['per_page'], error_out=False)
        cars = pagination.items
        results = CarSchema(many=True).dump(cars)
        return {"total_count": pagination.total, "pages": pagination.pages, "current_page": pagination_args['page'], "cars": results}

    @cars_bp.arguments(CarSchema)
    @cars_bp.response(201, CarSchema)
    def post(self, new_data):
        """Create a new car"""
        new_car = Car(**new_data)
        db.session.add(new_car)
        db.session.commit()
        return new_car


@cars_bp.route('/<int:car_id>')
class CarResource(MethodView):
    @cars_bp.response(200, CarSchema)
    def get(self, car_id):
        """Get a car by ID """
        car = db.session.get(Car, car_id)
        if not car:
            abort(404, message="Car ID not found")
        return car

    @cars_bp.arguments(CarSchema)
    @cars_bp.response(200, CarSchema)
    def put(self, update_data, car_id):
        """Update a car by ID"""
        car = db.session.get(Car, car_id)
        if not car:
            abort(404, message="Car ID not found")
        for key, value in update_data.items():
            if value: setattr(car, key, value)
        db.session.commit()
        return car

    @cars_bp.response(204)
    def delete(self, car_id):
        """Delete a car by ID"""
        car = db.session.get(Car, car_id)
        if not car:
            abort(404, message="Car ID not found")
        db.session.delete(car)
        db.session.commit()
        return 'sucess', 200
