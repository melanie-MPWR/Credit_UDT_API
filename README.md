# Universal Data Translator and Plaid Integration Demonstration API
    This is an api to demonstrate the speed and potential of our Universal Data Translator product,
    and to provide an example integration with the Plaid Open Banking platform.

### Environment Setup

    This demo api runs using uvicorn, so env vars need to be set from the cmd line.

    Necessary env vars are:
        CLIENT_ID=
        PLAID_API_KEY=

    Other Plaid env vars such as PLAID_PRODUCTS and PLAID_COUNTRY_CODES are populated in the code.

    An SSL certificate may need to be added globally - on Mac OS use the command:

    open /Applications/Python\ 3.12/Install\ Certificates.command   

### Plaid auth flow

    To be completed

### To run the FastAPI server use uvicorn from the cmd line with:

    uvicorn main:app  --reload --env-file .env

    The demo runs on PORT 8000 and can be accessed at http://127.0.0.1:8000

### Special endpoints

    /                  endpoint should return {healthcheck: ok}
    /docs              links to the Swagger documentation and test environment 
