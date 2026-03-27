import subprocess
import ipaddress
from concurrent.futures import ThreadPoolExecutor

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

    def discover_network(self, network: str):
        print(f"[*] Запускаю ICMP-сканирование сети: {network}")
        net = ipaddress.ip_network(network, strict=False)
        hosts = [str(ip) for ip in net.hosts()]
        
        discovered_hosts = []
        
        # Запускаем 50 потоков одновременно
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            results = list(executor.map(self._ping, hosts))
            
        for ip in results:
            if ip:
                # MAC-адрес мы подтянем позже из ARP-таблицы системы
                discovered_hosts.append({"ip": ip, "mac": "Unknown"})
                print(f"[+] Хост {ip} в сети!")
        
        return discovered_hosts
