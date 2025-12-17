from . import create_app
from .migrate import run_migrations

if __name__ == "__main__":
    app = create_app()
    run_migrations(app)
