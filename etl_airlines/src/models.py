from pydantic import BaseModel
from typing import Optional

class FlightRecord(BaseModel):
    Year: int
    Month: int
    DayofMonth: int 
    UniqueCarrier: str 
    FlightNum: int
    ArrDelay: Optional[float] = None
    DepDelay: Optional[float] = None
    Origin: str
    Dest: str
    Distance: int
    Cancelled: int
    CancellationCode: Optional[str] = None
    CarrierDelay: Optional[float] = None
    WeatherDelay: Optional[float] = None
    Diverted: int