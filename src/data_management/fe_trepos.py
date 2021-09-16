from sscutils import create_trepo_with_subsets

from .fe_raw_cols import CommonCols

events_table = create_trepo_with_subsets("events", group_cols=[CommonCols.season_id], prefix="fe")
formations_table = create_trepo_with_subsets("formations", prefix="fe")
formation_use_table = create_trepo_with_subsets("formation_use", prefix="fe")
lineups_table = create_trepo_with_subsets("lineups", prefix="fe")
matches_table = create_trepo_with_subsets("matches", prefix="fe")
players_table = create_trepo_with_subsets("players", prefix="fe")
seasons_table = create_trepo_with_subsets("seasons", prefix="fe")
teams_table = create_trepo_with_subsets("teams", prefix="fe")
