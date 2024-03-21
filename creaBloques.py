

import pandas as pd
# Lee el archivo Excel completo
archivo_base = input('Ingrese el nombre del archivo (sin extensión): ')  # Nombre base del archivo
archivo_excel = f"{archivo_base}.xlsx"  # Nombre del archivo con extensión
print('si no ingresas valor, se crearan bloques de 500')
filas=input('ingrese numero de filas de cada bloque: ')
print(filas)
if filas == '':
    filas=500
else:
    filas=int(filas)

df_original = pd.read_excel(archivo_excel)

# Obtener el encabezado
encabezado = list(df_original.columns)

# Dividir en bloques de 100 filas
bloques = [df_original[i:i+filas] for i in range(0, len(df_original), filas)]
carpeta_bloques = 'C:/Users/Raul/OneDrive - INDOTECH SAC/Proyecto/Bloques/'  # Carpeta donde se guardarán los bloques

# Iterar sobre los bloques y guardar en nuevos archivos
for i, bloque in enumerate(bloques):
    Cifra=str(i+1).zfill(4)
    nomenclatura= f"B{Cifra}.xlsx"  # Nombre del archivo con el número de bloque

    bloque.columns = encabezado  # Asignar el mismo encabezado que el original
    nombre_archivo = f'{carpeta_bloques}{archivo_base}{nomenclatura}'
    bloque.to_excel(nombre_archivo, index=False)  # Guardar el bloque en un archivo Excel

    print(f"Guardado  {archivo_base+nomenclatura} con {len(bloque)} filas.")

