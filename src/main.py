import argparse
from .scanner import Scanner
from .report import save_report
from .database import init_db, save_scan, get_history, get_scan_detail

def scan():
   
    init_db()

    parser = argparse.ArgumentParser(
        description="Использование: \nnetsen scan [IP-адрес]",
        add_help=False
    )

    subparsers = parser.add_subparsers(dest="command")
    
    
    scan_parser = subparsers.add_parser("scan")
    scan_parser.add_argument("network", type=str, help="Ваша сеть")
    scan_parser.add_argument("--ports", type=int, nargs="+", help="Выбор портов")
    
    history_parser = subparsers.add_parser("history")

    args = parser.parse_args()

    def cmd_scan(args):
        s = Scanner()
        data = s.discover_network(args.network)
        save_report(data)
        save_scan(data, args.network)

    def cmd_history(args):
        scans = get_history()
        if not scans:
            print("История пуста")
            return
        for scan_data in scans:
            print(f"[{scan_data['id']}] {scan_data['date']} | {scan_data['network']} | найдено хостов: {scan_data['total']}")

    COMMANDS = {
        "scan": cmd_scan,
        "history": cmd_history,
    }

    COMMANDS.get(args.command, lambda _: parser.print_help())(args)


if __name__ == "__main__":
    scan()
