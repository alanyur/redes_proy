import time
import requests

# URL del servidor final que entrega los últimos 20 datos del sensor en formato JSON
URL = "http://127.0.0.1:8000/api/ultimos"

# Bucle infinito para consultar el servidor cada 10 segundos
while True:
    try:
        # Solicita los últimos datos al servidor
        resp = requests.get(URL)
        
        if resp.status_code == 200:
            # Convierte la respuesta JSON en una lista de diccionarios
            datos = resp.json()

            # Analiza cada dato recibido
            for d in datos:
                # Verifica si la temperatura está fuera del rango esperado (0°C a 40°C)
                if d["temperatura"] > 40 or d["temperatura"] < 0:
                    print(f"[ALERTA] Temperatura fuera de rango: {d['temperatura']}°C")

                # Alerta si la humedad supera el 90%
                if d["humedad"] > 90:
                    print(f"[ALERTA] Humedad alta: {d['humedad']}%")

                # Alerta si la presión atmosférica es baja (menos de 960 hPa)
                if d["presion"] < 960:
                    print(f"[ALERTA] Presión baja: {d['presion']} hPa")
        else:
            # Imprime error si el código de respuesta HTTP no es 200
            print(f"[Error] Código de respuesta: {resp.status_code}")

    except Exception as e:
        # Captura cualquier error de conexión o excepción durante la solicitud
        print(f"[Error] No se pudo consultar el servidor: {e}")

    # Espera 10 segundos antes de hacer la siguiente consulta
    time.sleep(10)

