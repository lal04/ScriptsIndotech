import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import pandas as pd
inicio=time.time()

# Define Brave path
brave_path = "C:/Program Files/BraveSoftware/Brave-Browser/Application/brave.exe"
options = webdriver.ChromeOptions()
options.binary_location = brave_path

# Create new automated instance of Brave
#driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options )
listaRuc=[]
NumeroArchivo=int(input('ingrese numeracion de archivo: '))
driver.get('https://www.datosperu.org/')
driver.maximize_window()
print('esta informacion la puedes en punto de partida')
nActividad=int(input('ingrese numero de actividad: '))
print('numero ingresado, sera el minimo de filas para convertir en excel')
condicion=input('ingrese numero minimo de filas: ')
if condicion=='':
    condicion=30000
else:
    condicion=int(condicion)


try:
    #este try itera en las actividades 
    while True:
        #########
        #codigo basura
        actividad=driver.find_element(By.XPATH,f'//*[@id="categorias"]/div[2]/div[{nActividad}]/div/a').text
        print(actividad)
        #########
        #click en la primerta nActividad
        #usamos condicional pra crear excel
        
        driver.find_element(By.XPATH,f'//*[@id="categorias"]/div[2]/div[{nActividad}]/div/a').click()
        nActividad+=1
        try:
            #este try itera en las empresas de cada ciiu de cada actidad
            pagigaCIIU=driver.current_url
            #este try intenta iterar en cada ciiu de cada actividad
            nCIIU=1
            while True:
                ########
                #CODIGO BASURA
                nombreCIIU=driver.find_element(By.XPATH,f'//*[@id="categorias"]/div[3]/div[{nCIIU}]/div/a').text
                print(' ',nombreCIIU)
                #########

                driver.find_element(By.XPATH,f'//*[@id="categorias"]/div[3]/div[{nCIIU}]/div/a').click()
                nCIIU+=1
                nEmpresa=1
                try:
                    npagina=2#inicio de pagina por default
                    paginador=driver.current_url#obtiene el url de de la pagina donde se encuentran listadas las empresas
                    condicion=True
                    while condicion:
                        try:  
                            empresa=driver.find_element(By.XPATH, f'//*[@id="categorias"]/div[3]/div[{nEmpresa}]/div/a').text
                            # Dividir el string en partes utilizando el texto " (RUC: " como separador
                            partes = empresa.split(" (RUC: ")
                           
                            # Obtener el RUC y eliminar el ")" al final
                            ruc = partes[1].replace(")", "")
                            # Crear un diccionario con los datos unificados
                            datos = {
                                "ruc": ruc,
                                }
                            listaRuc.append(datos)
                            nEmpresa+=1
                            print('     ',datos)
                        except:
                            ulrSiguiente=paginador.replace('.php',f'-pagina-{npagina}.php')
                            driver.get(ulrSiguiente)
                            print(len(listaRuc))
                            npagina+=1
                            # Verificar si hay empresas en la nueva página
                            empresas_en_pagina = driver.find_elements(By.XPATH, '//*[@id="categorias"]/div[3]/div')
                            if len(empresas_en_pagina) == 0:
                                
                                    
                                if len(listaRuc) >=condicion:    
                                    #debido a la cantidad demora en convertir a excel
                                    Datosperu=pd.DataFrame(listaRuc)
                                    Datosperu.to_excel(f'rucDatosPeru{NumeroArchivo}.xlsx', index=False)
                                    print(f'Se creo un excel de {len(listaRuc)} filas')
                                    # Abre un archivo en modo de apéndice ('a' para agregar).
                                    # Si el archivo no existe, se creará. Si existe, se escribirá al final.
                                    with open(f'punto de partida-rucDatosPeru{NumeroArchivo}.txt', 'w') as archivo:
                                        # Escribe líneas en el archivo usando el método write().
                                        fin=time.time()
                                        archivo.write(f'tiempo de ejecucion:  {fin-inicio} segundos\n')
                                        inicio=time.time()
                                        archivo.write(f'Se creo un excel de {len(listaRuc)} filas\n')
                                        archivo.write(f'la secuencia debe seguien el:\n Actividad: {nActividad}')
                                        # El archivo se cierra automáticamente después del bloque "with".
                                        print("Contenido agregado al archivo.")
                                    NumeroArchivo+=1
                                    listaRuc=[]
                                print("No hay más empresas en las siguientes páginas.")
                                #regresar a la pagina donde estan los ciiu
                                driver.get(pagigaCIIU)
                                #detenemos el bucle while
                                condicion=False
                            else:
                                #reiniciamos el valor para iterar desde el inicio de la lista de empresas
                                nEmpresa=1
                except:
                    print('son todas las empresas del CIIU')
                    #aqui debemos pasar al siguiente pagina, por el moneto solo damos 'atras'
        except:
            print('esas son todos los ciiu de la actividad\nregresamos a la pagina anterios')
            driver.get('https://www.datosperu.org/')      
except:
    print('esas son todas las actividades')
fin=time.time()
print(f'el tiempo de ejecucion: {fin-inicio}')