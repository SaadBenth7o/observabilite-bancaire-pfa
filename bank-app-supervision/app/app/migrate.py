from .extensions import db
from .models import *  # noqa

def run_migrations(app):
    with app.app_context():
        db.create_all()
