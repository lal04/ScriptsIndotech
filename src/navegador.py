import time
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException,NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager  # Descarga y gestiona ChromeDriver automáticamente
from selenium.webdriver.common.action_chains import ActionChains

TIEMPO_DE_ESPERA=10

class Navegador:
    """
    Clase que gestiona un navegador web utilizando Selenium WebDriver para controlar pestañas, 
    navegación, y el cierre del navegador.

    Atributos:
    ----------
    driver : WebDriver
        Instancia del controlador de Selenium para interactuar con el navegador.
    tabs : list
        Lista de identificadores de las pestañas abiertas en el navegador.
    """
    
    def __init__(self,  driver=None):
        """
        Inicializa una nueva instancia de la clase Navegador.

        Parámetros:
        -----------
        driver_path : str, opcional
            La ruta al ejecutable del WebDriver, si se desea especificar uno manualmente.
            Si no se proporciona, se usará ChromeDriverManager para gestionar el controlador automáticamente.
        """
        chrome_options = Options()
        chrome_options.add_argument("--start-maximized")  # Inicia el navegador maximizado
        
        # Inicializa el webdriver usando la ruta proporcionada o ChromeDriverManager
        if driver:
            self.driver = driver
        else:
            self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
        
        self.tabs = [self.driver.current_window_handle]  # Guarda la referencia de la pestaña inicial
        self.espera = WebDriverWait(self.driver, TIEMPO_DE_ESPERA)
        self.accion=ActionChains(self.driver)
        
    @staticmethod
    def manejar_errores(fun):
        def envoltura(*args, **kwargs):
            try:
                return fun(*args, **kwargs)
            except Exception as e:
                print(f'Método: {fun.__name__}')
                print(f'Detalle:\n{e}')
        return envoltura

        
    def acciones(self, mensaje:str=None, tap:int=None, espacio:int=None):
        if mensaje:
            self.accion.send_keys(mensaje).perform()
        elif tap:
            for _ in range(tap):
                self.accion.send_keys(Keys.TAB).perform()
        elif espacio:
            for _ in range(espacio):
                self.accion.send_keys(Keys.ESCAPE).perform()
        else: 
            self.accion.send_keys(Keys.RETURN).perform()
            
    def esperar_elemeto(self, xpath:str ,tiemepo_segundos=None):
 
        try:
            if tiemepo_segundos:
                elemento=WebDriverWait(self.driver, tiemepo_segundos).until(EC.presence_of_element_located((By.XPATH, xpath)))
            else:
                elemento=WebDriverWait(self.driver, TIEMPO_DE_ESPERA).until(EC.presence_of_element_located((By.XPATH, xpath)))
            
            return elemento
        
        except TimeoutException:
            return False
        
    def llenar_input(self, mensaje, objeto_selenium=None, xpath_input=None)->None:
        if objeto_selenium and objeto_selenium is not False:
            objeto_selenium.clear()
            objeto_selenium.send_keys(mensaje)
        elif xpath_input:
            input =self.driver.find_element(By.XPATH, f'{xpath_input}')
            input.clear()
            input.send_keys(mensaje)
    @manejar_errores   
    def buscar_elemento_xpath(self,xpath:str=None, etiqueta:str=None, clase:str=None, nombre:str=None, elemento=None):
        try: 
            if elemento is None:
                elemento=self.driver
                
            if xpath:
                
                return elemento.find_element(By.XPATH, f'{xpath}')
            elif clase:
                return elemento.find_element(By.CLASS_NAME, f'{clase}')
            elif etiqueta:
                
                return elemento.find_elements(By.TAG_NAME, f'{etiqueta}')
            elif nombre:
                return elemento.find_element(By.NAME, f'{nombre}')
        except NoSuchElementException:
            return False
        
    def scroll(self, elemento=None)->None:
        if elemento:
        
            self.driver.execute_script("arguments[0].scrollIntoView();", elemento)
        else:
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            
        time.sleep(0.2)
        
    def click_xpath(self, xpath)->None:
        self.driver.find_element(By.XPATH, f'{xpath}').click()
        
        
    def extraer_texto_xpath(self, xpath):
         
        return self.driver.find_element(By.XPATH, xpath).text   
        
        
    def _extraer_datos_tabla(self, xpath_tbody:str, cantidad_de_filas:int|None=None, columna:int|None =None, columnas_especifico:list|None=None):
        try:    
            #esperar a que cargue la infomacion de la persona
            tabla=self.esperar_elemeto(xpath_tbody, 5)
            filas = tabla.find_elements(By.TAG_NAME, 'tr')
            if columna:
                numero_columna=f'/td[{columna}]'
            else:
                numero_columna=''
                
            datos_filas=[]
            for fila in range(len(filas)):
                if columnas_especifico:
                    datos_columnas_especificas=[]
                    for col_especifico in columnas_especifico:
                        temporales=self.extraer_texto_xpath(f'{xpath_tbody}/tr[{fila+1}]/td[{col_especifico}]')
                        datos_columnas_especificas.append(temporales)
                        datos=' '.join(datos_columnas_especificas)
                else:
                    datos=self.extraer_texto_xpath(f'{xpath_tbody}/tr[{fila+1}]{numero_columna}')
                    
                datos_filas.append(datos)
                if cantidad_de_filas:
                    if len(datos_filas)==cantidad_de_filas:
                        break
                
            filas=', '.join(datos_filas)
            return filas
        except:
            return 'Sin datos'

    def abrir_pestana(self, url="about:blank") -> str:
        """
        Abre una nueva pestaña en el navegador y navega a la URL especificada.

        Parámetros:
        -----------
        url : str, opcional
            La URL a la que se desea navegar en la nueva pestaña. Por defecto, se abre una pestaña en blanco.

        Retorna:
        --------
        str:
            El identificador de la nueva pestaña creada.
        """
        # Abre una nueva pestaña en blanco
        self.driver.execute_script("window.open('');")
        nueva_pestana = self.driver.window_handles[-1]
        self.tabs.append(nueva_pestana) 
        self.cambiar_pestana(len(self.tabs) - 1)  # Cambia a la nueva pestaña
        self.driver.get(url)
        return nueva_pestana
        
    def activar_pestana(self, id=None):
        """
        Activa (cambia a) la pestaña asociada al identificador `self.id`.
        """
        if id:
            self.driver.switch_to.window(id)
        else:
            
            self.driver.switch_to.window(self.id)
        

    def cambiar_pestana(self, index):
        """
        Cambia a una pestaña abierta usando el índice de la lista de pestañas.

        Parámetros:
        -----------
        index : int
            El índice de la pestaña a la que se desea cambiar. El índice debe estar dentro del rango de pestañas abiertas.
        """
        if 0 <= index < len(self.tabs):
            self.driver.switch_to.window(self.tabs[index])
        else:
            print("Índice de pestaña fuera de rango")

    def cerrar_pestana(self, index):
        """
        Cierra una pestaña abierta basada en su índice en la lista de pestañas.

        Parámetros:
        -----------
        index : int
            El índice de la pestaña que se desea cerrar. El índice debe estar dentro del rango de pestañas abiertas.
        """
        if 0 <= index < len(self.tabs):
            self.driver.switch_to.window(self.tabs[index])
            self.driver.close()
            self.tabs.pop(index)
            # Cambia a la última pestaña activa después de cerrar
            if self.tabs:
                self.driver.switch_to.window(self.tabs[-1])
        else:
            print("Índice de pestaña fuera de rango")

    def navegar_a_url(self, url):
        """
        Navega a una URL en la pestaña actualmente activa.

        Parámetros:
        -----------
        url : str
            La URL a la que se desea navegar en la pestaña activa.
        """
        self.driver.get(url)

    def cerrar_navegador(self):
        """
        Cierra el navegador completamente y todas las pestañas abiertas.
        """
        self.driver.quit()
