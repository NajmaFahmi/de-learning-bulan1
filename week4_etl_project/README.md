# ETL Pipeline -- DVD Rental Dataset


## Overview
This pipeline extracts film and rental data from CSV files, applies business transformations, and loads the results into PostgreSQL using an upsert strategy 
for idempotent execution. Built as part of a Data Engineering learning portfolio.



## Architecture
CSV Files → Extract (Pydantic Validation) → Transform (Business Logic) → Load (UPSERT) → PostgreSQL



## Tech Stack
- Python 3.13
- PostgreSQL 16
- pandas — CSV ingestion
- Pydantic — data validation
- SQLAlchemy — database connection and query execution
- pytest — unit testing
- python-dotenv — environment variable management



## Project Structure
week4_etl_project/
    |-- data/
        |-- processed/
        |-- raw/            # source CSV files
    |-- logs/               # pipeline logs
    |-- src/
        |-- __init__.py
        |-- extractor.py    # extract layer: read and validate csv
        |-- transformer.py  # transform layer: business logic
        |-- loader.py       # load layer: upsert to postgresql    
        |-- models.py       # pydantic validation models
        |-- logger.py       # logging setup
    |-- tests/
        |-- __init__.py
        |-- test_extractor.py
        |-- test_loader.py
        |-- test_transformer.py
    |-- .env.example        # environment variable template
    |-- config.py
    |-- main.py             # pipeline entry point
    |-- requirements.txt



## Setup & Installation
1. Clone this repository
2. Create and activate virtual environment:
```bash
   python -m venv venv
   source venv/bin/activate
```
3. Install dependencies:
```bash
   pip install -r requirements.txt
```
4. Copy `.env.example` to `.env` and fill in your credentials:
```bash
   cp .env.example .env
```
5. Create target tables in PostgreSQL:
```sql
   CREATE TABLE IF NOT EXISTS film_transformed (
       film_id INTEGER PRIMARY KEY,
       title VARCHAR(255),
       description TEXT,
       release_year INTEGER,
       rental_duration INTEGER,
       rental_rate NUMERIC(4,2),
       film_length INTEGER,
       rating VARCHAR(10),
       duration_category VARCHAR(10),
       is_premium BOOLEAN
   );

   CREATE TABLE IF NOT EXISTS rental_transformed (
       rental_id INTEGER PRIMARY KEY,
       rental_date TIMESTAMP,
       inventory_id INTEGER,
       customer_id INTEGER,
       return_date TIMESTAMP,
       staff_id INTEGER,
       is_returned BOOLEAN,
       rental_duration_days INTEGER
   );
```
6. Run the pipeline:
```bash
   python main.py
```



## Pipeline Flow
Extract --> Tranform --> Load

1. Extract
Reads `film.csv` and `rental.csv` from `data/raw/`. Each row is validated 
against a Pydantic model — invalid rows are skipped and logged.

2. Transform
Applies business logic to validated records:
- Film: categorize duration, normalize rating, flag premium titles
- Rental: calculate rental duration, flag returned rentals

3. Load
Upserts transformed records into PostgreSQL. If a record already exists 
(conflict on primary key), all columns are updated with the new values.



## Data Transformations
**Film data:**
| Column | Transformation |
|--------|---------------|
| `duration_category` | Short (<60 min), Medium (60-120 min), Long (>120 min) |
| `rating` | Uppercased and whitespace stripped |
| `is_premium` | True if `rental_rate >= 3.99` |
| `rental_rate` | Converted to string for PostgreSQL NUMERIC compatibility |
| `film_length` | Renamed from `length` (reserved word in PostgreSQL) |

**Rental data:**
| Column | Transformation |
|--------|---------------|
| `is_returned` | True if `return_date` is not None |
| `rental_duration_days` | Days between `rental_date` and `return_date` |



## Testing
```bash
pytest tests/ -v
```
Expected output: 11 passed



## Sample Output
2026-05-08 18:54:27 | INFO | main        | Starting pipeline...
2026-05-08 18:54:27 | INFO | extractor   | Extraction complete: 1000 success, 0 errors
2026-05-08 18:54:27 | INFO | transformer | Transformation complete: 1000 success, 0 errors
2026-05-08 18:54:30 | INFO | loader      | Loading complete: 16044 success, 0 errors
2026-05-08 18:54:30 | INFO | main        | Pipeline complete.