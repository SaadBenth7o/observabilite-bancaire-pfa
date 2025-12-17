from .extensions import db
from .models import User, Account
from decimal import Decimal
from flask import Flask
from . import create_app

def main():
    app = create_app()
    with app.app_context():
        if not db.session.query(User).filter_by(email="admin@demo.local").first():
            admin = User(email="admin@demo.local", role="admin")
            admin.set_password("admin123")
            db.session.add(admin)
            db.session.commit()

        user = db.session.query(User).filter_by(email="user@demo.local").first()
        if not user:
            user = User(email="user@demo.local", role="user")
            user.set_password("user12345")
            db.session.add(user)
            db.session.commit()

        if not db.session.query(Account).filter_by(user_id=user.id).first():
            a1 = Account(user_id=user.id, iban="MA0000000000000000001", account_type="checking", balance=Decimal("1000.00"))
            a2 = Account(user_id=user.id, iban="MA0000000000000000002", account_type="savings", balance=Decimal("2500.00"))
            db.session.add_all([a1, a2])
            db.session.commit()
        print("Seed complete. Login admin@demo.local/admin123 or user@demo.local/user12345")

if __name__ == "__main__":
    main()
