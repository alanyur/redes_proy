from flask import Flask, request, render_template_string
import sqlite3
import os

# Ruta al archivo de base de datos SQLite
DB_PATH = "datos.db"

# Crear una instancia de la aplicación Flask
app = Flask(__name__)

# Función para inicializar la base de datos con la tabla necesaria
def inicializar_bd():
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        # Crear la tabla "mediciones" si no existe
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS mediciones (
                id INTEGER,
                timestamp REAL,
                temperatura REAL,
                presion REAL,
                humedad REAL
            )
        ''')
        conn.commit()

# Ruta API que recibe datos del servidor intermedio
@app.route('/api/datos', methods=['POST'])
def recibir():
    datos = request.get_json()  # Recibe JSON desde el servidor intermedio
    if not datos:
        return {"error": "No se recibieron datos"}, 400

    try:
        # Insertar los datos en la base de datos
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO mediciones (id, timestamp, temperatura, presion, humedad)
                VALUES (?, ?, ?, ?, ?)
            ''', (
                datos['id'],
                datos['timestamp'],
                datos['temperatura'],
                datos['presion'],
                datos['humedad']
            ))
            conn.commit()
        print("[Servidor Final] Datos almacenados:", datos)
        return {"mensaje": "Datos almacenados"}, 200

    except Exception as e:
        print("Error al guardar en la base:", e)
        return {"error": "Fallo al guardar datos"}, 500

# Ruta web para visualizar los últimos 20 datos con gráficos
@app.route('/')
def ver_datos():
    import datetime  # Importar aquí para evitar conflictos si Flask corre en modo producción
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM mediciones ORDER BY timestamp DESC LIMIT 20")
        datos = cursor.fetchall()

    # Preparar los datos para el gráfico: invertir para mostrar del más antiguo al más reciente
    datos = datos[::-1]
    etiquetas = [datetime.datetime.fromtimestamp(row[1]).strftime('%H:%M:%S') for row in datos]
    temperaturas = [row[2] for row in datos]
    presiones = [row[3] for row in datos]
    humedades = [row[4] for row in datos]

    # HTML embebido con plantilla y gráfico usando Chart.js
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Dashboard Sensorial</title>
        <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
        <style>
            body { font-family: sans-serif; padding: 20px; }
            h1, h2 { text-align: center; }
            table { border-collapse: collapse; width: 100%; margin-top: 30px; }
            th, td { border: 1px solid #ccc; padding: 8px; text-align: center; }
            th { background-color: #f2f2f2; }
            canvas { max-width: 100%; margin-top: 40px; }
        </style>
        <script>
            // Recarga automática cada 5 segundos para actualizar los datos en tiempo real
            setTimeout(() => {
                window.location.reload();
            }, 5000);
        </script>
    </head>
    <body>
        <h1>Dashboard Sensorial</h1>
        <canvas id="graficoSensor"></canvas>

        <h2>Últimos 20 Datos del Sensor</h2>
        <table>
            <tr>
                <th>ID</th><th>Timestamp</th><th>Temperatura (°C)</th><th>Presión (hPa)</th><th>Humedad (%)</th>
            </tr>
            {% for fila in datos %}
            <tr>
                <td>{{ fila[0] }}</td>
                <td>{{ fila[1] }}</td>
                <td>{{ fila[2] }}</td>
                <td>{{ fila[3] }}</td>
                <td>{{ fila[4] }}</td>
            </tr>
            {% endfor %}
        </table>

        <script>
        const ctx = document.getElementById('graficoSensor').getContext('2d');
        const chart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: {{ etiquetas|tojson }},
                datasets: [
                    {
                        label: 'Temperatura (°C)',
                        data: {{ temperaturas|tojson }},
                        borderColor: 'red',
                        fill: false
                    },
                    {
                        label: 'Presión (hPa)',
                        data: {{ presiones|tojson }},
                        borderColor: 'blue',
                        fill: false
                    },
                    {
                        label: 'Humedad (%)',
                        data: {{ humedades|tojson }},
                        borderColor: 'green',
                        fill: false
                    }
                ]
            },
            options: {
                responsive: true,
                scales: {
                    y: { beginAtZero: false },
                    x: { title: { display: true, text: 'Hora' } }
                }
            }
        });
        </script>
    </body>
    </html>
    """

    return render_template_string(
        html,
        datos=datos,
        etiquetas=etiquetas,
        temperaturas=temperaturas,
        presiones=presiones,
        humedades=humedades
    )

# API que devuelve los últimos 20 registros como JSON
@app.route('/api/ultimos', methods=['GET'])
def api_ultimos():
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM mediciones ORDER BY timestamp DESC LIMIT 20")
        filas = cursor.fetchall()

    resultado = [
        {"id": f[0], "timestamp": f[1], "temperatura": f[2], "presion": f[3], "humedad": f[4]}
        for f in filas
    ]
    return resultado

# Punto de entrada principal del programa
if __name__ == "__main__":
    inicializar_bd()  # Asegura que la base esté creada antes de iniciar
    print("[Servidor Final] Corriendo en puerto 8000")
    app.run(host="127.0.0.1", port=8000)

