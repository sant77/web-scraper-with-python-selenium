from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from src.utils.logs_config import set_logs_configuration
from dotenv import load_dotenv
import time
import logging
import os
def connection_mongo(data_base_name, max_attempts=3, delay=5):

    set_logs_configuration()

    for attempt in range(1, max_attempts + 1):

        try:
            load_dotenv()
            
            host_mongo = os.environ.get("host_mongo")
            port_mongo = os.environ.get("port_mongo")
            user_mongo = os.environ.get("user_mongo")
            password_mongo = os.environ.get("password_mongo")

            # Intenta conectar a MongoDB
            client = MongoClient(host_mongo,
                                 port=int(port_mongo),
                                 username=user_mongo,
                                 password=password_mongo)
                                 
            db = client[data_base_name]

            return db  # Retorna la conexión exitosa

        except ConnectionFailure as e:
            logging.error(f'attempts {attempt}: error connecting to  MongoDB - {e}')

            if attempt < max_attempts:
                logging.info(f'waiting {delay} seconds before to new attempts...')
                time.sleep(delay)
            else:
                logging.warn(f'Could not stablish connection after {max_attempts} attempts.')
                raise(ConnectionFailure)

        except Exception as e:
            logging.error(f"unexpect error {e}")
            raise(Exception)
