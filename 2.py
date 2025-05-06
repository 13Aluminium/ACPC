import pandas as pd
import json

def extract_unique_values(input_file, output_json):
    """
    Extract unique values from each column of a CSV file (except specified columns)
    and store them in a JSON file.
    
    Args:
        input_file (str): Path to the input CSV file
        output_json (str): Path to the output JSON file
    """
    # Read the CSV file
    df = pd.read_csv(input_file)
    
    # Columns to exclude
    exclude_columns = ['Inst_Name', 'First Rank', 'Last Rank']
    
    # Dictionary to store unique values for each column
    unique_values = {}
    
    # Iterate through each column and get unique values
    for column in df.columns:
        # Skip the excluded columns
        if column in exclude_columns:
            continue
        
        # Get list of unique values for the column (convert to strings to ensure JSON compatibility)
        unique_vals = df[column].dropna().unique().tolist()
        
        # Convert any non-string values to strings
        unique_vals = [str(val) for val in unique_vals]
        
        # Add to dictionary
        unique_values[column] = unique_vals
    
    # Write to JSON file
    with open(output_json, 'w', encoding='utf-8') as f:
        json.dump(unique_values, f, indent=4)
    
    print(f"Unique values extracted and saved to {output_json}")
    
    # Return the dictionary for inspection
    return unique_values

if __name__ == "__main__":
    input_file = "final_csv/0.csv"  # Your final CSV file with city column
    output_json = "0.json"  # Output JSON file
    
    unique_values = extract_unique_values(input_file, output_json)
    
    # Print sample of the unique values
    print("\nSample of unique values extracted:")
    for column, values in list(unique_values.items())[:3]:  # Show first 3 columns
        print(f"{column}: {values[:5] if len(values) > 5 else values}")  # Show up to 5 values per column