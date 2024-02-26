from flask import Blueprint, jsonify, request
from jsonschema import validate
from src.utils.webScraper import ScraperSelenium
from src.config  import PATH
import json
import os 

shema_path = os.path.join(PATH, "shema/DANE_petion_post.json")

dian_methods = Blueprint("dian_methods", __name__)

@dian_methods.post("/api/v1/scrape_dian_information")
def get_information_from_dane():

    get_json_post = request.get_json()

    with open(shema_path, 'r') as schema_file:
             schema = json.load(schema_file)

    validate(instance=get_json_post, schema=schema)
  
    
    list_of_cufes = get_json_post["cufes"]

    response ={}

    for cufe in list_of_cufes:

        scraper = ScraperSelenium("https://catalogo-vpfe.dian.gov.co/User/SearchDocument")

        link, emisor_nit, emisor_name, receptor_nit, receptor_name, events = scraper.find_dane_elements(cufe)
        
        response.update(
               { cufe:{
                    "events": events,

                    "sellerInformation":{
                          "Document": emisor_nit,
                          "Name":emisor_name
                    },

                    "receiverInformation":{
                          "Document": receptor_nit,
                          "Name": receptor_name
                    },
                    "linkGraphicRepresentation":link

              } })


    return jsonify(response), 200
