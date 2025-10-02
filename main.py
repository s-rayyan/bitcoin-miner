from time import sleep
from os import get_terminal_size, path
from math import floor
from random import choice, randint
import System
from System import Console
import json
import sys


class MinerGame:
    RESET = "\033[0m"

    def __init__(self):
        self.money = 100
        self.delay = 1000
        self.miners = []
        self.miner_types = (
            "Wood Stone Copper Iron Gold Sapphire Diamond Ruby Emerald "
            "Platinum Titanium Uranium Krypton Neutron Quantum Omega "
            "Alpha Beta Gamma Delta Sigma"
        ).split()
        self.SAVE_FILE = "save.json"
        self.load_game()

    # ==================== LOADING ====================
    def loading_animation(self, text="Bitcoin Miner Booting..."):
        self.clear()
        cols = get_terminal_size().columns
        rows = get_terminal_size().lines*5
        stream_chars = "01"

        for _ in range(rows):
            line = "".join(
                f"\033[32m{choice(stream_chars)}\033[0m" if randint(0, 5) else " "
                for _ in range(cols)
            )
            print(line)
        sleep(0.5)
        msg = text.center(cols)
        print(f"\033[1;32m{msg}\033[0m")
        sleep(1)

    # ==================== GAME STATE ====================
    def load_game(self):
        if path.exists(self.SAVE_FILE):
            try:
                with open(self.SAVE_FILE, "r") as f:
                    data = json.load(f)
                    self.money = data.get("money", 100)
                    self.miners = data.get("miners", [])
            except Exception:
                self.money, self.miners = 100, []

    def save_game(self):
        with open(self.SAVE_FILE, "w") as f:
            json.dump({"money": self.money, "miners": self.miners}, f)

    # ==================== UTILITIES ====================
    def color(self, text, fg=None, bg=None):
        colors = {
            "black": 30, "red": 31, "green": 32, "yellow": 33,
            "blue": 34, "magenta": 35, "cyan": 36, "white": 37,
            "bright_black": 90, "bright_red": 91, "bright_green": 92,
            "bright_yellow": 93, "bright_blue": 94, "bright_magenta": 95,
            "bright_cyan": 96, "bright_white": 97,
        }
        seq = ""
        if fg in colors:
            seq += f"\033[{colors[fg]}m"
        if bg in colors:
            seq += f"\033[{colors[bg] + 10}m"
        print(f"{seq}{text}{self.RESET}")

    def center(self, text):
        return text.center(get_terminal_size().columns)

    def get_key(self):
        return Console.ReadKey(True).KeyChar

    def clear(self):
        Console.Clear()
        self.menu()

    def menu(self):
        text = "   ".join(f"{i+1} {opt}" for i, opt in enumerate(["Open Shop", "View Miners", "Gambling Room"]))
        text = text.ljust(get_terminal_size().columns)
        self.color(text, bg="green")

    def show_bitcoin(self):
        self.color(f"You have {self.money:,} Bitcoin", fg="bright_yellow")

    # ==================== MINERS ====================
    def get_value(self, miner):
        idx = self.miner_types.index(miner) + 1
        return round(idx ** 1.8)

    def get_price(self, miner):
        amt = self.miners.count(miner)
        idx = self.miner_types.index(miner) + 1
        base = 5 * (idx ** 3.69)
        return round(base * (1.15 ** amt))

    def calc_increment_value(self):
        return sum(self.get_value(i) for i in self.miners)

    # ==================== PAGES =====================

    def shop(self):
        def buy(index):
            miner = self.miner_types[index]
            price = self.get_price(miner)
            if self.money >= price:
                self.money -= price
                self.miners.append(miner)
                self.color(f"✔ Bought {miner} miner!", fg="bright_green")
                self.save_game()
            else:
                self.color("✘ Not enough Bitcoin!", fg="bright_green")

        index = 0
        while True:
            self.clear()
            self.color(self.center("=== SHOP ==="), fg="yellow")
            self.show_bitcoin()

            miner = self.miner_types[index]
            price = self.get_price(miner)
            owned = self.miners.count(miner)

            print(f"\nMiner: {miner}")
            print(f"Price: {price:,} Bitcoin")
            print(f"Owned: {owned}")
            print("\nUse [A]/[D] to browse, [Space] to buy, [Q] to quit")

            key = self.get_key()
            if key == "d":
                index = (index + 1) % len(self.miner_types)
            elif key == "a":
                index = (index - 1) % len(self.miner_types)
            elif key == " ":
                buy(index)
                sleep(1)
            elif key == "q":
                self.clear()
                break

    def gamble_bitcoin(self):
        while True:
            self.clear()
            self.color(self.center("=== GAMBLING ROOM ==="), fg="yellow")
            self.color(f"Current Balance: {self.money}", fg="green")
            self.color("Bet an amount, then pick a number (3-10) for the dice size. If the roll is 3, your bet is multiplied by your number.", fg="green")

            # Get bet
            self.color("Enter how much money you are willing to bet", fg="yellow")
            try:
                Console.Write("> ")
                amount = int(Console.ReadLine())
            except ValueError:
                self.color("Invalid input!", fg="red")
                continue

            if amount > self.money or amount <= 0:
                self.color("Invalid bet amount!", fg="red")
                sleep(1.5)
                continue

            # Get multiplier
            self.color("Pick the number for the dice size and multiplier (3–10)", fg="yellow")
            try:
                Console.Write("> ")
                multiplier = int(Console.ReadLine())
            except ValueError:
                self.color("Invalid input!", fg="red")
                continue

            if multiplier < 3 or multiplier > 10:
                self.color("Multiplier must be between 3 and 10!", fg="red")
                sleep(1.5)
                continue

            # Dice roll animation
            num = -1
            for step in range(30):
                num = randint(1, multiplier)
                sys.stdout.write("\rRolling... " + (f"\033[92m{num}\033[0m" if num == 3 else f"\033[91m{num}\033[0m"))
                sys.stdout.flush()
                sleep(0.08)
            print("")

            # Win or lose
            if num == 3:
                winnings = amount * multiplier
                self.money += winnings
                self.color(f"🎉 You rolled a 3! You won {winnings}. New balance: {self.money}", fg="green")
            else:
                self.money -= amount
                self.color(f"❌ You rolled {num}. You lost {amount}. New balance: {self.money}", fg="red")

            # Check if broke
            if self.money <= 0:
                self.color("You're out of money! Game over.", fg="red")
                break

            # Play again?
            self.color("Play again? (y/n)", fg="yellow")
            if self.get_key() != "y":
                break
        self.clear()

    def show_miners(self):
        self.clear()
        self.color(self.center("=== YOUR MINERS ==="), fg="yellow")
        if not self.miners:
            self.color("You don't own any miners yet!", fg="bright_green")
        else:
            counts = {m: self.miners.count(m) for m in self.miner_types if m in self.miners}
            for miner, count in counts.items():
                self.color(f"{miner}: x{count}", fg="bright_green")
        print("\nPress any key to return...")
        self.get_key()
        self.clear()

    # ==================== WAIT ====================
    def wait(self, amt=None, skip=[]):
        steps = 24
        chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789@#$%&*()[]{}<>/\\|-_=+;:,"
        width = int(max(10, get_terminal_size().columns / 3 - 10))
        delay = (amt or (self.delay / 1000)) / steps

        for step in range(steps):
            sleep(delay)
            progress = (step + 1) / steps
            locked = floor(progress * width)

            # build flickering line
            line = "".join(
                "█" if i < locked else (choice("01") if randint(0, 12) == 0 else "░")
                for i in range(width)
            )
            pct = int(progress * 100)
            hash_len = 8
            stable = "".join(
                choice("0123456789ABCDEF") if i >= floor((1 - progress) * hash_len) else " "
                for i in range(hash_len)
            )
            status = f" DECRYPT {pct:3d}% | HASH [{stable}] "

            Console.SetCursorPosition(0, Console.CursorTop if step == 0 else Console.CursorTop - 2)
            self.color(line, fg="bright_green")
            self.color(status, fg="green")

            if Console.KeyAvailable:
                key = self.get_key()
                if key not in skip:
                    
                    return key

        Console.SetCursorPosition(0, Console.CursorTop - 2)
        self.color("█" * width, fg="bright_green")

    # ==================== MAIN LOOP ====================
    def run(self):
        Console.CursorVisible = False
        self.loading_animation()
        self.clear()
        while True:
            Console.SetCursorPosition(0,2)
            self.show_bitcoin()
            key = self.wait(skip=[" "])
            if key == "1":
                self.shop()
            elif key == "2":
                self.show_miners()
            elif key == "3":
                self.gamble_bitcoin()
            self.money += self.calc_increment_value()
            self.save_game()


MinerGame().run()
