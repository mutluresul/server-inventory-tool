
# Server Inventory Tool

## 1. About the project

Server Inventory Tool is a simple Python program for managing a list of servers.

The program can:
- Show all servers or servers from one environment.
- Add and remove servers.
- Check one server or all servers using ping.
- Save server data in a JSON file.
- Create CSV and text reports.
- Work with a text menu or terminal commands (CLI).

## 2. Requirements

- Python 3 installed.
- A terminal, such as the terminal in PyCharm.
- The `ping` command installed on your computer for server checks.

On Linux and macOS the program uses `ping -c 1`. On Windows it uses `ping -n 1`.

Some networks block ping. A server marked `down` may still be running.

## 3. Project files


```text
server-inventory-tool/
    main.py
    meny.py
    lagring.py
    kontroller.py
    servrar.json
    .gitignore
    README.md
    REDOGORELSE.md
    REFLEKTION.md
```



- [main.py](main.py) starts the program and reads CLI arguments with `argparse`.
- [meny.py](meny.py) shows the menu and asks the user for information.
- [lagring.py](lagring.py) loads and saves JSON, manages servers, and creates reports.
- [kontroller.py](kontroller.py) checks servers with ping and saves their status.
- [servrar.json](servrar.json) contains the saved server list.
- [.gitignore](.gitignore) keeps generated files out of Git.
- [REDOGORELSE.md](REDOGORELSE.md) explains the code and why it is used.
- [REFLEKTION.md](REFLEKTION.md) explains my design choices , alternative solutions, and additional features.


The folder `rapporter/` is created automatically when a report is exported.

## 4. Start the text menu

Open a terminal in the project folder (the folder containing `main.py`).

Run:

```bash
python main.py
```

If your computer uses `python3`, run `python3 main.py` instead.

The menu has these options:

```text
1. Show all servers
2. Show servers by environment
3. Add a server
4. Remove a server
5. Check one server
6. Check all servers
7. Export report
8. Exit
```

Enter a number and press Enter. The menu appears again after each action until you choose `8`.

### Add a server

Choose `3`. Enter the server name, address, environment, and role.

- The environment must be `dev`, `test`, or `prod`.
- You cannot add two servers with the same name.
- The program asks again if a field is empty or the environment is invalid.
- Server names cannot contain spaces.
- A new server starts with status `unknown`.

### Remove a server

Choose `4` and enter the server name.

If the server is in `prod`, the program asks for extra confirmation. Type `yes` to remove it. Any other answer cancels the removal.

### Check a server

Choose `5` to check one server or `6` to check all servers.

The program runs ping and sets the status to `up` or `down`. It also saves the last check time, for example `2026-11-17 14:30`.

## 5. Use terminal commands (CLI)

Run these commands in the project folder:

| Command | What it does |
| --- | --- |
| `python main.py --help` | Show the help text |
| `python main.py --lista` | Show all servers |
| `python main.py --lista --miljo prod` | Show only prod servers |
| `python main.py --kontrollera web01` | Check one server |
| `python main.py --kontrollera-alla` | Check all servers |
| `python main.py --export` | Create CSV and text reports |

Use `--miljo` together with `--lista`.

The program uses exit codes:
- `0` means the command was successful.
- `1` means a check found a `down` server, the requested server was not found, or the program could not load the data file.

On Linux or macOS, you can see the exit code after a command:

```bash
python main.py --kontrollera web01
echo $?
```

## 6. JSON data

By default, servers are stored in `servrar.json`.

Example server:

```json
{
  "namn": "web01",
  "adress": "example.com",
  "miljo": "prod",
  "roll": "webbserver",
  "status": "unknown",
  "senast_kontrollerad": ""
}
```

Each server is a dictionary, and all servers are stored in a list.

Valid environments are `dev`, `test`, and `prod`. Valid statuses are `up`, `down`, and `unknown`.

The program loads the JSON file when it starts. It saves the file after a server is added, removed, or checked.

If the JSON file does not exist, the program starts with an empty list. If the JSON content is broken, the program shows an error instead of loading it.

## 7. Change the data file with an environment variable

The program reads the `INVENTORY_DATAFIL` environment variable. If it is not set, it uses `servrar.json`.

On Linux or macOS:

```bash
export INVENTORY_DATAFIL=test_servers.json
python main.py --lista
```

On Windows PowerShell:

```powershell
$env:INVENTORY_DATAFIL = "test_servers.json"
python main.py --lista
```

If the selected file does not exist, the program starts with an empty list. The file is created when server data is saved.

## 8. Export reports

Use menu option `7` or run:

```bash
python main.py --export
```

The program creates files in the `rapporter/` folder, for example:

```text
rapporter/inventory_2026-11-17_143000.csv
rapporter/summary_2026-11-17_143000.txt
```

The CSV file contains all servers and a header row. It can be opened in Excel or another spreadsheet program.

The text file shows the number of servers with status `up`, `down`, and `unknown`, for all servers and for each environment.

## 9. Additional features

The program also checks user input to avoid mistakes. In meny.py, the user cannot leave fields empty or use spaces in server names. The program also asks again if the environment is not dev, test, or prod.

When exporting a report, the program creates both a CSV file and a text file. The text file shows how many servers are up, down, or unknown in each environment. This makes it easier to see the server status.



## 10. Test the program

To test the program:

1. Run `python main.py` and check the menu.
2. Run `python main.py --lista` to show servers.
3. Add a server and check that it is saved in JSON.
4. Run `python main.py --kontrollera db01` to test ping.
5. Run `python main.py --export` to create reports.



