import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

def load_and_process_data():
    # Load data
    df = pd.read_csv(r'D:\Data_Science\Project_2\updated_stock_df.csv')
    
    # Display data info for debugging
    st.write("Available columns:", df.columns.tolist())
    st.write("Sample data:", df.head())
    
    # Get actual stock columns (excluding date/time columns)
    stock_columns = df.select_dtypes(include=['float64', 'int64']).columns
    return df[stock_columns]

def plot_correlation(data):
    # Calculate correlation
    correlation_matrix = data.corr()
    
    # Create figure
    fig, ax = plt.subplots(figsize=(12, 8))
    sns.heatmap(correlation_matrix, 
                annot=True,
                cmap='coolwarm',
                fmt='.2f',
                linewidths=0.5)
    plt.title('Stock Price Correlation Heatmap')
    return fig

def main():
    st.title('Stock Price Correlation Analysis')
    
    # Load and process data
    stock_data = load_and_process_data()
    
    # Create and display correlation matrix
    st.subheader("Correlation Matrix")
    st.dataframe(stock_data.corr())
    
    # Create and display heatmap
    fig = plot_correlation(stock_data)
    st.pyplot(fig)

if __name__ == "__main__":
    main()