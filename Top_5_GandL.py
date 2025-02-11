import pandas as pd
import matplotlib.pyplot as plt
import os
import streamlit as st

st.title('Top 5 Gainers and Losers (Month-wise)')

# Load data from CSV files
csv_path = "D:/Data_Science/Project_2/csv_file"
csv_files = os.listdir(csv_path)
df_list = [pd.read_csv(os.path.join(csv_path, f)) for f in csv_files]
df = pd.concat(df_list, ignore_index=True)

# Display the first few rows of the loaded data
st.write("Sample data from loaded CSV files:")
st.dataframe(df.head())

# Rename the ticker column to symbol and ensure date column is properly formatted
df.rename(columns={'Ticker': 'symbol', 'Date': 'date', 'Close': 'close'}, inplace=True)

# Custom date parser to handle specific datetime string formats
def try_parsing_date(text):
    for fmt in ('%Y-%m-%d_%H-%M-%S', '%Y-%m-%d', '%m/%d/%Y'):
        try:
            return pd.to_datetime(text, format=fmt)
        except (ValueError, TypeError):
            continue
    return pd.NaT

df['date'] = df['date'].apply(try_parsing_date)

# Handle NaT values by filling them with the previous or next valid date
df['date'].fillna(method='ffill', inplace=True)
df['date'].fillna(method='bfill', inplace=True)

# Display the first few rows after date parsing
st.write("Data after date parsing:")
st.dataframe(df.head())

# Extract year and month from date
df['year'] = df['date'].dt.year
df['month'] = df['date'].dt.month

# Sort the DataFrame by symbol and date
df.sort_values(by=['symbol', 'date'], inplace=True)

# Calculate monthly returns
df['monthly_return'] = df.groupby(['symbol', 'year', 'month'])['close'].transform(lambda x: x.pct_change().cumsum())

# Display the first few rows after calculating monthly returns
st.write("Data after calculating monthly returns:")
st.dataframe(df.head())

# Function to plot top gainers and losers
def plot_top_gainers_and_losers(df, year, month):
    monthly_df = df[(df['year'] == year) & (df['month'] == month)]
    if monthly_df.empty:
        st.write(f"No data available for {year}-{month:02d}")
        return

    monthly_df = monthly_df.groupby('symbol')['monthly_return'].last().reset_index()
    top_gainers = monthly_df.sort_values(by='monthly_return', ascending=False).head(5)
    top_losers = monthly_df.sort_values(by='monthly_return', ascending=True).head(5)

    fig, ax = plt.subplots(1, 2, figsize=(14, 6), sharey=True)
    top_gainers.plot.bar(x='symbol', y='monthly_return', ax=ax[0], color='green', legend=False)
    top_losers.plot.bar(x='symbol', y='monthly_return', ax=ax[1], color='red', legend=False)

    ax[0].set_title(f'Top 5 Gainers - {year}-{month:02d}')
    ax[0].set_ylabel('Monthly Return')
    ax[1].set_title(f'Top 5 Losers - {year}-{month:02d}')
    fig.suptitle(f'Top 5 Gainers and Losers for {year}-{month:02d}')
    st.pyplot(fig)

# Plot for each month
for year in df['year'].unique():
    for month in range(1, 13):
        st.write(f"Processing {year}-{month:02d}...")
        plot_top_gainers_and_losers(df, year, month)
