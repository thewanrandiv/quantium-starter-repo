import pandas as pd
import glob
import os

# Find all CSV files in the data folder
csv_files = glob.glob('*.csv')

if not csv_files:
    print("No CSV files found in the data folder!")
    print("Please ensure the CSV files are in a 'data' folder in the same directory as this script.")
else:
    print(f"Found {len(csv_files)} CSV file(s): {csv_files}")

# Initialize an empty list to store dataframes
all_data = []

# Process each CSV file
for file in csv_files:
    print(f"\nProcessing {file}...")
    
    # Read the CSV file
    df = pd.read_csv(file)
    
    # Display the first few rows to understand the structure
    print(f"Original data shape: {df.shape}")
    print(f"Columns: {df.columns.tolist()}")
    
    # Strip whitespace from column names (CSVs can be finicky)
    df.columns = df.columns.str.strip()
    
    # Filter for Pink Morsels only
    df_pink = df[df['product'].str.strip() == 'Pink Morsels'].copy()
    print(f"Pink Morsels rows: {len(df_pink)}")
    
    # Calculate sales (quantity * price)
    df_pink['sales'] = df_pink['quantity'] * df_pink['price']
    
    # Select only the required columns
    df_formatted = df_pink[['sales', 'date', 'region']].copy()
    
    # Rename columns to match the required format (capitalize first letter)
    df_formatted.columns = ['Sales', 'Date', 'Region']
    
    # Add to our list
    all_data.append(df_formatted)

# Combine all dataframes
if all_data:
    combined_df = pd.concat(all_data, ignore_index=True)
    
    print(f"\n{'='*50}")
    print(f"Combined data shape: {combined_df.shape}")
    print(f"\nFirst few rows of combined data:")
    print(combined_df.head(10))
    
    print(f"\nSummary statistics:")
    print(combined_df.describe())
    
    # Save to output file
    output_file = 'pink_morsels_sales.csv'
    combined_df.to_csv(output_file, index=False)
    print(f"\n✓ Data successfully saved to '{output_file}'")
    print(f"Total rows in output: {len(combined_df)}")
else:
    print("\nNo data to process!")