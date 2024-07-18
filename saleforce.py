from src.saleforce import Saleforce
import pandas as pd
import sys

def main():
    nombre=input("ingrese el nombre del archivo (sin extencion .xlsx): \n>")
    

    

    lista=[]
    try:
        df=pd.read_excel(f"{nombre}.xlsx")
        sf=Saleforce()
        sf.inicio_sesion()
    except:
        print("No existe!!!\npresione enter para terminar")
        input()
        sys.exit()
    
    for i in df["ruc"]:
        diccionario={
            "ruc":i,
        }
        nuevo={**diccionario, **sf.consultar_sale(i, ["Pc", "Nodo"])}
        
        
        lista.append(nuevo)
        #print(sf.consultar_sale(i,["Pc","Nodo"]))
        
        
    df=pd.DataFrame(lista)

    df.to_excel(f"{nombre}-SF.xlsx", index=False)
    
if __name__=="__main__":
    main()


