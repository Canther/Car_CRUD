from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates

db = SQLAlchemy()


class Car(db.Model):
    __tablename__ = 'cars'
    id = db.Column(db.Integer, primary_key=True)
    make = db.Column(db.String(50), nullable=False)
    model = db.Column(db.String(50), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    color = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Float, nullable=False)

    @validates('make', 'model', 'color')
    def validate_not_empty(self, key, value):
        if not value:
            raise ValueError(f"{key} cannot be empty")
        return value

    @validates('year')
    def validate_year(self, key, value):
        if not value or value < 1885 or value > 2030:
            raise ValueError(f"{key} must be between 1885 and 2030")
        return value

    @validates('price')
    def validate_price(self, key, value):
        if not value or value < 0:
            raise ValueError(f"{key} must be positive")
        return value

    def __init__(self, make, model, year, color, price):
        self.make = make
        self.model = model
        self.year = year
        self.color = color
        self.price = price

    def __repr__(self):
        return f"<Car {self.make} {self.model} {self.year} {self.color} {self.price}>"


def init_db_with_example_data(num_entries: int = 20):
    make_list = ['Toyota', 'Honda', 'Ford', 'Chevrolet', 'Nissan', 'Volkswagen', 'Mercedes-Benz', 'BMW', 'Audi',
                 'Hyundai', 'Kia', 'Subaru', 'Mazda', 'Jeep', 'Ram', 'GMC', 'Buick', 'Cadillac', 'Lexus']
    model_list = ['Prius', 'Civic', 'Silverado', 'Jetta', '3-Series', 'A4']
    color_list = ['Silver', 'Blue', 'Red', 'Black', 'White', 'Green', 'Yellow', 'Orange']
    year_list = [2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008]
    price_list = [5000.45, 6000.22, 7000.0, 8000.0, 9000, 10000.3, 11000.0, 13000.2, 14000.1]
    for i in range(num_entries):
        car = Car(make=make_list[i % len(make_list)], model=model_list[i % len(model_list)],
                  year=year_list[i % len(year_list)], color=color_list[i % len(color_list)],
                  price=price_list[i % len(price_list)])
        db.session.add(car)
    db.session.commit()
