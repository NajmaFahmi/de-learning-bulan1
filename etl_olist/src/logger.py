import logging 
import os 
from datetime import datetime 


### Create Log Function
def get_logger(name: str) -> logging.Logger:
    # a. create directory
    os.makedirs("logs", exist_ok=True)

    # b. create logger variable
    logger = logging.getLogger(name)
    # set it's level to debug
    logger.setLevel(logging.DEBUG)

    # c. create logging format
    formatter = logging.Formatter(
        '%(asctime)s | %(levelname)s | %(name)s | %(message)s',
        datefmt = '%Y-%m-%d %H:%M:%S'
    )

    ## d. Create Handler 1 --> write logging in a file
    log_file = f"logs/pipeline_{datetime.now().strftime('%Y%m%d')}.log"
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    ## e. Create Handler 2 --> show logging to the terminal
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)

    ## f. add those 2 handler
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    ## g. return logger
    return logger

