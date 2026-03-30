import argparse
from scanner import Scanner
from report import save_report


def scan():
    parser = argparse.ArgumentParser(description="Утилита для сканирования сети")

    subparsers = parser.add_subparsers(dest="command")
    
    scan = subparsers.add_parser("scan")
    scan.add_argument("network",type=str,help="Ваша сеть")
    scan.add_argument("--ports",type=int,nargs="+",help="Выбор портов")
    
    history = subparsers.add_parser("history")

    args = parser.parse_args()


    if args.command == "scan":
        print("Начинаю сканирование")
        s = Scanner()
        data = s.discover_network(args.network)
        save_report(data)
    elif args.command == "history":
        print("История не доступна")

if __name__ == "__main__":
    scan()
