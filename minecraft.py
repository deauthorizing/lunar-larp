import os
import sys
import json
import re
from colorama import Fore, Style, init
import wcwidth 

# -*- coding: utf-8 -*-

init(autoreset=True)

PASTEL_PINK = "\033[38;2;238;152;183m"
RESET = Style.RESET_ALL

def _force_utf8():
    try:
        if os.name == "nt":
            import ctypes
            ctypes.windll.kernel32.SetConsoleOutputCP(65001)
            ctypes.windll.kernel32.SetConsoleCP(65001)
        if hasattr(sys.stdout, "reconfigure"):
            sys.stdout.reconfigure(encoding="utf-8")
            sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

_force_utf8()

def resize_console(cols=90, rows=40):
    try:
        if os.name == "nt": 
            os.system(f"mode con: cols={cols} lines={rows}")
        else:  
            sys.stdout.write(f"\x1b[8;{rows};{cols}t")
            sys.stdout.flush()
    except Exception as e:
        pass


resize_console(90, 40)

def set_console_title(title: str):
    try:
        if os.name == "nt":  
            os.system(f"title {title}")
        else: 
            sys.stdout.write(f"\33]0;{title}\a")
            sys.stdout.flush()
    except Exception:
        pass


set_console_title("fusi and wish made this haha, t.me/larpforfree for more.")


def unicode_supported() -> bool:
    enc = (sys.stdout.encoding or "").lower()
    return "utf" in enc


def term_width(default: int = 80) -> int:
    try:
        return os.get_terminal_size().columns
    except Exception:
        return default


def visible_len(s: str) -> int:
    return sum(wcwidth.wcwidth(ch) for ch in s)


ANSI_ESCAPE = re.compile(r'\x1b\[[0-?]*[ -/]*[@-~]')

def strip_ansi(s: str) -> str:
    return ANSI_ESCAPE.sub('', s)


