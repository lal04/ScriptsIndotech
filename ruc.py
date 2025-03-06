from src.navegador import Navegador
from src.sunat_selenium import Sunat
from src.utilidades import Utilidades
def main():
    data_frame= Utilidades.leer_archivo('BD')
    
    sunat=Sunat(Navegador())
    
    for item in data_frame['RUC']:
        print(f"\n{item}\n\n")
        print(sunat.consultar(item))
    

if __name__ == '__main__':
    main()