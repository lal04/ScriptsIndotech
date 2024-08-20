import os
from dotenv import load_dotenv
import requests

class Osiptel:
    """
    La clase `Osiptel` se encarga de interactuar con la API de OSIPTEL para realizar consultas sobre líneas telefónicas 
    registradas en Perú. Utiliza variables de entorno para gestionar el CAPTCHA y validar las solicitudes.

    Atributos:
    ----------
    recaptcha : str
        El valor del ReCaptcha necesario para realizar la consulta en la API de OSIPTEL.
    googlecaptchatokenold : str
        El token de Google CAPTCHA necesario para realizar la consulta en la API de OSIPTEL.

    Métodos:
    --------
    __init__():
        Inicializa la clase cargando las variables de entorno y validando el CAPTCHA.

    validar_captcha() -> bool:
        Valida el CAPTCHA realizando una consulta a OSIPTEL y verificando el resultado.

    consulta_osiptel(ruc=20522317285, estado=True, tipo_documento=2) -> str:
        Realiza una consulta a la API de OSIPTEL con el RUC especificado, analiza los datos de respuesta 
        y devuelve un string que resume la cantidad de líneas asociadas a diferentes operadores.
    """

    def __init__(self) -> None:
        """
        Inicializa una instancia de la clase `Osiptel`. Carga las variables de entorno necesarias para las consultas
        a OSIPTEL, y valida el CAPTCHA antes de permitir cualquier consulta.

        Si el CAPTCHA no es válido, se muestra un mensaje de error.
        """
        load_dotenv()
        self.recaptcha = os.getenv("RECAPTCHA")
        self.googlecaptchatokenold = os.getenv("GOOGLECAPTCHATOKENOLD")
        if not self.validar_captcha():
            print('Error con el captcha,\n Intente nuevamente!!')
       
    def validar_captcha(self) -> bool:
        """
        Valida el CAPTCHA realizando una consulta a la API de OSIPTEL.

        Returns:
        --------
        bool
            `True` si el CAPTCHA es válido, `False` en caso contrario.
        """
        resultado = self.consulta_osiptel()
        if resultado == 'M93 C10 E0 O0':
            return True
        else:
            return False
        
    def consulta_osiptel(self, ruc=20522317285, estado:bool=True, tipo_documento:int=2) -> str:
        """
        Realiza una consulta a la API de OSIPTEL utilizando el RUC y el tipo de documento proporcionados.

        Parameters:
        -----------
        ruc : int, optional
            El número de RUC para el cual se desea realizar la consulta (por defecto es 20522317285).
        estado : bool, optional
            Indica si la consulta debe realizarse (por defecto es True).
        tipo_documento : int, optional
            El tipo de documento (02 para RUC y 01 para DNI) (por defecto es 2).

        Returns:
        --------
        str
            Un string que resume la cantidad de líneas asociadas a diferentes operadores en el formato:
            'M{TELEFONICA} C{AMERICA MOVIL} E{ENTEL} O{OTROS}'.
            Si ocurre un error durante la consulta, se devuelve `False`.
        """
        if estado:
            data = {
                "columns[0][data]": 0,
                "columns[0][name]": "indice",
                "order[0][column]": 0,
                "order[0][dir]": "asc",
                "length": 1000000000,  # Indica el número de líneas a mostrar, el máximo es 1000000000
                "models[IdTipoDoc]": tipo_documento,  # Tipo 02 es para RUC y el 01 es para DNI
                "models[NumeroDocumento]": ruc,
                "models[ReCaptcha]": self.recaptcha,
                "models[GoogleCaptchaTokenOLD]": self.googlecaptchatokenold,
            }
            r = requests.post("https://checatuslineas.osiptel.gob.pe/Consultas/GetAllCabeceraConsulta/", data=data)
        
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
                print("Ocurrió un error consulta Osiptel")
                print(r.status_code)
                return False
        else:
            return ''
