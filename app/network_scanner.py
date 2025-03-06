from scapy.all import ARP, Ether, srp, ICMP, IP, sr1
import socket
import subprocess

def scan_network(ip_range="192.168.18.12/24"):
    print(f"📡 Scanning network, IP range: {ip_range}...\n")
    
    #CRIA O PACOTE ARP
    arp = ARP(pdst=ip_range)
    ether = Ether(dst="ff:ff:ff:ff:ff:ff")
    packet = ether/arp
    
    #ENVIA O PACOTE ARP E RECEBE A RESPOSTA
    result = srp(packet, timeout=2, verbose=0)[0]
    
    #CRIA UMA LISTA DE DICIONÁRIOS COM OS DISPOSITIVOS ENCONTRADOS
    devices = []
    for sent, received in result:
        try:
            hostname = socket.gethostbyaddr(received.psrc)[0]
        except (socket.herror, socket.gaierror):
            hostname = "Unknown"

        devices.append({'ip': received.psrc, 'mac': received.hwsrc, 'hostname': hostname})

    #ENVIA PACOTES ICMP(PING) PARA IPs ENCONTRADOS
    for device in devices:
        ip = device['ip']
        icmp_packet = IP(dst=ip)/ICMP()
        response = sr1(icmp_packet, timeout=2, verbose=0)
        if response is None:
            device['icmp_response'] = "❌ Não responde ao ping"
        else:
            device['icmp_response'] = "✅ Responde ao ping"
    return devices


def monitor_dns_traffic(devices, pihole_ip):
    for device in devices:
        ip = device['ip']
        # USE TCPDUMP PARA CAPTURAR O TRÁFEGO DNS
        command = f"sudo tcmpdump - i any src {ip} and port 53 -c 10"
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if pihole_ip in result.stdout:
            device['dns_traffic'] = "Using Pi-hole"
        else:
            device['dns_traffic'] = "Using external DNS"
