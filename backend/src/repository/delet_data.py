from src.repository.conector import connection_mongo


def delet_all_data():

    db = connection_mongo("scraper_data_dane")

    collection = db["bill"]

    # 

    # Buscar si ya existe un documento con el mismo identificador único
    existente = collection.delete_many({})

    return existente
    
if "__main__" == __name__:

    print(delet_all_data())