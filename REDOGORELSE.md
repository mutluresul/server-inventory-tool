# Code Explanation - Server Inventory Tool

This document explains how I used Python in my Server Inventory Tool project.

## 1. Three Python constructs

**If statement:** An `if` statement checks a condition. For example, in `meny.py`, I use `if choice == "1":` to show the server list when the user chooses option 1. I also use `elif` and `else` for other choices.

**For loop:** A `for` loop goes through items in a list. In `lagring.py`, `find_server()` uses `for server in servers:` to look for a server with the correct name.

**Function:** I create functions with `def`. For example, `def find_server(servers, name):` creates a function that searches for a server. It returns the server if found, or `None` if it does not exist.

I also use a `while True` loop in `start_menu()` to keep the menu open until the user chooses 8.

## 2. Lists and dictionaries

I store all servers in a **list**. Each server is a **dictionary** with these keys: `namn`, `adress`, `miljo`, `roll`, `status`, and `senast_kontrollerad`.

A list is useful because I can add, remove, and go through several servers. A dictionary is useful because every value has a clear name. For example, `server["namn"]` gives the server name and `server["status"]` gives its status.

All six values in a server dictionary are strings (str), including the status and the last checked timestamp.

## 3. Why I use JSON and CSV

I use **JSON** to save the server list in `servrar.json`. JSON can store lists and dictionaries, so it works well with my Python data. The program reads the file when it starts and saves changes after I add, remove, or check a server.

I use **CSV** for reports. CSV has rows and columns and can be opened in Excel. In `export_report()`, I create a CSV file with a header and all the servers. JSON is for saving data, and CSV is for showing the data in a report.

## 4. Modules and functions

I divided my program into four Python files:

- `main.py` starts the program and handles terminal commands such as `--lista` and `--export`.
- `meny.py` shows the text menu and reads user input.
- `lagring.py` adds, removes, loads, and saves servers. It also creates reports.
- `kontroller.py` checks servers with ping and updates their status.

This makes the code easier to read. I can also use the same functions from the menu and from the terminal commands without writing them twice.

## 5. Python standard library modules

I use modules from the Python standard library:

- `json` reads and writes the server data.
- `csv` creates the CSV report.
- `os` reads `INVENTORY_DATAFIL` and helps choose the ping command for the operating system.
- `pathlib` checks if a file exists and creates the `rapporter` folder.
- `datetime` adds the time of a server check and the time to report filenames.
- `subprocess` runs the ping command.
- `argparse` reads commands like `--kontrollera web01`.
- `sys` sends the program's exit code to the terminal.

I do not need to install extra Python packages.

## 6. Good coding practices

**Clear names:** I use names like `find_server()`, `save_servers()`, and `check_server()`. These names make it easier to understand what each function does.

**Small functions and separate modules:** Each function has a task. For example, `find_server()` searches for a server, and `save_servers()` saves the list. This helps me avoid repeating code.

**Checking user input:** In `meny.py`, I check for empty answers, invalid environments, and duplicate server names. The program also asks for confirmation before removing a `prod` server. This helps prevent mistakes.

## 7. Sources and help

For this project, I mainly used the course materials and my notes from previous python lessons. These helped me remember and understand python concepts we learned in class and how to use them in my project.

I also used YouTube tutorials and Python websites such as Real Python when I needed more explanations or examples. These sources helped me understand topics like functions, lists, dictionaries, JSON, and error handling.

I used AI as a learning assistant during the project. It helped me understand error messages, find and fix mistakes in my code, develop my ideas and understand Python concepts that I found difficult. I also used AI to get feedback on my code and improve the documentation.

I tried to understand the suggestions before using them and make sure they matched what I had learned in the course. As a result, using different sources helped me better understand the topics I found difficult and improve my Python skills.
