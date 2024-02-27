from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
import time

def connection_mongo(data_base_name, intentos_maximos=3, espera_entre_intentos=5):
    for intento in range(1, intentos_maximos + 1):
        try:
            # Intenta conectar a MongoDB
            client = MongoClient("localhost",
                                 port=27017,
                                 username="usuario_admin",
                                 password="contraseña_admin")
                                 
            db = client[data_base_name]

            return db  # Retorna la conexión exitosa

        except ConnectionFailure as e:
            print(f'Intento {intento}: Error de conexión a MongoDB - {e}')

            if intento < intentos_maximos:
                print(f'Esperando {espera_entre_intentos} segundos antes de intentar nuevamente...')
                time.sleep(espera_entre_intentos)
            else:
                print(f'No se pudo establecer la conexión después de {intentos_maximos} intentos. Saliendo.')
