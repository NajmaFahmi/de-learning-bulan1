from src.models import FlightRecord
from src.transformer import transform_data


### Create testing for transform function

## 1. Test 'is_delayed'
def test_is_delayed():
    # raw data (yg sama saat di extract, sebelum di transform)
    data = FlightRecord(
        Year = 2008, 
        Month = 1, 
        DayofMonth = 3, 
        UniqueCarrier = 'WN', 
        FlightNum = 335, 
        Origin = 'IAD', 
        Dest = 'TPA', 
        Distance = 810, 
        Cancelled = 0, 
        CancellationCode = 'N', 
        ArrDelay = -14.0, 
        DepDelay = 20.0, 
        WeatherDelay = None, 
        CarrierDelay = None, 
        Diverted = 0
    )

    result = transform_data([data])
    assert result[0]['is_delayed'] == True


## 2. Test 'DistanceCategory'
def test_distance_category():
    # raw data (yg sama saat di extract)
    data = FlightRecord(
        Year = 2008, 
        Month = 1, 
        DayofMonth = 3, 
        UniqueCarrier = 'WN', 
        FlightNum = 335, 
        Origin = 'IAD', 
        Dest = 'TPA', 
        Distance = 1500, 
        Cancelled = 0, 
        CancellationCode = 'N', 
        ArrDelay = -14.0, 
        DepDelay = 20.0, 
        WeatherDelay = None, 
        CarrierDelay = None, 
        Diverted = 0
    )

    result = transform_data([data])
    assert result[0]['DistanceCategory'] == 'Medium'


# 3. Test 'CancellationReason'
def test_cancellation_reason():
    # raw data (yg sama saat di extract)
    data = FlightRecord(
        Year = 2008, 
        Month = 1, 
        DayofMonth = 3, 
        UniqueCarrier = 'WN', 
        FlightNum = 335, 
        Origin = 'IAD', 
        Dest = 'TPA', 
        Distance = 810, 
        Cancelled = 1, 
        CancellationCode = 'B', 
        ArrDelay = None, 
        DepDelay = None, 
        WeatherDelay = None, 
        CarrierDelay = None, 
        Diverted = 0
    )

    result = transform_data([data])
    assert result[0]['CancellationReason'] == "Weather"


# 4. Test 'is_weather_delay'
def test_is_weatherdelay():
    # raw data (yg sama saat di extract)
    data = FlightRecord(
        Year = 2008, 
        Month = 1, 
        DayofMonth = 3, 
        UniqueCarrier = 'WN', 
        FlightNum = 335, 
        Origin = 'IAD', 
        Dest = 'TPA', 
        Distance = 810, 
        Cancelled = 0, 
        CancellationCode = None, 
        ArrDelay = 5.0, 
        DepDelay = 7.0, 
        WeatherDelay = 1, 
        CarrierDelay = 0, 
        Diverted = 0
    )

    result = transform_data([data])
    assert result[0]['is_weather_delay'] == True


# 5. Test 'is_cancelled'
def test_is_cancelled():
    # raw data (yg sama saat di extract)
    data = FlightRecord(
        Year = 2008, 
        Month = 1, 
        DayofMonth = 3, 
        UniqueCarrier = 'WN', 
        FlightNum = 335, 
        Origin = 'IAD', 
        Dest = 'TPA', 
        Distance = 810, 
        Cancelled = 1, 
        CancellationCode = "A", 
        ArrDelay = None, 
        DepDelay = None, 
        WeatherDelay = None, 
        CarrierDelay = None, 
        Diverted = 0
    )

    result = transform_data([data])
    assert result[0]['is_cancelled'] == True
