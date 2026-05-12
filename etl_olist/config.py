import os 
from dotenv import load_dotenv

load_dotenv()

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "latihan_de")
DB_USER = os.getenv("DB_USER", "najma")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")


DATABASE_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

RAW_DATA_DIR = "data/raw"
ORDERS_CSV = f"{RAW_DATA_DIR}/olist_orders_dataset.csv"
CUSTOMERS_CSV = f"{RAW_DATA_DIR}/olist_customers_dataset.csv"
ORDER_ITEMS_CSV = f"{RAW_DATA_DIR}/olist_order_items_dataset.csv"
PAYMENTS_CSV = f"{RAW_DATA_DIR}/olist_order_payments_dataset.csv"
REVIEWS_CSV = f"{RAW_DATA_DIR}/olist_order_reviews_dataset.csv"
PRODUCTS_CSV = f"{RAW_DATA_DIR}/olist_products_dataset.csv"
SELLERS_CSV = f"{RAW_DATA_DIR}/olist_sellers_dataset.csv"
ENGLISH_PRODUCT_CSV = f"{RAW_DATA_DIR}/product_category_name_translation.csv"