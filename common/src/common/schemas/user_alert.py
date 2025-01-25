from typing import Optional

from pydantic import BaseModel


class UserAlertCreate(BaseModel):
    email: str
    min_price: Optional[float] = None
    max_price: Optional[float] = None
    category: Optional[str] = None
    city: Optional[str] = None
    region: Optional[str] = None
    size: Optional[float] = None
    size_flexibility: Optional[bool] = None


class UserAlertResponse(BaseModel):
    id: int
    email: str
    min_price: Optional[float] = None
    max_price: Optional[float] = None
    category: Optional[str] = None
    city: Optional[str] = None
    region: Optional[str] = None
    size: Optional[float] = None
    size_flexibility: Optional[bool] = None

    class Config:
        from_attributes = True
