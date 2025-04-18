from typing import Any
import datetime
from fastapi import HTTPException


def is_date(value: Any) -> datetime.date:
    print(f"parsing date {value}", )
    if not isinstance(value, datetime.date):
        try:
            return datetime.datetime.strptime(value, "%Y-%m-%d").date()
        except:
            raise HTTPException(status_code=502, detail=f"unable to convert obj {value} to date")

    else:
        return value