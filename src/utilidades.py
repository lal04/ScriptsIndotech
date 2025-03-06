import pandas as pd
import os
class Utilidades:
    
    def manejar_errores(fun):
        def envoltura(*args, **kwargs):
            try:
                return fun(*args, **kwargs)
            except Exception as e:
                print(f'Método: {fun.__name__}')
                print(f'Detalle:\n{e}')
        return envoltura
    
    
    @staticmethod
    @manejar_errores
    def leer_archivo(ruta:str=None, tipe_entrada:str='xlsx'):
       
        ruta_base=os.getcwd()
        ruta_completa=os.path.abspath(os.path.normpath(os.path.join(ruta_base, f'{ruta}.{tipe_entrada}')))
                    
        data_frame =pd.read_excel(ruta_completa)
        
        return data_frame
        