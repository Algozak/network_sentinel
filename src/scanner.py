import subprocess
import ipaddress
from concurrent.futures import ThreadPoolExecutor
import socket

COMMON_PORTS = [21, 22, 23, 25, 53, 80, 110, 135, 139, 443, 445, 3306, 3389, 8080]

class Scanner:
    def __init__(self, timeout: float = 1.0, max_workers: int = 50):
        self.timeout = timeout
        self.max_workers = max_workers

    def _ping(self, ip: str):
        # -c 1 (1 пакет), -W 1 (таймаут 1 сек)
        command = ['ping', '-c', '1', '-W', str(self.timeout), ip]
        result = subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        if result.returncode == 0:
            return ip
        return None
    def get_mac(self, ip: str):
        #"""Возвращает MAC-адрес из ARP-таблицы системы"""
        try:
            # Вызываем системную команду arp -n [IP]
            output = subprocess.check_output(["arp", "-n", ip], stderr=subprocess.STDOUT).decode()
            # Ищем в выводе что-то похожее на MAC (XX:XX:XX:XX:XX:XX)
            import re
            mac = re.search(r"(([a-f0-9]{2}:){5}[a-f0-9]{2})", output)
            return mac.group(0) if mac else "Unknown"
        except:
            return "Unknown"

    def scan_single_port(self, ip, port):
        """Проверяет один конкретный порт на одном IP."""
        # AF_INET = IPv4, SOCK_STREAM = TCP
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(0.5)  # Очень важно! Чтобы не ждать долго на закрытых портах
            result = s.connect_ex((ip, port))
            if result == 0:
                return port
        return None

    def scan_ports(self, ip):
        """Сканирует список популярных портов для заданного IP."""
        open_ports = []
        print(f"[*] Сканирую порты для {ip}...")
        
        # Снова используем многопоточность, чтобы сканировать порты быстро
        with ThreadPoolExecutor(max_workers=20) as executor:
            # Передаем в функцию scan_single_port фиксированный IP и меняющийся порт
            results = executor.map(lambda p: self.scan_single_port(ip, p), COMMON_PORTS)
            
        for port in results:
            if port:
                open_ports.append(port)
                
        return open_ports    

    def discover_network(self, network: str):
        print(f"[*] Запускаю сканирование сети: {network}")
        net = ipaddress.ip_network(network, strict=False)
        hosts = [str(ip) for ip in net.hosts()]
        
        discovered_hosts = []
        
        # Запускаем 50 потоков одновременно
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            results = list(executor.map(self._ping, hosts))
            
        for ip in results:
            if ip:
                mac = self.get_mac(ip)
                open_ports = self.scan_ports(ip)
                host_info = {
                    "ip": ip,
                    "mac": mac,
                    "ports": open_ports
                }

                discovered_hosts.append(host_info)
                ports_str = ", ".join(map(str, open_ports)) if open_ports else "все закрыты"

                print(f"[+] Хост {ip} в сети! | Его MAC-адрес - {mac} | Открытые порты: {ports_str}")
        
        return discovered_hosts
