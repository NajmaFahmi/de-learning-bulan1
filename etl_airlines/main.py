from src.extractor import extract_data
from src.transformer import transform_data
from src.loader import load_data
from src.logger import get_logger


# Activate logger
logger = get_logger("main")


# Rangkai ETL Pipeline
def run_flight_pipeline():
    logger.info("Starting Flight ETL Pipeline...")

    try:
        extracted_data = extract_data()
        transformed_data = transform_data(extracted_data)
        load_data(transformed_data)
        logger.info("Pipeline completed!")

    except Exception as e:
        logger.critical(f"Pipeline Error: {e}")


# Run pipeline
if __name__ == "__main__":
    run_flight_pipeline()