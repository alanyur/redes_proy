import socket       # Para comunicaciones TCP
import struct       # Para desempaquetar datos binarios
import json         # (No se usa directamente, pero útil si se quiere guardar localmente)
import requests     # Para reenviar los datos como JSON vía HTTP al servidor final

# Dirección IP y puerto en los que este servidor intermedio escucha conexiones
HOST = '127.0.0.1'
PORT = 5000

# Estructura del paquete binario esperado: short, double, float, float, float
# ('<' indica little-endian)
FORMATO_BINARIO = '<h d f f f'  # id (int16), timestamp (double), temperatura, presion, humedad (floats)

# Función para recibir y desempaquetar datos desde el cliente sensor
def recibir_datos(conn):
    tamanio = struct.calcsize(FORMATO_BINARIO)  # Calcula cuántos bytes debe leer
    datos = conn.recv(tamanio)                  # Recibe exactamente ese número de bytes
    print(f"[Debug] Recibido {len(datos)} bytes")

    if not datos or len(datos) < tamanio:
        return None  # Si no hay datos suficientes, retornar None

    try:
        # Desempaquetar los datos binarios en variables Python
        unpacked = struct.unpack(FORMATO_BINARIO, datos)
        print("[DEBUG] Unpacked:", unpacked)
    except Exception as e:
        print("[ERROR] unpack falló:", e)
        return None

    # Convertir la tupla desempacada en un diccionario
    return {
        'id': unpacked[0],
        'timestamp': unpacked[1],
        'temperatura': unpacked[2],
        'presion': unpacked[3],
        'humedad': unpacked[4]
    }

# Función para reenviar los datos ya desempaquetados al servidor final mediante HTTP POST
def reenviar(datos_dict):
    try:
        response = requests.post("http://127.0.0.1:8000/api/datos", json=datos_dict)
        print("Reenviado al servidor final:", response.status_code)
    except Exception as e:
        print("Error al reenviar:", e)

# Función principal que implementa el servidor TCP que recibe datos binarios
def servidor_intermedio():
    # Crear un socket TCP
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))  # Asociar a IP y puerto
        s.listen()            # Escuchar conexiones entrantes
        print(f"[Servidor Intermedio] Escuchando en {HOST}:{PORT}")

        while True:
            # Aceptar conexión de un cliente
            conn, addr = s.accept()
            with conn:
                print(f"[+] Conexión desde {addr}")
                datos = recibir_datos(conn)
                if datos:
                    print("[OK] Datos recibidos:", datos)
                    reenviar(datos)
                else:
                    print("[!] Datos inválidos")

# Punto de entrada del programa
if __name__ == "__main__":
    servidor_intermedio()
