from sscutils import create_trepo_with_subsets

countries_table = create_trepo_with_subsets("countries", prefix="pv")
player_info_table = create_trepo_with_subsets("player_info", prefix="pv")
seasons_table = create_trepo_with_subsets("season_info", prefix="pv")
match_info_table = create_trepo_with_subsets("match_info", prefix="pv")
player_transfers_table = create_trepo_with_subsets("player_transfers", prefix="pv")
team_info_table = create_trepo_with_subsets("team_info", prefix="pv")
match_lineups_table = create_trepo_with_subsets("match_lineups", prefix="pv")
player_values_table = create_trepo_with_subsets("player_values", prefix="pv")
team_relations_table = create_trepo_with_subsets("team_relations", prefix="pv")
