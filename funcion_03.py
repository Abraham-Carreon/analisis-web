import socket
import os
import logging
import sys
import hashlib
from virus_total_apis import PublicApi
from datetime import datetime  # Importar datetime para obtener la marca de tiempo
logging.basicConfig(filename='JAK.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def escanear_puertos(ip, puertos_a_escanear):
    try:
        # Crear un nombre de archivo con marca de tiempo
        now = datetime.now()
        timestamp = now.strftime("%m-%d-%H-%M-%S")
        filename = f'Reportes/Reporte_Scan_{timestamp}.txt'

        with open(filename, "w") as archivo:
            archivo.write("Objetivo:\t {}\n".format(ip))
            for puerto in puertos_a_escanear:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(5)
                resultado = s.connect_ex((ip, puerto))
                if resultado == 0:
                    archivo.write("Puerto {}:\t Abierto\n".format(puerto))
                else:
                    archivo.write("Puerto {}:\t Cerrado\n".format(puerto))
                s.close()
    except socket.error as error:
        logging.error("Error de conexion")
        sys.exit()


def leer_k():
    """
    Funcion para leer el archivo que contiene la apikey
    """
    key = os.path.join("key", "apikey.txt")
    try:
        
        with open(key, "r") as f:
            return f.read().strip()
    except FileNotFoundError:
        logging.error("No existe apikey.txt. Agrega en la carpeta el archivo y coloca tu API_Key en el desde virus total.")
        return None
    logging.info("Llave obtenida exitosamente")

def virus_api(file, key):
    api = PublicApi(key)

    with open(file, "rb") as f:
        hash_md5 = hashlib.md5(f.read()).hexdigest()

    resp = api.get_file_report(hash_md5)

    info = ""

    if "response_code" in resp and resp["response_code"] == 200:
        if "results" in resp:
            msg = resp["results"].get("verbose_msg", "...")
            info += f'Verbose message: {msg}\n'

            if "positives" in resp["results"]:
                if resp["results"]["positives"] > 0:
                    info += "Archivo malicioso\n"
                else:
                    info += "Archivo seguro\n"

            sha1 = resp["results"].get("sha1", "sin datos")
            sha256 = resp["results"].get("sha256", "sin datos")
            fecha = resp["results"].get("scan_date", "sin datos")
            total = resp["results"].get("total", "sin datos")
            permalink = resp["results"].get("permalink", "sin datos")

            info += f'SHA1: {sha1}\n'
            info += f'SHA256: {sha256}\n'
            info += f'Fecha escaneo: {fecha}\n'
            info += f'Motores de escaneo usados: {total}\n'
            info += f'Enlace al informe completo: {permalink}\n'
        else:
            info += "Sin resultados.\n"
    else:
        info += "No fue posible conectar.\n"
        logging.error("No fue posible conectar")

    now = datetime.now()
    timestamp = now.strftime("%m-%d-%H-%M-%S")
    filename = f'Consultas/Reporte_VT_{timestamp}.txt'

    with open(filename, "w") as f:
        f.write(info)

    return info
def eliminarArchivosPrevios():
    """ 
    Se usa para eliminar las imagenes y pdf pasados
    """
    carpetas_a_borrar = ["img", "pdf"]
    for carpeta in carpetas_a_borrar:
        try:
            for archivo in os.listdir(carpeta):
                ruta_archivo = os.path.join(carpeta, archivo)
                os.remove(ruta_archivo)
        except FileNotFoundError:
            logging.info("Eliminacion de archivos terminada fallida")
            pass
