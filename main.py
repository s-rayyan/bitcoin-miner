from time import sleep
import System
from System import Console
from os import get_terminal_size
import json
import os
from math import floor

class MinerGame:
    RESET = "\033[0m"

    def __init__(self):
        self.money = 100
        self.delay = 1000
        self.miners = []
        self.miner_types = "Wood Stone Copper Iron Gold Sapphire Diamond Ruby Emerald Platinum Titanium Uranium Krypton Neutron Quantum Omega Alpha Beta Gamma Delta Sigma".split(" ")
        self.SAVE_FILE = "save.json"
        self.load_game()

    # ==================== GAME STATE ====================
    def load_game(self):
        if os.path.exists(self.SAVE_FILE):
            with open(self.SAVE_FILE, "r") as f:
                try:
                    data = json.load(f)
                    self.money = data.get("money", 100)
                    self.miners = data.get("miners", [])
                except Exception:
                    self.money = 100
                    self.miners = []

    def save_game(self):
        data = {"money": self.money, "miners": self.miners}
        with open(self.SAVE_FILE, "w") as f:
            json.dump(data, f)

    # ==================== UTILITIES ====================
    def color(self, text, fg=None, bg=None):
        colors = {
            "black": 30, "red": 31, "green": 32, "yellow": 33,
            "blue": 34, "magenta": 35, "cyan": 36, "white": 37,
            "bright_black": 90, "bright_red": 91, "bright_green": 92,
            "bright_yellow": 93, "bright_blue": 94, "bright_magenta": 95,
            "bright_cyan": 96, "bright_white": 97
        }
        seq = ""
        if fg and fg in colors:
            seq += f"\033[{colors[fg]}m"
        if bg and bg in colors:
            seq += f"\033[{colors[bg]+10}m"
        print(f"{seq}{text}{self.RESET}")

    def get_key(self):
        return Console.ReadKey(True).KeyChar

    def clear(self):
        Console.Clear()
        self.menu()

    def menu(self):
        options = ["Shop", "Miners"]
        index = 1
        text = ""
        for i in options:
            text += str(index) + " " + i + "   "
            index += 1
        for _ in range(get_terminal_size().columns - len(text)):
            text += " "
        self.color(text, bg="red")

    def show_bitcoin(self):
        print(f"You have {self.money} Bitcoin")

    # ==================== MINER FUNCTIONS ====================
    def get_value(self, miner):
        idx = self.miner_types.index(miner) + 1
        return round(idx ** 1.8)

    def get_price(self, miner):
        idx = self.miner_types.index(miner) + 1
        return round(5 * (idx ** 3.69))

    def calc_increment_value(self):
        return sum(self.get_value(i) for i in self.miners)

    def shop(self):
        def buy(index):
            price = self.get_price(self.miner_types[index])
            if self.money >= price:
                self.money -= price
                self.miners.append(self.miner_types[index])
                print(f"Successfully acquired {self.miner_types[index]} miner")
                self.save_game()

        index = 0
        while True:
            self.clear()
            print("Select a miner with the A and D keys, and use Space to select, Q to quit")
            self.show_bitcoin()
            print("Name: " + self.miner_types[index])
            print("Price: " + str(self.get_price(self.miner_types[index])) + " Bitcoin")
            key = self.get_key()
            if key == "d":
                index = (index + 1) % len(self.miner_types)
            if key == "a":
                index = (index - 1) % len(self.miner_types)
            if key == " ":
                buy(index)
                break
            if key == "q":
                break

    def show_miners(self):
        self.clear()
        print("These are your bitcoin miners, press any key to go back")
        self.miners.sort(key=lambda x: self.miner_types.index(x))
        prev = None
        group = []

        for miner in self.miners:
            if miner == prev:
                group.append(miner)
            else:
                if prev is not None:
                    print(prev + " x" + str(len(group)))
                prev = miner
        group = [miner]
        
        if prev is not None:
            print(prev + " x" + str(len(group)))        
        self.get_key()

    # ==================== WAIT FUNCTION ====================
    def wait(self, amt=None, skip=[]):
        for step in range(10):
            sleep(amt or self.delay / 1000 / 10)
            txt = ""
            tot = get_terminal_size().columns / 10 / 5
            for j in range(floor(tot * (step + 1))):
                txt += "0"
            for j in range(floor(tot * (10 - step))):
                txt += " "
            Console.SetCursorPosition(0, Console.CursorTop if step == 0 else Console.CursorTop - 1)
            self.color(txt, bg="bright_red", fg="white")
            if Console.KeyAvailable:
                key = self.get_key()
                if key not in skip:
                    return key

    # ==================== MAIN LOOP ====================
    def run(self):
        while True:
            self.clear()
            self.show_bitcoin()
            key = self.wait(skip=[" "])
            if key == "1":
                self.shop()
            if key == "2":
                self.show_miners()
            self.money += self.calc_increment_value()
            self.save_game()

game = MinerGame()
game.run()
