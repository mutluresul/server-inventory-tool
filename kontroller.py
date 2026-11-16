
# Check servers with ping.

import os
import subprocess
from datetime import datetime
from lagring import save_servers


# Check one server and save the result.
def check_server(server, servers, data_file):
    if os.name == "nt":
        command = ["ping", "-n", "1", server["adress"]]
    else:
        command = ["ping", "-c", "1", server["adress"]]

    # Try to ping the server
    try:
        result = subprocess.run(command, capture_output=True, text=True, timeout=5)

        # Check if ping was successful
        if result.returncode == 0:
            server["status"] = "up"
        else:
            server["status"] = "down"
    # Handle timeout error
    except subprocess.TimeoutExpired:
        print("Ping took too long.")
        server["status"] = "down"
    # Handle missing ping command
    except FileNotFoundError:
        print("Could not run ping.")
        server["status"] = "down"

    server["senast_kontrollerad"] = datetime.now().strftime("%Y-%m-%d %H:%M")

    save_servers(servers, data_file)

    print(f"{server['namn']}: {server['status']}")

    return server["status"]


# Check every server.
def check_all_servers(servers, data_file):
    all_up = True

    for server in servers:
        status = check_server(server, servers, data_file)

        if status == "down":
            all_up = False

    return all_up
