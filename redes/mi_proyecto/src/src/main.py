import subprocess
import time
import os

def ejecutar_servidor_final():
    return subprocess.Popen(["python", "./servidor_final.py"])

def ejecutar_servidor_intermedio():
    return subprocess.Popen(["python", "./servidor_intermedio.py"])

def ejecutar_cliente_sensor():
    ruta = "./cliente_sensor"
    if not os.path.exists(ruta):
        print("❌ Ejecutable del cliente sensor no encontrado.")
        return None
    return subprocess.Popen([ruta])

if __name__ == "__main__":
    print("🟢 Iniciando todos los módulos del sistema...\n")

    proc_final = ejecutar_servidor_final()
    time.sleep(1)  # Espera 1 segundo para dar tiempo a que levante el servidor

    proc_intermedio = ejecutar_servidor_intermedio()
    time.sleep(1)  # Espera 1 segundo más

    proc_sensor = ejecutar_cliente_sensor()

    print("\n✅ Todos los procesos fueron lanzados.")
    print("Presiona Ctrl+C para detener.")

    try:
        proc_final.wait()
        proc_intermedio.wait()
        proc_sensor.wait()
    except KeyboardInterrupt:
        print("\n🛑 Deteniendo procesos...")
        proc_final.terminate()
        proc_intermedio.terminate()
        proc_sensor.terminate()
        print("✅ Procesos detenidos.")
