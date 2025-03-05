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
        self.osiptel=nav.osiptel
        self.saleforce=nav.saleforce
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
            #time.sleep(0.5)
            # campo_busqueda = self.driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div/div[2]/div[2]/form/div[1]/div/input')
            # campo_busqueda.clear()
            # campo_busqueda.send_keys(ruc)
            self.llenar_input(ruc, xpath_input='/html/body/div[1]/div[2]/div/div[2]/div[2]/form/div[1]/div/input')
            
            #boton_buscar = self.driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div/div[2]/div[2]/form/div[5]/div/button[1]')
            boton_buscar=self.buscar_elemento_xpath('/html/body/div[1]/div[2]/div/div[2]/div[2]/form/div[5]/div/button[1]')
            boton_buscar.send_keys(Keys.RETURN)
            
            # Espera para asegurarse de que la alerta se maneje si aparece
            #time.sleep(0.5)
            
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
        
            try:
                #self.driver.find_element(By.XPATH, '/html/body/div/div[2]/div/div[3]/div[2]/div[1]/div/div/p')
                self.buscar_elemento_xpath('/html/body/div/div[2]/div/div[3]/div[2]/div[1]/div/div/p')
                lista_xpath=[2,6,7,8]
            except:
                lista_xpath=[1,5,6,7]
 
            # Extraer los datos de la primera página
            time.sleep(1)
            #datos = self.driver.find_element(By.XPATH, f'/html/body/div/div[2]/div/div[3]/div[2]/div[{lista_xpath[0]}]/div/div[2]/h4').text
            datos=self.extraer_texto_xpath(f'/html/body/div/div[2]/div/div[3]/div[2]/div[{lista_xpath[0]}]/div/div[2]/h4')
            razon_social = datos.split(' - ')[1]
            #estado = self.driver.find_element(By.XPATH, f'/html/body/div/div[2]/div/div[3]/div[2]/div[{lista_xpath[1]}]/div/div[2]/p').text
            estado=self.extraer_texto_xpath(f'/html/body/div/div[2]/div/div[3]/div[2]/div[{lista_xpath[1]}]/div/div[2]/p')
            
            #condicion = self.driver.find_element(By.XPATH, f'/html/body/div/div[2]/div/div[3]/div[2]/div[{lista_xpath[2]}]/div/div[2]/p').text
            condicion=self.extraer_texto_xpath(f'/html/body/div/div[2]/div/div[3]/div[2]/div[{lista_xpath[2]}]/div/div[2]/p')
            
            #domicilio_fiscal=self.driver.find_element(By.XPATH, f'/html/body/div/div[2]/div/div[3]/div[2]/div[{lista_xpath[3]}]/div/div[2]/p').text
            domicilio_fiscal=self.extraer_texto_xpath(f'/html/body/div/div[2]/div/div[3]/div[2]/div[{lista_xpath[3]}]/div/div[2]/p')
            

            
            # Pasamos a la página de representantes legales
            #representantes_legales = self.driver.find_element(By.XPATH, '/html/body/div/div[2]/div/div[5]/div[3]/div[3]/form/button')
            representantes_legales=self.buscar_elemento_xpath('/html/body/div/div[2]/div/div[5]/div[3]/div[3]/form/button')
            representantes_legales.send_keys(Keys.RETURN)
            #time.sleep(1)
            #tabla_representantes = self.driver.find_element(By.XPATH, '/html/body/div/div[2]/div[2]/div[2]/div/div/table/tbody')
            ##############################################################################
            #############################################################################
            # tabla_representantes=self.buscar_elemento_xpath('/html/body/div/div[2]/div[2]/div[2]/div/div/table/tbody')
            # filas = tabla_representantes.find_elements(By.TAG_NAME, 'tr')
            # lista_representantes = []
            
            # for i in range(len(filas)):
            #     #fila = self.driver.find_element(By.XPATH, f'/html/body/div/div[2]/div[2]/div[2]/div/div/table/tbody/tr[{i+1}]').text
            #     fila=self.extraer_texto_xpath( f'/html/body/div/div[2]/div[2]/div[2]/div/div/table/tbody/tr[{i+1}]')
            #     lista_representantes.append(fila)
            
            # representantes = ',    '.join(lista_representantes)
            representantes=self._extraer_datos_tabla('/html/body/div/div[2]/div[2]/div[2]/div/div/table/tbody',columnas_especifico=[2,3,4])
            ####################################################################
            ###################################################################
            numeros_osiptel=self.osiptel.consulta_osiptel(ruc)
            
            if self.saleforce.verificar_estado_sesion():
                sale = self.saleforce.consultar_sale(ruc, ['Pc', 'Nodo', 'contacto'])
            else:
                
                self.saleforce.inicio_sesion()
                sale = self.saleforce.consultar_sale(ruc, ['Pc', 'Nodo', 'contacto'])
                
            data_contactos=sale['contacto']
            contactos = [
                f"{nombre} {cargo} {telefono}".strip()
                for _, nombre, _, cargo, telefono in data_contactos
                if nombre and telefono
            ]

            # Unir toda la información en una sola cadena separada por comas
            presentacion_contactos = ',    '.join(contactos)
                        
            # retornar datos extraídos de Sunat
            resultado = f"""
                            Razon social: {razon_social}
                            Ruc: {ruc}
                            Estado: {estado.split('\n')[0]}
                            Condicion: {condicion.split('\n')[0]}
                            Domicilio fiscal: {domicilio_fiscal}
                            Representantes legales: {representantes}
                            Osiptel: {numeros_osiptel}
                            Propietario cliente SALEFORCE: {sale['Pc']}
                            Nodo SALEFORCE: {sale['Nodo']}
                            Contactos SALEFORCE: {presentacion_contactos}
                            """
            
            self.driver.get('https://e-consultaruc.sunat.gob.pe/')
            
            return resultado        
        except Exception as e:
            
            
            print('Error en consulta Sunat con Selenium')
            print(e)
            self.driver.get('https://e-consultaruc.sunat.gob.pe/')
            datos_sunat=sbi.ruc(ruc)
            if datos_sunat:
                return datos_sunat
            else:
            
                return 'Ocurrio un error! intenta con otro ruc o intente nuevamente en unos minutos'
        
    