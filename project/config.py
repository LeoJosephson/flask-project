from dotenv import load_dotenv
import os

load_dotenv()
pg_user = os.environ['POSTGRES_USER']
pg_pwd = os.environ['POSTGRES_PASSWORD']
pg_port = os.environ['POSTGRES_PORT']
host = os.environ.get("DOCKER_HOST", os.environ["HOST"]) #check if it's running on docker


DEV_DB_URL = f"postgresql://{pg_user}:{pg_pwd}@{host}:{pg_port}/flaskproject"
TESTING_DB_URL = f"postgresql://{pg_user}:{pg_pwd}@{host}:{pg_port}/flask_project_test"


class Config(object):
    # SQLAlchemy settings
    SQLALCHEMY_DATABASE_URI = DEV_DB_URL
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Flask Settings
    DEBUG = False
    TESTING = False

class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    SQLALCHEMY_DATABASE_URI = TESTING_DB_URL
    DEBUG = True
    TESTING = True

