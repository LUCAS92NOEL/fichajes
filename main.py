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
url = "https://rodassso.ayesa.com/usuario/Bienvenida.aspx" # URL de la página web a scrapear
ficharHoyIncidencias = 0;
ficharDiasPasados = 1;
urlFechasPasadas = "https://rodassso.ayesa.com/usuario/datosDiarios.aspx?Fecha="
fechasPasadas = ['04/11/2024', '05/11/2024', '06/11/2024', '07/11/2024', '08/11/2024','11/11/2024']

user= "ntrapero@ayesa.com"
passs= "4Y3s4123456789-"
# ***************** FIN PARAMETROS DE ENTRADA *********************


## ABRIR PAGINA
driver = webdriver.Chrome();
driver.get(url)
time.sleep(2)

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

def fichar(hora , entradaSalida):
    button_nueva = driver.find_element(By.ID, "Button_Nueva").click()
    time.sleep(2)
    
    # Encuentra el select PICADA OLVIDADA
    driver.find_element(By.ID, "Dropdown_incidencias2").click()
    option = driver.find_element(By.XPATH, "//option[@value='85']")
    option.click()

    input_element = driver.find_element(By.ID, "TextBox_desde")
    input_element.clear()
    input_element.send_keys(hora)

     # Localiza el campo textarea por su ID
    textarea_element = driver.find_element(By.ID, "TextBox_Observaciones")
    textarea_element.send_keys(entradaSalida)

    # Localiza el botón "Solicitar" usando su ID
    time.sleep(1)
    boton_solicitar = driver.find_element(By.ID, "btnSolicitar").click()
    time.sleep(2)
    

if ficharHoyIncidencias==1:
    element = driver.find_element(By.XPATH, '//div[@class="saldo_semanal col-lg-3 col-md-3 col-xs-3"]/h2/a[@id="Hyperlink_Hoy"]')
    fecha_texto = element.text
    fecha = fecha_texto.split(", ")[1]
    print("fecha {}",fecha)
    link_element = driver.find_element(By.ID, "Hyperlink_Hoy").click()
    time.sleep(1)
    
    # PULSAR SOLICITUDES
    driver.find_elements(By.CSS_SELECTOR, 'ul.nav.nav-tabs li')[1].click()  
    time.sleep(2)
    
    fichar("08:00" , "entrada")
    if isViernes(fecha):
        fichar("14:30" , "salida")
    else:
        fichar("14:00" , "salida")
        fichar("15:00" , "entrada")
        fichar("17:30" , "salida")

if ficharDiasPasados == 1:
    for fecha in fechasPasadas:
        time.sleep(1)
        driver.get(urlFechasPasadas+fecha)
        time.sleep(2)
        driver.find_elements(By.CSS_SELECTOR, 'ul.nav.nav-tabs li')[1].click()    # PULSAR SOLICITUDES
        time.sleep(1)
        ## Comprobar si fichar
        fichar("08:00" , "entrada")
        if isViernes(fecha):
            fichar("14:30" , "salida")
        else:
            fichar("14:00" , "salida")
            fichar("15:00" , "entrada")
            fichar("17:30" , "salida")

time.sleep(120)
    
    