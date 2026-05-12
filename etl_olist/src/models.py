from pydantic import BaseModel
from typing import Optional
from decimal import Decimal
from datetime import datetime


# create pydantic validation class
class OrderRecord(BaseModel):
    order_id: str 
    customer_id: str 
    order_status: str 
    order_purchase_timestamp: datetime      # tadinya str
    order_estimated_delivery_date: Optional[datetime] = None
    order_delivered_customer_date: Optional[datetime] = None
    customer_city: str 
    customer_state: str 
    product_id: Optional[str] = None
    product_category_name: Optional[str] = None
    product_category_name_english: Optional[str] = None
    price: Optional[Decimal] = None              # aslinya float
    freight_value: Optional[float] = None
    seller_id: Optional[str] = None
    payment_type: Optional[str] = None 
    payment_value: Optional[Decimal] = None      # aslinya float 
    review_score: Optional[int] = None