import pandas as pd

def update_quota_column(input_csv_file, output_csv_file):
    """
    Reads a CSV file, updates the 'Quota' column by replacing 'GUJCET-Based' with 'GUJCET_Rank',
    and saves the modified data to a new CSV file.

    Args:
        input_csv_file (str): Path to the input CSV file.
        output_csv_file (str): Path to the output CSV file.
    """
    try:
        # Read the CSV file into a pandas DataFrame
        df = pd.read_csv(input_csv_file)

        # Check if the 'Quota' column exists
        if 'Quota' in df.columns:
            # Replace 'GUJCET-Based' with 'GUJCET_Rank' in the 'Quota' column
            df['Quota'] = df['Quota'].replace('GUJCET-Based', 'GUJCET_Rank')

            # Save the updated DataFrame to a new CSV file
            df.to_csv(output_csv_file, index=False)
            print(f"Successfully updated '{input_csv_file}'. The modified data is saved to '{output_csv_file}'.")
        else:
            print(f"Error: The 'Quota' column was not found in '{input_csv_file}'.")

    except FileNotFoundError:
        print(f"Error: The input file '{input_csv_file}' was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    input_file = input("Enter the path to the input CSV file: ")
    output_file = input("Enter the path for the output CSV file: ")
    update_quota_column(input_file, output_file)