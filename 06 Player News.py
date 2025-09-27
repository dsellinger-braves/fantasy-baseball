import requests
import json
import csv

def extract_rotowire_news(player_id, days=30):
    """
    Extracts the story and lastModified fields from Rotowire news from the ESPN API.

    Args:
        player_id (int): The player ID.
        days (int): The number of days to retrieve news for.

    Returns:
        list: A list of dictionaries, where each dictionary contains the story and
              lastModified for Rotowire news items. Returns None if there's an error.
    """
    url = f"https://site.api.espn.com/apis/fantasy/v3/games/flb/news/players?days={days}&playerId={player_id}"

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        stories = []
        if 'news' in data and 'feed' in data['news']:
            for item in data['news']['feed']:
                if isinstance(item, dict) and item.get('type') == 'Rotowire':
                    story_info = {
                        'player_id': player_id,  # Add player_id to the output
                        'headline': item.get('headline', ''),
                        'story': item.get('story', ''),
                        'lastModified': item.get('lastModified', '')
                    }
                    stories.append(story_info)
                elif isinstance(item, str):
                  print(f"Warning: String news feed item encountered: {item[:50]}...")
        return stories

    except requests.exceptions.RequestException as e:
        print(f"Error fetching data for player {player_id}: {e}")
        return None
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON for player {player_id}: {e}")
        return None
    except KeyError as e:
        print(f"Key error for player {player_id}: {e}")
        return None

def process_player_ids_from_csv(input_csv, output_csv):
    """
    Reads player IDs from a CSV, fetches Rotowire news, and writes to a new CSV.

    Args:
        input_csv (str): Path to the input CSV file containing player IDs.
        output_csv (str): Path to the output CSV file to write the news stories.
    """
    try:
        player_ids = []
        with open(input_csv, 'r') as csvfile:
            reader = csv.reader(csvfile)
            next(reader, None) #Skip the header row.
            for row in reader:
                player_ids.append(int(row[0])) #Assumes player_id is the first column.

        all_stories = []
        for player_id in player_ids:
            stories = extract_rotowire_news(player_id)
            if stories:
                all_stories.extend(stories)

        if all_stories:
            with open(output_csv, 'w', newline='', encoding='utf-8') as csvfile:
                fieldnames = ['player_id', 'headline', 'story', 'lastModified']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                for story in all_stories:
                    writer.writerow(story)
            print(f"Successfully wrote news stories to {output_csv}")
        else:
            print("No news stories found.")

    except FileNotFoundError:
        print(f"Error: Input CSV file '{input_csv}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    input_csv_file = 'C:/Users/danie/Documents/Fantasy Baseball/2025 Season/Projections/player_id_list.csv'  # Replace with your input CSV file path
    output_csv_file = 'C:/Users/danie/Documents/Fantasy Baseball/2025 Season/Projections/news_output.csv'  # Replace with your desired output CSV file path

    process_player_ids_from_csv(input_csv_file, output_csv_file)