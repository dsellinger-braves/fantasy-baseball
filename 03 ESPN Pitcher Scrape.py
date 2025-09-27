import requests
import json
import csv
import os

positions = [13,14,15]
limit = 50
offsets = [0, 50, 100, 150, 200]
year = 2025

# positions = [13]
# limit = 50
# offsets = [0]

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

url = 'https://lm-api-reads.fantasy.espn.com/apis/v3/games/flb/seasons/2025/segments/0/leaguedefaults/1?scoringPeriodId=0&view=kona_player_info'
url2 = 'https://lm-api-reads.fantasy.espn.com/apis/v3/games/flb/seasons/2025/segments/0/leaguedefaults/1?scoringPeriodId=0&view=kona_playercard'  
url3 = 'https://site.api.espn.com/apis/fantasy/v3/games/flb/news/players?days=30&playerId=31097'

def export_players_to_csv(players, filename, folder):
    if not players:
        print("No player data to export.")
        return

    filepath = os.path.join(folder, filename)

    try:
        os.makedirs(folder, exist_ok=True)

        with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = players[0].keys() if players else []
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            writer.writerows(players)

        print(f"Player stats exported to {filepath}")

    except Exception as e:
        print(f"Error exporting to CSV: {e}")


try:
    for offset in offsets:
        for position in positions:
            headers['X-Fantasy-Filter'] = json.dumps({
                "players": {
                    "filterSlotIds": {"value": [position]},
                    "filterStatsForExternalIds": {"value": [year]},
                    "filterStatsForSourceIds": {"value": [1]},
                    "sortAppliedStatTotal": {"sortAsc": False, "sortPriority": 3, "value": "102025"},
                    "sortDraftRanks": {"sortPriority": 2, "sortAsc": True, "value": "ROTO"},
                    "sortPercOwned": {"sortAsc": False, "sortPriority": 4},
                    "limit": 50,
                    "offset": offset,
                    "filterRanksForScoringPeriodIds": {"value": [1]},
                    "filterRanksForRankTypes": {"value": ["STANDARD"]},
                    "filterStatsForTopScoringPeriodIds": {"value": 5, "additionalValue": ["002025", "102025", "002024", "012025", "022025", "032025", "042025", "062025", "010002025"]}
                }
            })

            response = requests.get(url, headers=headers)
            response.raise_for_status()
            jsonData = response.json()

            players = jsonData.get('players', [])

            if players:
                player_stats_list = []
                for player in players:
                    try:
                        player_stats = {
                            "player_id": player.get('id'),
                            "first_name": player.get('player', {}).get('firstName'),
                            "last_name": player.get('player', {}).get('lastName'),
                            "player_name":player.get('player', {}).get('firstName') + " " + player.get('player', {}).get('lastName'),
                            "injured_status": player.get('player', {}).get('injuryStatus'),
                            "team_id": player.get('player', {}).get('proTeamId'),
                            "position_id": player.get('player', {}).get('defaultPositionId'),
                            "eligible": player.get('player', {}).get('eligibleSlots'),
                            "rank":player.get('player',{}).get('draftRanksByRankType',{}).get('ROTO',{}).get('rank'),
                            "average_draft_position": player.get('player', {}).get('ownership', {}).get('averageDraftPosition'),
                            "adp_change": player.get('player', {}).get('ownership', {}).get('averageDraftPositionPercentChange'),
                            "percentOwned": player.get('player', {}).get('ownership', {}).get('percentOwned'),
                            "percentStarted": player.get('player', {}).get('ownership', {}).get('percentStarted'),
                            "percentOwnedChange": player.get('player', {}).get('ownership', {}).get('percentChange'),
                            "seasonOutlook": player.get('player', {}).get('seasonOutlook'),
                            str(year-1)+"rating": player.get('ratings', {}).get('0',{}).get('totalRating'),
                            str(year-1)+"total_rank": player.get('ratings', {}).get('0',{}).get('totalRanking'),
                            str(year-1)+"positional_rank": player.get('ratings', {}).get('0',{}).get('positionalRanking'),
                            "IP": player.get('player',{}).get('stats',{})[0].get('stats',{}).get('34')/3,
                            "QS": player.get('player',{}).get('stats',{})[0].get('stats',{}).get('63'),
                            "ERA": (player.get('player',{}).get('stats',{})[0].get('stats',{}).get('45'))/(player.get('player',{}).get('stats',{})[0].get('stats',{}).get('34')/3)*9,
                            "WHIP": (player.get('player',{}).get('stats',{})[0].get('stats',{}).get('37')+player.get('player',{}).get('stats',{})[0].get('stats',{}).get('39'))/(player.get('player',{}).get('stats',{})[0].get('stats',{}).get('34'))/3*9,
                            "K": player.get('player',{}).get('stats',{})[0].get('stats',{}).get('48')}
                            #"SV+HDs": player.get('player',{}).get('stats',{})[0].get('stats',{}).get('57')+player.get('player',{}).get('stats',{})[0].get('stats',{}).get('60')
                        stats = player.get('player', {}).get('stats', {})
                        if stats and stats[0] and stats[0].get('stats'):
                                sv = stats[0]['stats'].get('57')
                                hds = stats[0]['stats'].get('60')
                                if sv is not None and hds is not None:
                                    player_stats["SV+HDs"] = sv + hds
                                elif hds is not None:
                                        player_stats["SV+HDs"] = hds
                                elif sv is not None:
                                        player_stats["SV+HDs"] = sv
                                else:
                                        player_stats["SV+HDs"]= None
                      
                        
                        player_stats_list.append(player_stats)
                    except (IndexError, TypeError, AttributeError) as e:
                        print(f"Error processing player {player.get('id', 'Unknown')}: {e}")
                        # Optional: continue

                filename = f"espn_player_stats_pos{position}_offset{offset}.csv"
                export_players_to_csv(player_stats_list, filename, "C:/Users/danie/Documents/Fantasy Baseball/2025 Season/Projections/ESPN Projection/Pitchers")
                print(f"Processed position {position}, offset {offset}")
                # print(player_stats_list)

            else:
                print(f"No player data found for position {position}, offset {offset}")

except requests.exceptions.RequestException as e:
    print(f"Error: {e}")
except json.JSONDecodeError as e:
    print(f"Error decoding JSON: {e}")
except Exception as e:
    print(f"An unexpected error occurred: {e}")