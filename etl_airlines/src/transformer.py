from src.models import FlightRecord
from typing import List
from src.logger import get_logger


# activate logging
logger = get_logger("transformer")


# create transform function
def transform_data(extracted_data: List[FlightRecord]) -> List[dict]:
    logger.info("Starting data transformation")
    transformed_data = []
    errors = 0

    for row in extracted_data:
        try:
            # convert object data into dict
            data = row.model_dump()

            # flight was delayed or not
            if data['DepDelay'] is not None and data['DepDelay'] > 15:
                data['is_delayed'] = True
            else:
                data['is_delayed'] = False
            
            # categorize distance
            if data['Distance'] < 750:
                data['DistanceCategory'] = "Short"
            elif data['Distance'] < 2500:
                data['DistanceCategory'] = "Medium"
            else:
                data['DistanceCategory'] = "Long"
            
            # decode cancellation reason
            if data['CancellationCode'] == "A":
                data['CancellationReason'] = "Carrier"
            elif data['CancellationCode'] == "B":
                data['CancellationReason'] = "Weather"
            elif data['CancellationCode'] == "C":
                data['CancellationReason'] = "NAS"
            elif data['CancellationCode'] == "D":
                data['CancellationReason'] = "Security"
            else:
                data['CancellationReason'] = None
            
            # was delay caused by weather or not
            if data['WeatherDelay'] is not None and data['WeatherDelay'] > 0:
                data['is_weather_delay'] = True 
            else:
                data['is_weather_delay'] = False 
            
            # was flight cancelled or not
            if data['Cancelled'] == 1:
                data['is_cancelled'] = True 
            else:
                data['is_cancelled'] = False
            
            # change column order
            new_order = ['Year', 'Month', 'DayofMonth', 'UniqueCarrier', 'FlightNum',
                        'Origin', 'Dest', 'Distance', 'DistanceCategory', 'Cancelled',
                        'is_cancelled', 'CancellationCode', 'CancellationReason',
                        'is_delayed', 'ArrDelay', 'DepDelay', 'is_weather_delay',
                        'WeatherDelay', 'CarrierDelay', 'Diverted']
            reordered_data = {key: data[key] for key in new_order}

            # add into a new list
            transformed_data.append(reordered_data)
        
        except Exception as e:
            logger.warning(f"Row {row} skipped, because: {e}")
            errors += 1
    
    logger.info(f"Transformation complete: {len(transformed_data)} success, {errors} errors")
    return transformed_data
