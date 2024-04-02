
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import pandas as pd


# Define Brave path
brave_path = "C:/Program Files/BraveSoftware/Brave-Browser/Application/brave.exe"
options = webdriver.ChromeOptions()
options.binary_location = brave_path

# Create new automated instance of Brave
#driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options )
listaRuc=[]
def creaExcel(listaRuc):
    print(len(listaRuc))
    global NumeroArchivo
    if len(listaRuc) >=10000:    
        #debido a la cantidad demora en convertir a excel
        Datosperu=pd.DataFrame(listaRuc)
        Datosperu.to_excel(f'rucDatosPeru{NumeroArchivo}.xlsx', index=False)
        print(f'de creo un excel de {len(listaRuc)} filas')
        print(f'la secuencia debe seguien el:\n actividad: {nActividad+1}\nCIIU:{nCIIU+1}\nempresa: {nEmpresa+1}\n Pagina: {npagina+1}')
        NumeroArchivo+=1
        listaRuc=[]
        return listaRuc

NumeroArchivo=2
global NumeroArvhivo

driver.get('https://www.datosperu.org/')
driver.maximize_window()
nActividad=4
try:
    #este try itera en las actividades 
    while True:
        #########
        #codigo basura
        actividad=driver.find_element(By.XPATH,f'//*[@id="categorias"]/div[2]/div[{nActividad}]/div/a').text
        print(actividad)
        #########
        #click en la primerta nActividad
        driver.find_element(By.XPATH,f'//*[@id="categorias"]/div[2]/div[{nActividad}]/div/a').click()
        nActividad+=1
        try:
            #este try itera en las empresas de cada ciiu de cada actidad
            pagigaCIIU=driver.current_url
            #este try intenta iterar en cada ciiu de cada actividad
            nCIIU=8
            while True:
                ########
                #CODIGO BASURA
                nombreCIIU=driver.find_element(By.XPATH,f'//*[@id="categorias"]/div[3]/div[{nCIIU}]/div/a').text
                print(' ',nombreCIIU)
                #########

                driver.find_element(By.XPATH,f'//*[@id="categorias"]/div[3]/div[{nCIIU}]/div/a').click()
                nCIIU+=1
                nEmpresa=22
                try:
                    npagina=26#inicio de pagina por default
                    paginador=driver.current_url#obtiene el url de de la pagina donde se encuentran listadas las empresas
                    condicion=True
                    while condicion:
                        try:  
                            empresa=driver.find_element(By.XPATH, f'//*[@id="categorias"]/div[3]/div[{nEmpresa}]/div/a').text
                            # Dividir el string en partes utilizando el texto " (RUC: " como separador
                            partes = empresa.split(" (RUC: ")
                            # Obtener la razon social
                            razon_social = partes[0]
                            # Obtener el RUC y eliminar el ")" al final
                            ruc = partes[1].replace(")", "")
                            # Verificar si hay nombre comercial presente
                            if " - " in razon_social:
                                nombre_comercial = razon_social.split(" - ")[0]
                                razon_social = razon_social.split(" - ")[1]
                            else:
                                nombre_comercial = ""
                            # Crear un diccionario con los datos unificados
                            datos = {
                                "ruc": ruc,
                                "razon social": razon_social,
                                "nombre comercial": nombre_comercial
                                }
                            listaRuc.append(datos)
                            nEmpresa+=1
                            print('     ',datos)
                        except:
                            ulrSiguiente=paginador.replace('.php',f'-pagina-{npagina}.php')
                            driver.get(ulrSiguiente)
                            npagina+=1
                            # Verificar si hay empresas en la nueva página
                            empresas_en_pagina = driver.find_elements(By.XPATH, '//*[@id="categorias"]/div[3]/div')
                            if len(empresas_en_pagina) == 0:
                                print("No hay más empresas en las siguientes páginas.")
                                #regresar a la pagina donde estan los ciiu
                                driver.get(pagigaCIIU)
                                #detenemos el bucle while
                                condicion=False
                            else:
                                #reiniciamos el valor para iterar desde el inicio de la lista de empresas
                                nEmpresa=1
                except:
                    nuevaLista=creaExcel(listaRuc)
                    listaRuc=nuevaLista
                    print('son todas las empresas del CIIU')
                    #aqui debemos pasar al siguiente pagina, por el moneto solo damos 'atras'
        except:
            print('esas son todos los ciiu de la actividad\nregresamos a la pagina anterios')
            driver.get('https://www.datosperu.org/')
except:
    print('esas son todas las actividades')




print('fin')