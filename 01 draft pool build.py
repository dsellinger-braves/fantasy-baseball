
## Source URL: https://fantasy.espn.com/baseball/players/projections?leagueId=130215
## Source API: https://lm-api-reads.fantasy.espn.com/apis/v3/games/flb/seasons/2025/players?scoringPeriodId=0&view=players_wl

##Copy view from Preview into a txt file and save as player list.json
##Run this script to convert the json file to a csv file

import json
import csv

def load_local_json(filepath="C:/Users/danie/Documents/Fantasy Baseball/2025 Season/Projections/player list.json"):  # Change to your file name
    """Loads JSON data from a local file."""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data
    except FileNotFoundError:
        print(f"Error: File not found at {filepath}")
        return None
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None

def write_data_to_csv(data, filename="C:/Users/danie/Documents/Fantasy Baseball/2025 Season/Projections/espn_fantasy_players.csv"):
    """Writes JSON data directly to a CSV file."""
    if not data:
        print("No data to write to CSV.")
        return

    if isinstance(data, list) and data:  # Check if it's a list of dictionaries
        if isinstance(data[0], dict):
            fieldnames = data[0].keys()
            try:
                with open(filename, "w", newline="", encoding="utf-8") as csvfile:
                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                    writer.writeheader()
                    writer.writerows(data)
                print(f"Data written to {filename}")
            except Exception as e:
                print(f"Error writing to CSV: {e}")
        else:
            print("Data is not a list of dictionaries. Cannot write to CSV.")
    else:
        print("Data is not a list or is empty. Cannot write to CSV.")

if __name__ == "__main__":
    player_data = load_local_json("C:/Users/danie/Documents/Fantasy Baseball/2025 Season/Projections/player list.json") # change the file name here.

    if player_data:
        write_data_to_csv(player_data)
    else:
        print("Failed to load player data.")