#include <iostream>
#include <ctime>
#include <cstdlib>
#include <unistd.h>
#include <arpa/inet.h>

#pragma pack(push, 1)
struct SensorData {
    int16_t id;
    double timestamp;
    float temperatura;
    float presion;
    float humedad;
};
#pragma pack(pop)

int main() {
    const char* SERVER_IP = "127.0.0.1";
    const int SERVER_PORT = 5000;

    int16_t sensor_id = 101;

    while (true) {
        int sock = socket(AF_INET, SOCK_STREAM, 0);
        if (sock < 0) {
            std::cerr << "Error creando socket\n";
            return 1;
        }

        sockaddr_in serverAddr{};
        serverAddr.sin_family = AF_INET;
        serverAddr.sin_port = htons(SERVER_PORT);
        inet_pton(AF_INET, SERVER_IP, &serverAddr.sin_addr);

        if (connect(sock, (sockaddr*)&serverAddr, sizeof(serverAddr)) < 0) {
            std::cerr << "No se pudo conectar al servidor intermedio\n";
            close(sock);
            sleep(5);
            continue;
        }

        SensorData datos;
        datos.id = sensor_id;
        datos.timestamp = static_cast<double>(std::time(nullptr));
        datos.temperatura = 20.0f + static_cast<float>(rand() % 1000) / 50.0f;
        datos.presion = 950.0f + static_cast<float>(rand() % 1000) / 10.0f;
        datos.humedad = 30.0f + static_cast<float>(rand() % 700) / 10.0f;

        std::cout << "[Sensor] Enviando: ID=" << datos.id
                  << " Temp=" << datos.temperatura
                  << " Pres=" << datos.presion
                  << " Hum=" << datos.humedad
                  << " Time=" << datos.timestamp << "\n";

        ssize_t sent = send(sock, &datos, sizeof(datos), 0);
        if (sent > 0)
            std::cout << "[Sensor] Datos enviados correctamente (" << sent << " bytes)\n";
        else
            std::cerr << "Error al enviar datos\n";

        close(sock);
        sensor_id++; // incrementa el ID en cada iteración

        // Opcional: reiniciar ID si quieres limitar el rango (ej. 101 a 110)
        if (sensor_id > 110)
            sensor_id = 101;

        sleep(5); // espera 5 segundos antes del siguiente envío
    }

    return 0;
}
