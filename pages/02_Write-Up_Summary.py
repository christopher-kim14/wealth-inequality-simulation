import streamlit as st

st.title("Write-Up Summary")

st.markdown("""
## Overview

For my creative final project, I developed an interactive simulation to explore the issue of wealth inequality using mathematical tools from counting and number theory. My project models how a fixed amount of wealth can be distributed among a group of individuals and how different taxation/redistribution systems impact economic outcomes over time.

This simulation allows users to:
- Set the number of players and total initial wealth
- Choose whether to set a minimum wealth for all players
- Manually or automatically distribute the remaining wealth
- Manually or automatically determine income per player
- Select from different tax systems:
  - Progressive Tax based on overall percentile of wealth 
    - Top 10%: 25% tax
    - 75–90%: 15% tax
    - 50–75%: 10% tax
    - Bottom 50%: 5% tax
  - Flat Wealth Tax
  - Modulo Tax using modular arithmetic
- Track changes in wealth across multiple rounds
- Analyze inequality using the standard deviation and the Gini coefficient

---

## Discrete Mathematics Concepts Used

### 1. Counting: Stars and Bars
I used the stars and bars theorem to calculate how many ways wealth can be distributed among players. If there are _W_ total units of wealth and _n_ players, the number of non-negative integer distributions is:

$$
C(W + n - 1, n - 1) = \\binom{W + n - 1}{n - 1}
$$

This result tells us how many different possible compositions of wealth exist, given the total initial wealth and the minimum wealth per player set by the user. I included this to illustrate the vast number of possible wealth distributions, even under simple constraints.

### 2. Counting: Functions and Relations
In discrete math, a function is a rule that assigns each element in a domain (inputs) to exactly one element in a codomain (outputs). In this simulation, we define several such mappings:

- $$ f_1: \\text{Player} \\rightarrow \\text{Wealth} $$
- $$ f_2: \\text{Player} \\rightarrow \\text{Income} $$
- $$ f_3: \\text{Player} \\rightarrow \\text{Tax\ Paid} $$

These are all examples of maps/relations. Each round updates these mappings as wealth and tax values change, showing how these mathematical functions evolve over time.

### 3. Number Theory: Modulo Arithmetic
I used modular arithmetic to implement the Modulo Tax, where a player's tax is computed as:

$$
\\text{Tax} = \\text{Wealth} \\bmod x
$$

where _x_ is the user-specified divisor. This type of taxation simulates a cyclical/leftover-based taxation system. Thus, modular arithmetic allows us to group players by wealth residue classes and apply taxes in a mathematically cyclical way.



### 4. Euclidian/Division Algorithm
The division algorithm states that for integers _m_, _n_, there exist unique integers _q_ and _r_ such that:

$$
m = qn + r \quad \\text{and} \quad 0 \leq r < n
$$

This is used every time we divide the tax pool evenly among players and when the user chooses not to manually distribute the remaining wealth or income.
This ensures a simple and fair-as-possible distribution using the logic of the division algorithm, where for the wealth/income every player gets the same share _q_ and any remainder _r_ is either ignored or tracked.
For the tax pool, the quotient _q_ is the redistributed amount, and _r_ is the remainder that represents the undistributed wealth from the pool. Understanding this helps explain why redistribution is sometimes not perfectly equal.




### 5. Number Theory: Greatest Common Denominator (GCD)
The Greatest Common Divisor (GCD) is the largest integer that divides two numbers without leaving a remainder. In this simulation, I used it to determine whether wealth redistribution after taxation could be done fairly — meaning equal amounts without leftovers.
If _T_ = total tax pool after a round and _n_ = number of players, then:

$$
\\text{Redistribution is fair} \iff \gcd(T, n) = n \quad \\text{or} \quad T \\bmod n = 0
$$

For example, if the tax pool is 25 and there are 5 players:

$$
\gcd(25, 5) = 5 \quad \Rightarrow \quad \\text{Fair redistribution}
$$

But if the pool is 23:

$$
\gcd(23, 5) = 1 \quad \Rightarrow \quad \\text{Unfair redistribution}
$$

---

## Inequality Metrics

### Standard Deviation

Standard deviation measures how far individual wealth values deviate from the mean wealth across all players. A low standard deviation means wealth is tightly clustered around the mean (more equal), while a high standard deviation means wealth is spread out with large disparities between rich and poor players (less equal).
Thus, in my simulation standard deviation helps track how consistently wealth is distributed and how taxation/redistribution affect inequality from round to round.


### Gini Coefficient

The Gini Coefficient is a widely used measure of inequality in economics. It is based on the Lorenz curve, which compares the actual distribution of wealth to a perfectly equal distribution.
The formula is:

$$
G = \\frac{2 \sum_{i=1}^{n} i x_i}{n \sum_{i=1}^{n} x_i} - \\frac{n + 1}{n}
$$

where $x_i$ are the sorted wealth values (from poorest to richest) and _n_ is the number of players. The value of the Gini Coefficient is always between 0 and 1, where $G = 0$ represents perfect equality (everyone has the same wealth) and $G = 1$ represents perfect inequality (one person has all the wealth). 
In this simulation, the Gini coefficient is tracked across rounds and serves as the key indicator of whether the tax system is positively or negatively impacting wealth inequality.

---

## Works Cited

- https://discrete.openmathbooks.org/dmoi3/
- https://matthbeck.github.io/papers/aop.noprint.pdf
- https://www.census.gov/topics/income-poverty/income-inequality/about.html
- https://inequality.org/facts/taxes-inequality-in-united-states/
- https://www.investopedia.com/ask/answers/042415/what-are-differences-between-regressive-proportional-and-progressive-taxes.asp
- https://ourworldindata.org/what-is-the-gini-coefficient
- https://en.wikipedia.org/wiki/Gini_coefficient
""")
