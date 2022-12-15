from flask_migrate import Migrate
import os

from extensions.database import db

def init_app(app):
    Migrate(app, db, directory="project/migrations", compare_type=True)