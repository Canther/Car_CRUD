import pytest
from app.database import Car, db


# Test case for car creation
def test_car_creation(client):
    """
    Test case for car creation.
    This test case creates a car object and commits it to the database.
    """
    car = Car(make="make", model="model", year=2000, color="color", price=5000.0)
    db.session.add(car)
    db.session.commit()
    assert car.id is not None


# Test cases for car make validation
def test_car_make_validation(client):
    """
    This test case attempts to create a car object with an empty make and expects a ValueError.
    """
    with pytest.raises(ValueError):
        car = Car(make="", model="model", year=2000, color="color", price=5000.0)
        db.session.add(car)
        db.session.commit()


def test_car_model_validation(client):
    """
    This test case attempts to create a car object with an empty model and expects a ValueError.
    """
    with pytest.raises(ValueError):
        car = Car(make="make", model="", year=2000, color="color", price=5000.0)
        db.session.add(car)
        db.session.commit()


@pytest.mark.parametrize("year", [1050, 3000, ""])
def test_car_year_validation(year):
    """
    This test case attempts to create a car object with an invalid year (either too low, too high, or empty) and expects a ValueError.
    """
    with pytest.raises(ValueError):
        car = Car(make="make", model="model", year=year, color="color", price=5000.0)
        db.session.add(car)
        db.session.commit()


def test_car_color_validation(client):
    """
    This test case attempts to create a car object with an empty color and expects a ValueError.
    """
    with pytest.raises(ValueError):
        car = Car(make="make", model="model", year=2000, color="", price=5000.0)
        db.session.add(car)
        db.session.commit()


def test_car_price_validation(client):
    """
    This test case attempts to create a car object with a negative price and expects a ValueError.
    """
    with pytest.raises(ValueError):
        car = Car(make="make", model="model", year=2000, color="color", price=-5000.0)
        db.session.add(car)
        db.session.commit()
