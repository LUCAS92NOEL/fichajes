from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
import requests
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
import time
import math

# ***************** INI PARAMETROS DE ENTRADA *********************
url = "https://rodassso.ayesa.com/usuario/Bienvenida.aspx"
ficharHoyIncidencias = 1;
# ***************** FIN PARAMETROS DE ENTRADA *********************


## ABRIR PAGINA
driver = webdriver.Chrome();
driver.get(url)
time.sleep(2)

# URL de la página web a scrapear
url = "https://news.ycombinator.com/"
user= ""
passs= ""

driver.find_element(By.ID, "i0116").send_keys(user)
driver.find_element(By.XPATH, '//input[@class="win-button button_primary button ext-button primary ext-primary"]').click()
time.sleep(2)
driver.find_element(By.ID, "i0118").send_keys(passs)
driver.find_element(By.XPATH, '//input[@class="win-button button_primary button ext-button primary ext-primary"]').click()
time.sleep(15)
def isViernes(fecha_str):
    fecha = datetime.strptime(fecha_str, "%d/%m/%Y")
    # Comprobar el día de la semana (0 = Lunes, 6 = Domingo)
    es_viernes = fecha.weekday() == 4
    # Mostrar resultado
    if es_viernes:
        return 1;#es viernes
    else:
        return 0;


if ficharHoyIncidencias==1:
    element = driver.find_element(By.XPATH, '//div[@class="saldo_semanal col-lg-3 col-md-3 col-xs-3"]/h2/a[@id="Hyperlink_Hoy"]')
    fecha_texto = element.text
    fecha = fecha_texto.split(", ")[1]
    print("fecha {}",fecha)
    link_element = driver.find_element(By.ID, "Hyperlink_Hoy").click()
    time.sleep(2)
    
    # Espera a que el elemento sea visible y luego haz clic en él
    second_li = driver.find_elements(By.CSS_SELECTOR, 'ul.nav.nav-tabs li')[1]  # [1] es el segundo elemento (0 basado)

    # Realiza el clic en el segundo <li>
    second_li.click()

    time.sleep(1)
    button_nueva = driver.find_element(By.ID, "Button_Nueva").click()
    time.sleep(2)

    #Pulsar fichaje olvidado
    select_element = driver.find_element(By.ID, "Dropdown_incidencias2")
    select = Select(select_element)
    select.select_by_value("85")
    
    if isViernes(fecha):
        print("VIERNES")
    else:
        print("Otro Dia de la semana")
        

time.sleep(120)
    
    