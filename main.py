from functools import reduce
import operator

from fastapi import FastAPI, Path, Query
from fastapi.middleware.cors import CORSMiddleware
from plaid.model.accounts_balance_get_request import AccountsBalanceGetRequest

from Factories.account_factory import generate_accounts
from Factories.factory_utils import prep_transaction_for_Couchbase, prep_account_for_Couchbase
from Factories.transaction_factory import generate_transactions
from Models.utility import AccessToken
from Models.transaction import create_transaction_model
from Models.account import create_account_model
from Couchbase.create_transaction import create_transaction
from Factories.example_transaction import example
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
import os
import plaid
from plaid.api import plaid_api
from plaid.model.item_public_token_exchange_request import ItemPublicTokenExchangeRequest
from plaid.model.transactions_sync_request import TransactionsSyncRequest
from plaid.model.products import Products
from plaid.model.sandbox_public_token_create_request import SandboxPublicTokenCreateRequest
from Couchbase.couchbase_db import CouchbaseClient
from Models.utils import randint

db_conn_str = os.getenv('DB_CONN_STR')
db_username = os.getenv('DB_USERNAME')
db_password = os.getenv('DB_PASSWORD')

PLAID_CLIENT_ID=os.getenv('CLIENT_ID')
PLAID_SECRET=os.getenv('PLAID_API_KEY')

PLAID_PRODUCTS = os.getenv('PLAID_PRODUCTS', 'transactions').split(',')
PLAID_COUNTRY_CODES = os.getenv('PLAID_COUNTRY_CODES', 'US').split(',')
INSTITUTION_ID = os.getenv('INSTITUTION_ID')

def empty_to_none(field):
    value = os.getenv(field)
    if value is None or len(value) == 0:
        return None
    return value

# Parameters used for the OAuth redirect Link flow.
#
# Set PLAID_REDIRECT_URI to 'http://localhost:3000/'
# The OAuth redirect flow requires an endpoint on the developer's website
# that the bank website should redirect to. You will need to configure
# this redirect URI for your client ID through the Plaid developer dashboard
# at https://dashboard.plaid.com/team/api.
PLAID_REDIRECT_URI = empty_to_none('PLAID_REDIRECT_URI')

host = plaid.Environment.Sandbox

products = []
for product in PLAID_PRODUCTS:
    products.append(Products(product))

app = FastAPI(debug=True)
origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Couchbase client object shared by all routes
couchbase_db = CouchbaseClient()
print(f"USERNAME: {db_username}")
couchbase_db.init_app(db_conn_str, db_username, db_password, app)
couchbase_db.connect()

configuration = plaid.Configuration(
    host=host,
    api_key={
        'clientId': PLAID_CLIENT_ID,
        'secret': PLAID_SECRET,
    }
)

api_client = plaid.ApiClient(configuration)
client = plaid_api.PlaidApi(api_client)
access_token = None


@app.get("/")
async def health_check():
    return {'health': 'ok'}

@app.get("/create_sandbox_access_token")
async def create_sandbox_access_token():
    global access_token
    pt_request = SandboxPublicTokenCreateRequest(
        institution_id=INSTITUTION_ID,
        initial_products=[Products('transactions')]
    )
    pt_response = client.sandbox_public_token_create(pt_request)
    # The generated public_token can now be
    # exchanged for an access_token
    exchange_request = ItemPublicTokenExchangeRequest(
        public_token=pt_response['public_token']
    )
    exchange_response = client.item_public_token_exchange(exchange_request)
    print(exchange_response)
    access_token = exchange_response.access_token
    _access_token = AccessToken(
        access_token=access_token,
        item_id=exchange_response.item_id,
        request_id=exchange_response.request_id
    )
    return JSONResponse(content=jsonable_encoder(_access_token))


@app.get("/getTransactions/{number}")
async def getTransactions(number: int):
    request = TransactionsSyncRequest(
        access_token=access_token,
    )
    response = client.transactions_sync(request)
    transactions = response['added']

    # the transactions in the response are paginated, so make multiple calls while incrementing the cursor to
    # retrieve all transactions
    while (response['has_more']):
        request = TransactionsSyncRequest(
            access_token=access_token,
            cursor=response['next_cursor']
        )
        response = client.transactions_sync(request)
        transactions += response['added']

    _transactions = [create_transaction_model(transaction) for transaction in transactions]
    if number:
        return JSONResponse(content=jsonable_encoder(_transactions[:number]))
    return JSONResponse(content=jsonable_encoder(_transactions))

@app.get("/createNewTransaction", status_code=201)
async def create_single_transaction():
    transactions = generate_transactions(1)
    [prep_transaction_for_Couchbase(couchbase_db, transaction) for transaction in transactions]
    return JSONResponse(content={"info" : f"{1} transaction record created"})

@app.get("/createNewTransaction/{number}", status_code=201)
async def create_multiple_transactions(number: int = Path(..., description="Number of transactions to create", ge=1, le=1000)):
    transactions = generate_transactions(number)
    [prep_transaction_for_Couchbase(couchbase_db, transaction) for transaction in transactions]
    return JSONResponse(content={"info" : f"{number} transactions records created"})

@app.get("/getAccounts")
async def getAccounts():
    request = AccountsBalanceGetRequest(access_token=access_token)
    response = client.accounts_balance_get(request)
    accounts = response['accounts']
    _accounts = [create_account_model(account) for account in accounts]
    return JSONResponse(content=jsonable_encoder(_accounts))

@app.get("/createNewAccount", status_code=201)
async def create_single_account():
    accounts = generate_accounts(1)
    [prep_account_for_Couchbase(couchbase_db, account) for account in accounts]
    return JSONResponse(content={"info": f"{1} account record created"})

# Example query for associated transactions http://127.0.0.1:8000/createNewTransaction/10?generate_associated_transactions=true
@app.get("/createNewAccount/{number}", status_code=201)
async def create_multiple_accounts(
        number: int = Path(..., description="Number of accounts to create", ge=1, le=1000),
        generate_associated_transactions: bool = Query(False,
                                                       description="Generate randomised transactions associated with account ids")

):
    accounts = generate_accounts(number)
    account_ids = [account['account_id'] for account in accounts]
    [prep_account_for_Couchbase(couchbase_db, account) for account in accounts]

    if generate_associated_transactions:
        transactions = reduce(operator.concat,[generate_transactions(randint(), account_id) for account_id in account_ids])
        [prep_transaction_for_Couchbase(couchbase_db, transaction) for transaction in transactions]

        return JSONResponse(content={"info": f"{number} account records created and {len(transactions)} associated transactions created, with account_ids {', '.join(account_ids)}"})

    return JSONResponse(content={"info" : f"{number} account records created"})
