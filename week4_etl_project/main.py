from src.extractor import extract_films, extract_rentals
from src.transformer import transform_films, transform_rentals
from src.loader import load_films, load_rentals
from src.logger import get_logger


## Activate Logger
logger = get_logger("main")


## Rangkai ETL Pipeline
def run_pipeline():
    # logging (start)
    logger.info("Starting pipeline...")

    try:
        # Extract Data
        films = extract_films()
        rentals = extract_rentals()

        # Transform Data
        transformed_films = transform_films(films)
        transformed_rentals = transform_rentals(rentals)

        # Load Data into Database
        load_films(transformed_films)
        load_rentals(transformed_rentals)

        # logging (finish)
        logger.info("Pipeline complete.")

    except Exception as e:
        # logging (error)
        logger.critical(f"Error: {e}")


## Run Pipeline
if __name__ == "__main__":
    run_pipeline()