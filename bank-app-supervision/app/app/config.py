import os

class Config:
    SECRET_KEY = os.environ.get("FLASK_SECRET_KEY", "dev-secret")
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", "sqlite:///bank.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO")
    APP_ENV = os.environ.get("APP_ENV", "dev")

    # Elastic APM
    ELASTIC_APM = {
        "SERVICE_NAME": os.environ.get("ELASTIC_APM_SERVICE_NAME", "bank-flask-app"),
        "SERVER_URL": os.environ.get("ELASTIC_APM_SERVER_URL"),
        "SECRET_TOKEN": os.environ.get("ELASTIC_APM_SECRET_TOKEN"),
        "ENVIRONMENT": os.environ.get("APP_ENV", "dev"),
    }
