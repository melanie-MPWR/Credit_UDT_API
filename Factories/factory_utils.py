from pprint import pprint

from Factories.transaction_factory import generate_transactions
from Models.account import create_account_model
from Models.transaction import create_transaction_model
from Couchbase.create_transaction import create_transaction
from Couchbase.create_account import create_account
from uuid import uuid4 as v4

def generate_number_of_transactions(number: int, couchbase_db: any):
    transactions = generate_transactions(number)
    [prep_transaction_for_Couchbase(couchbase_db, transaction) for transaction in transactions]
    return transactions

def prep_transaction_for_Couchbase(couchbase_db, new_transaction):
    pprint(f"NEW TRANSACTION================, {new_transaction}")
    transaction = create_transaction_model(new_transaction)
    print(transaction)
    _id = str(v4())
    try:
        create_transaction(transaction, _id, couchbase_db)
    except:
        pass
    return _id

def prep_account_for_Couchbase(couchbase_db, new_account):
    print(new_account)
    account = create_account_model(new_account)
    _id = str(v4())
    try:
        create_account(account, _id, couchbase_db)
    except:
        pass
    return _id