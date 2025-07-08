#include <iostream>     
#include <ctime>       
#include <cstdlib>      
#include <unistd.h>     
#include <arpa/inet.h>  // Para funciones de red (sockets, inet_pton, etc.)

// Estructura compacta que representa un paquete de datos del sensor
#pragma pack(push, 1)
struct SensorData {
    int16_t id;          // ID del sensor
    double timestamp;    // Marca de tiempo (Unix epoch)
    float temperatura;   // Temperatura en °C
    float presion;       // Presión en hPa
    float humedad;       // Humedad relativa en %
};
#pragma pack(pop)

int main() {
    // Dirección y puerto del servidor intermedio
    const char* SERVER_IP = "127.0.0.1";
    const int SERVER_PORT = 5000;

    int16_t sensor_id = 101; // ID inicial del sensor

    while (true) {
        // Crear socket TCP
        int sock = socket(AF_INET, SOCK_STREAM, 0);
        if (sock < 0) {
            std::cerr << "Error creando socket\n";
            return 1;
        }

        // Configurar dirección del servidor
        sockaddr_in serverAddr{};
        serverAddr.sin_family = AF_INET;
        serverAddr.sin_port = htons(SERVER_PORT); // Puerto en orden de red
        inet_pton(AF_INET, SERVER_IP, &serverAddr.sin_addr); // Convertir IP

        // Conectar con el servidor
        if (connect(sock, (sockaddr*)&serverAddr, sizeof(serverAddr)) < 0) {
            std::cerr << "No se pudo conectar al servidor intermedio\n";
            close(sock); // Cerrar socket antes de reintentar
            sleep(5);    // Esperar 5 segundos y volver a intentar
            continue;
        }

        // Generar datos simulados del sensor
        SensorData datos;
        datos.id = sensor_id;
        datos.timestamp = static_cast<double>(std::time(nullptr)); // Tiempo actual en segundos
        datos.temperatura = 20.0f + static_cast<float>(rand() % 1000) / 50.0f; // 20°C a ~40°C
        datos.presion = 950.0f + static_cast<float>(rand() % 1000) / 10.0f;    // 950 hPa a ~1050 hPa
        datos.humedad = 30.0f + static_cast<float>(rand() % 700) / 10.0f;      // 30% a ~100%

        // Mostrar los datos generados
        std::cout << "[Sensor] Enviando: ID=" << datos.id
                  << " Temp=" << datos.temperatura
                  << " Pres=" << datos.presion
                  << " Hum=" << datos.humedad
                  << " Time=" << datos.timestamp << "\n";

        // Enviar los datos al servidor intermedio
        ssize_t sent = send(sock, &datos, sizeof(datos), 0);
        if (sent > 0)
            std::cout << "[Sensor] Datos enviados correctamente (" << sent << " bytes)\n";
        else
            std::cerr << "Error al enviar datos\n";

        close(sock);     // Cerrar conexión
        sensor_id++;     // Incrementar ID para siguiente envío

        sleep(5);        // Esperar 5 segundos antes del siguiente envío
    }

    return 0;
}
