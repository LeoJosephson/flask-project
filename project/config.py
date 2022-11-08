pg_user = "postgres"
pg_pwd = "1404"
pg_port = "5432"

DEV_DB_URL = f"postgresql://{pg_user}:{pg_pwd}@localhost/flaskproject"
TESTING_DB_URL = f"postgresql://{pg_user}:{pg_pwd}@localhost/flask_project_test"

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

