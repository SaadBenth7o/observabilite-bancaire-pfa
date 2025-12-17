from app.app import create_app
from app.app.migrate import run_migrations

if __name__ == "__main__":
    app = create_app()
    run_migrations(app)
