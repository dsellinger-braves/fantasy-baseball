import os
import glob
import pandas as pd
import requests
import csv
import json

def api_to_csv(api_url, csv_filename="C:/Users/danie/Documents/Fantasy Baseball/2025 Season/Projections/ESPN Projection/espn_news.csv"):
    """
    Fetches data from an ESPN Fantasy API and converts it to a CSV file,
    extracting only 'fullname', 'injuryStatus', and 'injuryDetails'.

    Args:
        api_url (str): The URL of the ESPN Fantasy API.
        csv_filename (str, optional): The name of the CSV file to create. 
                                      Defaults to "espn_player_data.csv".
    """
    headers = {
    'X-Fantasy-Filter': json.dumps({
        "players": {
            "filterSlotIds": {"value": [0]},
            "filterStatsForExternalIds": {"value": [year]},
            "filterStatsForSourceIds": {"value": [1]},
            "sortAppliedStatTotal": {"sortAsc": False, "sortPriority": 3, "value": "102025"},
            "sortDraftRanks": {"sortPriority": 2, "sortAsc": True, "value": "ROTO"},
            "sortPercOwned": {"sortAsc": False, "sortPriority": 4},
            "limit": 50,
            "offset": 0,
            "filterRanksForScoringPeriodIds": {"value": [1]},
            "filterRanksForRankTypes": {"value": ["STANDARD"]},
            "filterStatsForTopScoringPeriodIds": {"value": 5, "additionalValue": ["002025", "102025", "002024", "012025", "022025", "032025", "042025", "062025", "010002025"]}
        }
    })
}
    
    try:
        response = requests.get(api_url)
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
        data = response.json()

        players = data.get("players",)

        if not players:
            print("No player data found in the API response.")
            return

        headers = ["fullname", "injuryStatus", "injuryDetails"]

        with open(csv_filename, "w", newline="", encoding="utf-8") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=headers)
            writer.writeheader()

            for player_info in players:
                player = player_info.get("player", {})
                row = {
                    "fullname": player.get("fullName"),
                    "injuryStatus": player.get("injuryStatus"),
                    "injuryDetails": player.get("injuryDetails")
                }
                writer.writerow(row)

        print(f"Data successfully written to {csv_filename}")

    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from API: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

# Example usage:
api_url = "https://lm-api-reads.fantasy.espn.com/apis/v3/games/flb/seasons/2025/segments/0/leaguedefaults/1?scoringPeriodId=0&view=kona_playercard"
api_to_csv(api_url)