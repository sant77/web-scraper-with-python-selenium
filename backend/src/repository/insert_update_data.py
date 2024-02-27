from src.repository.conector import connection_mongo



def insert_update_data(datos):

    db = connection_mongo("scraper_data_dane")

    collection = db["bill"]

    # Extraer el identificador único
    id_unico = list(datos.keys())[0]

    # Buscar si ya existe un documento con el mismo identificador único
    existente = collection.find_one({'_id': id_unico})

    if existente:
        # Si existe, actualiza el documento
        collection.update_one({'_id': id_unico}, {'$set': datos})
        print(f'Documento actualizado con id {id_unico}')
    else:
        # Si no existe, inserta un nuevo documento
        collection.insert_one({**datos, '_id': id_unico})
        print(f'Nuevo documento insertado con id {id_unico}')
    
if "__main__" == __name__:

    data_test =  {
    "1f28b0cafdafdfc493c2d2abff1168fe99f56395f8c77f7ae492c31972c404ddc54339e51cad28e7e77277a44ca3664a": {
        "events": [
            {
                "eventName": "Acuse de recibo de la Factura Electrónica de Venta ",
                "eventNumber": "030"
            },
            {
                "eventName": "Recibo del bien o prestación del servicio ",
                "eventNumber": "032"
            }
        ],
        "linkGraphicRepresentation": "https://catalogo-vpfe.dian.gov.co/Document/DownloadPDF?trackId=1f28b0cafdafdfc493c2d2abff1168fe99f56395f8c77f7ae492c31972c404ddc54339e51cad28e7e77277a44ca3664e&token=e6c834221210d54c708f0a64b5a6c965ccc13d08623c9c61592779f9ec97abaf",
        "receiverInformation": {
            "Document": "800071617",
            "Name": "CUMMINS DE LOS ANDES S.A "
        },
        "sellerInformation": {
            "Document": "901596817",
            "Name": "COLOMBIA PLATAFORM SAS "
        }
    }
}
    insert_update_data(data_test)