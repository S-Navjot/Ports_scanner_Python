import socket
from datetime import datetime
import os
from concurrent.futures import ThreadPoolExecutor

#Function to clear Terminal. Working on Windonws (cls) and MAC/Linux (clear)
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def host_target():
    user_input_ip = input("Enter an IP Address (IPv4) or Domain name: ")
    try:
        hostname = socket.gethostbyname(user_input_ip)
        print(f"Target: {hostname}")
        return hostname
    except socket.gaierror as e:
        print(f"Error: {e}. Please enter a valid IP address or domain name.")
        return host_target()

def get_ports_to_scan():
    while True:
        user_input = input("Enter ports to scan (e.g., 22, 80, 1000-2000): ")
        print()
        ports = []
        ranges = user_input.split(',')
        try:
            for part in ranges:
                if '-' in part:
                    start, end = map(int, part.split('-'))
                    if start < 1 or end > 65535:
                        raise ValueError("Ports must be between 0 and 65535")
                    ports.extend(range(start, end + 1))
                else:
                    port = int(part)
                    if port < 1 or port > 65535:
                        raise ValueError("Ports must be between 0 and 65535")
                    ports.append(port)
            return ports
        except ValueError as e:
            print(f"Error: {e}. Please enter valid ports.")

def scan_port(target, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(1)
    result = s.connect_ex((target, port))
    s.close()
    return port, result

def scan_ports(target, ports):
    with ThreadPoolExecutor(max_workers=100) as executor:
        futures = [executor.submit(scan_port, target, port) for port in ports]
        for future in futures:
            port, result = future.result()
            if result == 0:
                print(f'{target} : {port}/TCP is [open]')

def scanners():
    while True:
        clear_screen()
        target = host_target()
        if not target:
            continue
        ports = get_ports_to_scan()
        start = datetime.now()
        try:
            scan_ports(target, ports)
        except Exception as e:
            print(f"Error: {e}")
        end = datetime.now()
        print(f"\nScan duration: {end - start}")
        break

if __name__ == '__main__':
    clear_screen()
    print("""Welcome in this TCP Ports scanner!
          \nGithub : https://github.com/S-Navjot/Ports_scanner_Python/tree/main
          \nPlease select your choice:""")
    while True:
        user_choice = int(input("""\n1 - Scan ports (single, range, or multiple)
                                   \n2 - Quit the program 
                                   \nSelect a choice between 1 and 2: """))
        if user_choice == 1:
            scanners()
        elif user_choice == 2:
            quit()
        else:
            print("\nError, you must select a number between 1 and 2")
