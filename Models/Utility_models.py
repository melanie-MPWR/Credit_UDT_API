from pydantic import BaseModel

class AccessToken(BaseModel):
    access_token: str
    item_id: str
    request_id: str
