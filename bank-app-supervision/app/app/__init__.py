import os
from flask import Flask
from .config import Config
from .extensions import db, migrate, login_manager, apm, prometheus_metrics, init_logging
from .routes.auth import auth_bp
from .routes.accounts import accounts_bp
from .routes.transactions import tx_bp
from .routes.dashboard import dashboard_bp
from .models import User

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config())

    # Logging + extensions
    init_logging(app)
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    prometheus_metrics.init_app(app)

    # --- APM : utilise le dict Config.ELASTIC_APM ---
    apm_cfg = app.config.get("ELASTIC_APM", {})
    if apm_cfg.get("SERVER_URL"):
        # l’agent lit toute la config depuis app.config["ELASTIC_APM"]
        apm.init_app(app)

    # Blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(accounts_bp)
    app.register_blueprint(tx_bp)
    app.register_blueprint(dashboard_bp)

    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(User, int(user_id))

    @app.get("/healthz")
    def healthz():
        return {"status": "ok"}, 200

    return app

