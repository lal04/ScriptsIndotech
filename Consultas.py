import time
import datetime
import pandas as pd
import sys
import os
import shutil
import requests
from bs4 import BeautifulSoup as sp
from concurrent.futures import ThreadPoolExecutor
inicio = time.time()
 #creamos el incio de sesion salea force
cliente=requests.Session()
#datos para el inico de sesion sale force
data={
    'username': 'briam.acuna@indotechsac.com.fvi',
    'Fingerprint': '%7B%22platform%22:%22Win32%22,%22window%22:%22728x1366%22,%22screen%22:%22768x1366%22,%22color%22:%2224-24%22,%22timezoneOffset%22:%22300%22,%22canvas%22:%221099983893%22,%22sessionStorage%22:%22true%22,%22LocalStorage%22:%22true%22,%22indexDB%22:%22true%22,%22webSockets%22:%22true%22,%22plugins%22:%22PDF%20Viewer:Portable%20Document%20Format%5CnChrome%20PDF%20Viewer:Portable%20Document%20Format%5CnChromium%20PDF%20Viewer:Portable%20Document%20Format%5CnMicrosoft%20Edge%20PDF%20Viewer:Portable%20Document%20Format%5CnWebKit%20built-in%20PDF:Portable%20Document%20Format%5Cn%22,%22drm%22:1,%22languages%22:%5B%22es-419%22,%22es%22,%22es-ES%22,%22en%22,%22en-GB%22,%22en-US%22%5D,%22fonts%22:%22%22,%22codecs%22:%22goEIqgoIQqoCqH4=%22,%22mediaDevices%22:%22audioinput::%5Cnvideoinput::%5Cnaudiooutput::%5Cn%22%7D',
    'ExtraLog': '%5B%7B%22width%22:1366%7D,%7B%22height%22:768%7D,%7B%22language%22:%22es-419%22%7D,%7B%22offset%22:5%7D,%7B%22scripts%22:%5B%7B%22size%22:249,%22summary%22:%22if%20(self%20==%20top)%20%7Bdocument.documentElement.style.v%22%7D,%7B%22size%22:586,%22summary%22:%22var%20SFDCSessionVars=%7B%5C%22server%5C%22:%5C%22https:%5C%5C/%5C%5C/login.sal%22%7D,%7B%22url%22:%22https://telefonicab2b.my.site.com/fvi/jslibrary/SfdcSessionBase208.js%22%7D,%7B%22url%22:%22https://telefonicab2b.my.site.com/fvi/jslibrary/LoginHint208.js%22%7D,%7B%22size%22:26,%22summary%22:%22LoginHint.hideLoginForm();%22%7D,%7B%22size%22:36,%22summary%22:%22LoginHint.getSavedIdentities(false);%22%7D,%7B%22url%22:%22https://telefonicab2b.my.site.com/fvi/jslibrary/baselogin.js%22%7D,%7B%22url%22:%22https://telefonicab2b.my.site.com/marketing/survey/survey1/1386%22%7D,%7B%22url%22:%22https://telefonicab2b.my.site.com/marketing/survey/survey4/1386%22%7D,%7B%22size%22:356,%22summary%22:%22function%20handleLogin()%7Bdocument.login.un.value=doc%22%7D%5D%7D,%7B%22scriptCount%22:10%7D,%7B%22iframes%22:%5B%22https://login.salesforce.com/login/sessionserver212.html%22%5D%7D,%7B%22iframeCount%22:1%7D,%7B%22referrer%22:%22NO_REFERRER%22%7D%5D',
    'pw': 'Lmeeaqenicld0@S',
    'un': 'briam.acuna@indotechsac.com.fvi',
    'pqs': '?startURL=%2Ffvi%2Fhome%2Fhome.jsp&ec=302&inst=5I'
}
#login
cliente.post('https://telefonicab2b.my.site.com/fvi/login', data=data)
#tiempo de respuesta del servidor y tiempo de lectura
timeout=(400,1200)
tiempo_nuevo_intento=2
# Lista de tokens
tokens = [
    "eyJlbWFpbCI6ImFudG9uaW9ydWl6QHlvcG1haWwuY29tIn0.AADEePgISZY5A9WA4WZYtV-7Sy58nsydJGl1s7fR5m0"
    "eyJlbWFpbCI6ImNlc2FyYW50b25paW9AeW9wbWFpbC5jb20ifQ.WfIw_fFlCnUZMZrkzzkCii94BgALS2KFDsk-l4_t79I"
    "eyJlbWFpbCI6InF1aXNwZW1hbWFuaUB5b3BtYWlsLmNvbSJ9.jYmF507RGgv1D5spfi8i0_mxfJMyDJ0aZMBglX9UVWE"
    "eyJlbWFpbCI6ImdlcmFyZG9nYWxpYW5vQHlvcG1haWwuY29tIn0.pUCwheXjwSfJrzIcKmr0dd5PJKSXFxhDKxe2z8LXSzc"
    "eyJlbWFpbCI6ImFudG9uaW9pbmd1cm9AeW9wbWFpbC5jb20ifQ.Rbvm946ELpcmHO2gzWaTEFoxz8-1dfFBdXiDD2g1M6A"
    "eyJlbWFpbCI6InBlZHJvcmZmZm9xdWUxMkB5b3BtYWlsLmNvbSJ9.PW9G-yPsC3S3EU5WywQp4_FubJedsdyKjx4pJcrnMJA",
    "eyJlbWFpbCI6InBlZHJvcm9xdWUxMjM0QHlvcG1haWwuY29tIn0.Nw6dwjTMhqtFH0hugjAmaLeJ07OtD1FP5ELoMRX6TvI",
    "eyJlbWFpbCI6InphbWJyYW5vaW5kb3JlY2hAeW9wbWFpbC5jb20ifQ.OVXpClsbHTEoqvCBYmr4cJdNmoBJfcVPDAf0j1Rduoo",
    "eyJlbWFpbCI6InBlZHJvcmZmZm9xdWUxMkB5b3BtYWlsLmNvbSJ9.PW9G-yPsC3S3EU5WywQp4_FubJedsdyKjx4pJcrnMJA",
    "eyJlbWFpbCI6InphbWJyYW5vX3JhdWxAeW9wbWFpbC5jb20ifQ.-VYSTwJA4XZ2ovyXPCHW8jqF3et1yqKmSsXjFKMbf5A",
    "eyJlbWFpbCI6InphbWJyYW5vX2x1aXNAeW9wbWFpbC5jb20ifQ.7S8BO0yldp6VbVJm77pR7TEyejqrM9dwY21XmqEAMaU",
    "eyJlbWFpbCI6ImFudG9uaW9fcGVyZXpAeW9wbWFpbC5jb20ifQ.BZhww4jSqkSVi7VEv-CGC1K0oIdJMzWKHuPfCGMvMNw",
    "eyJlbWFpbCI6ImFudG9uaW9fZ2VuYXJvQHlvcG1haWwuY29tIn0.03-l_Saa19GQxW_m1rk3UaSXzFapQDPxaqAlj3OsiE4",
    "eyJlbWFpbCI6Im1vdmlzaW5kb3NhY0B5b3BtYWlsLmNvbSJ9.GaJ5gtsiB4EZMRy256fA2y-cOIPQm4bS3sII49hSvdM",
    "seyJlbWFpbCI6Im1vdmlzaW5kb0B5b3BtYWlsLmNvbSJ9.hZGuXA4OopEcjU7WG4y5UueOg4xUtzqz5EJFEh-YtC0",
    "eyJlbWFpbCI6InBlcnVodWFuY2FAeW9wbWFpbC5jb20ifQ.Zh33o6cmcMUbEP6J09cXOqRKV9IBD5r7ZqI7NZdv3U0",
    "eyJlbWFpbCI6InRlY2hodWFuY2FAeW9wbWFpbC5jb20ifQ.h8fbWLXZFChT22pihxPtLk2UAVorZE_e2oAQ8kMfnEU",
    "eyJlbWFpbCI6InRlY2hodWFuY2F5b0B5b3BtYWlsLmNvbSJ9.cVR4oRYqQ-EafRFzBWypdaqwQbmpRcJwn_TX4XdifTg",
    "eyJlbWFpbCI6ImluZG9odWFuY2F5b0B5b3BtYWlsLmNvbSJ9.kzMV4bUq84jynZO45VFPjZeFrK9kYYJW3MRQmUtNfz4",
    "eyJlbWFpbCI6InJhdWx6YW1icmFub2xlb24xNUBnbWFpbC5jb20ifQ.g6gEVC4z1ZkED9Rk6Z1EyYtiSqqBoAGziyUr6JEtJ5Y",
    "eyJlbWFpbCI6InJhYW1icmFub2wxODg4NUB5b3BtYWlsLmNvbSJ9.fWKi-gBFzGRmD9z205FnFbfEvEaRjpC8WXNf_nUDRZY",
    "eyJlbWFpbCI6ImluZG9zYWMxOTk5NUB5b3BtYWlsLmNvbSJ9.HtFi0vOxo16FWKnc1teM75iespYQkFvj_z5f7OroGUE",
    "eyJlbWFpbCI6ImdzamdraGwyNzUydW5vQHlvcG1haWwuY29tIn0.gZ0JplbkRVDM0oipA_T1orACpEP9nqcY4WVChXRWMoo",
    "eyJlbWFpbCI6ImdzZ2ZzYnhjYjE1NjU2QHlvcG1haWwuY29tIn0.tiYQr6NYoGlPXnhW-SKmo-VF0QX0E1OrKV2IH0_D3QA",
    "eyJlbWFpbCI6ImdzZ2ZzYnhjYkB5b3BtYWlsLmNvbSJ9.eVnla4m-RLYdWAsNvKUrr4XuzkC7vP1PGujAL2ZlDuY",
    "eyJlbWFpbCI6Imx1aXNmZW9saXMxNTZnZ2dnQHlvcG1haWwuY29tIn0.yvXWOH2IX9iZczU6Eu8uWQUUjxUr0vmIJvSgmB9G0JQ",
    "eyJlbWFpbCI6Imx1aXNmZWxpcGVzb2xpczE1NmdnZ2dAeW9wbWFpbC5jb20ifQ.dag7T-qVrkCROSUgroKau0mgHG96Xm9OwMpYyHVfmVo",
    "eyJlbWFpbCI6Imx1aXNmZWxpcGVzb2xpczE1NkB5b3BtYWlsLmNvbSJ9.J7aThA0-I17zu0XUhGf6r6IxMKc8ajvyJRkBbxKbXko",
    "eyJlbWFpbCI6Imx1aXNmZWxpcGVzb2xpc0B5b3BtYWlsLmNvbSJ9.IrxVsrGwUqi9cvAC8ctbmn510-tyDb8TsM7DxvYBfiI",
    "eyJlbWFpbCI6ImluZG9zYWNodWFuY2F5bzE1NkB5b3BtYWlsLmNvbSJ9.uQnLh1N2ZZgKer-alsMikVGAeNZEGrVgdkwdAma3UOQ",
    "eyJlbWFpbCI6ImluZG9zYWNodWFuY2F5b0B5b3BtYWlsLmNvbSJ9.JmRLSTNnZYjZMG1eeRd_7a0QkcBdRoySBwqpxXYvHtA",
    "eyJlbWFpbCI6InBlcGl0b2VsdGVsaWJsZTEyM0B5b3BtYWlsLmNvbSJ9.TGpokHZbl1OGy_vkoT_jAUHIfaiCIENSeRcAVEmbzB8",
    "eyJlbWFpbCI6InBlZHJvcmZmZm9xZTEyQHlvcG1haWwuY29tIn0.liDj7dnMAx66tXG52nClSF0X_jie50f0B3VS1-12neU",
    "eyJlbWFpbCI6ImdhdG8zMmx1aXNtYW5yaXF1ZTE1M0B5b3BtYWlsLmNvbSJ9.ABwIPRJaCg22NOyVK8v61boNDN-X7eH1sT_2gPObo7o",
    "eyJlbWFpbCI6ImZyZXVoYXByZWZyYXZ1LTg5MDhAeW9wbWFpbC5jb20ifQ.naemhvjjUl7uKlr9VQISB3TbWL54_8SI7cGTupKIhMM",
    "eyJlbWFpbCI6InBlcnJpdG9maWp1MTUyMjJAeW9wbWFpbC5jb20ifQ.R2ogdSfsNEED4gOXSvS1sAJPfhKkhrk3VRJhRW3_B1c",
    "eyJlbWFpbCI6ImdhdG8zMmx1aXNtYW5yaXF1ZUB5b3BtYWlsLmNvbSJ9.NHlyEB_ToEj63JrpBueNC-dAll7h-k6HFVwlfupV-JQ",
    "eyJlbWFpbCI6InBlcnJpdG9maWp1QHlvcG1haWwuY29tIn0.1klG2kbigPiUZOfygGmKlT67kLUtVHRY4JAzNgEX8EA",
    "Fin"
]
def consultar_ruc(ruc, token):
    try:
        print(ruc)
        url = f"https://dniruc.apisperu.com/api/v1/ruc/{ruc}?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.{token}"
        response = requests.get(url,timeout=timeout)
        saleforce=consultar_sale(ruc)
        if response.status_code == 200:
            data = response.json()
            success_value = data.get("success", 'FALSO')
            if success_value:
                # Filtrar el JSON según las claves deseadas
                claves = ["ruc", "razonSocial", "estado", "condicion", "direccion", "departamento", "provincia", "distrito"]
                data_filtrado = {k: v for k, v in data.items() if k in claves}
                data_filtrado.update(saleforce)
                data_con_fecha={
                    "fecha": datetime.datetime.now().strftime("%d/%m/%Y")
                }
                data_con_fecha.update(data_filtrado)
                return data_con_fecha
            else:
                # Si "success" es Falso, devuelve un diccionario personalizado
                No_encontrado={
                    "fecha": datetime.datetime.now().strftime("%d/%m/%Y"),
                    "ruc": ruc,
                    "estado": "No activo",
                }
                No_encontrado.update(saleforce)
                #print(No_encontrado)
                return No_encontrado
        elif response.status_code == 401:
            # Cambia el token e intenta nuevamente
            print(f"Token {token} ha alcanzado su límite. Cambiando a siguiente token.")
            new_token = next_token()
            global current_token  # Asegura que la variable global sea modificada
            current_token = new_token  # Actualiza el token actual
            return consultar_ruc(ruc, new_token)
    except requests.exceptions.ConnectionError as e:
        print(f"Error de conexión en consultar_sale: {e}")
        print(f"consulta ruc, esperamos {tiempo_nuevo_intento} segundos...")
        time.sleep(tiempo_nuevo_intento)
        return consultar_ruc(ruc, token)  # Reintento de la solicitud    
