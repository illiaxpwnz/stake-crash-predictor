import numpy as np
import matplotlib.pyplot as plt
import random

# Function to simulate a single crash round
def simulate_crash_round():
    # Generate a crash multiplier between 1.01 and 1000
    return max(1.01, min(1000, np.random.pareto(a=2) + 1))

# Function to simulate multiple crash rounds and gather statistics
def simulate_crash_game(num_rounds):
    results = [simulate_crash_round() for _ in range(num_rounds)]
    return results

# Function to analyze the multiplier data
def analyze_multipliers(results):
    thresholds = [2, 5, 10, 50, 100, 500, 1000]
    counts = {threshold: 0 for threshold in thresholds}
    for result in results:
        for threshold in thresholds:
            if result >= threshold:
                counts[threshold] += 1
    return counts

# Function to simulate the Martingale strategy
def simulate_martingale_strategy(results, initial_bet, cashout_multiplier):
    balance = 0
    bet = initial_bet
    max_bet = initial_bet
    for result in results:
        if result >= cashout_multiplier:
            balance += bet * (cashout_multiplier - 1)
            bet = initial_bet
        else:
            balance -= bet
            bet *= 2
            if bet > max_bet:
                max_bet = bet
        if balance < -10000:  # Stop if the loss exceeds a large amount (e.g., $10,000)
            break
    return balance, max_bet

# Main simulation
num_rounds = 1000000
results = simulate_crash_game(num_rounds)

# Analyze the results
multiplier_counts = analyze_multipliers(results)
print("Multiplier Analysis:")
for threshold, count in multiplier_counts.items():
    print(f"Multipliers >= x{threshold}: {count} times ({count / num_rounds * 100:.2f}%)")

# Plot histogram of multipliers
plt.hist(results, bins=100, log=True)
plt.xlabel('Multiplier')
plt.ylabel('Frequency')
plt.title('Distribution of Crash Game Multipliers')
plt.show()

# Simulate the Martingale strategy
initial_bet = 0.01
cashout_multiplier = 2.0
balance, max_bet = simulate_martingale_strategy(results, initial_bet, cashout_multiplier)
print(f"Martingale Strategy Results:")
print(f"Final Balance: ${balance:.2f}")
print(f"Max Bet Placed: ${max_bet:.2f}")

# Simulate different strategies
strategies = {
    "Martingale": (0.01, 2.0),
    "Aggressive": (0.01, 5.0),
    "Conservative": (0.01, 1.5)
}

for strategy_name, (initial_bet, cashout_multiplier) in strategies.items():
    balance, max_bet = simulate_martingale_strategy(results, initial_bet, cashout_multiplier)
    print(f"{strategy_name} Strategy Results:")
    print(f"Initial Bet: ${initial_bet:.2f}, Cashout Multiplier: x{cashout_multiplier}")
    print(f"Final Balance: ${balance:.2f}")
    print(f"Max Bet Placed: ${max_bet:.2f}")
    print("-" * 30)
