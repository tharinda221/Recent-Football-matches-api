from fastapi import FastAPI
import requests
import json
from datetime import datetime, timedelta

def get_recent_football_matches():
    api_key = '74f6e505873e48f18a071a1bad783d35'  # Replace with your API key

    today = datetime.now().date()
    next_week = today + timedelta(days=7)

    url = f'https://api.football-data.org/v4/matches?dateFrom={today}&dateTo={next_week}'

    headers = {'X-Auth-Token': api_key}

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        match_list = response.json()['matches']
        matches = []
        for match in match_list:
            home_team = match['homeTeam']['name']
            away_team = match['awayTeam']['name']
            match_time = datetime.fromisoformat(match['utcDate']).strftime('%Y-%m-%d %H:%M:%S')
            match_data = {
                "homeTeam": home_team,
                "awayTeam": away_team,
                "match_time": match_time
            }
            matches.append(match_data)
        output = {"matches": matches}
        print(json.dumps(output))
        return output
    else:
        print(f"Error retrieving match data: {response.status_code}")
        return {}

app = FastAPI()


@app.get("/football-on-coming-week")
def football_on_coming_week():
    return get_recent_football_matches()