from app import create_app
try:
    # si présent dans ton projet
    from app.app.migrate import run_migrations
except Exception as e:
    print("⚠️ Migrations ignorées :", e)
    def run_migrations(app): 
        pass

if __name__ == "__main__":
    app = create_app()
    run_migrations(app)
    print("Migrations OK/ignorées")
