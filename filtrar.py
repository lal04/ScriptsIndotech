import pandas as pd
import os
import re


import sys

def main():
    """
    Función principal que filtra un DataFrame y guarda el resultado en un archivo Excel.

    Lee un archivo Excel, filtra las filas según ciertas condiciones en las columnas 'estado', 'condicion' y 'Nodo',
    y guarda el resultado en un archivo Excel llamado 'salida.xlsx'.
    """
    # Obtener la ruta actual del directorio
    ruta_actual = os.getcwd()
    
    

    def encontrar_archivos_excel(patron_str=r'^BD\d{8}B\d{4}\.xlsx$', ruta=os.getcwd()):
        # Compilar el patrón de búsqueda usando el argumento proporcionado
        patron = re.compile(patron_str)

        # Listar todos los archivos en el directorio especificado
        todos_los_archivos = os.listdir(ruta)

        # Filtrar los archivos que coinciden con el patrón
        archivos_coincidentes = [archivo for archivo in todos_los_archivos if patron.match(archivo)]

        return archivos_coincidentes

        
        
    def filtro(ruta_archivo):
        try:
            print(ruta_archivo)
            df = pd.read_excel(f"{ruta_archivo}")
        except:
            
            
            print(f"Archivo NO ENCONTRADO!! ")
            sys.exit()
        
        


        
        # Mover el archivo Excel a la carpeta "completados"
        if not os.path.exists('completados'):
            os.makedirs('completados')
        os.rename(ruta_archivo, f'completados/{ruta_archivo.split("\\")[-1]}')
        
        # Convertir las columnas 'estado' y 'condicion' a tipo string
        df['estado'] = df['estado'].astype(str)
        df['condicion'] = df['condicion'].astype(str)

        # Aplicar el filtro
        filtro_estado = ~(df['estado'].str.contains('no activo', case=False))
        filtro_condicion = ~(df['condicion'].str.contains('no habido|no hallado|pendiente', case=False))
        filtro_nodo = (df['Nodo'].str.strip().str.contains(r'indotech|error|no encontrado|NCP_PER_PYME_NO CARTERIZADO FVI', case=False)) | (df['Nodo'].str.strip().isin(['', ' ']))
        filtro = filtro_estado & filtro_condicion & filtro_nodo
        resultado = df[filtro]
        
        # Mover el archivo Excel a la siguiente carpeta 5.Lote
        
        ruta_lote = os.path.join(ruta_actual.replace("4.Filtrado","5.Lote") ,f'{ruta_archivo.split("\\")[-1].replace(".xlsx","")}-F.xlsx')
        

        # Guardar el resultado en un archivo Excel
        resultado.to_excel(ruta_lote, index=False)
        print("se aplico el filtro correctamente!!")
    print(
            """
            ==========================
            Proceso 4.Filtrado
            ===========================
            filtraras solo un archivo? (si, SI, s, S)
            """
        )
        
    respuesta=input(">")
    if respuesta.lower() in ["si", "s"]:
    
        # Lectura del archivo Excel
        archivo = input('Ingresa el nombre del archivo: ')
        ruta_archivo = os.path.join(ruta_actual, f'{archivo}.xlsx') # Obtener la ruta completa del archivo
        
        filtro(ruta_archivo)
        
    else:
        #patron de nombre del excel que se buscara
        #tiene un valor por defecto que que es '^BD\d{8}B\d{4}\.xlsx$' que es de los bloques de la base de datos 3.bloque
        patron = r'.*SF\.xlsx$' # esto indica que solo se quedaran archivos que termine en SF.xlsx

        lista = encontrar_archivos_excel(patron)
        for excel in lista:
            filtro(excel)
    
if __name__=='__main__':
    main()
