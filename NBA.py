from nba_api.stats.endpoints import shotchartdetail
from nba_api.stats.static import players
import pandas as pd
import time

# ✅ Target player names (must match NBA API exactly)
nba_player_names = [
    "Shai Gilgeous-Alexander",
    "Jayson Tatum",
    "Luka Dončić",
    "Giannis Antetokounmpo",
    "Nikola Jokić"
]

# 📅 Seasons to pull
nba_season_labels = [
    "2019-20", "2020-21", "2021-22", "2022-23", "2023-24", "2024-25"
]

# 🔍 Get all active NBA players
nba_players = players.get_active_players()

# 🎯 Filter only the players you want
filtered_players = [p for p in nba_players if p['full_name'] in nba_player_names]

# 📦 Initialize container
all_shots_df = pd.DataFrame()

# 🔁 Loop through players and seasons
for player in filtered_players:
    player_id = player['id']
    player_name = player['full_name']

    for season in nba_season_labels:
        try:
            # 📊 Pull shot chart data
            shot_chart = shotchartdetail.ShotChartDetail(
                team_id=0,
                player_id=player_id,
                season_type_all_star='Regular Season',
                season_nullable=season,
                context_measure_simple='FGA'
            )

            shot_chart_data = shot_chart.get_data_frames()[0]

            if not shot_chart_data.empty:
                shot_chart_data['player_name'] = player_name
                shot_chart_data['player_id'] = player_id
                shot_chart_data['season'] = season
                all_shots_df = pd.concat([all_shots_df, shot_chart_data], ignore_index=True)
                print(f"✅ {player_name} ({season}) added")
            else:
                print(f"⚠️ No data for {player_name} ({season})")

            time.sleep(1)

        except Exception as e:
            print(f"❌ Error for {player_name} ({season}): {e}")
            time.sleep(1.5)

# 👀 Display or export
# Export full dataset to CSV
all_shots_df.to_csv("multi_season_shot_data.csv", index=False)
print("✅ Data exported to multi_season_shot_data.csv")
#print(all_shots_df.columns)
#print(all_shots_df.tail(20))
#print(all_shots_df[['player_name', 'season', 'GAME_DATE', 'SHOT_ZONE_BASIC', 'SHOT_DISTANCE', 'SHOT_MADE_FLAG']].head(10))
# all_shots_df.to_csv("multi_season_shot_data.csv", index=False)
