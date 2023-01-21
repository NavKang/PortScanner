import socket
import threading
from termcolor import colored
import pyfiglet

def doozy():
    ascii_art = pyfiglet.figlet_format("doozy")
    print(ascii_art)

doozy()

# Define the target host and ports to scan
host = input("Enter the target host: ")
start_port = int(input("Enter the start port: "))
end_port = int(input("Enter the end port: "))
retries = int(input("Enter the number of retries: "))
save_to_file = input("Do you want to save the results to a file? (y/n) ")

open_ports = []

def scan(host, port, retries):
    global open_ports
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        result = sock.connect_ex((host, port))
        if result == 0:
            open_ports.append(port)
            return colored(f'Port {port} is open', 'green')
        else:
            if retries > 0:
                return scan(host, port, retries-1)
            else:
                return colored(f'Port {port} is closed', 'red')
    except:
        if retries > 0:
            return scan(host, port, retries-1)
        else:
            return colored(f'Error in connecting to {host}:{port}', 'yellow')

def threaded_scan(host, start_port, end_port, retries):
    threads = []
    for port in range(start_port, end_port+1):
        t = threading.Thread(target=scan, args=(host, port, retries))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

threaded_scan(host, start_port, end_port, retries)

if open_ports:
    print(f'Open ports: {open_ports}')
else:
    print("No open ports found.")

if save_to_file.lower() == 'y':
    with open('port_scan_results.txt', 'w') as f:
        for port in open_ports:
            f.write(f"{port}\n")
        print(f"Results saved to port_scan_results.txt")
