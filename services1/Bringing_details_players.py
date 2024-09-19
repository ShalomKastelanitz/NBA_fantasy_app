import requests

# פונקציה להבאת נתונים מה-API עבור עונה מסוימת
def fetch_data(season):
    url = f"http://b8c40s8.143.198.70.30.sslip.io/api/PlayerDataTotals/query?season={season}&pageSize=1000"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch data for season {season}")
        return None

# חישוב ATR - יחס אסיסטים לאיבודי כדור
def calculate_atr(assists, turnovers):
    if turnovers == 0:
        return assists  # הימנעות מחלוקה ב-0
    return assists / turnovers

# חישוב PPG Ratio - יחס נקודות למשחק
def calculate_ppg_ratio(points, games):
    if games == 0:
        return 0
    return points / games

# חישוב אחוז קליעה לשתיים או לשלוש
def calculate_percentage(made, attempts):
    if attempts == 0:
        return 0
    return (made / attempts) * 100

# פונקציה לאיסוף ועיבוד הנתונים מהעונות השונות
def fetch_and_process_data():
    seasons = [2022, 2023, 2024]
    data = {}

    for season in seasons:
        season_data = fetch_data(season)
        if season_data:
            for player_data in season_data:
                player_id = player_data['playerId']  # נניח שיש לך מזהה ייחודי לשחקן

                if player_id in data:
                    # הוספת עונה אם היא לא קיימת ברשימה
                    if season not in data[player_id]['seasons']:
                        data[player_id]['seasons'].append(season)
                    # עדכון נתונים סה"כ
                    data[player_id]['total_points'] += player_data.get('points', 0)
                    data[player_id]['total_games'] += player_data.get('games', 0)
                else:
                    # יצירת נתונים חדשים לשחקן
                    data[player_id] = {
                        'name': player_data['playerName'],
                        'position': player_data['position'],
                        'team': player_data['team'],
                        'seasons': [season],
                        'total_points': player_data.get('points', 0),
                        'total_games': player_data.get('games', 0),
                        'atr': calculate_atr(player_data.get('assists', 0), player_data.get('turnovers', 0)),
                        'two_percent': calculate_percentage(player_data.get('twoFg', 0),
                                                            player_data.get('twoAttempts', 0)),
                        'three_percent': calculate_percentage(player_data.get('threeFg', 0),
                                                              player_data.get('threeAttempts', 0))
                    }

    # עיבוד PPG Ratio בסוף התהליך לאחר חישוב כל העונות
    for player_id, player in data.items():
        player['ppg_ratio'] = calculate_ppg_ratio(player['total_points'], player['total_games'])

    return list(data.values())
