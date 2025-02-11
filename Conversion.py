import yaml
import pandas as pd
import os

# Function to read YAML data and transform it into CSV
def yaml_to_csv(yaml_folder, output_folder):
    all_data = []
    missing_ticker_files = []

    for month_dir in os.listdir(yaml_folder):
        month_path = os.path.join(yaml_folder, month_dir)
        if os.path.isdir(month_path):
            for date_file in os.listdir(month_path):
                if date_file.endswith('.yaml'):
                    file_path = os.path.join(month_path, date_file)
                    with open(file_path, 'r') as f:
                        try:
                            data = yaml.safe_load(f)
                            if isinstance(data, list):
                                for entry in data:
                                    if 'Ticker' in entry:
                                        entry['Ticker'] = entry.pop('Ticker')  # Keep 'Ticker' as is
                                        entry['date'] = date_file.split('.')[0]  # Add date info from filename
                                        entry['month'] = month_dir  # Add month info from directory name
                                        all_data.append(entry)
                                    else:
                                        missing_ticker_files.append(file_path)
                            else:
                                print(f"Unexpected data structure in {file_path}")
                        except Exception as e:
                            print(f"Error reading {file_path}: {e}")

    # Log files that are missing the 'Ticker' key
    if missing_ticker_files:
        print("Files missing 'Ticker' key:")
        for file in missing_ticker_files:
            print(file)
    else:
        print("All files contain 'Ticker' key.")

    # Transform data to DataFrame
    df = pd.DataFrame(all_data)
    print("DataFrame Structure:")
    print(df.head())  # Print first few rows of the DataFrame to inspect

    # Save DataFrame to CSV files organized by Tick
    if 'Ticker' in df.columns:
        for ticker in df['Ticker'].unique():
            ticker_data = df[df['Ticker'] == ticker]
            ticker_data.to_csv(os.path.join(output_folder, f'{ticker}.csv'), index=False)
    else:
        print("Error: 'Ticker' key not found in the DataFrame.")

yaml_to_csv(r"D:\\Data_Science\\Project_2\\yaml_file", r"D:\\Data_Science\\Project_2\\csv_file")
