from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from ..extensions import db
from ..models import Account, Transaction
from ..services import deposit, withdraw, transfer
from decimal import Decimal

tx_bp = Blueprint("tx", __name__, url_prefix="/tx")

def _get_user_account(acc_id):
    acc = db.session.get(Account, acc_id)
    if not acc or acc.user_id != current_user.id:
        return None
    return acc

@tx_bp.get("/")
@login_required
def list_tx():
    accounts = db.session.query(Account).filter_by(user_id=current_user.id).all()
    txs = db.session.query(Transaction).join(Account).filter(Account.user_id==current_user.id).order_by(Transaction.id.desc()).limit(50).all()
    return render_template("transactions.html", accounts=accounts, txs=txs)

@tx_bp.post("/deposit")
@login_required
def deposit_view():
    acc = _get_user_account(int(request.form["account_id"]))
    amount = Decimal(request.form["amount"])
    if not acc:
        flash("Account not found.", "error")
        return redirect(url_for("tx.list_tx"))
    try:
        deposit(acc, amount)
        db.session.commit()
        flash("Deposit OK.", "info")
    except Exception as e:
        db.session.rollback()
        flash(str(e), "error")
    return redirect(url_for("tx.list_tx"))

@tx_bp.post("/withdraw")
@login_required
def withdraw_view():
    acc = _get_user_account(int(request.form["account_id"]))
    amount = Decimal(request.form["amount"])
    if not acc:
        flash("Account not found.", "error")
        return redirect(url_for("tx.list_tx"))
    try:
        withdraw(acc, amount)
        db.session.commit()
        flash("Withdraw OK.", "info")
    except Exception as e:
        db.session.rollback()
        flash(str(e), "error")
    return redirect(url_for("tx.list_tx"))

@tx_bp.post("/transfer")
@login_required
def transfer_view():
    src = _get_user_account(int(request.form["src_id"]))
    dst = _get_user_account(int(request.form["dst_id"]))
    amount = Decimal(request.form["amount"])
    if not src or not dst:
        flash("Account not found.", "error")
        return redirect(url_for("tx.list_tx"))
    try:
        transfer(src, dst, amount)
        db.session.commit()
        flash("Transfer OK.", "info")
    except Exception as e:
        db.session.rollback()
        flash(str(e), "error")
    return redirect(url_for("tx.list_tx"))
