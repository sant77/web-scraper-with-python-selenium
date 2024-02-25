from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

options = webdriver.ChromeOptions() 
options.add_argument("download.default_directory=C:/Users/USUARIO/OneDrive/Escritorio/proyectos trabajo/scraperDian/src")

driver = webdriver.Chrome(options=options)

driver.get("https://catalogo-vpfe.dian.gov.co/User/SearchDocument")

# Find input text field
input_text_fname = driver.find_element(By.ID, 'DocumentKey')
button = driver.find_element(By.CLASS_NAME, 'btn.btn-primary.search-document.margin-top-40')
# Take a screenshot before entering a value
driver.save_screenshot("screenshot-1.png")

# Enter a value in the input text field
input_text_fname.send_keys("1f28b0cafdafdfc493c2d2abff1168fe99f56395f8c77f7ae492c31972c404ddc54339e51cad28e7e77277a44ca3664e")
button.click()
# Take a screenshot after entering a value
driver.save_screenshot("screenshot-2.png")
text = driver.find_elements(By.CLASS_NAME, 'col-md-4')
table = driver.find_elements(By.CLASS_NAME, "table-responsive")
download = driver.find_element(By.CLASS_NAME, "downloadPDFUrl")
print(download.get_property('href'))
#print(text.text)
for elemento in text:
    print(elemento.text)
for elementT in table:
    print(elementT.text)
driver.quit()