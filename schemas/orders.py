from datetime import datetime
from pydantic import BaseModel, ConfigDict
from typing import Optional
from db.models.orders import Status


class OrderCreate(BaseModel):
    item_id: int


class OrderRead(BaseModel):
    id: Optional[int]
    item_id: int
    user_id: Optional[int]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    status: Optional[Status]

    model_config = ConfigDict(
        from_attributes=True,
        use_enum_values=True,
        validate_assignment=True
    )

