from colassigner import ColAccessor


class CommonCols(ColAccessor):
    _prefix = "pv"

    country_id = "country_id"
    player_id = "player_id"
    season_id = "season_id"
    season_year_id = "season_year"
    competition_id = "competition_id"
    match_id = "match_id"
    team_id = "team_id"
    transfer_id = "transfer_id"
    valuation_id = "valuation_id"


class CountriesCols(ColAccessor):
    country_name = "country_name"
    continent_name = "continent_name"


class PlayerInfoCols(ColAccessor):
    player_name = "player_name"
    preferred_foot = "preferred_foot"
    place_of_birth = "place_of_birth"
    broad_position = "broad_position"
    specific_position = "specific_position"
    date_of_birth = "date_of_birth"
    national_team_name = "national_team_name"
    national_team_nation = "national_team_nation"
    national_app_kind = "national_app_kind"
    place_of_birth_country = "place_of_birth_country"
    citizenship_1 = "citizenship_1"
    citizenship_2 = "citizenship_2"
    full_name = "full_name"
    height = "height"


class SeasonInfoCols(ColAccessor):
    season_type = "season_type"
    competition_name = "competition_name"
    country = "country"


class MatchInfoCols(ColAccessor):
    score = "score"
    date = "date"

    class TeamId(ColAccessor):
        _prefix = CommonCols.team_id

        home = "home"
        away = "away"

    class TeamName(TeamId):
        _prefix = "team_name"


class PlayerTransfersCols(ColAccessor):
    date = "date"
    is_loan = "is_loan"
    is_end_of_loan = "is_end_of_loan"
    transfer_fee = "transfer_fee"

    class TeamId(ColAccessor):
        _prefix = CommonCols.team_id

        left = "left"
        joined = "joined"


class TeamInfoCols(ColAccessor):
    name = "name"
    founded = "founded"
    stadium = "stadium"
    members = "members"
    mean_age = "mean_age"
    address = "address"
    squad_size = "squad_size"


class MatchLineupsCols(ColAccessor):
    side = "side"
    starter = "starter"
    player_country = "player_country"
    player_name = "player_name"


class PlayerValuesCols(ColAccessor):
    date = "date"
    value = "value"


class TeamRelationsCols(ColAccessor):
    team_name_child = "team_name__child"

    class TeamId(ColAccessor):
        _prefix = CommonCols.team_id

        child = "child"
        parent = "parent"