def consultar_sale(ruc):
    try: 
        #consulta de ruc con sesion iniciada
        url2=f'https://telefonicab2b.my.site.com/fvi/_ui/search/ui/UnifiedSearchResults?searchType=2&sen=001&sen=003&sen=005&sen=500&sen=006&str={ruc}'
        response=cliente.get(url2, timeout=timeout)
        html=response.text
        # Crear un objeto BeautifulSoup
        soup = sp(html, 'html.parser')
        # Usar el método find o find_all de BeautifulSoup para seleccionar la tabla con la clase list
        table = soup.find('table', class_='list') # Puedes usar find_all si hay más de una tabla con esa clase
        if table == None:
            data_saleForce={
                    'Nodo':'No encontrado',
                    'Sub segmento global':'',
                    'Sub segmento local':'',
                    'contacto': '',          
                }
            return data_saleForce
        else:
            # Usar el método find_all de BeautifulSoup para seleccionar todos los elementos a que tienen el atributo href dentro de la tabla
            links = table.find_all('a', href=True)
            consulta=links[-3].get('href')
            #entremos a la informacion del ruc encontrado
            response=cliente.get(f'https://telefonicab2b.my.site.com{consulta}')
            html=response.text
            # Crear un objeto BeautifulSoup
            soup = sp(html, 'html.parser')
            # verificamos que sea un cliente o que el id de la eqiqueta exista
            verifi = soup.find(id="CF00Nw00000097xcg_ilecell")
            if verifi == None:
                data_saleForce={
                    'Nodo':'Error',
                    'Sub segmento global':'',
                    'Sub segmento local':'',
                    'contacto': '',            
                }
                return data_saleForce
            else:
                nodo = soup.find(id="CF00Nw00000097xcg_ilecell").text     
                sub_seg_global=soup.find(id="00Nw0000008XxJ2_ileinner").text
                sub_seg_local=soup.find(id="00Nw0000008XxJ1_ileinner").text
                filas=soup.find('table', class_='list').find_all('tr')
                datos_tabla=[]
        
                for fila in filas:
                    # Encontrar todas las celdas de la fila
                    celdas = fila.find_all(['td', 'th'])
                    # Extraer el texto de cada celda y añadirlo a la lista de datos
                    datos_fila = [celda.get_text(strip=True) for celda in celdas]
                    datos_tabla.append(datos_fila)
                    # Eliminar la primera fila
                    sinEncabezado = datos_tabla[1:]
                
                data_saleForce={
                    'Nodo':nodo,
                    'Sub segmento global':sub_seg_global,
                    'Sub segmento local':sub_seg_local,
                    'contacto': sinEncabezado
                }
            return data_saleForce
    except requests.exceptions.ConnectionError as e:
        print(f"Error de conexión en consultar_sale: {e}")
        print(f"consulta sale, esperamos {tiempo_nuevo_intento} segundos...")
        time.sleep(tiempo_nuevo_intento)
        return consultar_sale(ruc)  # Reintento de la solicitud
