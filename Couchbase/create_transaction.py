import json
import os
from pprint import pprint
from typing import Union, Any
from typing_extensions import Annotated
from plaid.model.transaction import Transaction

from couchbase.exceptions import DocumentExistsException, DocumentNotFoundException
from fastapi import APIRouter, Depends, HTTPException, Path, status, Query


def create_transaction(
    transaction: Transaction,
    id: str,
    db: any
) -> Transaction:
    """Create Transaction with specified ID"""
    pprint(f"ACCESSING COUCHBASE {transaction}, {vars(db)}")
    _transaction = json.loads(json.dumps(transaction, indent=4, sort_keys=True, default=str))
    try:
        db.insert_document("transactions", id, _transaction)
        return Transaction
    except DocumentExistsException:
        raise HTTPException(status_code=409, detail="Transaction already exists")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {e}")
    return