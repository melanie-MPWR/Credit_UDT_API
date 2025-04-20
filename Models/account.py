from __future__ import annotations
from plaid.model.account_base import AccountBase
from plaid.model.account_balance import AccountBalance
from plaid.model.account_type import AccountType
from plaid.model.account_subtype import AccountSubtype
from plaid.model.account_holder_category import AccountHolderCategory

def create_balance(balances):
    return AccountBalance(
        available=balances.get('available'),
        current=balances.get('current'),
        limit=balances.get('limit'),
        iso_currency_code=balances.get('iso_currency_code'),
        unofficial_currency_code=balances.get('unofficial_currency_code'),
    )

def create_type(type):
    return AccountType(
        value=type,
    )

def create_subtype(subtype):
    return AccountSubtype(
        value=subtype,
    )

def create_holder_category(holder_category):
    return AccountHolderCategory(
        value=holder_category,
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

    if 'type' in account_data and account_data['type']:
        type = account_data['type']
        account_data['type'] = create_type(type)

    if 'subtype' in account_data and account_data['subtype']:
        subtype = account_data['subtype']
        account_data['subtype'] = create_subtype(subtype)

    if 'holder_category' in account_data and account_data['holder_category']:
        holder_category = account_data['holder_category']
        account_data['holder_category'] = create_holder_category(holder_category)


    return create_account(account_data).to_dict()