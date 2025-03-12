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
fechasPasadas = [

  '02/01/2025', '03/01/2025',
  '07/01/2025', '08/01/2025', '09/01/2025', '10/01/2025',
  '13/01/2025', '14/01/2025', '15/01/2025', '16/01/2025', '17/01/2025',
  '20/01/2025', '21/01/2025', '22/01/2025', '23/01/2025', '24/01/2025',
  '27/01/2025', '28/01/2025', '29/01/2025', '30/01/2025', '31/01/2025',

  
  '03/02/2025', '04/02/2025', '05/02/2025', '06/02/2025', '07/02/2025',
  '10/02/2025', '11/02/2025', '12/02/2025', '13/02/2025', '14/02/2025',
  '17/02/2025', '18/02/2025', '19/02/2025', '20/02/2025', '21/02/2025',
  '24/02/2025', '25/02/2025', '26/02/2025', '27/02/2025', '28/02/2025',


  '03/03/2025', '04/03/2025', '05/03/2025', '06/03/2025', '07/03/2025',
  '10/03/2025', '11/03/2025', '12/03/2025'
];

user= "ntrapero@ayesa.com"
passs= "4Y3s412345678911-"
# ***************** FIN PARAMETROS DE ENTRADA *********************


## ABRIR PAGINA
driver = webdriver.Chrome();
driver.get(url)
time.sleep(2)

driver.find_element(By.ID, "i0116").send_keys(user)
driver.find_element(By.XPATH, '//input[@class="win-button button_primary high-contrast-overrides button ext-button primary ext-primary"]').click()
time.sleep(2)
driver.find_element(By.ID, "i0118").send_keys(passs)
driver.find_element(By.XPATH, '//input[@class="win-button button_primary high-contrast-overrides button ext-button primary ext-primary"]').click()
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
    time.sleep(1)

    input_element = driver.find_element(By.ID, "TextBox_desde")
    input_element.clear()
    input_element.send_keys(hora)
    time.sleep(1)

     # Localiza el campo textarea por su ID
    textarea_element = driver.find_element(By.ID, "TextBox_Observaciones")
    textarea_element.send_keys(entradaSalida)
    time.sleep(1)

    # Localiza el botón "Solicitar" usando su ID
    time.sleep(1)
    boton_solicitar = driver.find_element(By.ID, "btnSolicitar").click()
    time.sleep(3)

def validarFichar(horaparam , entradaSalida):
    try:
        table_wrapper = driver.find_element(By.ID, 'DataGrid_solicitudes_wrapper')
        table = table_wrapper.find_element(By.TAG_NAME, 'table')
        rows = table.find_elements(By.TAG_NAME, 'tr')
    except Exception as e:
        print("No hay solicitudes")
        return 1; #hay que fichar

    # Iterar a través de todas las filas encontradas
    for row in rows:
        # Obtener la hora en la columna 6 (índice 5) y las observaciones en la columna 9 (índice 8)
        cells = row.find_elements(By.TAG_NAME, 'td')
        
        if len(cells) >= 9:  # Verificar que la fila tenga suficientes celdas
            hora = cells[5].text.strip()  # Columna 6 (hora)
            observaciones = cells[8].text.strip()  # Columna 9 (observaciones)
            
            # Verificar si la fila contiene los valores buscados
            if hora == horaparam and observaciones == entradaSalida:
                print("Fila encontrada con hora "+hora+" y observaciones "+entradaSalida)
                return 0; # NO hay que fichar
    else:
        print("No se encontró ninguna fila con la condición especificada.")
        return 1; #hay que fichar
    

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
        time.sleep(0.5)
        driver.get('https://rodassso.ayesa.com/usuario/DatosDiarios.aspx')
        time.sleep(0.5)

        calendario = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.ID, "acCalendarioMensual"))
)

# Buscar el enlace para la fecha "2 de enero" dentro del calendario
fecha_enero_2 = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//a[@title='2 de enero']"))
)

# Hacer clic en el enlace para seleccionar la fecha
fecha_enero_2.click()

        time.sleep(1.5)
        driver.find_elements(By.CSS_SELECTOR, 'ul.nav.nav-tabs li')[1].click()    # PULSAR SOLICITUDES
        time.sleep(0.5)
        ## Comprobar si fichar
        if validarFichar("08:00" , "entrada") == 1:
            fichar("08:00" , "entrada")
        if isViernes(fecha):
            if validarFichar("14:30" , "salida") == 1:
                fichar("14:30" , "salida")
        else:
            if validarFichar("14:00" , "salida") == 1:
                fichar("14:00" , "salida")
            if validarFichar("15:00" , "entrada") == 1:
                fichar("15:00" , "entrada")
            if validarFichar("17:30" , "salida") == 1:
                fichar("17:30" , "salida")

time.sleep(120)
    
    