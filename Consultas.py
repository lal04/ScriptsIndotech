import time
import datetime
import pandas as pd
import sys
import os
import re
from src.token import Token
from src.saleforce import Saleforce
import shutil
import requests
from concurrent.futures import ThreadPoolExecutor
tk=Token()
 #creamos el incio de sesion salea force
sf=Saleforce()
sf.inicio_sesion()

inicio = time.time()
#tiempo de respuesta del servidor y tiempo de lectura
timeout=(400,1200)
tiempo_nuevo_intento=2
# Lista de tokens
respuesta=input("Tienes tokens para ingresar?(si,no,s,n,)\n>").lower()
if respuesta in ["si","s"]:

    for i in range(int(input("Cuantos tokens?\n>"))):
        tk.agregar_token(input(f"Ingrese el token {i+1}: "))
tokens = tk.obtener_lista_tokens()
respuesta=input("Desea ordenar los tokens?(si,no,s,n,)\nPuede tomar unos minutos!!\n>").lower()
if respuesta in ["si","s"]:
    print("Orenando tokens...")
    tk.ordenar_tokens(tokens)

def consultar_ruc(ruc, token):
    try:
        print(ruc)
        url = f"https://dniruc.apisperu.com/api/v1/ruc/{ruc}?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.{token}"
        response = requests.get(url,timeout=timeout)
        campos_a_consultar=["Nodo", "Sub segmento global", "Sub segmento local", "contacto"]
        saleforce=sf.consultar_sale(ruc,campos_a_consultar )
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

# print('Maximo:15\nMinimo:4')
# hilos=int(input('ingrese el numero de hilos: '))
hilos=10





def varios(nombreArchivo):
    #analizamos el archivo excel
    try:
        df = pd.read_excel(f"{nombreArchivo}.xlsx")
        numero_filas_inicial=df.shape[0]
    except Exception as e:
        print("No se encontro el archivo!!")
        print(f"Error:\n\n{e}")

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
    #verificar que haya 500 filas
    numero_filas_final=df_ordenado.shape[0]
    if numero_filas_inicial == numero_filas_final:
        print(f"se consultaron {numero_filas_final} de {numero_filas_inicial}")
        df_ordenado.to_excel(f"{nombreArchivo}SF.xlsx", index=False)
    else: 
        with open('consultar_nuevamente.txt', 'w') as archivo:
            archivo.write(nombreArchivo +'\n')
            archivo.close()
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
        #mover archivo
        shutil.move(f'{nombreArchivo}.xlsx',completado)
        print('Archivos movidos correctamente!!')
    except:
        print('Ocurrio un error!! no se movieron los archivos')

def encontrar_archivos_excel():
    # Definir el patrón de búsqueda usando expresiones regulares
    patron = re.compile(r'^BD\d{8}B\d{4}\.xlsx$')

    # Listar todos los archivos en el directorio especificado
    todos_los_archivos = os.listdir()

    # Filtrar los archivos que coinciden con el patrón
    archivos_coincidentes = [archivo for archivo in todos_los_archivos if patron.match(archivo)]

    return archivos_coincidentes
print('consultara solo un archivo? (si, no)')
numero_de_consultas=input('> ')
if numero_de_consultas.lower() in ['s', 'si']:

    print('ingresar nombre excacto, para podre mover los archivos')
    nombreArchivo=input("ingrese el nombre del archivo: ")
    varios(nombreArchivo)
else: 
    print('se consultaran todos los archivos con la siguiente nomenclatura: \n BDxxxxxxxxBxxxx ')

    archivos_a_iterar=encontrar_archivos_excel()
    for archivo in archivos_a_iterar:
        varios( archivo.replace(".xlsx", ""))
        print(f"se termnino la ejecucion del archivo {archivo}")


fin = time.time()
print("Tiempo de ejecucion:", fin - inicio)
input("presione enter para terminar")