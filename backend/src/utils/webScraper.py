from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from src.utils.logs_config import set_logs_configuration
from selenium.webdriver.common.action_chains import ActionChains
import logging
import platform
import random
import re
import time


class ScraperSelenium():

    def __init__(self, webpage_url:str) -> None:

        self.webpage_url = webpage_url
        self.pattern_nit = r'[^0-9]'
        self.date_pattern = r"\b(19\d\d|20\d\d)[-/](0[1-9]|1[0-2])[-/](0[1-9]|[12]\d|3[01])\b"
        self.attempts = 10

    def find_dane_elements(self,cufe:str):

        set_logs_configuration()

        # Contador de intentos

        count = 0

        # En caso de tranajar en docker o local se hará una configuración diferente

        if platform.system() == "Linux":
            # Setup Chrome options
            chrome_options = Options()
            chrome_options.add_argument("--headless")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--disable-gpu")  # This is important for some versions of Chrome
            chrome_options.add_argument("--remote-debugging-port=9222")  # This is recommended

            # Set path to Chrome binary
            chrome_options.binary_location = "/opt/chrome/chrome-linux64/chrome"

            # Set path to ChromeDriver
            chrome_service = ChromeService(executable_path="/opt/chromedriver/chromedriver-linux64/chromedriver")

            # Set up driver
            driver = webdriver.Chrome(service=chrome_service, options=chrome_options)
        
        else:
             driver = webdriver.Chrome() 

        try:
            # Se accede a la pagina
            driver.get(self.webpage_url)

            # Se simula un tiempo de espera
            time.sleep(random.randint(0,2))
            
            # Find input text field
            input_text_fname = driver.find_element(By.ID, 'DocumentKey')
            
            # Take a screenshot before entering a value
            driver.save_screenshot("screenshot-1.png")

            # Enter a value in the input text field
            input_text_fname.send_keys(cufe)

            actions = ActionChains(driver)

            # Se realiza varios intentos para vencer el Captcha
            while driver.current_url == self.webpage_url:
                actions.move_by_offset(random.randint(1, 10), random.randint(1, 10)).perform()
                button = driver.find_element(By.CLASS_NAME, 'btn.btn-primary.search-document.margin-top-40')
                
                
                time.sleep(abs(random.gauss(1,2)))
                
                button.click()

                driver.implicitly_wait(3)

                # Si falla retorna none
                if count >= self.attempts:

                    logging.warn("the scrapper is not able to pass the first page. Incorrect cufe or impossible to bit the reCAPTCHA")
  
                    return None, None, None, None, None, None
                
                count = 1 + count

            # Se obtiene los valores buscados
            text = driver.find_elements(By.CLASS_NAME, 'col-md-4')
            table = driver.find_elements(By.CLASS_NAME, "table-responsive")
            download = driver.find_element(By.CLASS_NAME, "downloadPDFUrl")

            # Se toma el link de descarga del pdf
            link = download.get_property('href')
        
            # Se convierte en una lista cada palabra capturada 
            emisor_list = text[1].text.split(" ") 
            receptor_list = text[2].text.split(" ")

            # La cuarta posición se extrae solo los números
            emisor_nit = re.sub(self.pattern_nit, "", emisor_list[3])
            receptor_nit = re.sub(self.pattern_nit, "", receptor_list[3])

            # A partir de la 5 se usauna función que vuelve a unir todo en un solo string
            emisor_name = self._join_name(emisor_list[4:])
            receptor_name = self._join_name(receptor_list[4:])

            # Función que separa cada evento
            events = self._look_for_events(table[1].text.split())
            

            driver.quit()

            return link, emisor_nit, emisor_name, receptor_nit, receptor_name, events
        
        except Exception as e:

            logging.error(f"unexpect error in Scraping {e}")
            raise(Exception)
            

    def _look_for_events(self, table:list):

        events = []

        # Se compone de tres estados:
        # El primero busca el número del evento
        # La siguiente concatena todo el texto hasta encontrar una fecha
        # El ultimo busca la palabra detalle para saber que finalizó con el evento

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
                 
                 events.append(
                     {
                        "eventNumber":number_event,
                         "eventName":type_of_event
                     }
                 )
                 number_event = ""
                 type_of_event = ""

                 state0 = 1
                 state1 = 0
                 state2 = 0

        return events
        
    def _join_name(self, name:list):

        full_sentence = ""
        
        for word in name:
            
            full_sentence += word + " "

        return full_sentence


        
    
if "__main__"== __name__:

    scraper = ScraperSelenium("https://catalogo-vpfe.dian.gov.co/User/SearchDocument")

    print(scraper.find_dane_elements("1f28b0cafdafdfc493c2d2abff1168fe99f56395f8c77f7ae492c31972c404ddc54339e51cad28e7e77277a44ca3664e"))

