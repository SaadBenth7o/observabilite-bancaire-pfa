from . import create_app
from .migrate import run_migrations

def main():
    app = create_app()
    run_migrations(app)

if __name__ == "__main__":
    main()
