import os
import pandas as pd
def main():
    # Obtener la ruta del directorio actual
    ruta_actual = os.getcwd()
    print("La ruta del directorio actual es:", ruta_actual)
    # Obtener la lista de nombres de archivos en la carpeta
    archivos = os.listdir(ruta_actual)
    # Lista para almacenar los DataFrames de cada archivo
    dfs = []
    numeroItems=0
    
    Nomenclaruta=input('introduce parte de la nomenclarura que tienen en comun lo archivos a unir: ')

    # recorremos la lista de archivos en la careta
    for archivo in archivos:
        # asegurarse de que solo leemos archivos Excel con 'rucDatosPeru' en el nombre
        try:
            if Nomenclaruta in archivo:
                ruta_archivo = os.path.join(ruta_actual, archivo)
                df = pd.read_excel(ruta_archivo)
                print(archivo)
                print(df.shape[0])
                numeroItems=numeroItems+df.shape[0]
                dfs.append(df)
        except Exception as e:
            print(f'no se encontraron coincidencias con "{Nomenclaruta}"')
            print(e)
    # Unir todos los DataFrames en uno solo
    df_final = pd.concat(dfs, ignore_index=True)
    #verificar si no falto ningun item
    if numeroItems==df_final.shape[0]:
        print(f'total de items: {df_final.shape[0]}->Verificado')
    else:
        print(f'no se registraron todos los items: {numeroItems-df_final.shape[0]} faltantes')
           
        
    #ingresa el nombre para el archivo unificado
    nombreArchivoFinal=input('ingresa el nombre para el archivo unificado (sin extencion: xlsx): ')
    # Escribir el DataFrame final en un archivo Excel
    ruta_archivo_salida = os.path.join(ruta_actual,f'{nombreArchivoFinal}.xlsx')

    df_final.to_excel(ruta_archivo_salida, index=False)

    print("Archivos Excel unidos satisfactoriamente.")
    
    

if __name__ == '__main__':
    main()