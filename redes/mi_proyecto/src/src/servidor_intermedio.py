# servidor_intermedio_py/servidor_intermedio.py
import socket
import struct
import json
import requests

HOST = '127.0.0.1'
PORT = 5000
FORMATO_BINARIO = '<h d f f f'  # ID, fecha_hora, temp, presion, humedad

def recibir_datos(conn):
    tamanio = struct.calcsize(FORMATO_BINARIO)
    datos = conn.recv(tamanio)
    print(f"[Debug] Recibido {len(datos)} bytes")

    if not datos or len(datos) < tamanio:
        return None

    try:
        unpacked = struct.unpack(FORMATO_BINARIO, datos)
        print("[DEBUG] Unpacked:", unpacked)
    except Exception as e:
        print("[ERROR] unpack falló:", e)
        return None

    return {
        'id': unpacked[0],
        'timestamp': unpacked[1],
        'temperatura': unpacked[2],
        'presion': unpacked[3],
        'humedad': unpacked[4]
    }



def reenviar(datos_dict):
    try:
        response = requests.post("http://127.0.0.1:8000/api/datos", json=datos_dict)
        print("Reenviado al servidor final:", response.status_code)
    except Exception as e:
        print("Error al reenviar:", e)

def servidor_intermedio():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print(f"[Servidor Intermedio] Escuchando en {HOST}:{PORT}")
        while True:
            conn, addr = s.accept()
            with conn:
                print(f"[+] Conexión desde {addr}")
                datos = recibir_datos(conn)
                if datos:
                    print("[OK] Datos recibidos:", datos)
                    reenviar(datos)
                else:
                    print("[!] Datos inválidos")

if __name__ == "__main__":
    servidor_intermedio()
