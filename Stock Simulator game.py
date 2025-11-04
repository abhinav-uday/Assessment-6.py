import random, json, os

stocks = {
    "TATA": 120.0,
    "RELIANCE": 60.0,
    "MARUTI": 25.0,
    "TESLA": 200.0
}

File = "stock_game.json"

players = {}

def load_game():
    global players
    if os.path.exists(File):
        with open(File, "r") as f:
            data = json.load(f)

        if "stocks" in data:
            stocks.update(data["stocks"])

        if "players" in data:
            players = data["players"]
        else:
            players = {}

        print("Game loaded!")
    else:
        print("No save file found. Starting fresh.")

def save_game():
    data = {"stocks": stocks, "players": players}
    with open(File, "w") as f:
        json.dump(data, f, indent=4)
    print("Game saved!")

def show_market(player):
    print("\nToday's Prices:")
    for s, p in stocks.items():
        print(f"{s}: ₹{p:.2f}")
    print(f"\nCash: ₹{player['cash']:.2f}")
    print("Holdings:", player["holdings"])

def next_day():
    for s in stocks:
        change = random.uniform(-0.2, 0.2)
        stocks[s] = round(stocks[s] * (1 + change), 2)

def buy_stock(player_name):
    player = players[player_name]
    stock = input("Which stock? ").upper()
    if stock not in stocks:
        print("Invalid stock!")
        return
    shares = int(input("How many shares? "))
    cost = stocks[stock] * shares
    if cost > player["cash"]:
        print("Not enough cash!")
    else:
        player["cash"] -= cost
        player["holdings"][stock] += shares
        players[player_name] = player  
        print(f"Bought {shares} of {stock} for ₹{cost:.2f}")

def sell_stock(player_name):
    player = players[player_name]
    stock = input("Which stock? ").upper()
    if stock not in stocks or player["holdings"][stock] == 0:
        print("You don't own this stock!")
        return
    shares = int(input("How many shares to sell? "))
    if shares > player["holdings"][stock]:
        print("Not enough shares!")
        return
    player["holdings"][stock] -= shares
    gain = stocks[stock] * shares
    player["cash"] += gain
    players[player_name] = player
    print(f"Sold {shares} of {stock} for ₹{gain:.2f}")

print("Welcome to the Multi-Player Stock Market Simulator!")
load_game()

player_name = input("Enter your name: ").strip().upper()

if player_name not in players:
    players[player_name] = {"cash": 10000.0, "holdings": {s: 0 for s in stocks}}
    print(f"New profile created for {player_name} with ₹10000 cash.")
else:
    print(f"Welcome back, {player_name}!")

while True:
    show_market(players[player_name])
    action = input("\n(Buy / Sell / Save / Next / Quit): ").lower()

    if action == "buy":
        buy_stock(player_name)
    elif action == "sell":
        sell_stock(player_name)
    elif action == "save":
        save_game()
    elif action == "next":
        next_day()
    elif action == "quit":
        next_day()
        save_game()
        print("Thanks for playing!")
        break
    else:
        print("Invalid action.")

