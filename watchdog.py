from time import sleep
from cli import parse_args
import ping
import random
import telnetlib

args = parse_args()

def extract_value(text, key):
    if isinstance(text, bytes):
        text = text.decode('utf-8', errors='ignore')

    for line in text.splitlines():
        if line.startswith(key):
            return line.split("=", 1)[1].strip()
    return None

def connect():
    tn = None
    try:
        tn = telnetlib.Telnet(args.ip_address,timeout=3)
        tn.read_until(b"password:",timeout=5)

        tn.write(args.admin_pass.encode("ascii") + b"\n")
        sleep(2)
        tn.write(b"wan show connection info\n")
        sleep(2)

        output = tn.read_very_eager()
        username = extract_value(output, "username=")
        password = extract_value(output, "password=")
        service_name = extract_value(output, "name=")

        if None in (username, password, service_name):
            raise RuntimeError("Failed to parse modem connection information.")

        random_service = f"tci{random.randint(1000, 9999)}"
        cmd = f"wan set service {service_name}\
        --protocol pppoe --username {username}\
        --password {password}\
        --servicename {random_service}\
        --nat enable --defaultroute yes --mtu 1480\n"

        tn.write(cmd.encode())
        sleep(2)
        return True

    except Exception as e:
        print(e)
        return False

    finally:
        if tn:
            tn.close()

fail_count = 0
while True:
    if ping.check_internet():
        fail_count = 0
        print("\r\x1b[KStatus: 🟢", end="", flush=True)
    else:
        fail_count += 1
        print(f"\r\x1b[KStatus: fail:({fail_count}/6)", end="", flush=True)

        if fail_count >= 6:
            print("\r\x1b[K🔄 Reconnecting...", end="", flush=True)
            if connect():
                print("\r\x1b[K✅ Reconnected successfully!", end="", flush=True)
            else:
                print("\r\x1b[K❌ Failed to reconnect.", end="", flush=True)

            fail_count = 0
            sleep(10)

    sleep(2)
