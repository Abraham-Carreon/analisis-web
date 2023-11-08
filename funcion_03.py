import socket 

def escanear_puertos(ip, puertos_a_escanear):
    try:
        with open("Reporte_Escaneo.txt", "w") as archivo:
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
        print("Error de conexión")
        sys.exit()
