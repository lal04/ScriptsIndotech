import os
import shutil

RUTAS_INICIALES = [
    'Indotech\\1.BDBruto\\completados',
    'Indotech\\2.BDNeto\\completados',
    'Indotech\\3.Bloque\\completados',
    'Indotech\\4.Filtrado\\completados',
    'Indotech\\5.Lote\\completados',
    'Indotech\\6.Funnel\\completados'
]

CARPETAS = ['1.BDBruto', '2.BDNeto', '3.Bloque', '4.Filtrado', '5.Lote', '6.Funnel']

EXTENSION='xlsx'

class Administrador:
    def __init__(self) -> None:
        self.rutas = RUTAS_INICIALES

    def verificar_carpetas(self):
        while True:
            carpeta_raiz = input('Ingresa el nombre de la carpeta raiz:\n>')
            if carpeta_raiz:
                break
            print("El nombre de la carpeta no puede estar vacío.")
        if not os.path.exists(carpeta_raiz):
            self.rutas = []
            for carpeta in CARPETAS:
                ruta = os.path.join(carpeta_raiz, carpeta, 'completados')
                try:
                    os.makedirs(ruta)
                    self.rutas.append(ruta)
                except OSError as e:
                    print(f"Error al crear la carpeta {ruta}: {e}")
            print('¡Sistema de carpetas creado correctamente!')
        else:
            self.rutas = [os.path.join(carpeta_raiz, carpeta, 'completados') for carpeta in CARPETAS]
            print('¡Sistema de carpetas existente!')

    def _obtener_rutas(self, nombre, proceso_actual, extension):
        proceso_actual -= 1
        origen = os.path.join(self.rutas[proceso_actual].replace('completados', ''), nombre + '.' + extension)
        destino = os.path.join(self.rutas[proceso_actual], nombre + '.' + extension)
        siguiente=os.path.join(self.rutas[proceso_actual+1].replace('completados', ''), nombre + '.' + extension)
        return [origen, destino], siguiente

    def _validar_proceso(self, proceso_actual):
        if proceso_actual < 1 or proceso_actual > len(self.rutas):
            raise ValueError("Proceso actual fuera del rango permitido.")

    def mover_a_completados(self, nombre, proceso_actual=1, extension=EXTENSION):
        self._validar_proceso(proceso_actual)
        rutas= self._obtener_rutas(nombre, proceso_actual, extension)
        origen=rutas[0]
        destino=rutas[1]
        try:
            shutil.move(origen, destino)
            print(f'"{nombre}.{extension}" movido a completados!!')
        except FileNotFoundError:
            print(f'El archivo {origen} no existe.')
        except shutil.Error as e:
            print(f'Error al mover el archivo: {e}')
        except Exception as e:
            print(f'Ocurrió un error inesperado: {e}')

    def mover_al_siguiente(self, nombre, proceso_actual=1, extension=EXTENSION):
        self._validar_proceso(proceso_actual)
        try:
            origen, destino = self._obtener_rutas(nombre, proceso_actual, extension)
    
            shutil.move(origen[0], destino)
            print(f'"{nombre}.{extension}" se movio al siguiente proceso!!')
        except FileNotFoundError:
            print(f'El archivo {origen[0]} no existe.')
        except shutil.Error as e:
            print(f'Error al mover el archivo: {e}')
        except Exception as e:
            print(f'Ocurrió un error inesperado: {e}')
            
    def comprobar_bd_pendientes(self)->list:
        
        lista_archivos_carpeta=[archivo for archivo in os.listdir(self.rutas[0].replace('completados', '')) if EXTENSION in archivo]
        print(lista_archivos_carpeta)
        return lista_archivos_carpeta
