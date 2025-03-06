from src.navegador import Navegador
from src.sunat_selenium import Sunat
from src.utilidades import Utilidades
from tqdm import tqdm  # Importar tqdm para la barra de progreso

def main():
    try:
        nombre= input('Ingrese el nombre del archivo a leer (sin extensión): ')
        data_frame = Utilidades.leer_archivo(nombre)
        
        if 'RUC' not in data_frame.columns:
            raise KeyError("La columna 'RUC' no existe en el DataFrame o está mal escrita.")
        
        # Convertir la columna RUC a string
        data_frame['RUC'] = data_frame['RUC'].astype(str)

        # Inicializar el objeto Sunat
        sunat = Sunat(Navegador())

        # Registrar tqdm para usarlo en apply
        tqdm.pandas()

        def funcion_argumento(fila):
            Utilidades.limpiar_consola()  # Limpiar la consola antes de imprimir
            tqdm.write(f'Consultando RUC: {fila["RUC"]}\n')  # Muestra solo la consulta actual
            return sunat.consultar(fila['RUC'])

        # Aplicar la función con barra de progreso
        data_frame['RRLL'] = data_frame.progress_apply(funcion_argumento, axis=1)
        
        data_frame.to_csv(f'{nombre}.csv', index=False)
        
        Utilidades.limpiar_consola()
        input('\nProceso completado. Presione Enter para salir...')

    except KeyError as e:
        input(f'Error: {e}\n\nPresione Enter para continuar...')

if __name__ == '__main__':
    main()
