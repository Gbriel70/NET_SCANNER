from network_scanner import scan_network, monitor_dns_traffic
from port_scanner import scan_ports_concurrent

def main():
    devices = scan_network()
    if not devices:
        print("No devices found")
    else:
        print("\n🌍 Dispositivos encontrados na rede:\n")
        print("IP\t\t\tMAC\t\t\tHOSTNAME\t\t\tPORTS\t\t\tSTATUS")
        print("=" * 120)

        #ESCANEIA PORTAS DE FORMA CONCORRENTE
        scan_ports_concurrent(devices)

        #VERIFICA O STATUS DO DNS
        pihole_ip = "192.168.18.12"
        monitor_dns_traffic(devices, pihole_ip)

        for device in devices:
            open_ports_str = ", ".join(map(str, device.get('open_ports', [])))
            dns_status = device.get('dns_traffic', 'Unknown')
            print(f"{device['ip']}\t{device['mac']}\t{device['hostname']}\t{device['icmp_response']}\t\t{open_ports_str}\t\t{dns_status}")

if __name__ == "__main__":
    main()