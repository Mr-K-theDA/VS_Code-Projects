import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import streamlit as st

st.title('Volatility Analysis of Stocks')

# Load data from CSV files
csv_path = "D:/Data_Science/Project_2/csv_file"
csv_files = os.listdir(csv_path)
df_list = [pd.read_csv(os.path.join(csv_path, f)) for f in csv_files]
df = pd.concat(df_list, ignore_index=True)

# Rename the ticker column to symbol
df.rename(columns={'Ticker': 'symbol'}, inplace=True)

# Sort the DataFrame by symbol and date
df.sort_values(by=['symbol', 'date'], inplace=True)

# Calculate daily returns
df['daily_return'] = df.groupby('symbol')['close'].pct_change()

# Calculate the standard deviation of daily returns (volatility) for each stock
volatility = df.groupby('symbol')['daily_return'].std().reset_index()
volatility.rename(columns={'daily_return': 'volatility'}, inplace=True)

# Interactive slider to select the number of top volatile stocks
num_stocks = st.slider('Select the number of top volatile stocks to display:', min_value=1, max_value=20, value=10)

# Get the top N most volatile stocks based on user input
top_volatile_stocks = volatility.sort_values(by='volatility', ascending=False).head(num_stocks)

# Filter the original DataFrame to include only the selected top volatile stocks
top_volatile_symbols = top_volatile_stocks['symbol'].tolist()
df_top_volatile = df[df['symbol'].isin(top_volatile_symbols)]

# Recalculate daily returns for the selected top volatile stocks
df_top_volatile['daily_return'] = df_top_volatile.groupby('symbol')['close'].pct_change()

# Define custom colors for the top 3 volatile stocks
colors = ['#1f77b4', '#ff7f0e', '#2ca02c'] + ['#d62728'] * (len(top_volatile_stocks) - 3)

# Add a new column for color mapping
top_volatile_stocks['color'] = colors

# Plotting the selected Top N Most Volatile Stocks
plt.figure(figsize=(12, 8))
sns.barplot(x='symbol', y='volatility', data=top_volatile_stocks, palette=top_volatile_stocks['color'].tolist())
plt.title(f'Top {num_stocks} Most Volatile Stocks')
plt.xlabel('Stock Ticker')
plt.ylabel('Volatility (Standard Deviation of Daily Returns)')

# Show the plot in Streamlit
st.pyplot(plt)

# Display the selected top N most volatile stocks
st.write(f"Top {num_stocks} Most Volatile Stocks")
st.dataframe(top_volatile_stocks)

# Calculate and display daily returns for the selected top volatile stocks
st.write(f"Daily Returns for Top {num_stocks} Most Volatile Stocks")
daily_returns_top_volatile = df_top_volatile[['symbol', 'date', 'daily_return']].dropna()
st.dataframe(daily_returns_top_volatile)
