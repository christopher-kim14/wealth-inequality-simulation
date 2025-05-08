import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
from math import comb, gcd

# Setup
st.title("Wealth Inequality Simulation")

num_players = st.slider("Number of Players", min_value=2, max_value=20, value=5)
total_wealth = st.number_input("Total Initial Wealth to be Distributed", min_value=1, value=100000)
set_minimums = st.checkbox("Set a minimum wealth for each player")
custom_income = st.checkbox("Manually choose income per player")

# Wealth distribution
if set_minimums:
    minimum_per_player = st.number_input("Minimum wealth per player", min_value=0, max_value=total_wealth, value=0)
else:
    minimum_per_player = 0
manual_distribution = st.checkbox("Manually distribute remaining wealth")
remaining_wealth = total_wealth - (minimum_per_player * num_players)
if remaining_wealth < 0:
    st.error("Error: Not enough total wealth")
    st.stop()

constrained_distributions = comb(remaining_wealth + num_players - 1, num_players - 1)
st.markdown(f"**Number of distinct ways to distribute remaining wealth (with minimum):** {constrained_distributions}")

players = {}
if manual_distribution:
    st.markdown("### Distribute remaining wealth manually:")
    remaining = remaining_wealth
    for i in range(num_players):
        name = f"Player {i + 1}"
        if i < num_players - 1:
            extra = st.number_input(f"{name}", min_value=0, max_value=remaining, key=f"extra_{i}")
            players[name] = minimum_per_player + extra
            remaining -= extra
        else:
            players[name] = minimum_per_player + remaining
            st.info(f"{name} receives the remaining ${remaining}.")
else:
    share = remaining_wealth // num_players
    for i in range(num_players):
        name = f"Player {i + 1}"
        players[name] = minimum_per_player + share
    st.info(f"Each player receives an equal share of ${share}.")

# Income
incomes = {}
def_income = total_wealth // 10
for p in players:
    if custom_income:
        incomes[p] = st.number_input(f"Income per round for {p}", min_value=0, value=def_income, key=f"income_{p}")
    else:
        incomes[p] = def_income

# Tax 
st.markdown("### Tax System")
tax_system = st.selectbox("Select tax system", ["Progressive Tax", "Flat Wealth Tax", "Modulo Tax"])
if tax_system == "Modulo Tax":
    mod_divisor = st.number_input("Enter divisor for modulo tax", min_value=1, value=10)

rounds = st.slider("Number of Rounds", 1, 50, 10)

# Gini Coefficient
def gini_coefficient(values):
    sorted_values = sorted(values)
    n = len(values)
    cumulative = sum((i + 1) * val for i, val in enumerate(sorted_values))
    total = sum(sorted_values)
    return (2 * cumulative) / (n * total) - (n + 1) / n if total > 0 else 0

# Simulation
if st.button("Run Simulation"):
    wealth_history = {p: [w] for p, w in players.items()}
    std_history = [np.std(list(players.values()))]
    gini_history = [gini_coefficient(list(players.values()))]

    for r in range(rounds):
        # Income 
        for p in players:
            players[p] += incomes[p]

        # Tax 
        pool = 0
        if tax_system == "Progressive Tax":
            player_list = list(players.items())
            def get_wealth(pair):
                return pair[1]
            sorted_players = sorted(player_list, key=get_wealth)
            ranks = {}
            for i in range(len(sorted_players)):
                name = sorted_players[i][0]
                ranks[name] = i
            for p in players:
                percentile = (ranks[p] + 1) / num_players
                if percentile > 0.9:
                    tax = int(players[p] * 0.25)
                elif percentile > 0.75:
                    tax = int(players[p] * 0.15)
                elif percentile > 0.5:
                    tax = int(players[p] * 0.10)
                else:
                    tax = int(players[p] * 0.05)
                players[p] -= tax
                pool += tax
        else:
            for p in players:
                if tax_system == "Modulo Tax":
                    tax = players[p] % mod_divisor if players[p] > mod_divisor else 0
                elif tax_system == "Flat Wealth Tax":
                    tax = int(players[p] * 0.10)
                players[p] -= tax
                pool += tax

        fair = pool % num_players == 0
        st.write(f"Round {r+1} tax pool: ${pool} → {'Equal redistribution 😀' if fair else 'Unequal redistribution 😔'}")

        # Redistribution
        share = pool // num_players
        for p in players:
            players[p] += share

        for p in players:
            wealth_history[p].append(players[p])
        std_history.append(np.std(list(players.values())))
        gini_history.append(gini_coefficient(list(players.values())))

    # Plots
    st.markdown("### Wealth Distribution Over Time")
    fig, ax = plt.subplots()
    for p, history in wealth_history.items():
        ax.plot(range(rounds + 1), history, label=p)
    ax.set_xlabel("Round")
    ax.set_ylabel("Wealth ($)")
    ax.set_title("Wealth by Player")
    ax.legend()
    st.pyplot(fig)
    st.markdown("### Standard Deviation Over Time")
    st.line_chart(std_history)
    st.markdown("### Gini Coefficient Over Time")
    st.line_chart(gini_history)
    st.success("Simulation complete!")
