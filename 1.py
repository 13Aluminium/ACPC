import pandas as pd
import re

def extract_city(input_file, output_file):
    # Read the CSV file
    df = pd.read_csv(input_file)
    
    # Define function to extract city from institution name
    def get_city(inst_name):
        # Look for text after comma or period
        match = re.search(r'[,.][\s]*([A-Z]+[A-Za-z\s]+)$', inst_name)
        if match:
            # Extract and clean city name
            city = match.group(1).strip()
            return city
        else:
            return "Unknown"
    
    # Apply the function to create new City column
    df['City'] = df['Inst_Name'].apply(get_city)
    
    # Save the updated dataframe to a new CSV file
    df.to_csv(output_file, index=False)
    
    print(f"Process completed successfully. Output saved to {output_file}")
    return df

# Example usage
if __name__ == "__main__":
    ip_file = input("write::::")
    input_file =   ip_file# Replace with your input file name
    output_file = ip_file + "mod.csv"  # Output file name
    
    result_df = extract_city(input_file, output_file)
    print("\nSample of processed data:")
    print(result_df[['Inst_Name', 'City']].head())