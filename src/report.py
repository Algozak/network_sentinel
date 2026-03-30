import json
import os
import datetime
def save_report(data: list, filename: str = "reports/scan_report.json"):
    # Проверим, есть ли папка для отчетов, если нет — создадим
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    full_report = {
        "scan_info": {
            "date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "target_network": "192.168.51.0/24", # можно передать как аргумент
            "total_hosts_found": len(data)
        },
        "hosts": data
    }
    
    try:
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(full_report, f, indent=4, ensure_ascii=False) 
        print(f"[!] Отчет успешно сохранен в: {filename}")
    except Exception as e:
        print(f"[!] Ошибка при сохранении отчета: {e}")
