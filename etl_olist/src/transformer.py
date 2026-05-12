from typing import List 
from src.models import OrderRecord
from src.logger import get_logger


# logger
logger = get_logger("transformer")


# create transformer function
def transform_data(extracted_data:List[OrderRecord]) -> List[dict]:
    logger.info("Starting data transformation..")
    transformed_data = []
    errors = 0
    
    for row in extracted_data:
        try:
            data = row.model_dump()

            if data['order_delivered_customer_date'] is not None and data['order_estimated_delivery_date'] is not None:
                data['delivery_delay_days'] = (data['order_delivered_customer_date'] - data['order_estimated_delivery_date']).days
                if data['delivery_delay_days'] > 0:
                    data['is_late_delivery'] = True 
                else:
                    data['is_late_delivery'] = False 
            else:
                data['delivery_delay_days'] = None
                data['is_late_delivery'] = None

            
            if data['payment_value'] is not None:
                if data['payment_value'] < 100:
                    data['payment_category'] = "Low"
                elif data['payment_value'] < 500:
                    data['payment_category'] = "Medium"
                else:
                    data['payment_category'] = "High"
            else:
                data['payment_category'] = None 
            

            if data['review_score'] is not None:
                if data['review_score'] <= 2:
                    data['review_category'] = "Bad"
                elif data['review_score'] == 3:
                    data['review_category'] = "Neutral"
                else:
                    data['review_category'] = "Good"
            else:
                data['review_category'] = None
            
            transformed_data.append(data)

        except Exception as e:
            logger.warning(f"Data {data} is skipped because: {e}")
            errors += 1
    

    logger.info(f"Data transformation is complete; {len(transformed_data)} success, {errors} error.")
    return transformed_data