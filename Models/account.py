from __future__ import annotations
from plaid.model.account_base import AccountBase
from plaid.model.bank_transfer_balance import BankTransferBalance

def create_balance(balance):
    return BankTransferBalance(
        available=balance.available,
        current=balance.current,
        limit=balance.limit,
        iso_currency_code=balance.iso_currency_code,
        unofficial_currency_code=balance.unofficial_currency_code,
        last_updated_datetime=balance.last_updated_datetime,
    )

def create_account(account):
    return AccountBase(
        account_id=account.account_id,
        balances=account.balances,
        holder_category=account.holder_category,
        mask=account.mask,
        name=account.name,
        official_name=account.official_name,
        subtype=account.subtype,
        type=account.type
    )


def create_account_model(account_data):
    # Process nested objects
    if 'balances' in account_data  and account_data['balances']:
        balances = account_data['balances']
        account_data['balances'] =  list(map(lambda balance: create_balance(balance), balances))

    return create_account(account_data).to_dict()