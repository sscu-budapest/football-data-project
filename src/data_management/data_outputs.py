from sscutils import create_trepo_with_subsets

season_coref = create_trepo_with_subsets("seasons", prefix="coref", no_subsets=True)
player_coref = create_trepo_with_subsets("players", prefix="coref", no_subsets=True)
team_coref = create_trepo_with_subsets("teams", prefix="coref", no_subsets=True)
match_coref = create_trepo_with_subsets("matches", prefix="coref", no_subsets=True)
