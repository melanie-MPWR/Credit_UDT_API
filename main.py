from fastapi import Body, FastAPI
from fastapi.encoders import jsonable_encoder
import os
import datetime as dt
import json
import time
from datetime import date, timedelta
import requests
import plaid
from plaid.api import plaid_api
from plaid.model.consumer_report_permissible_purpose import ConsumerReportPermissiblePurpose
from plaid.model.link_token_create_request import LinkTokenCreateRequest
from plaid.model.link_token_create_request_cra_options import LinkTokenCreateRequestCraOptions
from plaid.model.link_token_create_request_statements import LinkTokenCreateRequestStatements
from plaid.model.link_token_create_request_user import LinkTokenCreateRequestUser
from plaid.model.products import Products
from plaid.model.country_code import CountryCode


PLAID_CLIENT_ID=os.getenv('CLIENT_ID')
PLAID_SECRET=os.getenv('PLAID_API_KEY')
sandbox_url=os.getenv('SANDBOX_URL')
PLAID_PRODUCTS = os.getenv('PLAID_PRODUCTS', 'transactions').split(',')
PLAID_COUNTRY_CODES = os.getenv('PLAID_COUNTRY_CODES', 'US').split(',')
print(PLAID_CLIENT_ID)

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

configuration = plaid.Configuration(
    host=host,
    api_key={
        'clientId': PLAID_CLIENT_ID,
        'secret': PLAID_SECRET,
    }
)

api_client = plaid.ApiClient(configuration)
client = plaid_api.PlaidApi(api_client)

async def create_link_token():
    global user_token
    try:
        request = LinkTokenCreateRequest(
            products=products,
            client_name="Plaid Quickstart",
            country_codes=list(map(lambda x: CountryCode(x), PLAID_COUNTRY_CODES)),
            language='en',
            user=LinkTokenCreateRequestUser(
                client_user_id=str(time.time())
            )
        )
        if PLAID_REDIRECT_URI != None:
            request['redirect_uri'] = PLAID_REDIRECT_URI
        if Products('statements') in products:
            statements = LinkTokenCreateRequestStatements(
                end_date=date.today(),
                start_date=date.today() - timedelta(days=30)
            )
            request['statements'] = statements

        cra_products = ["cra_base_report", "cra_income_insights", "cra_partner_insights"]
        if any(product in cra_products for product in PLAID_PRODUCTS):
            request['user_token'] = user_token
            request['consumer_report_permissible_purpose'] = ConsumerReportPermissiblePurpose(
                'ACCOUNT_REVIEW_CREDIT')
            request['cra_options'] = LinkTokenCreateRequestCraOptions(
                days_requested=60
            )
        # create link token
        response = client.link_token_create(request)
        return jsonable_encoder(response.to_dict())
    except plaid.ApiException as e:
        print(e)
        return json.loads(e.body)





@app.get("/")
async def health_check():
    access_token = await create_link_token()
    return {json.dumps(access_token)}


