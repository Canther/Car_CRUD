import pytest
import random
from flask import json, Flask

from app.database import db, Car
from app import app as original_app
from tests.conftest import client


@pytest.fixture
def add_car(app):
    def _add_car(car_properties):
        car = Car(**car_properties)
        db.session.add(car)
        db.session.commit()
        return car

    yield _add_car


@pytest.mark.parametrize("num_entries", [0, 1, 2, 5, 10, 11, 100, 1000])
def test_get_all_cars(client, num_entries, add_car):
    for _ in range(num_entries):
        add_car(get_sample_car())
    response = client.get('/cars/', query_string={'page': 1, 'per_page': num_entries + 2})
    car_count = len(response.json['cars'])
    assert car_count == num_entries
    assert response.status_code == 200


def get_sample_car():
    make_list = ['Toyota', 'Honda', 'Ford', 'Chevrolet', 'Nissan', 'Volkswagen', 'Mercedes-Benz', 'BMW', 'Audi',
                 'Hyundai', 'Kia', 'Subaru', 'Mazda', 'Jeep', 'Ram', 'GMC', 'Buick', 'Cadillac', 'Lexus']
    model_list = ['Prius', 'Civic', 'Silverado', 'Jetta', '3-Series', 'A4']
    color_list = ['Silver', 'Blue', 'Red', 'Black', 'White', 'Green', 'Yellow', 'Orange']
    year_list = [2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008]
    price_list = [5000.45, 6000.22, 7000.0, 8000.0, 9000, 10000.3, 11000.0, 13000.2, 14000.1]
    return {
        "make": random.choice(make_list),
        "model": random.choice(model_list),
        "year": random.choice(year_list),
        "color": random.choice(color_list),
        "price": random.choice(price_list)
    }


def test_get_single_car(client, add_car):
    sample_car = get_sample_car()
    car = add_car(sample_car)
    response = client.get(f'/cars/{car.id}')
    response_car = response.json
    sample_car['id'] = car.id
    assert response_car == sample_car
    assert response.status_code == 200


@pytest.mark.parametrize("num_entries", [0, 1, 2])
def test_get_single_car_not_found(client, num_entries, add_car):
    for _ in range(num_entries):
        add_car(get_sample_car())
    response = client.get('/cars/3')
    assert response.status_code == 404


@pytest.mark.parametrize("num_entries", [0, 1, 2])
def test_post_car(client, num_entries, add_car):
    for _ in range(num_entries):
        add_car(get_sample_car())
    response = client.post('/cars/', data=json.dumps(get_sample_car()), content_type='application/json')
    assert response.status_code == 201
    assert response.json['id'] is not None


def test_put_car(client, add_car):
    car = add_car(get_sample_car())
    updated_data = {"model": "updated", "year": car.year, "color": car.color, "price": car.price, 'make': car.make}
    response = client.put(f'/cars/{car.id}', data=json.dumps(updated_data), content_type='application/json')
    assert response.status_code == 200


def test_delete_car(client, add_car):
    car = add_car(get_sample_car())
    response = client.delete(f'/cars/{car.id}')
    assert response.status_code == 200


@pytest.mark.parametrize("num_entries", [0, 1, 10, 1000])
@pytest.mark.parametrize("per_page", [1, 10, 1000])
@pytest.mark.parametrize("page", [1, 10, 100])
def test_pagination(client, num_entries, per_page, page, add_car):
    '''Test that pagination works correctly'''
    for _ in range(num_entries):
        add_car(get_sample_car())
    response = client.get('/cars/', query_string={'page': page, 'per_page': per_page})
    car_count = len(response.json['cars'])
    expected_count = min(per_page, num_entries - (page - 1) * per_page)
    expected_count = max(0, expected_count)
    assert car_count == expected_count
    assert response.status_code == 200
    assert response.json['current_page'] == page
    assert response.json['total_count'] == num_entries
    assert response.json['pages'] == -(-num_entries // per_page)


def test_pagination_ids(client):
    '''Test that all ids are unique across all pages'''
    num_entries = 100
    all_ids = []
    for _ in range(num_entries):
        client.post('/cars/', data=json.dumps(get_sample_car()), content_type='application/json')
    response = client.get('/cars/', query_string={'page': 1, 'per_page': num_entries})
    total_pages = response.json['pages']
    for page in range(1, total_pages + 1):
        response = client.get('/cars/', query_string={'page': page, 'per_page': num_entries})
        ids = [car['id'] for car in response.json['cars']]
        for id in ids:
            assert id not in all_ids
            all_ids.append(id)


def test_rate_limit():
    local_app: Flask = original_app
    local_app.config['TESTING'] = False
    client = local_app.test_client()

    response = client.get('/cars/', query_string={'page': 1, 'per_page': 1})
    ratelimit = int(response.headers['X-RateLimit-Limit'])
    for i in range(ratelimit - 1):
        response = client.get('/cars/', query_string={'page': 1, 'per_page': 1})
        assert response.status_code == 200
    response = client.get('/cars/', query_string={'page': 1, 'per_page': 1})
    assert response.status_code == 429
