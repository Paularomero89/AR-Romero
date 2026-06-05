import argparse
import socket
from time import time


DEFAULT_TIMEOUT = 120
DEFAULT_SERVER_HOST = "localhost"
DEFAULT_SERVER_PORT = 80


class NetServiceChecker:
    """Wait for a network service to come online"""

    def __init__(self, host, port, timeout=DEFAULT_TIMEOUT):
        self.host = host
        self.port = port
        self.timeout = timeout
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def end_wait(self):
        self.sock.close()

    def check(self):
        """Check the service"""

        if self.timeout:
            end_time = time() + self.timeout

        while True:
            try:
                if self.timeout:
                    next_timeout = end_time - time()

                    if next_timeout <= 0:
                        return False

                    print(f"Setting socket timeout {round(next_timeout)}s")

                    self.sock.settimeout(next_timeout)

                self.sock.connect((self.host, self.port))

            except socket.timeout:
                return False

            except socket.error as err:
                print(f"Exception: {err}")

            else:
                self.end_wait()
                return True


if __name__ == "__main__":

    print("Script creado por: PAULA")

    parser = argparse.ArgumentParser(description="Wait for Network Service")

    parser.add_argument("--host", default=DEFAULT_SERVER_HOST)
    parser.add_argument("--port", type=int, default=DEFAULT_SERVER_PORT)
    parser.add_argument("--timeout", type=int, default=DEFAULT_TIMEOUT)

    args = parser.parse_args()

    host, port, timeout = args.host, args.port, args.timeout

    service_checker = NetServiceChecker(host, port, timeout)

    print(f"Checking for network service {host}:{port} ...")

    if service_checker.check():
        print("Service is available again!")
    else:
        print("Service is NOT available (timeout)")
        