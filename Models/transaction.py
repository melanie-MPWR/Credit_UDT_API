from __future__ import annotations
from enum import Enum
from plaid.model.transaction import Transaction
from plaid.model.location import Location
from plaid.model.payment_meta import PaymentMeta
from plaid.model.transaction_code import TransactionCode
from plaid.model.personal_finance_category import PersonalFinanceCategory
from plaid.model.business_finance_category import BusinessFinanceCategory
from plaid.model.transaction_counterparty import TransactionCounterparty


class CounterpartyType(str, Enum):
    MERCHANT = "merchant"
    FINANCIAL_INSTITUTION = "financial_institution"
    PAYMENT_APP = "payment_app"
    MARKETPLACE = "marketplace"
    PAYMENT_TERMINAL = "payment_terminal"
    INCOME_SOURCE = "income_source"


def create_location(location):
    return Location(
        address=location.address,
        city=location.city,
        region=location.region,
        postal_code=location.postal_code,
        country=location.country,
        lat=location.lat,
        lon=location.lon,
        store_number=location.store_number
    )

def create_payment_meta(payment_meta):
    return PaymentMeta(
        reference_number=payment_meta.reference_number,
        ppd_id=payment_meta.ppd_id,
        payee=payment_meta.payee,
        by_order_of=payment_meta.by_order_of,
        payer=payment_meta.payer,
        payment_method=payment_meta.payment_method,
        payment_processor=payment_meta.payment_processor,
        reason=payment_meta.reason
    )

def create_transaction_code(transaction_code):
    return TransactionCode(
        value=transaction_code.value
    )

def create_personal_finance_category(personal_finance_category):
    return PersonalFinanceCategory(
        primary=personal_finance_category.primary,
        detailed=personal_finance_category.detailed,
        confidence_level=personal_finance_category.confidence_level
    )

def create_business_finance_category(business_finance_category):
    return BusinessFinanceCategory(
        primary=business_finance_category.primary,
        detailed=business_finance_category.detailed,
        confidence_level=business_finance_category.confidence_level
    )

def create_transaction_counterparty(transaction_counterparty):
    # Get the type value from the input object
    # type_value = getattr(transaction_counterparty, 'type', None)
    #
    # # Validate the type value if it exists
    # if type_value is not None and type_value not in CounterpartyType._value2member_map_:
    #     valid_types = ', '.join([f"'{v}'" for v in CounterpartyType._value2member_map_.keys()])
    #     raise ValueError(f"Invalid counterparty type: '{type_value}'. Must be one of: {valid_types}")

    # Create and return the TransactionCounterparty model
    return TransactionCounterparty(
        name=transaction_counterparty.name,
        type=transaction_counterparty.type,
        website=transaction_counterparty.website,
        logo_url=transaction_counterparty.logo_url,
        entity_id=transaction_counterparty.entity_id,
        confidence_level=transaction_counterparty.confidence_level
    )

def create_transaction(transaction_data) -> Transaction:
    return Transaction(
        account_id=transaction_data.get('account_id'),
        amount=transaction_data.get('amount'),
        iso_currency_code=transaction_data.get('iso_currency_code'),
        unofficial_currency_code=transaction_data.get('unofficial_currency_code'),
        category=transaction_data.get('category'),
        category_id=transaction_data.get('category_id'),
        date=transaction_data.get('date'),
        location=transaction_data.get('location'),
        name=transaction_data.get('name'),
        payment_meta=transaction_data.get('payment_meta'),
        pending=transaction_data.get('pending'),
        pending_transaction_id=transaction_data.get('pending_transaction_id'),
        account_owner=transaction_data.get('account_owner'),
        transaction_id=transaction_data.get('transaction_id'),
        authorized_date=transaction_data.get('authorized_date'),
        authorized_datetime=transaction_data.get('authorized_datetime'),
        datetime=transaction_data.get('datetime'),
        payment_channel=transaction_data.get('payment_channel'),
        transaction_code=transaction_data.get('transaction_code'),
        check_number=transaction_data.get('check_number'),
        merchant_name=transaction_data.get('merchant_name'),
        original_description=transaction_data.get('original_description'),
        transaction_type=transaction_data.get('transaction_type'),
        logo_url=transaction_data.get('logo_url'),
        website=transaction_data.get('website'),
        personal_finance_category=transaction_data.get('personal_finance_category'),
        business_finance_category=transaction_data.get('business_finance_category'),
        personal_finance_category_icon_url=transaction_data.get('personal_finance_category_icon_url'),
        counterparties=transaction_data.get('counterparties'),
        merchant_entity_id=transaction_data.get('merchant_entity_id')
    )

def create_transaction_model(transaction_data):
    # Process nested objects
    if 'location' in transaction_data and transaction_data['location']:
        location = transaction_data['location']
        transaction_data['location'] = create_location(location)

    if 'payment_meta' in transaction_data and transaction_data['payment_meta']:
        payment_meta = transaction_data['payment_meta']
        transaction_data['payment_meta'] = create_payment_meta(payment_meta)

    if 'personal_finance_category' in transaction_data and transaction_data['personal_finance_category']:
        payment_meta = transaction_data['personal_finance_category']
        transaction_data['personal_finance_category'] = create_personal_finance_category(payment_meta)

    if 'create_business_finance_category' in transaction_data and transaction_data['create_business_finance_category']:
        payment_meta = transaction_data['create_business_finance_category']
        transaction_data['create_business_finance_category'] = create_personal_finance_category(payment_meta)

    if 'counterparties' in transaction_data  and transaction_data['counterparties']:
        counterparties = transaction_data['counterparties']
        transaction_data['counterparties'] =  list(map(lambda counterparty: create_transaction_counterparty(counterparty), counterparties))

    return create_transaction(transaction_data).to_dict()