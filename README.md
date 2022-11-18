# Flask api project for a Game Api  

This application uses [Flask](https://flask.palletsprojects.com) and [PostgreSQL](https://www.postgresql.org/), [Swagger](https://swagger.io/) for api documentation using [Flasgger](https://github.com/flasgger/flasgger) and [Pytest](https://docs.pytest.org/) and [Pytest-cov](https://pytest-cov.readthedocs.io/) for testing.

### Models
1. Game
2. User
3. Review
4. Category

<p align="center">
  <img src="https://github.com/LeoJosephson/flask-project/blob/main/diagram.png" width="400"
</p>

## Quickstart

### Clone repository

```
git clone https://github.com/LeoJosephson/flask-project.git
```
### Installation
Make sure you have [python](https://www.python.org/downloads/) installed  
  
Use the package manager [pip](https://pip.pypa.io/en/stable/) to install the additional packages
```
pip install -r requirements.txt
```

### Create Environment variables
create a file (.env) in the root of the project with the following variables:
  
| Variable name      | Description        | Example        |
| ------------------ | ------------------ | -------------- |
| FLASK_APP          | flask application  | project/app.py |
| POSTGRES_USER      | Postgres username  | "postgres"     |
| POSTGRES_PASSWORD  | Postgres password  | "password"     |
| POSTGRES_PORT      | Postgres port      | "5433"         |
| HOST               | host               | "localhost"    |


FLASK_APP variable must be equal to project/app.py  

if running in a docker running add a environment variable DOCKER_HOST="host.docker.internal" in the Dockerfile or in the .env file  
  
### Create database entities
make sure you are in the project folder
  
```flask shell``` to start flask shell
```python
from extensions import db
from models.category import Category
from models.game import Game
from models.user import User
from models.review import Review
db.create_all()
```
### Run application  
  
```
flask run 
```
### Run tests
```
python -m pytest
```
  
#### Create Html report for test coverage
```
python -m pytest --cov-report html --cov
```
The html coverage is located at htmlcov/index.html

### Access api documentation
The default endpoint is apidocs  
  
Example: http://127.0.0.1:5000/apidocs/
