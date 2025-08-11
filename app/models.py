from datetime import date
from pydantic import BaseModel, Field
from typing import Optional


class SearchRequest(BaseModel):
    destination: str = Field(..., description="שם יעד: עיר או אזור")
    check_in: date = Field(..., description="תאריך כניסה (YYYY-MM-DD)")
    check_out: date = Field(..., description="תאריך יציאה (YYYY-MM-DD)")


class SearchResult(BaseModel):
    hotel_name: str
    city: str
    region: str
    price_per_night: float
    nights: int
    total_price: float


class Hotel(BaseModel):
    id: int
    name: str
    city: str
    region: str
    price_per_night_for_two: float