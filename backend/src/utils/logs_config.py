import logging

def set_logs_configuration():
    # Set up logger
    logging.basicConfig(level=logging.INFO, 
                        format='%(asctime)s - %(levelname)s - %(message)s')
