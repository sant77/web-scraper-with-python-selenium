from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from src.utils.logs_config import set_logs_configuration
from selenium.webdriver.common.action_chains import ActionChains
import logging
import platform
import random
import re
import time
import requests
from dotenv import load_dotenv
import os

class ScraperSelenium():

    def __init__(self, webpage_url:str, two_captcha_api_key:str = None) -> None:
        self.webpage_url = webpage_url
        self.pattern_nit = r'[^0-9]'
        self.date_pattern = r"\b(19\d\d|20\d\d)[-/](0[1-9]|1[0-2])[-/](0[1-9]|[12]\d|3[01])\b"
        self.attempts = 3  # Reducido porque ahora usaremos 2Captcha
        self.two_captcha_api_key = two_captcha_api_key
        self.cloudflare_sitekey = "0x4AAAAAAAg1WuNb-OnOa76z"  # Sitekey de Cloudflare Turnstile

    def solve_captcha_with_2captcha(self):
        """Resuelve el captcha usando el servicio 2Captcha"""
        if not self.two_captcha_api_key:
            raise ValueError("API key de 2Captcha no proporcionada")
        
        # URL de la página para obtener el parámetro data-action
        page_url = self.webpage_url
        
        # Enviamos la solicitud a 2Captcha
        s = requests.Session()
        captcha_params = {
            'key': self.two_captcha_api_key,
            'method': 'turnstile',
            'sitekey': self.cloudflare_sitekey,
            'pageurl': page_url,
            'json': 1
        }
        
        try:
            # Enviar la solicitud para resolver el captcha
            response = s.post('http://2captcha.com/in.php', data=captcha_params)
            request_id = response.json().get('request')
            
            if not request_id:
                logging.error(f"Error al enviar captcha a 2Captcha: {response.text}")
                return None
                
            # Esperar la solución
            for _ in range(30):  # Máximo 30 intentos (30 segundos)
                time.sleep(1)  # Esperar 1 segundo entre intentos
                result = s.get(f'http://2captcha.com/res.php?key={self.two_captcha_api_key}&action=get&id={request_id}&json=1').json()
                
                if result.get('status') == 1:
                    return result.get('request')  # Token de solución
                    
            logging.error("Tiempo de espera agotado para 2Captcha")
            return None
            
        except Exception as e:
            logging.error(f"Error al resolver captcha con 2Captcha: {e}")
            return None

    def find_dane_elements(self, cufe:str):
        set_logs_configuration()
        count = 0

        if platform.system() == "Linux":
            chrome_options = Options()
            chrome_options.add_argument("--headless")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--remote-debugging-port=9222")
            chrome_options.binary_location = "/opt/chrome/chrome-linux64/chrome"
            chrome_service = ChromeService(executable_path="/opt/chromedriver/chromedriver-linux64/chromedriver")
            driver = webdriver.Chrome(service=chrome_service, options=chrome_options)
        else:
            driver = webdriver.Chrome() 

        try:
            driver.get(self.webpage_url)
            time.sleep(random.randint(1, 3))
            
            # Ingresar el CUFE
            input_text_fname = driver.find_element(By.ID, 'DocumentKey')
            input_text_fname.send_keys(cufe)
            
            # Resolver el captcha con 2Captcha
            captcha_token = self.solve_captcha_with_2captcha()
            if not captcha_token:
                logging.error("No se pudo resolver el captcha con 2Captcha")
                driver.quit()
                return None, None, None, None, None, None
                
            # Inyectar el token de solución en la página
            try:
                wait = WebDriverWait(driver, 10)
                captcha_element = wait.until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, 'input[name="cf-turnstile-response"]'))
                )
                driver.execute_script(f'arguments[0].value = "{captcha_token}";', captcha_element)
            except Exception as e:
                logging.error(f"No se pudo encontrar/inyectar el elemento del captcha: {e}")
                raise
            
            # Hacer clic en el botón de búsqueda
            button = driver.find_element(By.CLASS_NAME, 'btn.btn-primary.search-document.margin-top-40')
            button.click()
            
            # Esperar a que la página cargue (máximo 10 segundos)
            for _ in range(10):
                if driver.current_url != self.webpage_url:
                    break
                time.sleep(1)
            else:
                logging.warn("No se pudo pasar la página de captcha")
                driver.quit()
                return None, None, None, None, None, None

            # Obtener los datos de la página de resultados
            text = driver.find_elements(By.CLASS_NAME, 'col-md-4')
            table = driver.find_elements(By.CLASS_NAME, "table-responsive")
            download = driver.find_element(By.CLASS_NAME, "downloadPDFUrl")
            link = download.get_property('href')
        
            emisor_list = text[1].text.split(" ") 
            receptor_list = text[2].text.split(" ")

            emisor_nit = re.sub(self.pattern_nit, "", emisor_list[3])
            receptor_nit = re.sub(self.pattern_nit, "", receptor_list[3])

            emisor_name = self._join_name(emisor_list[4:])
            receptor_name = self._join_name(receptor_list[4:])

            events = self._look_for_events(table[1].text.split())
            
            driver.quit()
            return link, emisor_nit, emisor_name, receptor_nit, receptor_name, events
        
        except Exception as e:
            logging.error(f"Error inesperado en el scraping: {e}")
            driver.quit()
            raise Exception(e)
            
    def _look_for_events(self, table:list):
        events = []
        state0 = 1
        state1 = 0
        state2 = 0
        patron_numeros = r'^\d+$'
        number_event = ""
        type_of_event = ""

        for i in table[9:]:
            num = re.match(patron_numeros, i)

            if num != None and state0 == 1:
                number_event = i
                state1 = 1
                state0 = 0
                state2 = 0

            if state1 == 1 and i != number_event:
                if re.search(self.date_pattern, i):
                    state2 = 1
                    state1 = 0
                    state0 = 0
                else:
                    type_of_event += i + " "
            
            if state2 == 1 and i == "detalle":
                events.append({
                    "eventNumber": number_event,
                    "eventName": type_of_event
                })
                number_event = ""
                type_of_event = ""
                state0 = 1
                state1 = 0
                state2 = 0

        return events
        
    def _join_name(self, name:list):
        return " ".join(name)

if __name__ == "__main__":
    # Ejemplo de uso con 2Captcha
    load_dotenv()
    API_KEY_2CAPTCHA = os.environ.get("API_KEY_2CAPTCHA")

    scraper = ScraperSelenium(
        "https://catalogo-vpfe.dian.gov.co/User/SearchDocument",
        two_captcha_api_key=API_KEY_2CAPTCHA
    )
    
    print(scraper.find_dane_elements("1f28b0cafdafdfc493c2d2abff1168fe99f56395f8c77f7ae492c31972c404ddc54339e51cad28e7e77277a44ca3664e"))