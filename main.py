import socket
import os
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
from netaddr import *

#Function to clear Terminal. Working on Windonws (cls) and MAC/Linux (clear)
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

#Function allowing the user to enter the Ips/domains to be scanned
def host_target():
    while True:
        user_input_ip = input("Enter an IP Address (IPv4), IP range (e.g., 192.168.0.1-192.168.0.5), or Domain names (for multiple entries use ',' as separator (e.g., localhost, 1.1.1.1)) : ")
        hosts_list = []
        n = 1
        hostnames = user_input_ip.split(",")
        try:
            for host in hostnames:
                host = host.strip()
                if "-" in host:  # Check if the user entered an IP range
                    start_ip, end_ip = host.split("-")
                    ip_range = list(IPRange(start_ip.strip(), end_ip.strip()))
                    for ip in ip_range:
                        hosts_list.append(str(ip))
                        print(f"Target {n}: {ip}")
                        n += 1
                else:
                    new_host = socket.gethostbyname(host)
                    hosts_list.append(new_host)
                    print(f"Target {n}: {new_host}")
                    n += 1
            print()
            return hosts_list
        except socket.gaierror as e:
            print(f"Error: {e}. Please enter a valid IP address or domain name.")
            return host_target()
       
#Function allowing the user to enter the port(s) to be scanned
def get_ports_to_scan():
    while True:
        user_input = input("Enter ports to scan (e.g., 22, 80, 1000-2000): ")
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


#Function that creates a socket and allows connection to the selected address and ports
def scan_port(target, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(1)
    result = s.connect_ex((target, port))
    s.close()
    return port, result

#ThreadPoolExecutor function to run up to 100 scans in parallel
def scan_ports(targets, ports):
    for target in targets:
        with ThreadPoolExecutor(max_workers=100) as executor:
            futures = [executor.submit(scan_port, target, port) for port in ports]
            for future in futures:
                port, result = future.result()
                if result == 0:
                    print(f'{target} : {port}/TCP is [open]')
        print()

#Function used to request for all information (ports, ip/domain) and time management
def scanners():
    while True:
        clear_screen()
        targets = host_target()
        if not targets:
            continue
        ports = get_ports_to_scan()
        start = datetime.now()
        try:
            scan_ports(targets, ports)
        except Exception as e:
            print(f"Error: {e}")
        end = datetime.now()
        duration = end - start
        print(f"\nScan duration: {duration}")
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
