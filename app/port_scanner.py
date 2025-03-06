import nmap
from concurrent.futures import ThreadPoolExecutor

def scan_ports(ip, port_range="1-1024"):
    nm = nmap.PortScanner()
    nm.scan(ip, port_range)
    open_ports = []
    for host in nm[ip].all_protocols():
        len_port = nm[ip][host].keys()
        for port in len_port:
            if nm[ip][host][port]['state'] == 'open':
                open_ports.append(port)
    return open_ports


def scan_ports_concurrent(devices, max_workers=10):
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(scan_ports, device['ip']): device for device in devices}
        for future in futures:
            device = futures[future]
            try:
                open_ports = future.result()
                device['open_ports'] = open_ports
            except Exception as e:
                device['open_ports'] = []
                print(f"Error scanning ports for {device['ip']}: {e}")