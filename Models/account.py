from __future__ import annotations
from plaid.model.account_base import AccountBase
from plaid.model.account_balance import AccountBalance

def create_balance(balances):
    return AccountBalance(
        available=balances.available,
        current=balances.current,
        limit=balances.limit,
        iso_currency_code=balances.iso_currency_code,
        unofficial_currency_code=balances.unofficial_currency_code,
    )

def create_account(account):
    return AccountBase(
        account_id=account.get('account_id'),
        balances=account.get('balances'),
        holder_category=account.get('holder_category'),
        mask=account.get('mask'),
        name=account.get('name'),
        official_name=account.get('official_name'),
        subtype=account.get('subtype'),
        type=account.get('type')
    )


def create_account_model(account_data):
    # Process nested objects
    if 'balances' in account_data and account_data['balances']:
        balances = account_data['balances']
        account_data['balances'] = create_balance(balances)
    #     # account_data['balances'] = list(map(lambda balance: create_balance(balance), balances))

    return create_account(account_data).to_dict()