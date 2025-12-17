from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from ..extensions import db
from ..models import Account
from decimal import Decimal
import random

accounts_bp = Blueprint("accounts", __name__, url_prefix="/accounts")

@accounts_bp.get("/")
@login_required
def list_accounts():
    accs = db.session.query(Account).filter_by(user_id=current_user.id).all()
    return render_template("accounts.html", accounts=accs)

@accounts_bp.post("/create")
@login_required
def create_account():
    acc_type = request.form.get("account_type", "checking")
    iban = f"MA{random.randint(10**20, 10**21-1)}"
    acc = Account(user_id=current_user.id, iban=iban, account_type=acc_type, balance=Decimal("0"))
    db.session.add(acc)
    db.session.commit()
    flash("Account created.", "info")
    return redirect(url_for("accounts.list_accounts"))

@accounts_bp.post("/close/<int:acc_id>")
@login_required
def close_account(acc_id):
    acc = db.session.get(Account, acc_id)
    if not acc or acc.user_id != current_user.id:
        flash("Account not found.", "error")
        return redirect(url_for("accounts.list_accounts"))
    acc.status = "closed"
    db.session.commit()
    flash("Account closed.", "info")
    return redirect(url_for("accounts.list_accounts"))
