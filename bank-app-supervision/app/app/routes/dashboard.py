from flask import Blueprint, render_template
from flask_login import login_required, current_user
from ..extensions import db
from ..models import Account, Transaction
from sqlalchemy import func

dashboard_bp = Blueprint("dashboard", __name__)

@dashboard_bp.get("/")
@login_required
def home():
    total_balance = db.session.query(func.coalesce(func.sum(Account.balance), 0)).filter_by(user_id=current_user.id).scalar() or 0
    tx_count = db.session.query(func.count(Transaction.id)).join(Account).filter(Account.user_id==current_user.id).scalar()
    latest_txs = db.session.query(Transaction).join(Account).filter(Account.user_id==current_user.id).order_by(Transaction.id.desc()).limit(10).all()
    return render_template("dashboard.html", total_balance=total_balance, tx_count=tx_count, latest_txs=latest_txs)
