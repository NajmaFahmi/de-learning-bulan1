from pydantic import BaseModel
from typing import Optional
from decimal import Decimal
from datetime import datetime


## 1. Create Validation Model for film.csv
class FilmRecord(BaseModel):
    film_id: int 
    title: str
    description: str
    release_year: int 
    rental_duration: int 
    rental_rate: Decimal
    length: int 
    rating: str


## 2. Create Validation Model for rental.csv
class RentalRecord(BaseModel):
    rental_id: int 
    rental_date: datetime
    inventory_id: int 
    customer_id: int 
    return_date: Optional[datetime] = None
    staff_id: int
