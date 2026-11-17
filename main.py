# Start the server inventory program.

import argparse
import json
import sys

from lagring import get_data_file, load_servers, find_server, show_servers, export_report
from kontroller import check_server, check_all_servers
from meny import start_menu

def main():
    # Read commands from the terminal.
    parser = argparse.ArgumentParser(description="Server Inventory Tool")
    parser.add_argument("--lista", action="store_true", help="Show servers")
    parser.add_argument("--miljo", choices=["dev", "test", "prod"], help="Filter servers by environment")
    parser.add_argument("--kontrollera", help="Check one server by name")
    parser.add_argument("--kontrollera-alla", action="store_true", help="Check all servers")
    parser.add_argument("--export", action="store_true", help="Export reports")
    args = parser.parse_args()

    # Check if --miljo is used without --lista
    if args.miljo and not args.lista:
        print("Use --miljo together with --lista.")
        return 1

    # Load servers from JSON and handle errors.
    data_file = get_data_file()
    try:
        servers = load_servers(data_file)
    except json.JSONDecodeError:
        print("Invalid JSON file.")
        return 1

    # Run one command, or open the menu.
    if args.lista:
        show_servers(servers, args.miljo)
        return 0

    elif args.kontrollera:
        server = find_server(servers, args.kontrollera)

        if server is None:
            print("Server not found.")
            return 1

        status = check_server(server, servers, data_file)
        if status == "down":
            return 1
        return 0

    elif args.kontrollera_alla:
        all_up = check_all_servers(servers, data_file)
        if not all_up:
            return 1
        return 0

    # Export CSV and text reports
    elif args.export:
        csv_file, text_file = export_report(servers)
        print(f"CSV saved: {csv_file}")
        print(f"Summary saved: {text_file}")
        return 0

    else:
        start_menu(servers, data_file)
        return 0


if __name__ == "__main__":
    sys.exit(main())
