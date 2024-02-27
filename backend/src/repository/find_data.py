from src.repository.conector import connection_mongo



def find_data():

    db = connection_mongo("scraper_data_dane")

    collection = db["bill"]

    # 

    # Buscar si ya existe un documento con el mismo identificador único
    existentes = collection.find({})

    for documento in existentes:
        print(documento)

    
    
if "__main__" == __name__:

    find_data()