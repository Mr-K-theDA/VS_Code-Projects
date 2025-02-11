import pandas as pd
import matplotlib.pyplot as plt
import os
import streamlit as st

st.title('Cumulative Return Over the Years')

# Load data from CSV files
csv_path = "D:/Data_Science/Project_2/csv_file"
csv_files = os.listdir(csv_path)
df_list = [pd.read_csv(os.path.join(csv_path, f)) for f in csv_files]
df = pd.concat(df_list, ignore_index=True)

# Rename the ticker column to symbol and ensure date column is properly formatted
df.rename(columns={'Ticker': 'symbol', 'Date': 'date', 'Close': 'close'}, inplace=True)

# Custom date parser to handle specific datetime string formats
def custom_date_parser(date_str):
    return pd.to_datetime(date_str, format='%Y-%m-%d_%H-%M-%S', errors='coerce')

df['date'] = df['date'].apply(custom_date_parser)

# Handle NaT values by filling them with the previous or next valid date
df['date'].fillna(method='ffill', inplace=True)
df['date'].fillna(method='bfill', inplace=True)

# Extract year from date
df['year'] = df['date'].dt.year

# Sort the DataFrame by symbol and date
df.sort_values(by=['symbol', 'date'], inplace=True)

# Calculate daily returns
df['daily_return'] = df.groupby('symbol')['close'].pct_change()

# Calculate cumulative returns for each stock
df['cumulative_return'] = (1 + df['daily_return']).groupby(df['symbol']).cumprod() - 1

# Get the cumulative return at the end of each year for each stock
yearly_returns = df.groupby(['symbol', 'year'])['cumulative_return'].last().reset_index()

# Identify the top 5 performing stocks based on cumulative return for the latest year
latest_year = yearly_returns['year'].max()
top_performing_stocks = yearly_returns[yearly_returns['year'] == latest_year].sort_values(by='cumulative_return', ascending=False).head(5)

# Display the top 5 performing stocks for the latest year
st.write(f"Top 5 Performing Stocks Based on Cumulative Return for {latest_year}")
st.dataframe(top_performing_stocks)

# Filter the DataFrame to include only the top 5 performing stocks
df_top_performers = yearly_returns[yearly_returns['symbol'].isin(top_performing_stocks['symbol'])]

# Plotting the cumulative returns for the top 5 performing stocks
plt.figure(figsize=(14, 8))
for symbol in df_top_performers['symbol'].unique():
    stock_data = df_top_performers[df_top_performers['symbol'] == symbol]
    plt.plot(stock_data['year'], stock_data['cumulative_return'], label=symbol, marker='o')

plt.title('Cumulative Return for Top 5 Performing Stocks by Year')
plt.xlabel('Year')
plt.ylabel('Cumulative Return')
plt.xticks(rotation=45)  # Rotate x-axis labels for better readability
plt.legend(title='Stock Ticker', loc='best')
plt.grid(True)  # Add grid for better readability
plt.tight_layout()  # Adjust layout for better fit

# Show the plot in Streamlit
st.pyplot(plt)

# Display the cumulative returns for the top 5 performing stocks
st.write("Cumulative Returns for Top 5 Performing Stocks by Year")
st.dataframe(df_top_performers)
