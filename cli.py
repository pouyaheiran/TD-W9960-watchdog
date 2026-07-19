import argparse

def parse_args():
    parser = argparse.ArgumentParser(description="help")

    parser.add_argument(
        "-a",
        "--admin-pass",
        default="admin",
        help="Modem admin password"
    )

    parser.add_argument(
        "-i",
        "--ip-address",
        default="192.168.1.1",
        help="Modem IP address"
    )

    return parser.parse_args()
