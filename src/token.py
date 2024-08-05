from cryptography.fernet import Fernet
import os
from dotenv import load_dotenv
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed

class Token:
    def __init__(self) -> None:
        """
        Inicializa la clase Token.
        - Verifica y crea el archivo .env si no existe, generando una clave de encriptación.
        - Carga las variables de entorno desde el archivo .env.
        - Verifica y crea el archivo token.txt si no existe.
        - Inicializa el encriptador Fernet con la clave de encriptación obtenida de las variables de entorno.
        """
        if not os.path.exists(".env"):
            # Si no existe el archivo .env, crea uno con una clave de encriptación generada
            with open(".env", "w") as env:
                clave_encriptacion = self.generar_llave()
                env.write(f"CLAVE_DE_ENCRIPTACION='{clave_encriptacion}'")
                print("Se creó el archivo .env con la clave de encriptación")
        
        # Cargar las variables de entorno desde el archivo .env
        load_dotenv()

        if not os.path.exists("token.txt"):
            # Si no existe el archivo token.txt, crea uno vacío
            with open("token.txt", "w") as tk:
                print("Se creó el archivo token.txt")

        # Inicializar el encriptador Fernet con la clave de encriptación desde las variables de entorno
        clave = os.getenv("CLAVE_DE_ENCRIPTACION")
        self.encriptador = Fernet(clave.encode())

    def generar_llave(self) -> str:
        """
        Genera una nueva clave de encriptación Fernet y devuelve la clave en formato de cadena.
        """
        return Fernet.generate_key().decode()

    def agregar_token(self, nuevo_token: str) -> None:
        """
        Agrega un nuevo token encriptado al archivo token.txt.
        """
        with open("token.txt", "a") as tk:
            token_encriptado = self.encriptador.encrypt(nuevo_token.encode()).decode()
            tk.write(f"{token_encriptado}\n")
        print("Se agregó un nuevo token encriptado a token.txt")

    def obtener_lista_tokens(self) -> list:
        """
        Retorna una lista de tokens desencriptados obtenidos desde el archivo token.txt.
        """
        lista_de_tokens = []
        with open("token.txt", "r") as tk:
            lineas = tk.readlines()
        
        for linea in lineas:
            token_desencriptado = self.encriptador.decrypt(linea.encode()).decode()
            lista_de_tokens.append(token_desencriptado)
        
        return lista_de_tokens

    def verificar_consultas_de_token(self, token: str) -> bool:
        """
        Verifica la validez de un token consultando una API externa.
        Retorna True si la consulta es exitosa (código de estado 200), False si no es exitosa (código de estado 401).
        """
        url = f"https://dniruc.apisperu.com/api/v1/ruc/20131312955?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.{token}"
        try:
            r = requests.get(url)
            if r.status_code == 200:
                return True
            elif r.status_code == 401:
                return False
            else:
                print("Error al consultar la API")
                return False
        except Exception as e:
            print(f"Error al verificar el token {token}: {e}")
            return False

    def ordenar_tokens(self, lista: list) -> None:
        """
        Ordena los tokens de acuerdo al resultado de la verificación usando verificar_consultas_de_token.
        Los tokens verificados con éxito (True) se colocan al inicio de la lista ordenada.
        """
        lista_ordenada = []
        tk_activos = 0
        tk_no_activos = 0

        def verificar_y_ordenar(token):
            if self.verificar_consultas_de_token(token):
                return (True, token)
            else:
                return (False, token)

        with ThreadPoolExecutor(max_workers=10) as executor:
            future_to_token = {executor.submit(verificar_y_ordenar, token): token for token in lista}
            for future in as_completed(future_to_token):
                success, token = future.result()
                if success:
                    lista_ordenada.insert(0, token)
                    tk_activos += 1
                else:
                    lista_ordenada.append(token)
                    tk_no_activos += 1

        with open("token.txt", "w") as tk:
            for token in lista_ordenada:
                token_encriptado = self.encriptador.encrypt(token.encode()).decode()
                tk.write(f"{token_encriptado}\n")

        print("Tokens ordenados y actualizados en token.txt")
        print(f"tokens activos: {tk_activos}\n tokens no activos: {tk_no_activos}")


                
                
                
        
        
        