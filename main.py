from time import sleep
from os import get_terminal_size, path
from math import floor
from random import choice, randint
import System
from System import Console
import json
import sys
import threading

class MinerGame:
    RESET = "\033[0m"

    def __init__(self):
        self.money = 100
        self.delay = 1000
        self.miners = []
        self.miner_types = (
    "Wood Stone Copper Iron Gold Sapphire Diamond Ruby Emerald "
    "Platinum Titanium Uranium Krypton Neutron Quantum Omega "
    "Oblivion Celestium Etherion Aetherium Chronium Eternium "
    "Voidcrystal Singularity Arcanite Starforged Luminaris "
    "Nebulite Astralium Infinitycore Paradoxium Eternacite "
    "Mythrilon Voidcore"
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
        if bg == "dark_green":
            seq += "\033[48;5;22m"
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
        text = "   ".join(f"{i+1} {opt}" for i, opt in enumerate(["Open Shop", "View Miners", "Gambling Room", "Typing Challenge"]))
        text = text.ljust(get_terminal_size().columns)
        self.color(text, bg="dark_green")

    def show_bitcoin(self):
        self.color(f"You have {self.money:,} Bitcoin", fg="bright_yellow")


    # ==================== MINERS ====================
    def get_value(self, miner):
        idx = self.miner_types.index(miner) + 1
        return round((idx ** 2) * 2)  # base value scaling

    def get_price(self, miner):
        amt = self.miners.count(miner)
        idx = self.miner_types.index(miner) + 1
        base = (idx ** 2) * 100         # base price scaling
        return round(base * (1.1 ** amt))

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
                break
            elif key == "q":
                break
        self.clear()
        
    def typing_minigame(self):
        from time import time

        self.clear()
        self.color(self.center("=== TYPING CHALLENGE ==="), fg="yellow")

        words = [
    "cat", "dog", "sun", "tree", "book", "coin", "mine", "rock", "gold", "fast",
    "code", "game", "star", "cloud", "light", "fire", "snow", "wind", "leaf", "rain",
    "ball", "car", "cup", "door", "fish", "frog", "hat", "key", "pen", "shoe",
    "sky", "toy", "wave", "bike", "desk", "lamp", "nest", "ring", "ship", "train",
    "water", "zero", "apple", "ball", "bird", "cake", "duck", "ear", "farm", "gift",
    "hill", "king", "leaf", "moon", "nest", "owl", "pear", "rose", "snow", "tree",
    "wave", "yard", "bee", "cow", "fox", "hen", "pig", "rat", "ant", "bat"
        ]


        target_words = [choice(words) for _ in range(10)]
        target_text = " ".join(target_words)

        self.color(f"Type the following:\n  {target_text}", fg="bright_cyan")

        Console.Write("> ")
        start_time = time()
        typed = Console.ReadLine()
        end_time = time()

        time_taken = end_time - start_time
        typed_words = typed.strip().split()

        correct_words = sum(1 for a, b in zip(typed_words, target_words) if a == b)
        wpm = (len(typed_words) / time_taken) * 60

        if correct_words == len(target_words):
            reward = round(self.money * round(wpm * 2)/1000) 
            self.money += reward
            self.color(f"✔ Perfect! {correct_words}/10 words correct.", fg="bright_green")
            self.color(f"You typed at {int(wpm)} WPM and earned {reward:,} Bitcoin!", fg="bright_green")
        else:
            self.color(f"✘ {correct_words}/10 words correct.", fg="red")
            self.color(f"You gain 0 Bitcoin.", fg="red")

        self.color("Press any key to return...", fg="yellow")
        self.get_key()
        self.clear()

    def gamble_bitcoin(self):
        def draw_card():
            cards = [2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 11]  # 10 = J/Q/K, 11 = Ace
            return choice(cards)

        def hand_value(hand):
            total = sum(hand)
            # Adjust Ace (11 → 1 if bust)
            while total > 21 and 11 in hand:
                hand[hand.index(11)] = 1
                total = sum(hand)
            return total

        while True:
            self.clear()
            self.color(self.center("=== BLACKJACK ROOM ==="), fg="yellow")
            self.color(f"Current Balance: {self.money:,}", fg="green")
            # Get bet
            self.color("Enter your bet, enter a letter to quit", fg="yellow")
            try:
                Console.Write("> ")
                bet = int(Console.ReadLine())
            except ValueError:
                self.color("Invalid input!", fg="red")
                break

            if bet <= 0 or bet > self.money:
                self.color("Invalid bet amount!", fg="red")
                sleep(1.5)
                continue

            # Initial deal
            player = [draw_card(), draw_card()]
            dealer = [draw_card(), draw_card()]

            # Player's turn
            while True:
                self.clear()
                self.color(self.center("=== BLACKJACK ==="), fg="yellow")
                self.color(f"Your hand: {player} (Total: {hand_value(player)})", fg="green")
                self.color(f"Dealer shows: [{dealer[0]}, ?]", fg="red")

                if hand_value(player) > 21:
                    self.color("❌ You busted!", fg="red")
                    self.money -= bet
                    break

                self.color("Hit or Stand? (h/s)", fg="yellow")
                choice_key = self.get_key()
                if choice_key == "h":
                    player.append(draw_card())
                elif choice_key == "s":
                    break

            # Dealer's turn (if player not busted)
            if hand_value(player) <= 21:
                while hand_value(dealer) < 17:
                    dealer.append(draw_card())

                self.clear()
                self.color(self.center("=== RESULTS ==="), fg="yellow")
                self.color(f"Your hand: {player} (Total: {hand_value(player)})", fg="green")
                self.color(f"Dealer's hand: {dealer} (Total: {hand_value(dealer)})", fg="red")

                player_total = hand_value(player)
                dealer_total = hand_value(dealer)

                if dealer_total > 21 or player_total > dealer_total:
                    self.color(f"🎉 You win {bet}!", fg="bright_green")
                    self.money += bet
                elif player_total < dealer_total:
                    self.color(f"❌ You lose {bet}!", fg="red")
                    self.money -= bet
                else:
                    self.color("Push (tie). Bet returned.", fg="yellow")

            if self.money <= 0:
                self.color("You're broke! Game over.", fg="red")
                break

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
        i = 0
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
            elif key == "4":
                self.typing_minigame()

            self.money += self.calc_increment_value()

            if i == 25:
                self.save_game()
            
            sleep(0.1)
            i+=1

MinerGame().run()
