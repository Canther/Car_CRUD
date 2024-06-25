from marshmallow import Schema, fields
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field
from app.database import Car, db


class CarSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Car
        sqla_session = db.session

    id = auto_field(dump_only=True)
    make = auto_field(required=False, metadata={"example": "Toyota", "description": "Car make"})
    model = auto_field(required=False, metadata={"example": "Prius", "description": "Car model"})
    year = auto_field(required=False, metadata={"example": 2000, "description": "Car year. Must be between 1885 and 2030."})
    color = auto_field(required=False, metadata={"example": "Silver", "description": "Car color"})
    price = auto_field(required=False, metadata={"example": 5000.0, "description": "Car price"})


class PaginationSchema(Schema):
    page = fields.Int(dump_default=1, load_default=1)
    per_page = fields.Int(dump_default=10, load_default=10)


class FilterSchema(Schema):
    make = fields.Str(required=False, metadata={"description": "Car make"})
    model = fields.Str(required=False, metadata={"description": "Car model"})
    year = fields.Int(required=False, metadata={"description": "Car year."})
    color = fields.Str(required=False, metadata={"description": "Car color"})
    min_price = fields.Float(required=False, metadata={"description": "Minimum price"})
    max_price = fields.Float(required=False, metadata={"description": "Maximum price"})
