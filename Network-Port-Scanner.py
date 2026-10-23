import os
import socket
import ipaddress
from datetime import datetime

# ==========================================
#          NETWORK PORT SCANNER
# ==========================================

print("=" * 45)
print("          NETWORK PORT SCANNER")
print("=" * 45)


hostname = socket.gethostname()

try:
    local_ip = socket.gethostbyname(hostname)
except socket.gaierror:
    local_ip = "Unavailable"

print("Computer Name:", hostname)
print("Local IP Address:", local_ip)


def scan_port(target, port):
    scanner = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    scanner.settimeout(1)

    try:
        result = scanner.connect_ex((target, port))

        if result == 0:
            print(f"[OPEN]   Port {port}")
            return "OPEN"

        else:
            print(f"[CLOSED] Port {port}")
            return "CLOSED OR UNAVAILABLE"

    except socket.error as error:
        print(f"[ERROR]  Port {port}: {error}")
        return "ERROR"

    finally:
        scanner.close()


try:
    target = input("\nEnter target IPv4 address: ").strip()
    target_ip = ipaddress.ip_address(target)

    if not isinstance(target_ip, ipaddress.IPv4Address):
        raise ValueError("IPv4 address required.")

except ValueError:
    print("Error: Please enter a valid IPv4 address.")
    print("Example: 127.0.0.1")
    raise SystemExit


try:
    start_port = int(input("Enter starting port (1-65535): "))
    end_port = int(input("Enter ending port (1-65535): "))

    if not (1 <= start_port <= 65535):
        raise ValueError("Starting port must be between 1 and 65535.")

    if not (1 <= end_port <= 65535):
        raise ValueError("Ending port must be between 1 and 65535.")

    if start_port > end_port:
        raise ValueError("Starting port cannot exceed ending port.")

except ValueError as error:
    print("Input Error:", error)
    raise SystemExit


print("\n" + "=" * 45)
print("SCAN STARTED")
print("Target:", target)
print(f"Port Range: {start_port}-{end_port}")
print("=" * 45)

open_ports = 0
ports_scanned = 0
scan_results = []

scan_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")


for port in range(start_port, end_port + 1):
    status = scan_port(target, port)
    ports_scanned += 1

    if status == "OPEN":
        open_ports += 1

    scan_results.append(
        f"Port {port}: {status}"
    )


closed_ports = ports_scanned - open_ports

print("\n" + "=" * 45)
print("              SCAN SUMMARY")
print("=" * 45)
print("Target IP:", target)
print("Scan Time:", scan_time)
print("Ports Scanned:", ports_scanned)
print("Open Ports:", open_ports)
print("Closed or Unavailable:", closed_ports)
print("=" * 45)


try:
    with open(
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "scan_results.txt"),
    "w",
    encoding="utf-8") as file:
        file.write("NETWORK PORT SCANNER REPORT\n")
        file.write("=" * 40 + "\n")
        file.write(f"Computer Name: {hostname}\n")
        file.write(f"Local IP: {local_ip}\n")
        file.write(f"Target IP: {target}\n")
        file.write(f"Scan Time: {scan_time}\n")
        file.write(f"Port Range: {start_port}-{end_port}\n\n")

        file.write("PORT SCAN RESULTS\n")
        file.write("-" * 40 + "\n")

        for result in scan_results:
            file.write(result + "\n")

        file.write("\nSCAN SUMMARY\n")
        file.write("-" * 40 + "\n")
        file.write(f"Ports Scanned: {ports_scanned}\n")
        file.write(f"Open Ports: {open_ports}\n")
        file.write(f"Closed or Unavailable: {closed_ports}\n")

    print("\nResults saved to scan_results.txt")

except OSError as error:
    print("Could not save results:", error)

print("SCAN COMPLETED SUCCESSFULLY")