from .extensions import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import Numeric, ForeignKey
from sqlalchemy.orm import relationship

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), default="user", nullable=False)

    accounts = relationship("Account", back_populates="user", cascade="all, delete-orphan")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Account(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, ForeignKey("user.id"), nullable=False)
    iban = db.Column(db.String(34), unique=True, nullable=False)
    account_type = db.Column(db.String(20), nullable=False)  # checking/savings
    balance = db.Column(Numeric(12,2), nullable=False, default=0)
    status = db.Column(db.String(20), nullable=False, default="open")

    user = relationship("User", back_populates="accounts")
    transactions = relationship("Transaction", back_populates="account", cascade="all, delete-orphan")

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    account_id = db.Column(db.Integer, ForeignKey("account.id"), nullable=False)
    kind = db.Column(db.String(20), nullable=False)  # deposit/withdraw/transfer_in/transfer_out
    amount = db.Column(Numeric(12,2), nullable=False)
    ref_tx = db.Column(db.Integer, nullable=True)  # paired tx id for transfers

    account = relationship("Account", back_populates="transactions")
