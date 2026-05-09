from src.models import FlightRecord
import pandas as pd
import numpy as np
import config
from typing import List
from src.logger import get_logger


# panggil logger
logger = get_logger("extractor")


# create pydantic validation function (UNTUK DATA ASLI BESAR)
def extract_data() -> List[FlightRecord]:
    logger.info("Starting data extraction")

    data = pd.read_csv(config.AIRLINES_CSV)
    data = data.replace({np.nan: None})
    extracted_data = []
    errors = 0

    for index, row in data.iterrows():
        try:
            validated_row = FlightRecord(**row.to_dict())
            extracted_data.append(validated_row)
        except Exception as e:
            logger.warning(f"Row {row} skipped because: {e}")
            errors += 1
    
    logger.info(f"Extraction complete: {len(extracted_data)} success, {errors} errors")
    return extracted_data




## BUAT FILE UNTUK TESTING
## kalau testing dengan data asli yaitu data besar akan lama, kita ambil sample nya saja
## RUN INI DI TERMINAL
# head -n 10 data/raw/DelayedFlights.csv > tests/sample_flights.csv

# create pydantic validation function (UNTUK DATA TESTING SAJA)
def extract_data_testing(csv_path) -> List[FlightRecord]:
    logger.info("Starting data extraction")
    data = pd.read_csv(csv_path)
    data = data.replace({np.nan: None})
    extracted_data = []
    errors = 0
    for index, row in data.iterrows():
        try:
            validated_row = FlightRecord(**row.to_dict())
            extracted_data.append(validated_row)
        except Exception as e:
            logger.warning(f"Row {row} skipped because: {e}")
            errors += 1
    logger.info(f"Extraction complete: {len(extracted_data)} success, {errors} errors")
    return extracted_data

