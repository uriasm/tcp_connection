# tcp_connection

## Instrucciones para ejecutar el servidor y el cliente TCP

### Requisitos previos

1. **Python**: Asegúrate de tener Python instalado en tu sistema.

2. **Instalar dependencias**: Ejecuta el siguiente comando para instalar las dependencias necesarias:
    ```sh
    pip install -r requirements.txt
    ```

### Configuración

1. **Variables de entorno**: Crea un archivo `.env` en el directorio raíz del proyecto y copia el contenido de `.env.example` en él. Modifica los valores según sea necesario.

### Ejecutar el servidor

1. **Iniciar el servidor**: Ejecuta el siguiente comando para iniciar el servidor TCP:
    ```sh
    python tcp_server.py
    ```

### Ejecutar el cliente

1. **Iniciar el cliente**: Ejecuta el siguiente comando para iniciar el cliente TCP:
    ```sh
    python tcp_client.py
    ```

### Pruebas

1. **Ejecutar pruebas**: Para ejecutar las pruebas, utiliza el siguiente comando:
    ```sh
    pytest
    ```

### Notas

- Asegúrate de que el servidor esté en ejecución antes de iniciar el cliente.
- Puedes configurar el host y el puerto del servidor mediante las variables de entorno `TCP_SERVER_HOST` y `TCP_SERVER_PORT`.