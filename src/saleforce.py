import requests
from dotenv import load_dotenv
from bs4 import BeautifulSoup as sp
import time
import os
class Saleforce:
    def __init__(self) -> None:
        # Cargar las variables de entorno desde el archivo .env
        load_dotenv()
        self.user=os.getenv("USUARIO_SALEFORCE")
        self.password=os.getenv("PASSWORD")
        self.sesion=requests.Session()
        self.estado_de_sesion = False  # Variable para rastrear el estado de inicio de sesión

    def inicio_sesion(self):
        if not self.estado_de_sesion:  # Solo iniciar sesión si no está ya iniciada
            data = {
                'username': self.user,
                'pw': self.password,
                'un': self.user,
            }
            self.sesion.post('https://telefonicab2b.my.site.com/fvi/login', data=data)
            r=self.sesion.get('https://telefonicab2b.my.site.com/fvi/_ui/search/ui/UnifiedSearchResults?searchType=2&sen=001&sen=003&sen=005&sen=500&sen=006&str=20522317285')
            if r.ok:
                self.estado_de_sesion = True
                print("Inicio de sesión exitoso")
            else:
                print("Error en el inicio de sesión")
                
    def consultar_sale(self,ruc,campos=["Pc", "Nodo", "Sub segmento global","Sub segmento local","contacto"]):
        data_saleForce={}
        try:
            timeout=(400,1200)
            tiempo_nuevo_intento=2
            #consulta de ruc con sesion iniciada
            url2=f'https://telefonicab2b.my.site.com/fvi/_ui/search/ui/UnifiedSearchResults?searchType=2&sen=001&sen=003&sen=005&sen=500&sen=006&str={ruc}'
            response= self.sesion.get(url2, timeout=timeout)
            html=response.text
            # Crear un objeto BeautifulSoup
            soup = sp(html, 'html.parser')
            # Usar el método find o find_all de BeautifulSoup para seleccionar la tabla con la clase list
            table = soup.find('table', class_='list') # Puedes usar find_all si hay más de una tabla con esa clase
            if table == None:
                for campo in campos:
                    data_saleForce[campo]=""
                    
                return data_saleForce
            else:
                # Usar el método find_all de BeautifulSoup para seleccionar todos los elementos a que tienen el atributo href dentro de la tabla
                links = table.find_all('a', href=True)
                consulta=links[-3].get('href')
                #entremos a la informacion del ruc encontrado
                response=self.sesion.get(f'https://telefonicab2b.my.site.com{consulta}')
                html=response.text
                # Crear un objeto BeautifulSoup
                soup = sp(html, 'html.parser')
                # verificamos que sea un cliente o que el id de la eqiqueta exista
                verifi = soup.find(id="CF00Nw00000097xcg_ilecell" )
                if verifi == None:
                    for campo in campos:
                        if campo== "Nodo":
                            data_saleForce[campo]="Error"
                        else:
                            data_saleForce[campo]=""
                            
                    return data_saleForce
                else:
                    for campo in campos:
                        if campo=="Pc":
                            data_saleForce[campo]=pc=soup.find(id="acc1_ileinner").text.replace("\xa0[Cambiar]","")                 
                        elif campo=="Nodo":
                            data_saleForce[campo]=nodo = soup.find(id="CF00Nw00000097xcg_ilecell").text
                        elif campo=="Sub segmento global":
                            data_saleForce[campo]=sub_seg_global=soup.find(id="00Nw0000008XxJ2_ileinner").text
                        elif campo=="Sub segmento local":
                            data_saleForce[campo]=sub_seg_local=soup.find(id="00Nw0000008XxJ1_ileinner").text
                        elif campo=="contacto":
                            
                    
                    
                            filas=soup.find('table', class_='list').find_all('tr')
                            datos_tabla=[]

                            for fila in filas:
                                # Encontrar todas las celdas de la fila
                                celdas = fila.find_all(['td', 'th'])
                                # Extraer el texto de cada celda y añadirlo a la lista de datos
                                datos_fila = [celda.get_text(strip=True) for celda in celdas]
                                datos_tabla.append(datos_fila)
                                # Eliminar la primera fila
                                sinEncabezado = datos_tabla[1:]
                                data_saleForce[campo]=sinEncabezado

                return data_saleForce
        except requests.exceptions.ConnectionError as e:
            print(f"Error de conexión en consultar_sale: {e}")
            print(f"consulta sale, esperamos {tiempo_nuevo_intento} segundos...")
            time.sleep(tiempo_nuevo_intento)
            return self.consultar_sale(ruc)  # Reintento de la solicitud}