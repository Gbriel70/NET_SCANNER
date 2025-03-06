from scapy.all import ARP, Ether, srp, ICMP, IP, sr1
import socket

def scan_network(ip_range="192.168.18.12/24"):
    
    #CRIA O PACOTE ARP
    arp = ARP(pdst=ip_range)
    ether = Ether(dst="ff:ff:ff:ff:ff:ff")
    packet = ether/arp
    
    #ENVIA O PACOTE ARP E RECEBE A RESPOSTA
    result = srp(packet, timeout=3, verbose=0)[0]
    
    #CRIA UMA LISTA DE DICIONÁRIOS COM OS DISPOSITIVOS ENCONTRADOS
    devices = []
    for sent, received in result:
        try:
            hostname = socket.gethostbyaddr(received.psrc)[0]
        except socket.herror:
            hostname = "Unknown"
        devices.append({'ip': received.psrc, 'mac': received.hwsrc, 'hostname': hostname})

    #ENVIA PACOTES ICMP(PING) PARA IPs ENCONTRADOS
    for device in devices:
        ip = device['ip']
        icmp_packet = IP(dst=ip)/ICMP()
        response = sr1(icmp_packet, timeout=3, verbose=0)
        if response:
            device['icmp_response'] = True
        else:
            device['icmp_response'] = False
    return devices

if __name__ == "__main__":
    devices = scan_network()
    if not devices:
        print("No devices found")
    for device in devices:
        print(f"IP: {device['ip']}\tMAC: {device['mac']}\tDevice: {device['hostname']}")