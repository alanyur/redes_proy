import subprocess
import time
import os

# Lanza el servidor final (Flask) en segundo plano
def ejecutar_servidor_final():
    return subprocess.Popen(["python3", "./servidor_final.py"])

# Lanza el servidor intermedio (socket TCP) en segundo plano
def ejecutar_servidor_intermedio():
    return subprocess.Popen(["python3", "./servidor_intermedio.py"])

# Lanza el cliente sensor (programa en C++) si está compilado como ejecutable
def ejecutar_cliente_sensor():
    ruta = "./cliente_sensor"
    if not os.path.exists(ruta):
        print("❌ Ejecutable del cliente sensor no encontrado.")
        return None
    return subprocess.Popen([ruta])

# Lanza el cliente de consulta (que detecta alertas)
def ejecutar_consulta_cliente():
    ruta = "./consulta_cliente.py"
    if not os.path.exists(ruta):
        print("❌ Script consulta_cliente.py no encontrado.")
        return None
    return subprocess.Popen(["python3", ruta])

# Punto de entrada principal
if __name__ == "__main__":
    print("🟢 Iniciando todos los módulos del sistema...\n")

    # Lanzar procesos en orden con pequeñas esperas
    proc_final = ejecutar_servidor_final()
    time.sleep(1)  # Da tiempo a que el servidor final levante

    proc_intermedio = ejecutar_servidor_intermedio()
    time.sleep(1)  # Da tiempo a que el servidor intermedio escuche

    proc_sensor = ejecutar_cliente_sensor()
    proc_consulta = ejecutar_consulta_cliente()

    print("\n✅ Todos los procesos fueron lanzados.")
    print("Presiona Ctrl+C para detener.")

    try:
        # Espera a que los procesos terminen (hasta Ctrl+C)
        proc_final.wait()
        proc_intermedio.wait()
        if proc_sensor:
            proc_sensor.wait()
        if proc_consulta:
            proc_consulta.wait()

    except KeyboardInterrupt:
        # Si el usuario interrumpe, terminamos todos los procesos
        print("\n🛑 Deteniendo procesos...")
        proc_final.terminate()
        proc_intermedio.terminate()
        if proc_sensor:
            proc_sensor.terminate()
        if proc_consulta:    
            proc_consulta.terminate()
        print("✅ Procesos detenidos.")

