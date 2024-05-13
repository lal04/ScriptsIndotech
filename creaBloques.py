import os
import pandas as pd

# Lee el archivo Excel completo
archivo_base = input('Ingrese el nombre del archivo (sin extension): ')  # Nombre base del archivo
archivo_excel = f"{archivo_base}.xlsx"  # Nombre del archivo con extensión

# Solicitar al usuario el número de filas por bloque
filas = int(input('Ingrese el número de filas de cada bloque (500 por defecto): ') or '500')

# Mover el archivo Excel a la carpeta "completados"
os.makedirs('completados', exist_ok=True)
os.rename(archivo_excel, f'completados/{archivo_excel}')

# Leer el archivo Excel completo
df_original = pd.read_excel(f'completados/{archivo_excel}')

# Dividir el DataFrame en bloques y guardar en archivos individuales
ruta = os.path.abspath(archivo_excel).replace(f'2.BDNeto\\{archivo_excel}', '3.Bloque')
encabezado = list(df_original.columns)

for i, bloque in enumerate([df_original[i:i+filas] for i in range(0, len(df_original), filas)]):
    bloque.columns = encabezado
    bloque.to_excel(f'{ruta}\\{archivo_base}B{(i+1):04d}.xlsx', index=False)
    print(f"Guardado {archivo_base}B{(i+1):04d}.xlsx con {len(bloque)} filas.")

# Esperar a que el usuario presione enter para terminar
input('Presione enter para terminar.')
