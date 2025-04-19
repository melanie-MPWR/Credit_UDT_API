import json
from pprint import pprint
from typing import Union
from typing_extensions import Annotated
from plaid.model.transaction import Transaction

from couchbase.exceptions import DocumentExistsException, DocumentNotFoundException
from fastapi import APIRouter, Depends, HTTPException, Path, status, Query
from Couchbase.couchbase_db import get_db

TRANSACTION_COLLECTION = "transactions"

def create_transaction(
    transaction: Transaction,
    id: str,
    db=Depends(get_db),
) -> Transaction:
    """Create Transaction with specified ID"""
    pprint("TRANSACTION BEING SENT TO COUCHBASE! : ", json.dumps(transaction))
    try:
        db.insert_document(TRANSACTION_COLLECTION, id, transaction.model_dump())
        return Transaction
    except DocumentExistsException:
        raise HTTPException(status_code=409, detail="Transaction already exists")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {e}")
    return