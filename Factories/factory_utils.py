from pprint import pprint

from Factories.transaction_factory import generate_transactions
from Models.transaction import create_transaction_model
from Couchbase.create_transaction import create_transaction
from uuid import uuid4 as v4

def generate_number_of_transactions(number: int, couchbase_db: any):
    transactions = generate_transactions(number)
    [prep_transaction_for_Couchbase(couchbase_db, transaction) for transaction in transactions]
    return transactions

def prep_transaction_for_Couchbase(couchbase_db, new_transaction):
    transaction = create_transaction_model(new_transaction)
    print(transaction)
    _id = str(v4())
    # try:
    #     create_transaction(transaction, _id, couchbase_db)
    # except:
    #     pass
    return _id