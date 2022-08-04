from typing import Optional

from pydantic import BaseModel, Field


class User(BaseModel):
    user_id: int = Field(...)
    random_number: Optional[int] = Field(None)
