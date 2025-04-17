from fastapi import Body, FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware
from Models.Utility_models import AccessToken
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
import os
import datetime as dt
import json
import time
from datetime import date, timedelta
import requests
import plaid
from plaid.api import plaid_api
from plaid.model.consumer_report_permissible_purpose import ConsumerReportPermissiblePurpose
from plaid.model.item_public_token_exchange_request import ItemPublicTokenExchangeRequest
from plaid.model.link_token_create_request import LinkTokenCreateRequest
from plaid.model.link_token_create_request_cra_options import LinkTokenCreateRequestCraOptions
from plaid.model.link_token_create_request_statements import LinkTokenCreateRequestStatements
from plaid.model.link_token_create_request_user import LinkTokenCreateRequestUser
from plaid.model.products import Products
from plaid.model.country_code import CountryCode
from plaid.model.sandbox_public_token_create_request import SandboxPublicTokenCreateRequest
from plaid.model.sandbox_transfer_ledger_simulate_available_request import SandboxTransferLedgerSimulateAvailableRequest

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


@app.get("/")
async def health_check():
    return {'health': 'ok'}

@app.get("/create_sandbox_access_token")
async def create_sandbox_access_token():
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
    _access_token = AccessToken(
        access_token=exchange_response.access_token,
        item_id=exchange_response.item_id,
        request_id=exchange_response.request_id
    )
    return JSONResponse(content=jsonable_encoder(_access_token))