def next_token():
    # Retorna el siguiente token en la lista circular
    global current_token
    next_index = (tokens.index(current_token) + 1) % len(tokens)
    # Verificar si llegamos al valor de detencisón
    if tokens[next_index] == "Fin":
        print("Se agotaron las consultas para todos los tokens. Terminando la ejecución.")
        sys.exit()
    return tokens[next_index]
# Inicializa el token actual
current_token = tokens[0]
print('poner nombre excacto, para podre mover los archivos')
nombreArchivo=input("ingrese el nombre del archivo: ")
print('Maximo:15\nMinimo:4')
hilos=int(input('ingrese el numero de hilos: '))
#analizamos el archivo excel
df = pd.read_excel(f"{nombreArchivo}.xlsx")
#######
# Utilizar ThreadPoolExecutor para realizar consultas en paralelo
with ThreadPoolExecutor(max_workers=hilos) as executor:
    # Convertir nombres de columnas a minúsculas y seleccionar solo la columna 'ruc'
    df.columns = map(str.lower, df.columns)  # Convertir nombres de columnas a minúsculas
    #lista_json = df["RUC"].map(lambda ruc: consultar_ruc(ruc, current_token))
    lista_json = list(executor.map(lambda ruc: consultar_ruc(ruc, current_token), df["ruc"]))
