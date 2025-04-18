from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from plaid.model.accounts_balance_get_request import AccountsBalanceGetRequest

from Models.utility import AccessToken
from Models.transaction import create_transaction_model
from Models.account import create_account_model
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
import os
import plaid
from plaid.api import plaid_api
from plaid.model.item_public_token_exchange_request import ItemPublicTokenExchangeRequest
from plaid.model.transactions_sync_request import TransactionsSyncRequest
from plaid.model.products import Products
from plaid.model.sandbox_public_token_create_request import SandboxPublicTokenCreateRequest


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


@app.get("/getTransactions")
async def getTransactions():
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
    return JSONResponse(content=jsonable_encoder(_transactions))

@app.get("/getAccounts")
async def getAccounts():
    request = AccountsBalanceGetRequest(access_token=access_token)
    response = client.accounts_balance_get(request)
    accounts = response['accounts']

    _accounts = [create_account_model(account) for account in accounts]
    return JSONResponse(content=jsonable_encoder(_accounts))