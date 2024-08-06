# Python Port Scanner by S-Navjot

This project is a Python script that allows you to scan the ports of a specified IP address. The script uses the `socket` library to establish connections and determine the status of ports, as well as `ThreadPoolExecutor` to perform port scanning in parallel.

## Features  

- Scan ports of an IP address (IPv4)
- Utilizes parallelization to speed up the scan
- Displays open ports

## Installation  

### Prerequisites  

- Python 3.x must be installed on your machine. You can download it from [python.org](https://www.python.org/).

### Installation Steps  

1. Clone the GitHub repository:

   ```sh
   git clone https://github.com/S-Navjot/Ports_scanner_Python.git

### Usage Steps    

Open the Terminal
```sh
$ cd Ports_scanner_Python
$ python3 main.py
```

1. Enter the IPv4 Address you want to scan  
2. Enter first port to scan  
3. Enter last port to scan  

### Libraries Used  

* socket (https://docs.python.org/3/library/datetime.html)  
* datetime (https://docs.python.org/3/library/datetime.html)  
* os (https://docs.python.org/fr/3/library/os.html)  
* concurrent.futures (https://docs.python.org/3/library/concurrent.futures.html)  


### OS

Working on :
* Windows
* Linux
* MAC

## Versions

V1 (3rd August 2024)
--------------------
- First release

V1.1 (6th August 2024)
--------------------
- User can now select :
  - a single port (eg 22)
  - a range of ports (eg 100-200 (from 100 to 200))
  - multiple ports (eg 22, 80, 100-200 (22, 80 and from 100 to 200))
- User can't select a port lower than 1 or higher than 65535
- User can now choose between scan ports or leave the program
- Minor display updates 
