# ETL Pipeline -- Airlines Delay Dataset



## Overview
This pipeline extracts delayed flights data from CSV files, applies business transformations, and loads the results into PostgreSQL. Built as part of a Data Engineering learning portfolio.



## Architecture
CSV Files → Extract (Pydantic Validation) → Transform (Business Logic) → Load (Truncate & Restart Table) → PostgreSQL



## Tech Stack
- Python 3.13
- PostgreSQL 16
- pandas — CSV ingestion
- Pydantic — data validation
- SQLAlchemy — database connection and query execution
- pytest — unit testing
- python-dotenv — environment variable management



## Project Structure
etl_airlines/
    |-- data/
        |-- processed/
        |-- raw/            # source CSV files
    |-- logs/               # pipeline logs
    |-- src/
        |-- __init__.py
        |-- extractor.py    # extract layer: read and validate csv
        |-- transformer.py  # transform layer: business logic
        |-- loader.py       # load layer: truncate and restart table  
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
    CREATE TABLE IF NOT EXISTS delayed_flights_clean(
        id SERIAL PRIMARY KEY,	
        Year INTEGER,
        Month INTEGER,
        DayofMonth INTEGER,
        UniqueCarrier VARCHAR(10),
        FlightNum INTEGER,
        Origin VARCHAR(10),
        Dest VARCHAR(10),
        Distance INTEGER,
        DistanceCategory VARCHAR(10),
        Cancelled INTEGER,
        is_cancelled BOOLEAN,
        CancellationCode VARCHAR(10),
        CancellationReason VARCHAR(10),
        is_delayed BOOLEAN,
        ArrDelay FLOAT,
        DepDelay FLOAT,
        is_weather_delay BOOLEAN,
        WeatherDelay FLOAT,
        CarrierDelay FLOAT,
        Diverted INTEGER
    );
```
6. Run the pipeline:
```bash
   python main.py
```



## Pipeline Flow
Extract --> Transform --> Load

1. Extract
Reads `DelayedFlights.csv` from `data/raw/`. Each row is validated 
against a Pydantic model — invalid rows are skipped and logged.

2. Transform
Applies business logic to validated records:
specify flight delayed, categorize distance, decode cancellation reason, determine weather delay, assign flight cancelled.

3. Load
Insert transformed records into PostgreSQL. Using truncate table to delete previous records in the table (replaced with this new transformed records) and restart identity to restart serial id.



## Data Transformations
**Flight data:**
| Column | Transformation |
|--------|---------------|
| `is_delayed` | True if `DepDelay` is not None and `DepDelay` > 15 |
| `DistanceCategory` | Short (< 750 miles), Medium (750-2500 miles), Long (> 2500 miles) |
| `CancellationReason` | Carrier (code A), Weather (code B), NAS (code C), Security (code D) |
| `is_weather_delay` | True if `WeatherDelay` is not None and `WeatherDelay` > 0 | 
| `is_cancelled` | True if `Cancelled` == 1 | 



## Testing
```bash
pytest tests/ -v
```
Expected output: 7 passed



## Sample Output
2026-05-09 20:08:16 | INFO | main | Starting Flight ETL Pipeline...
2026-05-09 20:09:49 | INFO | extractor | Extraction complete: 1936758 success, 0 errors
2026-05-09 20:09:58 | INFO | transformer | Transformation complete: 1936758 success, 0 errors
2026-05-09 20:16:21 | INFO | loader | Loading complete: 1936758 success, 0 errors
2026-05-09 20:16:21 | INFO | main | Pipeline completed!