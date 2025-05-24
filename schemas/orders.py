from datetime import datetime
from pydantic import BaseModel, ConfigDict
from db.models.orders import Status


class OrderCreate(BaseModel):
    item_id: int


class OrderRead(BaseModel):
    id: int
    item_id: int
    user_id: int
    created_at: datetime
    updated_at: datetime
    status: Status

    model_config = ConfigDict(
        from_attributes=True,
        use_enum_values=True,
        validate_assignment=True
    )


class OrderUpdate(BaseModel):
    order_id: int
    status: Status
