import json
from pprint import pprint
from plaid.model.account_base import AccountBase
from couchbase.exceptions import DocumentExistsException
from fastapi import HTTPException


def create_account(
    account: AccountBase,
    id: str,
    db: any
) -> AccountBase:
    """Create Transaction with specified ID"""
    pprint(f"ACCESSING COUCHBASE {account}, {vars(db)}")
    _account = json.loads(json.dumps(account, indent=4, sort_keys=True, default=str))
    try:
        db.insert_document("accounts", id, _account)
        return AccountBase
    except DocumentExistsException:
        raise HTTPException(status_code=409, detail="Transaction already exists")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {e}")
    return