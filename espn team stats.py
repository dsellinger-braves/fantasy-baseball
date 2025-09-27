import requests
import json
import csv
import os

def get_espn_fantasy_data(league_id, team_id, season=2025):

    url = f"https://lm-api-reads.fantasy.espn.com/apis/v3/games/flb/seasons/{season}/segments/0/leagues/{league_id}?rosterForTeamId={team_id}&view=mDraftDetail&view=mLiveScoring&view=mMatchupScore&view=mPendingTransactions&view=mPositionalRatings&view=mRoster&view=mSettings&view=mTeam&view=modular&view=mNav"


    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)
        data = response.json()
        return data

    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from ESPN API: {e}")
        if response.status_code != 200: #Print the status code if it's not successful
            print(f"Status Code: {response.status_code}")
        if response.text: #Print the response text, which may contain more error info
            try:
                error_data = response.json() #Try to decode as JSON to print a more useful error message
                print(f"Response Body: {json.dumps(error_data, indent=4)}")
            except json.JSONDecodeError: #If not JSON, just print the raw text
                print(f"Response Body: {response.text}")

        return None
    except json.JSONDecodeError as e:
      print(f"Error decoding JSON response: {e}")
      print(f"Raw Response Text: {response.text}") #Print the raw text so we can see what's going on
      return None

