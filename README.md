# NetSen (Network Sentinel) 🕵️‍♂️

**NetSen** is a lightweight and fast console-based local network scanner written in Python. The project was created for educational purposes to help users learn the principles of network protocols and the architecture of CLI applications.

## 🚀 Features

* **Fast scanning:** Detects active hosts in a specified subnet.
* **Generator-based approach:** Uses iterators to handle large networks without overloading RAM.
* **Scan history:** Automatically saves results to a local SQLite database.
* **Compliance with Linux standards:** Database and report files are saved in accordance with the XDG specification to the `~/.local/share/netsen/` directory.
* **Installation as a CLI utility:** After installation, the direct system command `netsen` is available.

## 🤖 Using AI in the project

This project is a training ground. My goal as the author is not to mechanically memorize syntax, but to understand system architecture, network operations, and information security. 

In this regard:
* The scanning logic, tool selection, and overall concept were formulated by me.
* Complex routine tasks (writing SQL queries for the database, setting up relative imports, configuring `pyproject.toml`, and handling paths in Linux) were generated using AI (Claude).
* The project is used for reverse engineering: each line of generated code is analyzed and studied separately to understand the mechanics of the processes.


## 📦 Installation

To install the project, clone the repository and install it using `pip`:

```bash
git clone [https://github.com/Algozak/NetSen.git](https://github.com/Algozak/NetSen.git)
cd NetSen
pip install -e .
