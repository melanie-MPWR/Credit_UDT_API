from __future__ import annotations
from pydantic import BaseModel, Field
from typing import List, Optional, Any
from datetime import date
from plaid.model.transaction import Transaction
from plaid.model.location import Location
from plaid.model.payment_meta import PaymentMeta
from plaid.model.transaction_code import TransactionCode
from plaid.model.personal_finance_category import PersonalFinanceCategory
from plaid.model.business_finance_category import BusinessFinanceCategory
from plaid.model.transaction_counterparty import TransactionCounterparty


def create_counterparty(cp):
    return TransactionCounterparty(
        name=cp.name,
        type=cp.type,
        website=cp.website,
        logo_url=cp.logo_url,
        entity_id=cp.entity_id,
        confidence_level=cp.confidence_level
    )

def create_transaction_model(transaction_data):
    # Process nested objects
    if 'counterparties' in transaction_data:
        counterparties = transaction_data['counterparties']
        print("CONFIDENCE", list(map(lambda counterparty: create_counterparty(counterparty), transaction_data['counterparties']))
)

    # if 'location' in transaction_data and transaction_data['location']:
    #     transaction_data['location'] = Location(**transaction_data['location'])
    #
    # if 'payment_meta' in transaction_data and transaction_data['payment_meta']:
    #     transaction_data['payment_meta'] = PaymentMeta(**transaction_data['payment_meta'])
    #
    # if 'personal_finance_category' in transaction_data and transaction_data['personal_finance_category']:
    #     transaction_data['personal_finance_category'] = PersonalFinanceCategory(
    #         **transaction_data['personal_finance_category'])
    #
    # # Create and return the Transaction model
    # return Transaction(**transaction_data)

    return