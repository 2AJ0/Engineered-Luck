import random
import time
import sys

# =========================
# Utility
# =========================

def slow(text, delay=0.01):
    for c in text:
        print(c, end="", flush=True)
        time.sleep(delay)
    print()

def divider():
    print("\n" + "-" * 60 + "\n")

def clean(text):
    return text.strip().lower()

# =========================
# Game State
# =========================

balance = 0
debt = 0
rounds = 0

wins = 0
losses = 0

consecutive_losses = 0
consecutive_wins = 0

guess_history = []
bet_history = []

suspicion = 0
reveal_triggered = False

last_dealer_line = None

# =========================
# Dealer Speech
# =========================

def dealer(lines):
    global last_dealer_line
    filtered = [l for l in lines if l != last_dealer_line]
    if not filtered:
        filtered = lines
    line = random.choice(filtered)
    last_dealer_line = line
    slow("Dealer: " + line)

# =========================
# Rigging Logic
# =========================

def calculate_win_probability(bet, guess):
    base = 0.35

    if bet > 50:
        base -= 0.10

    if guess_history.count(guess) >= 3:
        base -= 0.08

    if len(guess_history) >= 2:
        if guess_history[-1] != guess_history[-2] and consecutive_losses > 0:
            base -= 0.05

    if consecutive_wins >= 2:
        base -= 0.10

    return max(base, 0.05)

# =========================
# Reveal Sequence
# =========================

def reveal_sequence():
    global reveal_triggered
    divider()
    slow("Dealer: One away.")
    time.sleep(1)
    slow("Dealer: Dramatic, right?")
    time.sleep(1)
    slow("Dealer: You thought that was luck?")
    time.sleep(1)
    slow("Dealer: We engineer those.")
    reveal_triggered = True
    divider()

# =========================
# Ending
# =========================

def end_game(message):
    divider()
    slow(message)
    slow("\nSUMMARY")
    slow(f"Rounds played: {rounds}")
    slow(f"Wins: {wins}")
    slow(f"Losses: {losses}")
    sys.exit()

# =========================
# Start
# =========================

divider()
slow("🎲 JUST ONE MORE", 0.04)
slow("Guess a number. Beat the house.")
input("\nPress Enter to sit at the table...")
divider()

dealer([
    "Let's begin.",
    "Try your luck.",
    "It's completely fair."
])

# =========================
# Main Loop
# =========================

while True:
    rounds += 1

    slow(f"\nBalance: {balance} | Debt: {debt}")

    action = clean(input("\nEnter bet amount or type 'leave': "))

    # =========================
    # Leave Logic
    # =========================

    if action == "leave":
        if not reveal_triggered:
            dealer([
                "Leaving already?",
                "That was quick.",
                "You just sat down."
            ])
        else:
            if rounds <= 12:
                end_game("Dealer: You noticed. Impressive.")
            else:
                end_game("Dealer: You knew. You stayed.")
        continue

    # =========================
    # Bet Validation
    # =========================

    try:
        bet = int(action)
        if bet <= 0:
            raise ValueError
    except:
        dealer(["Numbers. Just numbers."])
        continue

    bet_history.append(bet)

    # =========================
    # Guess
    # =========================

    try:
        guess = int(input("Guess a number (1–10): "))
        if guess < 1 or guess > 10:
            raise ValueError
    except:
        dealer(["That wasn't a real guess."])
        continue

    guess_history.append(guess)
    if len(guess_history) > 5:
        guess_history.pop(0)

    rolled = random.randint(1, 10)

    win_prob = calculate_win_probability(bet, guess)
    win = (guess == rolled) and (random.random() < win_prob)

    # =========================
    # Dramatic Roll
    # =========================

    slow("Rolling...")
    time.sleep(0.8)
    slow(f"The number was: {rolled}")

    # =========================
    # Near Miss Check
    # =========================

    near_miss = abs(guess - rolled) == 1

    if near_miss:
        suspicion += 1

    if consecutive_losses >= 3:
        suspicion += 1

    if bet > 50:
        suspicion += 1

    # =========================
    # Dramatic Reveal Trigger
    # =========================

    if (
        not reveal_triggered
        and rounds >= 10
        and suspicion >= 3
        and near_miss
    ):
        reveal_sequence()

    # =========================
    # Resolution
    # =========================

    if win:
        wins += 1
        consecutive_wins += 1
        consecutive_losses = 0
        balance += bet
        suspicion = max(0, suspicion - 1)

        if not reveal_triggered:
            dealer([
                "You got it.",
                "Lucky.",
                "Well played."
            ])
        else:
            dealer([
                "We let that one through.",
                "Engagement boost.",
                "Keeps it interesting."
            ])

    else:
        losses += 1
        consecutive_losses += 1
        consecutive_wins = 0

        if balance >= bet:
            balance -= bet
        else:
            debt += bet - balance
            balance = 0

        if not reveal_triggered:
            if near_miss:
                dealer([
                    "So close.",
                    "One away.",
                    "That stings."
                ])
            else:
                dealer([
                    "Not this time.",
                    "Unlucky.",
                    "House wins."
                ])
        else:
            dealer([
                "We needed tension.",
                "Drama matters.",
                "Retention design."
            ])
            