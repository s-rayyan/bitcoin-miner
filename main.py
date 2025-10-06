from time import sleep, time
from os import get_terminal_size, path
from math import floor, ceil
from random import choice, randint, seed
import System
from System import Console
import json
import threading

class MinerGame:
	RESET = "\033[0m"

	def __init__(self):
		self.money = 100
		self.delay = 1000
		self.miners = ["Wood"]
		self.miner_types = [
			"Wood", "Stone", "Copper", "Iron", "Gold", "Sapphire", "Diamond",
			"Ruby", "Emerald", "Platinum", "Titanium", "Uranium", "Krypton",
			"Neutron", "Quantum", "Omega", "Oblivion", "Celestium", "Etherion",
			"Aetherium"
		]

		seed(42)

		prefixes = [
			"Void", "Solar", "Lunar", "Aether", "Cryo", "Pyro", "Shadow", "Radiant",
			"Flux", "Chrono", "Nebula", "Vortex", "Hyper", "Myth", "Obliv", "Eternal",
			"Quantum", "Celest", "Astral", "Draco", "Tempest", "Storm", "Grav", "Omni",
			"Nova", "Frost", "Ignis", "Ether", "Spectra", "Paradox"
		]

		suffixes = [
			"ite", "ium", "iumX", "core", "stone", "crystal", "glass", "shard", "flux",
			"matrix", "forge", "metal", "sphere", "coreX", "quartz", "dust", "flare",
			"forgeX", "prime", "flareX", "lite", "iumZ", "stoneX", "coreZ"
		]

		# generate 500 consistent names
		for _ in range(5000):
			name = choice(prefixes) + choice(suffixes)
			self.miner_types.append(name)

		seed()

		self.SAVE_FILE = "save.json"
		self.load_game()

	# =============== LOADING ===============
	def loading_animation(self, text="Bitcoin Miner Booting..."):
		self.clear()
		cols = get_terminal_size().columns
		rows = 200
		stream_chars = "01"

		for _ in range(rows):
			line = "".join(
				f"\033[32m{choice(stream_chars)}\033[0m" if randint(0, 4) else " "
				for _ in range(cols)
			)
			print(line)
		sleep(0.5)
		msg = text.center(cols)
		print(f"\033[1;32m{msg}\033[0m")
		sleep(1)

	# =============== GAME STATE ===============
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

	# =============== UTILITIES ===============
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

	def border(self, title=""):
		cols = get_terminal_size().columns
		top = "═" * cols
		print(f"\033[48;5;22m{top}\033[0m")
		if title:
			self.color(self.center(f" {title} "), fg="bright_white", bg="dark_green")
			print(f"\033[48;5;22m{top}\033[0m")

	def menu(self):
		cols = get_terminal_size().columns
		opts = ["Shop", "Gambling", "Typing", "Stats"]
		menu_line = "   ".join(f"[{i+1}] {opt}" for i, opt in enumerate(opts))
		border = "═" * cols
		print(f"\033[48;5;22m{border}\033[0m")
		self.color(menu_line.center(cols), fg="bright_white", bg="dark_green")
		print(f"\033[48;5;22m{border}\033[0m")

	def show_bitcoin(self):
		self.color(f"Bitcoin: {self.money:,}          ", fg="bright_yellow")

	# =============== ECONOMY ===============
	def get_value(self, miner):
		idx = self.miner_types.index(miner) + 1
		return round((idx ** 3))

	def get_price(self, miner):
		amt = self.miners.count(miner)
		idx = self.miner_types.index(miner) + 1
		base = (idx ** 3.5) * 75
		return round(base * (1.12 ** amt))

	def calc_increment_value(self):
		return sum(self.get_value(i) for i in self.miners)

	# =============== SHOP ===============
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
				self.color("✘ Not enough Bitcoin!", fg="red")

		index = 0
		self.clear()
		self.border("SHOP")

		while True:
			Console.SetCursorPosition(0, 7)
			self.show_bitcoin()
			miner = self.miner_types[index]
			price = self.get_price(miner)
			owned = self.miners.count(miner)
			value = self.get_value(miner)
			timeToAfford = ceil((price-self.money)/self.calc_increment_value())
			toaText = f"{timeToAfford:,}" + " seconds" if timeToAfford > 0 else "You can afford this"
			self.color(f"Miner: {miner}                                         ", fg="cyan")
			self.color(f"Price: {price:,} Bitcoin                               ", fg="yellow")
			self.color(f"Bitcoin Per Second: {value:,}                                         ", fg="yellow")
			self.color(f"Owned: {owned:,}                                           ", fg="bright_white")
			self.color(f"Est. Time to Afford: {toaText}             ", fg="bright_white")
			self.color("\n[A]/[D] Browse [S] Last   [Space] Buy   [Q] Quit           ", fg="bright_magenta")
			key = None
			if Console.KeyAvailable:
				key = self.get_key()
				while Console.KeyAvailable:
				 	Console.ReadKey(True)  
			if key == "d" and (self.miner_types[index+1] in self.miners or (self.miner_types[index+1] not in self.miners and self.miner_types[index] in self.miners) ):
				index = (index + 1)
			elif key == "d":
				print(f"You have yet to unlock the {self.miner_types[index+1]} miner.")
				Console.SetCursorPosition(0, Console.CursorTop-1)
				sleep(0.7)
				print("                                                                               ")
			elif key == "s":
				index = max(self. miner_types.index(i) for i in self.miners)+1
			elif key == "a" and index != 0:
				index = (index - 1)
			elif key == " ":
				buy(index)
			elif key == "q":
				break
		self.clear()

	# =============== TYPING MINIGAME ===============
	def typing_minigame(self):
		self.clear()
		self.border("TYPING CHALLENGE")

		words = [
			"cat","dog","sun","run","fun","red","big","hot","cold","wet",
			"box","bag","car","bat","cap","bed","cup","pen","toy","top",
			"sit","run","hop","hit","cut","fix","mix","win","eat","fit",
			"man","boy","girl","mom","dad","kid","baby","fish","bird","bug",
			"cow","pig","ant","bee","hen","rat","fox","frog","bear","duck",
			"tree","leaf","wood","rock","sand","mud","rain","snow","wind","sky",
			"day","night","sun","moon","star","fire","ice","ball","game","play",
			"book","bag","door","wall","floor","room","key","lock","bell","shoe",
			"hat","shirt","pants","sock","coat","cake","milk","egg","rice","corn",
			"bread","water","salt","sugar","juice","cup","plate","fork","spoon","knife",
			"fast","slow","soft","hard","high","low","big","small","good","bad",
			"kind","mean","fun","mad","sad","happy","clean","dirty","new","old",
			"jump","kick","push","pull","make","take","find","get","see","go"
		]


		target_words = [choice(words) for _ in range(10)]
		target_text = " ".join(target_words)

		self.color("Type the following:", fg="bright_cyan")
		self.color(f" {target_text}", fg="cyan")

		Console.Write("> ")
		Console.CursorVisible = True

		start = None
		typed = ""

		while True:
			key = Console.ReadKey(True)
			if start is None:
				start = time()
			if key.Key == System.ConsoleKey.Enter:
				break
			elif key.Key == System.ConsoleKey.Backspace:
				if len(typed) > 0:
					Console.Write("\b \b")
					typed = typed[:-1]
			else:
				Console.Write(key.KeyChar)
				typed += key.KeyChar

		Console.CursorVisible = False
		end = time()
		time_taken = max(1, end - start)

		typed_words = typed.strip().split()
		correct = sum(1 for a, b in zip(typed_words, target_words) if a == b)
		wpm = (len(typed_words) / time_taken) * 60
		if wpm > 250:
			print("")
			print("WHY DID YOU CHEAT HUH?")
			print("WELL GO TO HELL")
			print("RESETTING YOUR SAVE FILE")
			print("SAY GOODBYE TO YOUR MINERS")
			self.money = -99
			self.miners = ["Wood"]
			Console.ReadLine()
			self.clear()
			return
		reward = round(self.money * 0.1 * (wpm / 30) * ((correct / 10)*(correct / 10)))
 
		self.money += reward

		self.color(f"\n✔ {correct}/10 words correct", fg="bright_green")
		self.color(f"Speed: {int(wpm)} WPM   Reward: {reward:,} Bitcoin", fg="yellow")

		self.color("\nPress any key to return...", fg="magenta")
		self.get_key()
		self.clear()

	# =============== GAMBLING ===============
	def gamble_bitcoin(self):
		def draw_card():
			return choice([2,3,4,5,6,7,8,9,10,10,10,10,11])

		def hand_value(hand):
			total = sum(hand)
			while total > 21 and 11 in hand:
				hand[hand.index(11)] = 1
				total = sum(hand)
			return total

		while True:
			self.clear()
			self.border("BLACKJACK")
			self.show_bitcoin()

			self.color("Enter your bet (or letter to quit): If you win, you get double your bet", fg="yellow")
			try:
				Console.Write("> ")
				bet = int(Console.ReadLine())
			except ValueError:
				break

			if bet <= 0 or bet > self.money:
				self.color("Invalid bet!", fg="red")
				sleep(1)
				continue
			player, dealer = [draw_card(), draw_card()], [draw_card(), draw_card()]

			while True:
				self.clear()
				self.border("BLACKJACK")
				self.color(f"Your hand: {player} (Total: {hand_value(player)})", fg="green")
				self.color(f"Dealer shows: [{dealer[0]}, ?]", fg="red")

				if hand_value(player) > 21:
					self.color("❌ You busted!", fg="red")
					self.money -= bet
					break

				self.color("\nHit or Stand? (h/s)", fg="yellow")
				choice_key = self.get_key()
				if choice_key == "h":
					player.append(draw_card())
				elif choice_key == "s":
					break

			if hand_value(player) <= 21:
				while hand_value(dealer) < 17:
					dealer.append(draw_card())

				self.clear()
				self.border("RESULTS")
				self.color(f"Your hand: {player} (Total: {hand_value(player)})", fg="green")
				self.color(f"Dealer's hand: {dealer} (Total: {hand_value(dealer)})", fg="red")

				p, d = hand_value(player), hand_value(dealer)
				if d > 21 or p > d:
					self.color(f"🎉 You win {bet*2}!", fg="bright_green")
					self.money += 2 * bet
				elif p < d:
					self.color(f"❌ You lose {bet}!", fg="red")
					self.money -= bet
				else:
					self.color("Push (tie).", fg="yellow")

			if self.money <= 0:
				self.color("You're broke! Game over.", fg="red")
				break

			self.color("Play again? (y/n)", fg="yellow")
			if self.get_key() != "y":
				break
		self.clear()

	# =============== STATS ===============
	def stats_screen(self):
		self.clear()
		self.border("PLAYER STATS")
		self.color(f"Money: {self.money:,}", fg="green")
		self.color(f"Total Miners: {len(self.miners)}", fg="cyan")
		self.color("\nYour Miners:", fg="magenta")

		counts = {}
		for m in self.miners:
			counts[m] = counts.get(m, 0) + 1
		for miner, amt in counts.items():
			self.color(f"  {miner}: {amt}", fg="bright_white")

		self.color("\nExtra Stats:", fg="blue")
		self.color(f"Value per Tick: {self.calc_increment_value()}", fg="bright_green")
		self.color(f"Unique Miners: {len(counts)}", fg="bright_cyan")

		self.color("\nPress any key to return...", fg="yellow")
		self.get_key()
		self.clear()

	# =============== WAIT + MAIN LOOP ===============
	def wait(self, amt=None, skip=[], skipallbut=None):
		steps = 24
		width = int(max(10, get_terminal_size().columns / 3 - 10))
		delay = (amt or (self.delay / 1000)) / steps

		for step in range(steps):
			sleep(delay)
			progress = (step + 1) / steps
			locked = floor(progress * width)

			line = "".join(
				"█" if i < locked else (choice("01") if randint(0, 12) == 0 else "░")
				for i in range(width)
			)
			pct = int(progress * 100)
			status = f" DECRYPT {pct:3d}% "

			Console.SetCursorPosition(0, Console.CursorTop if step == 0 else Console.CursorTop - 2)
			self.color(line, fg="bright_green")
			self.color(status, fg="green")

			if Console.KeyAvailable:
				key = self.get_key()
				if ((len(skip) > 0) or (key not in skip)) and (skipallbut == None or key in skipallbut):
					return key

		Console.SetCursorPosition(0, Console.CursorTop - 2)
		self.color("█" * width, fg="bright_green")

	def run(self):
		def inc_money():
			while True:
				self.money += self.calc_increment_value()
				sleep(self.delay / 1000)

		threading.Thread(target=inc_money, daemon=True).start()

		Console.CursorVisible = False
		self.loading_animation()
		self.clear()
		i = 0
		while True:
			Console.SetCursorPosition(0, 3)
			self.show_bitcoin()
			print(f"Bicoin Per Second: {self.calc_increment_value()}")
			key = self.wait(0.9, skipallbut="1 2 3 4".split(" "))
			if key == "1":
				self.shop()
			elif key == "2":
				self.gamble_bitcoin()
			elif key == "3":
				self.typing_minigame()
			elif key == "4":
				self.stats_screen()
			if i % 3 == 1:
				self.save_game()
			sleep(0.1)
			i += 1

MinerGame().run()
