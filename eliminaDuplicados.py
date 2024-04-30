import pandas as pd
def main():
    #encontrasmo la ruta actual
    #ruta_actual = os.getcwd()
    nombreArchivo=input('ingrese nombre del archivo: ')
    df = pd.read_excel(f'{nombreArchivo}.xlsx')
    print(f'numero de filas inicial: {df.shape[0]}')
    nfInicio=df.shape[0]

    # Suponiendo que tienes un DataFrame llamado df y deseas eliminar duplicados basados en la columna 'ruc'
    df_sin_duplicados = df.drop_duplicates(subset=['ruc'], keep='first')

    print(f'numero de filas final: {df_sin_duplicados.shape[0]}')
    nfFin=df_sin_duplicados.shape[0]
    # Abrir un archivo de texto en modo escritura
    with open(f'{nombreArchivo}.txt', 'w') as archivo:
        # Escribir contenido en el archivo
        archivo.write(f"Nombre del archivo: {nombreArchivo}.\n")
        archivo.write(f"numero de items inicio: {nfInicio}.\n")
        archivo.write(f"numero de items al finalizar: {nfFin}.\n")
        archivo.write(f"duplicados: {nfInicio-nfFin}.\n")
    print("Archivo creado satisfactoriamente.")
    
    
    nombreArchivoSalida=input('ingrese el nombre del archico de salida: ')
    
    df_sin_duplicados.to_excel(f'{nombreArchivoSalida}.xlsx',index=False)
    
if __name__== '__main__':
    main()
