
# Reflection – Server Inventory Tool

## Introduction

I made this Python program to keep track of servers, check if they respond to ping, and create reports. I wanted the code to be easy to follow and the program to work both from a text menu and from the command line.

In this document, I explain four choices I made, other ways I could have solved the same problems and what I would change if the program became bigger.

## 1. Storing servers in a list of dictionaries

**My choice:** In `lagring.py`, I store all servers in a list. Each server is a dictionary with fields such as `namn`, `adress`, `miljo`, and `status`. For example, `server["namn"]` gives the server name. The function `find_server()` goes through the list to find a server with a matching name.

**Alternative:** I could have used one dictionary with the server names as keys. Then I could find a server directly by writing something like `servers["web01"]`, instead of searching through a list.

**Why I chose this:** A list of dictionaries is easy to understand. I can use a `for` loop to show all servers, and the data is also easy to save as JSON. For the small number of servers in this assignment, I think this is enough.

**Advantages and disadvantages:** The advantage is that the structure is simple and each server's information is clearly named. The disadvantage is that searching can take longer when the list grows. I also need to check that a name is not already used before adding a server. That check is done with `find_server()` in `add_server()`.

**If things changed:** If I had thousands of servers and needed to search for names very often, I would consider using a dictionary with server names as keys. That would make searching easier, but I would have to change how the program stores and reads the data.

## 2. Saving the JSON file after every change

**My choice:** The program reads servers from a JSON file with `load_servers()` in `lagring.py`. When I add or remove a server, the program calls `save_servers()`. The `check_server()` function in `kontroller.py` also saves the new status and the time of the check.

**Alternative:** I could have saved everything only when the user exits the program. Another option would be to check all servers first and save the results together.

**Why I chose this:** I wanted changes to stay saved even if the user closes the program. For example, when I add a new server and start the program again, that server should still be in the list. Saving after each change makes this easy to understand.

**Advantages and disadvantages:** The main advantage is that I am less likely to lose changes. The disadvantage is that the whole JSON file is saved again each time. When `check_all_servers()` checks many servers, this means many file writes, which is not very efficient. Saving less often would be faster, but I could lose the latest changes if the program stopped before saving.

**If things changed:** With many servers, I would change `check_all_servers()` so that it checks all servers first and saves the JSON file only once at the end. The results would be updated in the server list during the checks. This would reduce the number of times the file is saved. I would also need to think about what happens if the program stops before saving.

## 3. Using separate modules and both a menu and CLI

**My choice:** I divided the code into four files. `main.py` starts the program and handles command-line arguments. `meny.py` handles the text menu. `lagring.py` handles server data and reports, and `kontroller.py` handles ping checks. Both the menu and CLI use the same functions, such as `show_servers()`, `check_server()`, and `export_report()`.

**Alternative:** I could have written all the code in one file or made a program with only a text menu.

**Why I chose this:** Each file has a clear job so it is easier to find the code I want to change. I also do not need two different versions of the same function. For example, checking a server works in the same way whether I choose it from the menu or run `python main.py --kontrollera web01`.

**Advantages and disadvantages:** This makes the program easier to read and update. The text menu is useful when I want to choose actions step by step. CLI commands are useful when I already know what I want to do. A disadvantage is that I have to understand imports between files and make sure both ways of using the program still work after a change.

**If things changed:** If I added more features, I would keep using separate functions and files. If the program needed to run automatically, I would mainly use CLI commands because they do not ask the user to choose from a menu.

## 4. Using subprocess to run ping

**My choice:** In `kontroller.py`, `check_server()` uses `subprocess.run()` to run the computer's `ping` command. On Linux and macOS it uses `-c 1`, while Windows uses `-n 1`. If the command returns exit code `0`, the server gets status `up`. Otherwise it gets `down`. I also set a five-second timeout.

**Alternative:** I could have used another Python tool for network checks, or checked a web server by trying to open its website instead of using ping.

**Why I chose this:** Ping is already available on many computers, and `subprocess.run()` lets Python start that command and read the result. I send the command as a list so that the program passes each part of the command separately. The timeout makes sure one check does not keep waiting for too long.

**Advantages and disadvantages:** It is a simple way to check whether a server responds, and I do not need to write the ping function myself. But ping may be blocked by a network. This means a server marked `down` might still be working. The computer also needs to have the `ping` command installed.

**If things changed:** If I used the tool to check real web services, I would consider adding another check for websites. I would still keep ping because it is useful for a basic network check.

## 5. Additional Features

### Feature 1: Report with Summary

In `lagring.py`, I added `make_summary()` and used it in `export_report()`. The program creates a CSV file with server details and a separate text report. The text report counts servers with the status `up`, `down`, or `unknown`, first for all servers and then for each environment: `dev`, `test`, and `prod`.

I chose this feature because the CSV file gives detailed information, but a short summary is easier to read quickly. For example, I can see how many production servers are down without going through every row in the CSV file.

The advantage is that I get both details and a quick overview. The limitation is that the report only shows the statuses currently saved in the JSON file. It does not show what happened during earlier checks. If I wanted that information, I would need to save a history of checks as another feature.

### Feature 2: Safer User Input

In `meny.py` , I use `ask_text()` and `ask_environment()` to check what the user types. `ask_text()` uses `.strip()` to remove spaces at the beginning and end of an answer. If the answer is empty, the program asks again. When entering a server name, a name such as `web 01` is rejected because it contains a space inside the name.

`ask_environment()` uses `.lower()` and only accepts `dev`, `test` , or `prod`. For example, typing `PROD` can still be accepted as `prod`. If the user enters a menu option that does not exist, the menu shows a message and asks again.

I chose this feature to avoid saving incorrect information by mistake. It is easier to ask again than to fix wrong server data later. One limitation is that the program does not fully check whether an address is a real or valid server address. That could be improved later.

## 6. If the program had to manage 1,000 servers or run every night

The program works well for a small list, but 1,000 servers would make some parts slower.

First, I would make it easy to work with one environment at a time, such as `dev`, `test`, or `prod`. This would help me find and manage the servers I need without looking at all 1,000 at once.

I would also change how the program saves results.Right now, `check_server()` saves the whole JSON file after every check. With 1,000 servers, checking each server once would mean saving the file 1,000 times.

Instead, I could change `check_all_servers()` so that it checks all servers first and saves the JSON file only once at the end. The results would be updated in the server list during the checks.

This would reduce the number of times the file is saved and could make the program faster. One disadvantage is that some results could be lost if the program stopped before saving.

Checking servers one by one could also take a long time, especially if some do not answer ping. If this became a problem, I would look for a way to check several servers at the same time. I would need to learn how to do this carefully, because it would make the code harder to understand.

If the program needed to run every night, I would use CLI commands instead of the text menu. The CLI can run without someone choosing menu options, although I would still need a separate way to start it at a set time. I would keep the reports so I could read the results the next day.

## Conclusion

In this project, I tried to choose solutions that I understand and that fit what the program needs.Using lists, dictionaries, JSON, and separate modules worked well for a small server inventory.

While working on the project, I learned that there can be different ways to solve the same problem. I realized that the solutions I chose have both advantages and disadvantages. For example, saving the data after every check is useful because the results are always updated, but it may not be the best solution when working with many servers.