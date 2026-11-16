
# Read, save and show servers. Create reports.

import csv
import json
import os
from datetime import datetime
from pathlib import Path


FIELDS = ["namn", "adress", "miljo", "roll", "status", "senast_kontrollerad"]
VALID_ENVIRONMENTS = ["dev", "test", "prod"]


# Get the data file name.
def get_data_file():
    file_name = os.environ.get("INVENTORY_DATAFIL", "servrar.json")
    return Path(file_name)


# Load servers from JSON. Return an empty list if the file does not exist.
def load_servers(data_file):
    if not data_file.exists():
        return []

    with open(data_file, "r", encoding="utf-8") as file:
        servers = json.load(file)

    return servers


# Save servers to JSON.
def save_servers(servers, data_file):
    with open(data_file, "w", encoding="utf-8") as file:
        json.dump(servers, file, indent=4, ensure_ascii=False)


# Find a server by name.
def find_server(servers, name):
    for server in servers:
        if server["namn"].lower() == name.lower():
            return server

    return None


# Add a new server and save the list.
def add_server(servers, name, address, environment, role, data_file):
    if find_server(servers, name) is not None:
        return False

    if environment not in VALID_ENVIRONMENTS:
        return False

    server = {
        "namn": name,
        "adress": address,
        "miljo": environment,
        "roll": role,
        "status": "unknown",
        "senast_kontrollerad": "",
    }

    servers.append(server)
    save_servers(servers, data_file)
    return True


# Remove a server and save the list.
def remove_server(servers, name, data_file):
    server = find_server(servers, name)

    if server is None:
        return False

    servers.remove(server)
    save_servers(servers, data_file)
    return True


# Show all servers or filter by environment.
def show_servers(servers, environment=None):
    selected_servers = []

    for server in servers:
        if environment is None or server["miljo"] == environment:
            selected_servers.append(server)

    if not selected_servers:
        print("No servers to show.")
        return

    print()
    print(f"{'NAME':<15} {'ADDRESS':<22} {'ENV':<8} {'ROLE':<20} {'STATUS':<9} LAST CHECKED")
    print("-" * 100)

    for server in selected_servers:
        print(
            f"{server['namn']:<15} {server['adress']:<22} "
            f"{server['miljo']:<8} {server['roll']:<20} "
            f"{server['status']:<9} {server['senast_kontrollerad']}"
        )

    print()


# Count servers by status and environment for the text report (VG).
def make_summary(servers):
    lines = ["SERVER INVENTORY - SUMMARY", ""]

    for environment in ["all", "dev", "test", "prod"]:
        total = 0
        up = 0
        down = 0
        unknown = 0

        for server in servers:
            if environment == "all" or server["miljo"] == environment:
                total += 1

                if server["status"] == "up":
                    up += 1
                elif server["status"] == "down":
                    down += 1
                else:
                    unknown += 1

        lines.append(
            f"{environment}: total={total}, up={up}, down={down}, unknown={unknown}"
        )

    text = ""

    for line in lines:
        text = text + line + "\n"

    return text


# Save a CSV report and a text summary.
def export_report(servers):
    report_folder = Path("rapporter")
    report_folder.mkdir(exist_ok=True)

    timestamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")
    csv_file = report_folder / f"inventory_{timestamp}.csv"

    with open(csv_file, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(servers)

    text_file = report_folder / f"summary_{timestamp}.txt"

    with open(text_file, "w", encoding="utf-8") as file:
        file.write(make_summary(servers))

    return csv_file, text_file
