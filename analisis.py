import argparse
import os
from funciones import busquedaCorreos
from funcion_03 import escanear_puertos, eliminarArchivosPrevios, leer_k, virus_api

if __name__ == '__main__':
    """
    Lista de funciones 
    """
    parser = argparse.ArgumentParser(description="Codigo con herramientas de ciberseguridad")
    parser.add_argument("-url", dest="url", help="Ingrese una url de la web a analizar")
    parser.add_argument("-vchk", metavar="VirusCheck", dest="VirusCheck", help="Nombre del archivo a analizar")
    parser.add_argument("-sct", metavar="ScanTarget", dest="ScanTarget", help="URL o IP junto con los puertos a escanear separados por comas (ejemplo: 'www.wikipedia.com,8080,80,90')") 
    params = parser.parse_args()

    """
    Crear carpetas para almacenar reportes
    """
    if not os.path.exists("Consultas"):
        os.makedirs("Consultas")
    if not os.path.exists("Reportes"):
        os.makedirs("Reportes")

    elif params.url:
        """
        Scrapping web y eliminar archivos previos 
        """
        if len(params.url) > 0:
            eliminarArchivosPrevios()
            busquedaCorreos(params.url)
        else:
            print("La URL es requerida")
    elif params.VirusCheck:
        """
        Realizar consulta VirusTotal y leer la clave del API
        """
        if len(params.VirusCheck) > 0:
            file = params.VirusCheck
            key = leer_k()
            if key:
                info = virus_api(file, key)
    elif params.ScanTarget:
        """
        Escanear puertos
        """
        target = params.ScanTarget.split(',')
        ip = target[0]
        if len(target) > 1:
            ports = []
            for port in target[1:]:
                ports.append(int(port))
        else:
            """
            En caso de que no se agregen puertos, default 80 y 8080
            """
            ports = [80, 8080]
        escanear_puertos(ip, ports)
    else:
        print("No hay argumentos")
