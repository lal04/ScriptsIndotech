import pandas as pd
import os 

def main():
    """
    Función principal que filtra un DataFrame y guarda el resultado en un archivo Excel.

    Lee un archivo Excel, filtra las filas según ciertas condiciones en las columnas 'estado', 'condicion' y 'Nodo',
    y guarda el resultado en un archivo Excel llamado 'salida.xlsx'.
    """
    # Obtener la ruta actual del directorio
    ruta_actual = os.getcwd()
    
    # Lectura del archivo Excel
    archivo = input('Ingresa el nombre del archivo: ')
    ruta_archivo = os.path.join(ruta_actual, f'{archivo}.xlsx')  # Obtener la ruta completa del archivo
    
    df = pd.read_excel(ruta_archivo)
    
    # Mover el archivo Excel a la carpeta "completados"
    if not os.path.exists('completados'):
        os.makedirs('completados')
    os.rename(ruta_archivo, f'completados/{archivo}.xlsx')
    
    # Convertir las columnas 'estado' y 'condicion' a tipo string
    df['estado'] = df['estado'].astype(str)
    df['condicion'] = df['condicion'].astype(str)

    # Aplicar el filtro
    filtro_estado = ~(df['estado'].str.contains('no activo', case=False))
    filtro_condicion = ~(df['condicion'].str.contains('no habido|no hallado|pendiente', case=False))
    filtro_nodo = (df['Nodo'].str.strip().str.contains(r'indotech|error|no encontrado|NCP_PER_PYME_NO CARTERIZADO FVI', case=False)) | (df['Nodo'].str.strip().isin(['', ' ']))
    filtro = filtro_estado & filtro_condicion & filtro_nodo
    resultado = df[filtro]

    # Guardar el resultado en un archivo Excel
    resultado.to_excel(f'{archivo}F.xlsx', index=False)
    print("se aplico el filtro correctamente!!")
    
if __name__=='__main__':
    main()
