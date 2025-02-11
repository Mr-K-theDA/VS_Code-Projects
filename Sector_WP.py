import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

# Constants
FIG_SIZE = (12, 8)

st.title('Sector-wise Performance: Average Yearly Return by Sector')

# File paths
stock_file_path = r'D:\Data_Science\Project_2\combined_file.csv'
sector_file_path = r'D:\Data_Science\Project_2\sector_data.csv'

# Load stock data
stock_df = pd.read_csv(stock_file_path)

# Convert 'date' column to datetime format and extract year
stock_df['date'] = pd.to_datetime(stock_df['date'], format='%Y-%m-%d_%H-%M-%S', errors='coerce')
stock_df['date'] = stock_df['date'].dt.strftime('%Y-%m-%d')  # Convert to 'YYYY-MM-DD' format
stock_df['year'] = pd.to_datetime(stock_df['date']).dt.year

# Drop rows with invalid dates
stock_df = stock_df.dropna(subset=['date'])

# Load sector data
sector_df = pd.read_csv(sector_file_path)
sector_df['symbol'] = sector_df['symbol'].str.strip()

# Merge stock data with sector data
merged_df = pd.merge(stock_df, sector_df, on='symbol', how='inner')

#print(merged_df.head())

if 'close' not in merged_df.columns:
    raise KeyError("The 'close' column is not found in the merged data")
                   
# Calculate daily returns
merged_df['daily_return'] = merged_df.groupby('symbol')['close'].pct_change()

#print(merged_df.head())
# Calculate yearly returns
yearly_returns = merged_df.groupby(['symbol', 'year'])['daily_return'].apply(lambda x: (1 + x).prod() - 1).reset_index()

# Merge yearly returns back into merged_df
merged_df = pd.merge(merged_df, yearly_returns, on=['symbol', 'year'], how='left', suffixes=('', '_yearly'))

# Calculate average yearly return by sector
sector_performance = merged_df.groupby('sector')['daily_return_yearly'].mean().reset_index().fillna(0)

# Display sector performance in Streamlit
st.write("Sector-wise Average Yearly Return")
plt.figure(figsize=FIG_SIZE)

# Plot the bar chart
plt.bar(sector_performance['sector'], sector_performance['daily_return_yearly'], color='skyblue')
plt.title('Average Yearly Return by Sector')
plt.xlabel('Sector')
plt.ylabel('Average Yearly Return')
plt.xticks(rotation=45)
plt.tight_layout()

# Show the plot in Streamlit
st.pyplot(plt)

# Optional: Save the combined dataframe to a new CSV file
merged_df.to_csv(r'D:\Data_Science\Project_2\merged_data.csv', index=False)

# Print the first few rows to check the output
symbols = merged_df['symbol'].unique()
chunk_size = 50
for i in range(0, len(symbols), chunk_size):
    chunk_symbols = symbols[i:i + chunk_size]
    chunk_df = merged_df[merged_df['symbol'].isin(chunk_symbols)]
    chunk_performance = chunk_df.groupby('symbol')['daily_return_yearly'].mean().reset_index().fillna(0)
    st.write(f"Average Yearly Return for symbols {i+1} to {i+len(chunk_symbols)}")
    st.table(chunk_performance)
print(chunk_performance)