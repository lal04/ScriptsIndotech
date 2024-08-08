
import os
from dotenv import load_dotenv
import requests


class Ositel:
    def __init__(self) -> None:
        """
        Inicializa una instancia de la clase Ositel.
        Carga las variables de entorno desde el archivo .env, incluyendo los tokens de reCAPTCHA y GoogleCaptchaTokenOLD.
        """
        load_dotenv()
        self.recaptcha=os.getenv("RECAPTCHA")
        self.googlecaptchatokenold=os.getenv("GOOGLECAPTCHATOKENOLD")
        
    def consulta_ostitel(self,ruc=20522317285, tipo_documento=2)->str:
        """
        Consulta la cantidad de líneas móviles asociadas a un RUC o DNI en el sistema de Ositel.

        Parámetros:
        - ruc: El número de RUC (por defecto 20522317285) o DNI a consultar.
        - tipo_documento: El tipo de documento, 2 para RUC y 1 para DNI (por defecto es 2).

        Retorna:
        - Un string que resume la cantidad de líneas móviles por operador en el formato:
          "M<número de líneas Telefónica> C<número de líneas Claro> E<número de líneas Entel> O<número de líneas Otros>".
        - Retorna False en caso de error.
        """
        data={
            
            "columns[0][data]": 0,
            "columns[0][name]": "indice",
            "order[0][column]": 0,
            "order[0][dir]": "asc",
            "length":1000000000,#indica el numero de lineas que se van a mostrar, el maximo es 1000000000
            "models[IdTipoDoc]": tipo_documento,#tipo 02 es para ruc y el 01 es para dni
            "models[NumeroDocumento]":ruc ,  
            
            "models[ReCaptcha]":self.recaptcha ,
            
            
            "models[GoogleCaptchaTokenOLD]":self.googlecaptchatokenold,
            }
        r=requests.post("https://checatuslineas.osiptel.gob.pe/Consultas/GetAllCabeceraConsulta/", data=data)
       
        if r.status_code == 200:
            response = r.json()

            # Inicializar el diccionario para contar operadores
            contadores = {
                "TELEFONICA DEL PERU S.A.A.": 0,
                "AMERICA MOVIL PERU S.A.C.": 0,
                "ENTEL PERU S.A.": 0,
                "OTROS": 0
            }

            # Contar las ocurrencias de cada operador
            for fila in response["aaData"]:
                operador = fila[3]
                if operador in contadores:
                    contadores[operador] += 1
                else:
                    contadores["OTROS"] += 1

            # Crear el resultado final
            resultado = (f"M{contadores['TELEFONICA DEL PERU S.A.A.']} "
                         f"C{contadores['AMERICA MOVIL PERU S.A.C.']} "
                         f"E{contadores['ENTEL PERU S.A.']} "
                         f"O{contadores['OTROS']}")

            return resultado
        else:
            print("Ocurrió un error consulta Ositel")
            print(r.status_code)
            return False
            
    

                
                
                
        
        
        