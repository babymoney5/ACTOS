import random
import numpy as np
import pandas as pd
from deap import base, creator, tools, algorithms
import ta


# Load your data (ensure the file path is correct)
data = pd.read_csv('/Users/ll/Downloads/BTC-USD.csv')  # Provide the correct path


# Display the first few rows of the data to ensure it's loaded correctly
print(data.head())


# Define the problem as a multi-objective optimization problem
creator.create("FitnessMulti", base.Fitness, weights=(1.0, -1.0, 1.0))  # Maximize profit, minimize drawdown, maximize Sharpe ratio
creator.create("Individual", list, fitness=creator.FitnessMulti)


# Define the individual and population
toolbox = base.Toolbox()
toolbox.register("attr_float", random.uniform, 0.1, 1.0)  # Avoid zero to prevent invalid ranges
toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_float, n=6)  # Ensure n=6
toolbox.register("population", tools.initRepeat, list, toolbox.individual)


# Define the evaluation function based on your MIHCS strategy
def evaluate(individual):
   ema_length_rsi, ema_length_short, ema_length_long, psar_start, psar_inc, psar_max = individual


   # Ensure the EMA lengths are at least 1
   ema_length_rsi = max(int(ema_length_rsi * 20), 1)
   ema_length_short = max(int(ema_length_short * 20), 1)
   ema_length_long = max(int(ema_length_long * 50), 1)
   psar_start = max(psar_start * 0.1, 0.01)
   psar_inc = max(psar_inc * 0.1, 0.01)
   psar_max = max(psar_max * 0.2, 0.1)


   # Calculate indicators
   data['RSI'] = ta.momentum.rsi(data['Close'], window=14)
   data['EMA_RSI'] = ta.trend.ema_indicator(data['RSI'], window=ema_length_rsi)
   data['EMA_Short'] = ta.trend.ema_indicator(data['Close'], window=ema_length_short)
   data['EMA_Long'] = ta.trend.ema_indicator(data['Close'], window=ema_length_long)
   data['PSAR'] = calculate_psar(data, psar_start, psar_inc, psar_max)


   # Initialize previous values
   prev_psar = data['PSAR'].shift(1)
   prev_rsi = data['RSI'].shift(1)


   # Define entry and exit conditions
   data['Long_Condition'] = (data['EMA_RSI'] > 60) & (data['EMA_Short'] > data['EMA_Long'])
   data['Short_Condition'] = (data['EMA_RSI'] < 40) & (data['PSAR'] > data['Close']) & (prev_psar <= data['PSAR'])
   data['Exit_Condition'] = (data['RSI'] > 55) & (prev_rsi > data['RSI'])


   # Initialize positions and signals
   data['Position'] = 0
   data['Position'] = np.where((data['Long_Condition']) & (data['Position'].shift(1) == 0), 1, data['Position'])
   data['Position'] = np.where((data['Short_Condition']) & (data['Position'].shift(1) == 0), -1, data['Position'])
   data['Position'] = np.where((data['Short_Condition'] | data['Exit_Condition']) & (data['Position'].shift(1) == 1), 0, data['Position'])
   data['Position'] = np.where((data['Long_Condition'] | data['Exit_Condition']) & (data['Position'].shift(1) == -1), 0, data['Position'])


   # Calculate returns
   data['Returns'] = data['Close'].pct_change() * data['Position'].shift(1)
   total_return = data['Returns'].sum()
   max_drawdown = calculate_max_drawdown(data['Returns'].cumsum())
   sharpe_ratio = calculate_sharpe_ratio(data['Returns'])


   # Ensure constraints
   num_trades = data['Position'].diff().abs().sum() / 2
   if num_trades < 10:  # Minimum number of trades
       return -np.inf, np.inf, -np.inf
  
   # Handle invalid values
   if np.isnan(total_return) or np.isnan(max_drawdown) or np.isnan(sharpe_ratio):
       return -np.inf, np.inf, -np.inf
  
   if np.isinf(total_return) or np.isinf(max_drawdown) or np.isinf(sharpe_ratio):
       return -np.inf, np.inf, -np.inf
  
   return total_return, max_drawdown, sharpe_ratio


# Define the custom functions
def calculate_psar(data, start, increment, maximum):
   try:
       psar = ta.trend.PSARIndicator(high=data['High'], low=data['Low'], close=data['Close'], step=increment, max_step=maximum)
       return psar.psar()
   except Exception as e:
       print(f"Error calculating PSAR: {e}")
       return pd.Series([np.nan] * len(data))


def calculate_max_drawdown(cumulative_returns):
   peak = cumulative_returns.expanding(min_periods=1).max()
   drawdown = (cumulative_returns - peak) / peak
   max_drawdown = drawdown.min()
   return max_drawdown


def calculate_sharpe_ratio(returns, risk_free_rate=0.0):
   mean_return = returns.mean()
   std_return = returns.std()
   if std_return == 0:
       return np.nan
   sharpe_ratio = (mean_return - risk_free_rate) / std_return
   return sharpe_ratio


# Register the evaluation function and other components to the toolbox
toolbox.register("evaluate", evaluate)
toolbox.register("mate", tools.cxBlend, alpha=0.5)
toolbox.register("mutate", tools.mutGaussian, mu=0, sigma=1, indpb=0.2)
toolbox.register("select", tools.selNSGA2)
toolbox.register("map", map)


# Main function to run the optimization
def main():
   pop = toolbox.population(n=100)
   hof = tools.ParetoFront()
   stats = tools.Statistics(lambda ind: ind.fitness.values)
   stats.register("avg", np.mean, axis=0)
   stats.register("std", np.std, axis=0)
   stats.register("min", np.min, axis=0)
   stats.register("max", np.max, axis=0)


   algorithms.eaMuPlusLambda(pop, toolbox, mu=100, lambda_=200, cxpb=0.9, mutpb=0.1, ngen=50,
                             stats=stats, halloffame=hof, verbose=True)


   return pop, stats, hof


if __name__ == "__main__":
   main()

