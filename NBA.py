from nba_api.stats.endpoints import shotchartdetail
from nba_api.stats.static import players
import pandas as pd

# 🔍 Get player ID from full name
def fetch_player_id(player_name_input):
    matched_players = [p for p in players.get_players() if p['full_name'] == player_name_input]
    return matched_players[0]['id'] if matched_players else None

# 📊 Get shot chart data for a player and season
def fetch_shot_data(player_name_input, season_string_input):
    player_id = fetch_player_id(player_name_input)
    if not player_id:
        print(f"❌ Player not found: {player_name_input}")
        return None
    chart = shotchartdetail.ShotChartDetail(
        team_id=0,
        player_id=player_id,
        season_type_all_star='Regular Season',
        season_nullable=season_string_input,
        context_measure_simple='FGA'
    )
    data = chart.get_data_frames()[0]
    return data

# ✅ Player names (must match NBA API exactly)
nba_player_names = [
    "Shai Gilgeous-Alexander",
    "Jayson Tatum",
    #"Luka Dončić",
    "Giannis Antetokounmpo"
    #"Nikola Jokić"

]

# 📅 Seasons to pull
nba_season_labels = [
    "2019-20", "2020-21", "2021-22", "2022-23", "2023-24", "2024-25"
]

# 📦 Collect all shot chart data
compiled_shot_data = []

for player_name in nba_player_names:
    for season_label in nba_season_labels:
        shot_data_frame = fetch_shot_data(player_name, season_label)
        if shot_data_frame is not None:
            shot_data_frame['Player'] = player_name
            shot_data_frame['Season'] = season_label
            compiled_shot_data.append(shot_data_frame)

# 🧮 Combine into one DataFrame
final_shot_data = pd.concat(compiled_shot_data, ignore_index=True)

# 💾 Optional: Save to CSV
# final_shot_data.to_csv("nba_shot_data_2019_2023.csv", index=False)

# 👀 Preview key columns
print(final_shot_data[['PLAYER_NAME', 'GAME_DATE', 'SHOT_TYPE', 'SHOT_ZONE_BASIC', 'SHOT_DISTANCE', 'SHOT_MADE_FLAG']].tail(10))