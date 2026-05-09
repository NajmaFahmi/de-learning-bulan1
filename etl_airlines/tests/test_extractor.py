from src.models import FlightRecord
from src.extractor import extract_data_testing
from typing import List 


# create testing for extractor function
sample_data = "tests/sample_flights.csv"

def test_extraction_data():
    extracted_data = extract_data_testing(sample_data)
    assert len(extracted_data) == 9     # 10 data = 9 records, 1 head


# create testing for the output
def test_output_extraction():
    extracted_data = extract_data_testing(sample_data)
    assert all(isinstance(f, FlightRecord) for f in extracted_data)