#ordenamos las columnas del excel
orden_columnas = [
    "fecha",
    "ruc",
    "razonSocial",
    "estado",
    "condicion",
    "direccion",
    "departamento",
    "provincia",
    "distrito",
    "Nodo",
    "Sub segmento global",
    "Sub segmento local",
    "contacto"]
df_final = pd.json_normalize(lista_json)
df_final_ordenado = df_final[orden_columnas]

# Ordenar el DataFrame por la columna 'Nombre' de forma alfabética
df_ordenado = df_final_ordenado.sort_values(by='departamento')

df_ordenado.to_excel(f"{nombreArchivo}SF.xlsx", index=False)
try:
    ###mover archivos creados
    # Obtener la ruta actual de la carpeta
    ruta_actual = os.path.abspath(f"{nombreArchivo}SF.xlsx")
    # Carpeta de destino
    ruta_destino=ruta_actual.replace(f'3.Bloque\\{nombreArchivo}SF.xlsx', f'4.Filtrado\\{nombreArchivo}SF.xlsx')
    #mover archivo
    shutil.move(ruta_actual, ruta_destino)
    ###mover archivo base a completados
    # Carpeta de destino
    completado=ruta_actual.replace(f'{nombreArchivo}SF.xlsx', f'completados\\{nombreArchivo}.xlsx')
    completado=ruta_actual.replace(f'{nombreArchivo}SF.xlsx', f'completados\\{nombreArchivo}.xlsx')
    #mover archivo
    shutil.move(f'{nombreArchivo}.xlsx',completado)
    print('Archivos movidos correctamente!!')
except:
    print('Ocurrio un error!! no se movieron los archivos')
fin = time.time()
print("Tiempo de ejecucion:", fin - inicio)
input("presione enter para terminar")