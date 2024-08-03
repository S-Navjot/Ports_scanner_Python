import socket
from datetime import datetime
import os
from concurrent.futures import ThreadPoolExecutor

def host_target():
    user_input_ip = input("Enter an IP Address (IPv4) : ")
    hostname = socket.gethostbyname(user_input_ip)
    print(f"Target : {hostname}")
    return hostname

def ports_to_scan():
    user_input_first_port = int(input("Enter first port of port range : "))
    user_input_last_port = int(input("Enter last port of port range : "))
    print(f"Ports range to scan : {user_input_first_port} - {user_input_last_port}")
    return [user_input_first_port, user_input_last_port]

def scan_port(target, port): #Function to scan 1 port
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(1)
    result = s.connect_ex((target, port))
    s.close()
    return port, result

def scan_ports(target, first_port, last_port):#Allow to scan multi-port in parallele
    with ThreadPoolExecutor(max_workers=100) as executor:
        ports = range(first_port, last_port + 1)
        futures = [executor.submit(scan_port, target, port) for port in ports]
        for future in futures:
            port, result = future.result()
            if result == 0:
                print(f'Port {port} is [open]')

def scanners():
    while True:
        try:
            os.system('cls' if os.name == 'nt' else 'clear')
            target = host_target()
            ports = ports_to_scan()
            start = datetime.now()
            scan_ports(target, ports[0], ports[1])
        except Exception as e:
            print(f"Error: {e}")
        end = datetime.now()
        print(f"Scan duration : {end - start}")
        break

if __name__ == '__main__':
    scanners()