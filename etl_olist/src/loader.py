from sqlalchemy import create_engine, text
from typing import List
import config
from src.logger import get_logger


# logger
logger = get_logger("loader")


## Create Engine
engine = create_engine(config.DATABASE_URL)


## Insert Data into Table (Data Film)
def load_data(transformed_data: List[dict]) -> None:
    logger.info("Starting data loading..")
    errors = 0

    with engine.connect() as conn:
        for data in transformed_data:
            try:
                conn.execute(text("""
                        insert into olist_orders_table (order_id,customer_id,order_status,order_purchase_timestamp,
                                order_estimated_delivery_date,order_delivered_customer_date,customer_city,
                                customer_state,product_id,product_category_name,product_category_name_english,
                                price,freight_value,seller_id,payment_type,payment_value,review_score,delivery_delay_days,
                                is_late_delivery,payment_category,review_category)
                        values (:order_id,:customer_id,:order_status,:order_purchase_timestamp,:order_estimated_delivery_date,
                                :order_delivered_customer_date,:customer_city,:customer_state,:product_id,:product_category_name,
                                :product_category_name_english,:price,:freight_value,:seller_id,:payment_type,:payment_value,:review_score,
                                :delivery_delay_days,:is_late_delivery,:payment_category,:review_category)
                        on conflict (order_id)
                        do update set
                                customer_id = excluded.customer_id ,
                                order_status = excluded.order_status ,
                                order_purchase_timestamp = excluded.order_purchase_timestamp ,
                                order_estimated_delivery_date = excluded.order_estimated_delivery_date ,
                                order_delivered_customer_date = excluded.order_delivered_customer_date ,
                                customer_city = excluded.customer_city ,
                                customer_state = excluded.customer_state ,
                                product_id = excluded.product_id ,
                                product_category_name = excluded.product_category_name ,
                                product_category_name_english = excluded.product_category_name_english ,
                                price = excluded.price ,
                                freight_value = excluded.freight_value ,
                                seller_id = excluded.seller_id,
                                payment_type = excluded.payment_type ,
                                payment_value = excluded.payment_value ,
                                review_score = excluded.review_score ,
                                delivery_delay_days = excluded.delivery_delay_days ,
                                is_late_delivery = excluded.is_late_delivery ,
                                payment_category = excluded.payment_category ,
                                review_category = excluded.review_category
                """), data)
            except Exception as e:
                logger.critical(f"Data {data} is skipped because: {e}")
                errors += 1

        logger.info(f"Loading data is completed with {errors} error.")
        conn.commit()
