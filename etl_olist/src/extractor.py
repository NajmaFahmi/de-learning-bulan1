from src.models import OrderRecord
from typing import List
import pandas as pd
import numpy as np
import config
from src.logger import get_logger


# logger
logger = get_logger("extractor")


# create extraction function
def extract_data() -> List[OrderRecord]:
    logger.info("Starting raw data extraction..")

    df_orders = pd.read_csv(config.ORDERS_CSV)
    df_customers = pd.read_csv(config.CUSTOMERS_CSV)
    df_order_items = pd.read_csv(config.ORDER_ITEMS_CSV)
    df_payments = pd.read_csv(config.PAYMENTS_CSV)
    df_reviews = pd.read_csv(config.REVIEWS_CSV)
    df_products = pd.read_csv(config.PRODUCTS_CSV)
    df_sellers = pd.read_csv(config.SELLERS_CSV)
    df_english_product = pd.read_csv(config.ENGLISH_PRODUCT_CSV)

    merged_data = pd.merge(df_orders, df_customers,
                           on='customer_id', how='left')
    merged_data = pd.merge(merged_data, df_order_items,
                           on='order_id', how='left')
    merged_data = pd.merge(merged_data, df_payments,
                           on='order_id', how='left')
    merged_data = pd.merge(merged_data, df_reviews,
                           on='order_id', how='left')
    merged_data = pd.merge(merged_data, df_products,
                           on='product_id', how='left')
    merged_data = pd.merge(merged_data, df_sellers,
                           on='seller_id', how='left')
    merged_data = pd.merge(merged_data, df_english_product,
                           on='product_category_name', how='left')

    merged_data = merged_data.replace({np.nan: None})

    extracted_data = []

    for index, row in merged_data.iterrows():
        try:
            record = OrderRecord(**row.to_dict())
            extracted_data.append(record)
        except Exception as e:
            print(f"Row {index} skipped beacuse: {e}")
            logger.warning(f"Extraction is failed because: {e}")
    
    logger.info(f"Extraction data is completed with: {len(extracted_data)} data.")
    return extracted_data
