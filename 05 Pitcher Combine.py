import os
import glob
import pandas as pd

def combine_csvs(folder):
    """Combines all CSV files in the specified folder into a single CSV, de-duplicating the data."""

    try:
        # Use glob to find all CSV files in the folder
        csv_files = glob.glob(os.path.join(folder, "*.csv"))

        if not csv_files:
            print(f"No CSV files found in {folder}")
            return

        all_data = []  # List to hold all dataframes

        for file in csv_files:
            try:
                df = pd.read_csv(file)  # Read each CSV into a DataFrame
                all_data.append(df)
                print(f"Successfully read {file}")  # helpful progress output

            except pd.errors.EmptyDataError:  # Handle empty files
                print(f"Warning: {file} is empty and will be skipped.")
            except pd.errors.ParserError as e:  # Handle parsing errors
                print(f"Error parsing {file}: {e}. This file will be skipped.")
            except Exception as e:  # Catch any other potential errors during reading
                print(f"Error reading {file}: {e}. This file will be skipped.")

        if all_data:  # Check if any data was successfully read
            combined_df = pd.concat(all_data, ignore_index=True)  # Combine all dataframes
            
            # De-duplication step:
            combined_df = combined_df.drop_duplicates() #remove duplicate rows
            
            output_filename = "combined_espn_pitcher_data.csv"
            output_path = os.path.join(folder, output_filename)

            combined_df.to_csv(output_path, index=False, encoding='utf-8')  # Save combined data
            print(f"Combined and de-duplicated data saved to {output_path}")
        else:
            print("No data could be read from any CSV files.")

    except FileNotFoundError:
        print(f"Error: Folder {folder} not found.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

# Example usage:
folder_path = "C:/Users/danie/Documents/Fantasy Baseball/2025 Season/Projections/ESPN Projection/Pitchers"
combine_csvs(folder_path)