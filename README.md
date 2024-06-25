# Cars API

## Description

This is a simple Cars API built with Python using Flask, SQLAlchemy, and Marshmallow. It provides endpoints for CRUD
operations on a car database.

## Setup

1. Clone the repository.

2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

3. Initialize the database:

```bash
flask init_db
```

or

```bash
flask init_db 100
```

to initialize the database with 100 cars.

## Usage

1. Start the server:

```bash
flask run
```

2. The API documentation is available at `http://localhost:5000/docs/swagger-ui`.

3. The available endpoints are:

- `GET /cars`: Fetch all cars.
- `POST /cars`: Create a new car.
- `GET /cars/<id>`: Fetch a specific car by its ID.
- `PUT /cars/<id>`: Update a specific car by its ID.
- `DELETE /cars/<id>`: Delete a specific car by its ID.

There is also a Homepage available at `http://localhost:5000/`.
It provides a simple interface to interact with database.

## Testing

To run the tests, execute the following command:

```bash
pytest
```

