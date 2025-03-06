import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.alert import Alert
from selenium.common.exceptions import NoAlertPresentException
from .navegador import Navegador

class Sunat(Navegador):
    """
    Clase para interactuar con la página de consulta de RUC de la SUNAT.

    Esta clase extiende la funcionalidad de la clase Navegador para proporcionar
    métodos específicos para consultar información de RUC en el sitio web de la SUNAT.
    
    Atributos:
        driver (webdriver): El controlador de Selenium utilizado para interactuar con el navegador.
        tabs (list): Lista de pestañas abiertas en el navegador.
        id (str): Identificador de la pestaña abierta para la página de SUNAT.
        osiptel (Osiptel): Instancia de la clase Osiptel para realizar consultas adicionales.
    """
    def __init__(self, nav) -> None:
        """
        Inicializa la clase Sunat.

        Args:
            nav (Navegador): Instancia de la clase Navegador que proporciona el controlador y las pestañas.
        """

        self.driver=nav.driver
        self.tabs=nav.tabs
        self.id=nav.abrir_pestana('https://e-consultaruc.sunat.gob.pe/')
    def consultar(self, ruc, sbi=None)->str:
        """
        Realiza una consulta de RUC en la página de SUNAT y obtiene información relevante.

        Este método busca el RUC proporcionado y extrae los siguientes datos:
        - Razón social
        - Estado
        - Condición
        - Domicilio fiscal
        - Representantes legales
        - Números de celular de OSIPTEL

        Args:
            ruc (str): El número de RUC a consultar.

        Returns:
            str: Un string con los datos obtenidos de la consulta o un mensaje de error si ocurre un problema.
        """
        self.activar_pestana()
        try:
        
            self.llenar_input(ruc, xpath_input='/html/body/div[1]/div[2]/div/div[2]/div[2]/form/div[1]/div/input')
            
            boton_buscar=self.buscar_elemento_xpath('/html/body/div[1]/div[2]/div/div[2]/div[2]/form/div[5]/div/button[1]')
            boton_buscar.send_keys(Keys.RETURN)
            
       
            
            # Manejo de alerta inesperada
            try:
                time.sleep(0.6)
                alert = Alert(self.driver)  # Intenta capturar la alerta
                alert_text = alert.text     # Intenta obtener el texto de la alerta
    
                alert.accept()              # Acepta la alerta para cerrar
                # Opcional: Manejar la lógica de regreso si aparece la alerta
                            
                
                return alert_text           
            except NoAlertPresentException:
                # Continúa si no hay alerta
                pass
        
            # Extraer los datos de la primera página
            time.sleep(1)
            
            self.scroll()
            
         
            representantes_legales=self.buscar_elemento_xpath(nombre='formRepLeg')
            if not representantes_legales:
                representantes='No se encontraron representantes legales'
            else:
            
                representantes_legales=representantes_legales.find_element("tag name", "button")
                representantes_legales.send_keys(Keys.RETURN)
        
                representantes=self._extraer_datos_tabla('/html/body/div/div[2]/div[2]/div[2]/div/div/table/tbody',columnas_especifico=[2,3,4])
                
            self.driver.get('https://e-consultaruc.sunat.gob.pe/')
            
            return representantes        
        except Exception as e:

            print('Error en consulta Sunat con Selenium')
            print(e)
            self.driver.get('https://e-consultaruc.sunat.gob.pe/')
            return 'Ocurrio un error! intenta con otro ruc o intente nuevamente en unos minutos'
        
    