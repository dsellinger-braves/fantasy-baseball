import requests

def get_player_data(league_id, team_id, scoring_period_id):
    """
    Retrieves player data from the ESPN Fantasy Baseball API and extracts specific attributes.

    Args:
        league_id (int): The ID of the fantasy league.
        team_id (int): The ID of the team.
        scoring_period_id (int): The scoring period ID.

    Returns:
        list: A list of dictionaries, where each dictionary contains player data.
              Returns None if an error occurs.
    """
    url = f"https://lm-api-reads.fantasy.espn.com/apis/v3/games/flb/seasons/2024/segments/0/leagues/{league_id}?forTeamId={team_id}&scoringPeriodId={scoring_period_id}&view=mRoster"

    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
        data = response.json()

        player_data = []
        for player in data['teams'][0]['roster']['entries']:
            player_info = {}
            player_info['onteamid'] = player['playerPoolEntry']['player']['onTeamId']
            player_info['fullName'] = player['playerPoolEntry']['player']['fullName']
            player_info['lineupSlotID'] = player['lineupSlotId']
            player_info['stats'] = {}

            for stat in player['playerPoolEntry']['player']['stats']:
                if stat.get('statSplitTypeId') == 3:
                    player_info['stats'] = stat.get('stats', {}) # get the stats dictionary.

            player_data.append(player_info)

        return player_data

    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return None
    except KeyError as e:
        print(f"Error parsing JSON: Missing key {e}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None



# Example usage:
league_id = 130215
team_id = 5
scoring_period_id = 195

player_data = get_player_data(league_id, team_id, scoring_period_id)

if player_data:
    for player in player_data:
        print(f"onteamid: {player['onteamid']}")
        print(f"fullName: {player['fullName']}")
        print(f"lineupSlotID: {player['lineupSlotID']}")
        print(f"Stats (statSplitTypeID 3): {player['stats']}")
        print("-" * 20)