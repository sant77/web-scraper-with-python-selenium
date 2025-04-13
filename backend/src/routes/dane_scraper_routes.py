from flask import Blueprint, jsonify, request
from jsonschema import validate
from src.utils.webScraper import ScraperSelenium
from src.utils.logs_config import set_logs_configuration
from src.repository.insert_update_data import insert_update_data
from src.config  import PATH
import json
import os 
import jsonschema
import logging
from dotenv import load_dotenv
import os

set_logs_configuration()

shema_path = os.path.join(PATH, "shema/DANE_petion_post.json")

dian_methods = Blueprint("dian_methods", __name__)

@dian_methods.post("/api/v1/scrape_dian_information")
def get_information_from_dane():

      try:
            # Se obtiene el json
            get_json_post = request.get_json()

            with open(shema_path, 'r') as schema_file:
                        schema = json.load(schema_file)

            # Se valida el formaro
            validate(instance=get_json_post, schema=schema)
            
            # Se extrae todo lso Cufes
            list_of_cufes = get_json_post["cufes"]

            response ={}
            load_dotenv()
            
            API_KEY_2CAPTCHA = os.environ.get("API_KEY_2CAPTCHA")
            
            for cufe in list_of_cufes:
                  
                  scraper = scraper = ScraperSelenium(
                                          "https://catalogo-vpfe.dian.gov.co/User/SearchDocument",
                                          two_captcha_api_key=API_KEY_2CAPTCHA
                                                )

                  link, emisor_nit, emisor_name, receptor_nit, receptor_name, events = scraper.find_dane_elements(cufe)

                  # Si el Cufe no viene vacio es decir capturó los datos:
                  if emisor_nit != None:

                        data_of_cufe =  { cufe:{
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

                              } }
                        
                        response.update(data_of_cufe)

                        # Se guarda la información
                        insert_update_data(data_of_cufe)

                  else:
                         # Sino se avisa que no fue exitoso la captura
                         response.update({cufe:"Unable to scrape data check out the cufe code or try again"})

            return jsonify(response), 200

      except  jsonschema.ValidationError as e :
            
            logging.warn(f"Incorrect json format:{e}")
            
            return jsonify({"response": 'Incorrect json format'}), 400
      
      except  Exception as e :
            
            logging.error(f"Unexepect error:{e}")
            
            return jsonify({"response": 'Unexepect error'}), 500