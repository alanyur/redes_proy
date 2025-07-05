from flask import Flask, request, render_template_string
import sqlite3
import os

DB_PATH = "datos.db"
app = Flask(__name__)

def inicializar_bd():
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
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

@app.route('/api/datos', methods=['POST'])
def recibir():
    datos = request.get_json()
    if not datos:
        return {"error": "No se recibieron datos"}, 400

    try:
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

# NUEVA RUTA WEB PARA VER LOS DATOS
@app.route('/')
def ver_datos():
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM mediciones ORDER BY timestamp DESC LIMIT 20")
        datos = cursor.fetchall()

    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Datos del Sensor</title>
        <style>
            table { border-collapse: collapse; width: 100%; }
            th, td { border: 1px solid #ccc; padding: 8px; text-align: center; }
            th { background-color: #f2f2f2; }
        </style>
    </head>
    <body>
        <h1>Últimos 20 Datos del Sensor</h1>
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
    </body>
    </html>
    """

    return render_template_string(html, datos=datos)

if __name__ == "__main__":
    inicializar_bd()
    print("[Servidor Final] Corriendo en puerto 8000")
    app.run(host="127.0.0.1", port=8000)
