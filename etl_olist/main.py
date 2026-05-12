from src.extractor import extract_data
from src.transformer import transform_data
from src.loader import load_data
from src.logger import get_logger


## Activate Logger
logger = get_logger("main")


## Rangkai ETL Pipeline
def run_pipeline():
    # logging (start)
    logger.info("Starting Olist ETL pipeline...")

    try:
        # Extract Data
        olist_data = extract_data()

        # Transform Data
        transformed_data = transform_data(olist_data)

        # Load Data into Database
        load_data(transformed_data)

        # logging (finish)
        logger.info("Pipeline complete.")

    except Exception as e:
        # logging (error)
        logger.critical(f"Error: {e}")


## Run Pipeline
if __name__ == "__main__":
    run_pipeline()