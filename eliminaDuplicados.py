import pandas as pd
import os

def main():
    # Obtener la ruta actual del directorio
    ruta_actual = os.getcwd()
    
    # Solicitar al usuario el nombre del archivo de Excel
    nombreArchivo = input('Ingrese nombre del archivo (sin la extensión .xlsx): ')
    
    # Leer el archivo Excel
    df = pd.read_excel(f'{nombreArchivo}.xlsx')
    print(f'Número de filas inicial: {df.shape[0]}')
    nfInicio = df.shape[0]

    # Convertir nombres de columnas a minúsculas y seleccionar solo la columna 'ruc'
    df.columns = map(str.lower, df.columns)  # Convertir nombres de columnas a minúsculas
    df_ruc = df[['ruc']]  # Seleccionar solo la columna 'ruc'

    # Normalizar la columna 'ruc':
    # 1. Eliminar filas con celdas vacías en la columna 'ruc'
    df_ruc = df_ruc.dropna(subset=['ruc'])

    # 2. Convertir la columna de str a int, manejando errores
    df_ruc['ruc'] = pd.to_numeric(df_ruc['ruc'], errors='coerce').astype('Int64')

    # 3. Filtrar los valores que están en el rango de 20000000000 a 20999999999
    df_filtrado = df_ruc[(df_ruc['ruc'] >= 20000000000) & (df_ruc['ruc'] <= 20999999999)]

    # 4. Eliminar duplicados basados en la columna 'ruc'
    df_sin_duplicados = df_filtrado.drop_duplicates(keep='first')

    # Mostrar el número final de filas
    print(f'Número de filas final: {df_sin_duplicados.shape[0]}')
    nfFin = df_sin_duplicados.shape[0]
    
    # Escribir en un archivo de texto
    with open(f'{nombreArchivo}.txt', 'w') as archivo:
        archivo.write(f"Nombre del archivo: {nombreArchivo}.\n")
        archivo.write(f"Número de ítems al inicio: {nfInicio}.\n")
        archivo.write(f"Número de ítems al finalizar: {nfFin}.\n")
        archivo.write(f"Duplicados y errados: {nfInicio - nfFin}.\n")
    print("Archivo creado satisfactoriamente.")
    
    # Mover el archivo Excel a la carpeta "completados"
    if not os.path.exists('completados'):
        os.makedirs('completados')
    os.rename(f'{nombreArchivo}.xlsx', f'completados/{nombreArchivo}.xlsx')
    
    # Crear la ruta de la siguiente carpeta para el proceso
    ruta_creacion = ruta_actual.replace("1.BDBruto", "2.BDNeto\\")
    
    # Solicitar al usuario el nombre con el que se identificará la base 
    nombreArchivo = input('Ingrese la nomenclatura para el archivo: ')
    
    # Guardar solo la columna 'ruc' en un nuevo archivo Excel y moverlo a la siguiente carpeta
    df_sin_duplicados.to_excel(f'{ruta_creacion}{nombreArchivo}.xlsx', index=False)
    print("Se creó el archivo en la carpeta siguiente, con el mismo nombre")

if __name__ == '__main__':
    main()
