## Overview  

This repository contains **Adaptive Crypto Trading Optimization System (ACTOS)** primarily for **Bitcoin (BTC)**, developed based on research and optimization techniques. These strategies leverage **trend, volatility, momentum, and volume indicators** to maximize profitability while minimizing drawdowns.  

The development of **ACTOS V1** was inspired by a research paper on **Multi-Indicator-based Hierarchical Strategies (MIHS)** for crypto market analysis ([ResearchGate Link](https://www.researchgate.net/publication/373942404_Multi_Indicator_based_Hierarchical_Strategies_for_Technical_Analysis_of_Crypto_market_Paradigm)). The study analyzed the effectiveness of **EMA, RSI, PSAR, and Bollinger Bands (BB)** under different market conditions, leading to the refinement of MIHCS into **ACTOS** strategies.  

---

## Strategies Included  

### **ACTOS V1 (Adaptive Cryptocurrency Trading Optimization System)**  
- Incorporates hierarchical decision making using **EMA, RSI, and PSAR** for trade execution.  
- Addresses **lagging effects** in EMA strategies by integrating additional confirmation indicators.  
- Designed for **trending markets**, with limited efficiency in **sideways markets**.  

### **NSGA-II Optimization (Not a Strategy, for Parameter Tuning Only)**  
- NSGA-II is a multi-objective optimization algorithm that finds a set of optimal solutions (Pareto front).
- It ranks solutions using non-dominated sorting and maintains diversity with crowding distance.
- Elitism ensures the best solutions persist across generations, improving efficiency and convergence.

### **ACTOS V2 (Refined version of ACTOS V1 based on NSGA-II optimization)**  
- **Optimizes EMA, RSI, and PSAR parameters** using **NSGA-II (Non-Dominated Sorting Genetic Algorithm II)**.  
- Improves **profitability, Sharpe ratio, and drawdown metrics**.  
- Helped refine **ACTOS V1** by reducing **lagging effects** in indicator calculations.
- Also **reinvests profits**, affecting compounding.  

## Technical Indicators Considered  

- **Trend Indicators**:  
  - **Exponential Moving Average (EMA)**: Detects trend direction.  
  - **Parabolic SAR (PSAR)**: Identifies potential reversals.  

- **Momentum Indicators**:  
  - **Relative Strength Index (RSI)**: Measures overbought/oversold conditions.  

- **Volatility Indicators**:  
  - **Bollinger Bands (BB)**: Captures price volatility.  

These indicators were selected based on their performance in **different market conditions** as analyzed in MIHCS research, and considerations of combined results.  

---

## 🔧 How to Use  

### **1. Use in TradingView (Pine Script)**  
- Copy **ACTOS-V1.pine** or **ACTOS-V2.pine** into TradingView.  
- Apply it to any asset (Crypto, Stocks, Forex).  
- Adjust input parameters if needed.  

### **2. Backtesting & Optimization (Python)**  
- Run **NSGA-II scripts** in the `NSGA-II` folder to fine-tune strategy parameters.  
- Requires `ta` and `deap` Python libraries (`pip install ta deap`).  

---

## 🔮 Future Work  

- **Developing a strategy for sideways markets** to improve performance during range-bound conditions.  
- **Exploring machine learning-based dynamic strategy switching** based on market conditions.  

---

## 🛠️ Contributions  

Want to improve the strategy?  

- Fork the repo & submit pull requests.  
- Share insights on **market adaptability** and **strategy optimization techniques**.  
- Join discussions on **parameter tuning** for different assets.  

---

## ⚠️ Disclaimer  

**This repository is for educational purposes only.**  
Algorithmic trading involves **significant risks**, and past performance **does not** guarantee future results.  
**Trade responsibly.**  

---


