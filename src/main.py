import argparse
from .scanner import Scanner
from .report import save_report


def scan():
    parser = argparse.ArgumentParser(
        description="Использование: \nnetsen scan [IP-адрес]",
        add_help=False
    )

    subparsers = parser.add_subparsers(dest="command")
    
    scan = subparsers.add_parser("scan")
    scan.add_argument("network",type=str,help="Ваша сеть")
    scan.add_argument("--ports",type=int,nargs="+",help="Выбор портов")
    
    history = subparsers.add_parser("history")

    args = parser.parse_args()


    def cmd_scan(args):
        s = Scanner()
        data = s.discover_network(args.network)
        save_report(data)

    def cmd_history(args):
        print("История не доступна")

    COMMANDS = {
        "scan": cmd_scan,
        "history": cmd_history,
    }

    COMMANDS.get(args.command, lambda _: parser.print_help())(args)

   

if __name__ == "__main__":

    scan()
