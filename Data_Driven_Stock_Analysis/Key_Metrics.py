import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Load data from CSV files
csv_path = "D:/Data_Science/Project_2/csv_file"
csv_files = os.listdir(csv_path)
df_list = [pd.read_csv(os.path.join(csv_path, f)) for f in csv_files]
df = pd.concat(df_list, ignore_index=True)

# Rename the ticker column to symbol
df.rename(columns={'Ticker': 'symbol'}, inplace=True)

# Calculate yearly return with actual column names (assuming 'close' and 'open' are correct)
df['yearly_return'] = (df['close'] - df['open']) / df['open']

# Market Summary
num_green_stocks = (df['yearly_return'] > 0).sum()
num_red_stocks = (df['yearly_return'] <= 0).sum()
average_price = df['close'].mean()
average_volume = df['volume'].mean()

# Top Green and Red Stocks
top_n = 10
top_green_stocks = df.sort_values(by='yearly_return', ascending=False).head(top_n)
top_red_stocks = df.sort_values(by='yearly_return').head(top_n)

# Define custom colors for the top 3 green stocks
green_colors = ['#1f77b4', '#ff7f0e', '#2ca02c'] + ['#d62728'] * (len(top_green_stocks) - 3)

# Define custom colors for the top 3 red stocks
red_colors = ['#1f77b4', '#ff7f0e', '#2ca02c'] + ['#d62728'] * (len(top_red_stocks) - 3)

# Plotting the Top Green and Red Stocks
fig, axes = plt.subplots(2, 1, figsize=(12, 14))

# Plot Top Green Stocks
sns.barplot(x='symbol', y='yearly_return', data=top_green_stocks, palette=green_colors, ci=None, ax=axes[0])
axes[0].set_title(f'Top {top_n} Green Stocks')

# Plot Top Red Stocks
sns.barplot(x='symbol', y='yearly_return', data=top_red_stocks, palette=red_colors, ci=None, ax=axes[1])
axes[1].set_title(f'Top {top_n} Red Stocks')

# Add market summary to the plot
fig.text(0.1, 0.01, f'Market Summary:\nNumber of Green Stocks: {num_green_stocks}\nNumber of Red Stocks: {num_red_stocks}\nAverage Price: {average_price:.2f}\nAverage Volume: {average_volume:.2f}', 
         fontsize=12, bbox=dict(facecolor='lightgrey', alpha=0.5))

plt.tight_layout()
plt.show()
