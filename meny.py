
# Show the menu and ask the user what to do.

from lagring import (
    VALID_ENVIRONMENTS,
    add_server,
    export_report,
    find_server,
    remove_server,
    show_servers,
)
from kontroller import check_server, check_all_servers


# Ask again if the user leaves the answer empty.
def ask_text(question, no_spaces=False):
    while True:
        answer = input(question).strip()

        if answer == "":
            print("Please enter a value.")
        elif no_spaces and " " in answer:
            print("Server names cannot contain spaces.")
        else:
            return answer


# Ask again until the environment is valid.
def ask_environment():
    while True:
        environment = ask_text("Environment (dev/test/prod): ").lower()

        if environment in VALID_ENVIRONMENTS:
            return environment

        print("Choose dev, test or prod.")


# Keep showing the menu until the user chooses 0.
def start_menu(servers, data_file):
    while True:
        print("\n=== Server Inventory Tool ===")
        print("1. Show all servers")
        print("2. Show servers by environment")
        print("3. Add a server")
        print("4. Remove a server")
        print("5. Check one server")
        print("6. Check all servers")
        print("7. Export report")
        print("8. Exit")

        choice = input("Your choice: ").strip()

        if choice == "1":
            show_servers(servers)

        elif choice == "2":
            environment = ask_environment()
            show_servers(servers, environment)

        elif choice == "3":
            name = ask_text("Server name: ", no_spaces=True)

            if find_server(servers, name) is not None:
                print("A server with this name already exists.")
                continue

            address = ask_text("Address: ")
            environment = ask_environment()
            role = ask_text("Role: ")

            if add_server(servers, name, address, environment, role, data_file):
                print("Server added.")
            else:
                print("Could not add server.")

        elif choice == "4":
            name = ask_text("Server name to remove: ", no_spaces=True)
            server = find_server(servers, name)

            if server is None:
                print("Server not found.")
                continue

            if server["miljo"] == "prod":
                answer = input("Production server! Remove it? (yes/no): ").strip().lower()

                if answer != "yes":
                    print("Removal cancelled.")
                    continue

            remove_server(servers, name, data_file)
            print("Server removed.")

        elif choice == "5":
            name = ask_text("Server name to check: ", no_spaces=True)
            server = find_server(servers, name)

            if server is None:
                print("Server not found.")
            else:
                check_server(server, servers, data_file)

        elif choice == "6":
            if len(servers) == 0:
                print("No servers to check.")
            else:
                check_all_servers(servers, data_file)

        elif choice == "7":
            csv_file, text_file = export_report(servers)
            print(f"CSV saved: {csv_file}")
            print(f"Summary saved: {text_file}")

        elif choice == "8":
            print("Goodbye!")
            break

        else:
            print("Invalid menu choice. Try again.")
