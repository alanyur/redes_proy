import time
import requests

# Ruta que devolverá los últimos 20 datos como JSON
URL = "http://127.0.0.1:8000/api/ultimos"

while True:
    try:
        resp = requests.get(URL)

        if resp.status_code == 200:
            datos = resp.json()  # lista de diccionarios

            ids_vistos = set()
            ids_duplicados = set()

            for d in datos:
                # Detectar ID duplicado
                if d["id"] in ids_vistos:
                    ids_duplicados.add(d["id"])
                else:
                    ids_vistos.add(d["id"])

                # Verificación de rangos
                if d["temperatura"] > 40 or d["temperatura"] < 0:
                    print(f"[ALERTA] Temperatura fuera de rango: {d['temperatura']}°C")
                if d["humedad"] > 90:
                    print(f"[ALERTA] Humedad alta: {d['humedad']}%")
                if d["presion"] < 960:
                    print(f"[ALERTA] Presión baja: {d['presion']} hPa")

            # Imprimir alertas por ID duplicado si existen
            for id_repetido in ids_duplicados:
                print(f"[ALERTA] ID duplicado detectado: {id_repetido}")

        else:
            print(f"[Error] Código de respuesta: {resp.status_code}")

    except Exception as e:
        print(f"[Error] No se pudo consultar el servidor: {e}")

    time.sleep(10)  # espera 10 segundos antes de volver a consultar