def center_text(s: str, color=PASTEL_PINK) -> str:
    vis_len = visible_len(strip_ansi(s))
    pad = max((term_width() - vis_len) // 2, 0)
    return " " * pad + color + s + RESET

def gradient_banner(text: str) -> str:
    lines = text.rstrip("\n").splitlines()
    vis_lens = [visible_len(line) for line in lines]
    max_vis = max(vis_lens) if vis_lens else 0
    pad = max((term_width() - max_vis) // 2, 0)
    out = []
    for i, line in enumerate(lines):
        color = Fore.WHITE if i % 2 == 0 else PASTEL_PINK
        out.append(" " * pad + color + line + RESET)
    return "\n".join(out)

def compute_banner_center(text: str) -> float:
    lines = text.rstrip("\n").splitlines()
    vis_lens = [visible_len(line) for line in lines]
    if not vis_lens:
        return term_width() / 2
    max_vis = max(vis_lens)
    pad = max((term_width() - max_vis) // 2, 0)
    return pad + max_vis / 2

def center_at(s: str, center_x: float, color=PASTEL_PINK) -> str:
    vis_len = visible_len(strip_ansi(s))
    pad = max(int(round(center_x - vis_len / 2)), 0)
    return " " * pad + color + s + RESET

def _make_box_lines(lines):
    max_vis = max(visible_len(s) for s in lines)
    width = max_vis + 2
    if unicode_supported():
        TL, TR, BL, BR, H, V = "┌", "┐", "└", "┘", "─", "│"
    else:
        TL, TR, BL, BR, H, V = "+", "+", "+", "+", "-", "|"

    top = TL + H * width + TR
    bottom = BL + H * width + BR

    body = []
    for s in lines:
        pad_right = max_vis - visible_len(s)
        body.append(f"{V} {s}{' ' * pad_right} {V}")

    return [PASTEL_PINK + top + RESET] + \
           [PASTEL_PINK + b + RESET for b in body] + \
           [PASTEL_PINK + bottom + RESET]

def print_centered_screen(title, choices):
    os.system("cls" if os.name == "nt" else "clear")
    banner_str = gradient_banner(BANNER)
    print(banner_str)

    center_x = compute_banner_center(BANNER)
    print()
    print(center_at(title, center_x, PASTEL_PINK))
    print()
    box_lines = _make_box_lines(choices)
    for bl in box_lines:
        plain = strip_ansi(bl)
        vis = visible_len(plain)
        base_pad = max((term_width() - vis) // 2, 0)
        shift = int(round(center_x - (base_pad + vis / 2)))
        final_pad = max(base_pad + shift, 0)
        print(" " * final_pad + bl)

BANNER_ASCII = r"""
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⠛⢦⡀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⠃⠀⠀⠱⡀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⠤⠒⠉⠉⠉⠉⠑⠒⠲⠤⢄⣀⡏⠉⠁⠒⠢⢷⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⠔⠋⠀⠀⠀⠀⢀⡀⠀⠀⠀⠀⠀⠀⠈⠑⠄⠀⠀⠀⠀⡇⠀
⢀⣠⡤⠖⠚⡏⠉⠉⠁⠉⠉⠉⠁⠀⠠⢄⠀⠎⠁⠀⠰⣀⠀⠀⠄⠈⠙⠆⠈⠂⠀⠀⠀⢸⠀
⠻⣧⡀⠀⢰⠀⠀⠀⠀⠀⠀⠀⠀⠀⠑⠒⠀⣀⡤⠤⠖⡒⠿⠥⣄⡀⠀⢠⠒⠄⠀⠀⠀⢸⠀
⠀⠀⠙⠲⢼⣀⠀⠀⠀⠀⠀⠀⠀⠀⣠⡴⠛⠁⢀⢴⡘⠰⡀⡦⡀⡍⠲⢄⠁⠁⠀⠀⠀⢸⠀
⠀⠀⠀⠀⠀⠈⢉⠗⠀⠀⠀⠀⢀⠞⠁⡄⣠⣧⠎⠘⠁⠀⠣⠁⠱⡏⢆⠈⠳⡀⠀⠀⠀⢸⠀
⠀⠀⠀⠀⠀⠀⢸⠀⠀⠀⠀⣠⠃⠀⢀⡇⠃⠁⠀⠀⠀⠀⠀⠀⠀⠡⠬⣼⡀⠙⡄⠀⠀⠸⡀
⠀⠀⠀⠀⠀⠀⠈⠀⠀⠀⢰⡇⠀⠀⢸⢹⠄⠀⠄⠀⠀⠀⠀⠀⠀⢀⣀⠉⢇⠀⣽⡄⠀⠀⡇
⠀⠀⠀⠀⠀⠀⢸⠀⠀⠀⣏⢠⠀⡆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢰⡏⢪⢷⣸⠀⣹⣴⠀⠀⡇
⠀⠀⠀⠀⠀⠀⢸⠀⠀⢰⠉⢌⣄⠟⣤⠀⣠⣀⠀⠀⠀⠀⠀⠀⢏⡵⠋⣾⣻⢡⠃⡇⡆⠀⡇
⠀⠀⠀⢀⠀⠀⠀⡆⠀⠘⠀⠀⠪⢴⢸⠙⠊⠉⠓⠀⠀⠀⠀⠀⠘⠯⠞⠁⠹⡹⠐⠀⠁⠀⡇
⠀⠀⡰⠁⠙⢦⡀⠘⡄⠀⠑⠄⣀⢹⢸⡄⠀⠀⠀⠀⠀⠤⠀⠀⠀⠀⠀⣠⡃⡇⡀⠀⠀⢀⠇
⠀⡜⠁⠀⠀⠀⠑⢄⠈⢦⠀⠀⠀⠹⡘⡌⣢⠤⣀⣀⣀⣀⣀⣀⡠⠴⠚⠓⡇⡏⢀⣠⠔⠊⠀
⢰⠁⠀⠀⠀⠀⠀⠈⢢⠀⠑⠒⠒⠒⢣⣩⣀⡞⠉⡽⢄⣀⣵⠛⢭⠑⡖⢲⣳⠉⠁⠀⠀⠀⠀
⡇⠀⠀⠀⠀⠀⠀⠀⠀⢣⠀⠀⠀⠀⢎⠀⡼⠀⠀⠀⠋⣻⠢⠀⠈⢇⠺⡘⠁⠀⠀⠀⠀⠀⠀
⠉⠉⠉⠑⠒⠢⣄⠀⢀⠜⠀⠀⠀⠀⡌⠀⣇⠀⠀⠀⢸⠝⣆⠀⠀⠸⡀⢱⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⢀⠎⠀⠠⠧⡤⢄⡀⠀⠀⠡⡀⠙⠀⠀⠀⢪⠀⡟⠀⠀⠀⡇⡜⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠘⠒⠠⠴⢮⣁⠀⡇⠀⠀⢰⠉⢢⣄⡀⠀⢸⠄⡇⠀⠀⡠⠋⢱⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⢠⠎⠀⠑⢤⠎⠁⠀⠀⠙⠫⣍⠁⠀⡽⠒⠋⠀⠀⠀⠑⢆⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠈⠉⠑⠒⣼⣀⠠⡪⠭⠩⢔⠄⠑⡎⢀⠀⣀⠤⡀⠀⠀⠈⣧⣀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⢀⡠⠊⠉⡠⠐⠛⠂⠤⠀⠀⠙⢄⠅⠀⠀⡠⠇⠓⠒⠓⡙⠀⠀⠑⣄⠀
⠀⠀⠀⠀⠀⠀⠀⢠⠎⠀⠀⠀⡀⠀⠀⠀⠀⠀⠀⠀⢸⡄⠀⠀⠀⠀⠀⢀⣀⡇⡀⠀⠀⠈⢢
⠀⠀⠀⠀⠀⠀⠀⠸⣀⣠⠤⠬⠮⠶⠒⠒⠤⠤⠤⠴⠢⠬⠥⠀⠄⠍⠍⠉⠀⠀⠀⠄⠠⠀⠈
"""

BANNER = BANNER_ASCII

MESSAGES = {
    "title": "Lunar Larp Tool / fusi and wish made this, t.me/larpforfree #StopPayingToLarp",
    "main_choices": [
        "1) Add Account",
        "2) Delete Accounts",
        "3) Show Accounts",
        "4) Quit",
    ],
    "prompt_main": "Select an option (1-4): ",
    "prompt_remove": "Select removal option (1-3): ",
    "remove_choices": [
        "1) Delete Everything",
        "2) Delete Cracked Accounts",
        "3) Delete Premium Accounts",
    ],
    "invalid_choice": "Invalid choice. Please try again.",
    "exit": "Exiting application...",
    "press_enter": "Press Enter to continue...",
    "enter_username": "Enter username: ",
    "username_warn": "Warning: Username format may cause server issues.",
    "enter_uuid": "Enter UUID: ",
    "uuid_warn": "Invalid UUID format.",
    "retry": "Try again? (y/n): ",
    "account_created": "Account created successfully!",
    "removed_all": "All accounts deleted.",
    "removed_cracked": "Cracked accounts deleted.",
    "removed_premium": "Premium accounts deleted.",
    "show_accounts": "Existing Accounts:",
    "no_accounts": "No accounts to display.",
    "error_load": "Unable to load accounts file.",
    "error_save": "Unable to save accounts file.",
    "saved": "Accounts saved successfully.",
}

def log(message, tag="INFO", color=Fore.WHITE, show_meta=True):
    if show_meta:
        print(color + f"[{tag}] {message}" + RESET)
    else:
        print(color + message + RESET)

def username_ok(name: str) -> bool:
    return 3 <= len(name) <= 16 and bool(re.match(r"^[A-Za-z0-9_]+$", name))

def uuid_ok(uid: str) -> bool:
    return bool(
        re.match(r"^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$", uid)
    )

class AccountStore:
    data = {"accounts": {}}
    path = os.path.join(os.path.expanduser("~"), ".lunarclient", "settings", "game", "accounts.json")

    @classmethod
    def load(cls):
        try:
            if os.path.exists(cls.path):
                with open(cls.path, "r", encoding="utf-8") as f:
                    cls.data = json.load(f)
            else:
                cls.data = {"accounts": {}}
        except Exception as e:
            log(f"{MESSAGES['error_load']} {e}", "ERROR", Fore.RED)
            sys.exit(1)

    @classmethod
    def save(cls):
        try:
            os.makedirs(os.path.dirname(cls.path), exist_ok=True)
            with open(cls.path, "w", encoding="utf-8") as f:
                json.dump(cls.data, f, indent=4)
            log(MESSAGES["saved"], "SUCCESS", PASTEL_PINK)
        except Exception as e:
            log(f"{MESSAGES['error_save']} {e}", "ERROR", Fore.RED)

    @classmethod
    def add_account(cls, username, uuid):
        cls.data.setdefault("accounts", {})
        cls.data["accounts"][uuid] = {
            "accessToken": uuid,
            "accessTokenExpiresAt": "2050-07-02T10:56:30.717167800Z",
            "eligibleForMigration": False,
            "hasMultipleProfiles": False,
            "legacy": True,
            "persistent": True,
            "userProperites": [],
            "localId": uuid,
            "minecraftProfile": {
                "id": uuid,
                "name": username
            },
            "remoteId": uuid,
            "type": "Xbox",
            "username": username
        }
        cls.data["activeAccountLocalId"] = uuid
        log(MESSAGES["account_created"], "SUCCESS", PASTEL_PINK)

    @classmethod
    def wipe_all(cls):
        cls.data["accounts"] = {}
        log(MESSAGES["removed_all"], "SUCCESS", PASTEL_PINK)

    @classmethod
    def wipe_cracked(cls):
        cls.data["accounts"] = {k: v for k, v in cls.data["accounts"].items() if uuid_ok(v["accessToken"])}
        log(MESSAGES["removed_cracked"], "SUCCESS", PASTEL_PINK)

    @classmethod
    def wipe_premium(cls):
        cls.data["accounts"] = {k: v for k, v in cls.data["accounts"].items() if not uuid_ok(v["accessToken"])}
        log(MESSAGES["removed_premium"], "SUCCESS", PASTEL_PINK)

    @classmethod
    def display(cls):
        log(MESSAGES["show_accounts"], "INFO", PASTEL_PINK)
        if not cls.data["accounts"]:
            log(MESSAGES["no_accounts"], "INFO", Fore.YELLOW)
        else:
            for uid, acc in cls.data["accounts"].items():
                log(f"{uid}: {acc['username']}", "ACCOUNT", PASTEL_PINK)

def add_account_flow():
    username = input(MESSAGES["enter_username"]).strip()
    if not username_ok(username):
        log(MESSAGES["username_warn"], "WARN", Fore.YELLOW)

    while True:
        uid = input(MESSAGES["enter_uuid"]).strip()
        if not uuid_ok(uid):
            log(MESSAGES["uuid_warn"], "WARN", Fore.RED)
            if input(MESSAGES["retry"]).strip().lower() != "y":
                return
        else:
            AccountStore.add_account(username, uid)
            AccountStore.save()
            break

def remove_menu():
    print_centered_screen(MESSAGES["title"], MESSAGES["remove_choices"])
    choice = input(MESSAGES["prompt_remove"]).strip()

    if choice == "1":
        AccountStore.wipe_all()
    elif choice == "2":
        AccountStore.wipe_cracked()
    elif choice == "3":
        AccountStore.wipe_premium()
    else:
        log(MESSAGES["invalid_choice"], "ERROR", Fore.RED)

    AccountStore.save()

def main_menu():
    while True:
        print_centered_screen(MESSAGES["title"], MESSAGES["main_choices"])
        choice = input(MESSAGES["prompt_main"]).strip()

        if choice == "1":
            add_account_flow()
        elif choice == "2":
            remove_menu()
        elif choice == "3":
            AccountStore.display()
        elif choice == "4":
            log(MESSAGES["exit"], "INFO", PASTEL_PINK)
            break
        else:
            log(MESSAGES["invalid_choice"], "ERROR", Fore.RED)

        input(MESSAGES["press_enter"])

def run():
    AccountStore.load()
    main_menu()
    AccountStore.save()

if __name__ == "__main__":
    run()
