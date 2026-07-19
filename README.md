# TD-W9960-watchdog

A simple watchdog script for the TP-Link TD-W9960 modem. It was created to work around the firmware issue where **PPPoE dial-up could not be reestablished in some cases**. The script monitors internet connectivity and automatically reconnects the PPPoE session when the modem gets stuck.

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```bash
python watchdog.py
```

Or specify a custom modem IP address and admin password:

```bash
python watchdog.py -i 192.168.1.1 -a admin-password
```


## TODO

- [ ] Better error handling
- [ ] Configurable check interval
- [ ] More detailed console output
