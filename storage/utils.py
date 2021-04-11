from netifaces import interfaces, ifaddresses, AF_INET

def ip4_addresses():
    """
    return host's ipv4 addresses
    """
    ip_list = []
    for interface in interfaces():
        if AF_INET in ifaddresses(interface):
            for link in ifaddresses(interface)[AF_INET]:
                if link['addr'] != "127.0.0.1":
                    ip_list.append(link['addr'])
    if len(ip_list) == 0:
        return None
    return ip_list[0]