from decimal import Decimal
from .models import db, Account, Transaction

def deposit(account: Account, amount: Decimal):
    if amount <= 0:
        raise ValueError("Amount must be positive.")
    account.balance = (account.balance or 0) + amount
    tx = Transaction(account=account, kind="deposit", amount=amount)
    db.session.add(tx)
    return tx

def withdraw(account: Account, amount: Decimal):
    if amount <= 0:
        raise ValueError("Amount must be positive.")
    if account.balance < amount:
        raise ValueError("Insufficient funds.")
    account.balance = account.balance - amount
    tx = Transaction(account=account, kind="withdraw", amount=amount)
    db.session.add(tx)
    return tx

def transfer(src: Account, dst: Account, amount: Decimal):
    if src.id == dst.id:
        raise ValueError("Cannot transfer to the same account.")
    if amount <= 0:
        raise ValueError("Amount must be positive.")
    if src.balance < amount:
        raise ValueError("Insufficient funds.")
    src.balance = src.balance - amount
    dst.balance = (dst.balance or 0) + amount
    out_tx = Transaction(account=src, kind="transfer_out", amount=amount)
    in_tx  = Transaction(account=dst, kind="transfer_in", amount=amount, ref_tx=out_tx.id)
    db.session.add_all([out_tx, in_tx])
    return out_tx, in_tx
