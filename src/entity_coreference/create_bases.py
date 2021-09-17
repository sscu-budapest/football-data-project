import numpy as np
import pandas as pd
from colassigner import ColAssigner

from ..data_management import fe_raw_cols as fe_rc
from ..data_management import fe_trepos as fe_t2
from ..data_management import pv_raw_cols as pv_rc
from ..data_management import pv_trepos as pv_t2

# manual part
start_date = pd.to_datetime(["2011-06-01"]).astype(int)[0]

fe_team_replacement_dic = {82: 24341}
fe_player_replacement_dic = {27800: 312814, 322402: 344042, 135468: 229172}


class CorefCols(ColAssigner):
    def __init__(self, pvsdf):
        super().__init__()
        self.pv_season_df = pvsdf

    def comp_type(self, df):
        return np.where(
            self.pv_season_df.reindex(df[pv_rc.CommonCols.season_id])[pv_rc.SeasonInfoCols.season_type].str.contains(
                "pokal"
            ),
            "cup",
            "league",
        )


def correct_height(s):
    return np.where(s > 130, s, s.median())


def correct_dob(s):
    allowed = pd.to_datetime(["1950-01-01", "2020-01-01"]).astype(int)
    return np.where((s > allowed[0]) & (s < allowed[1]), s, s.median())


def get_pv_season_id(df):
    return df[pv_rc.CommonCols.competition_id] + "-" + df[pv_rc.CommonCols.season_year_id]


def get_fe_bases():
    team_df = fe_t2.teams_table.get_full_df().drop(fe_team_replacement_dic.keys(), errors="ignore")

    match_df = (
        fe_t2.matches_table.get_full_df()
        .assign(
            date=lambda df: pd.to_datetime(df[fe_rc.MatchesCols.datetime]).astype(np.int64),
            home_teamid=lambda df: df[fe_rc.MatchesCols.TeamId.home].replace(fe_team_replacement_dic),
            away_teamid=lambda df: df[fe_rc.MatchesCols.TeamId.away].replace(fe_team_replacement_dic),
        )
        .loc[lambda df: df["date"] > start_date]
    )

    season_df = fe_t2.seasons_table.get_full_df().assign(
        name=lambda df: df[fe_rc.SeasonsCols.competition_name],
        fe_comp_uid=lambda df: df[fe_rc.CommonCols.area_name] + " " + df["name"],
    )

    comp_df = season_df.groupby("fe_comp_uid")[[fe_rc.CommonCols.area_name]].first()

    lineup_df = fe_t2.lineups_table.get_full_df().assign(
        starter=lambda df: np.where(df[fe_rc.LineupsCols.position] == "Sub", "sub", "starter"),
        fe_player_id=lambda df: df[fe_rc.CommonCols.player_id].replace(fe_player_replacement_dic),
    )

    player_df = (
        fe_t2.players_table.get_full_df()
        .drop(fe_player_replacement_dic.keys(), errors="ignore")
        .assign(
            dob=lambda pdf: lineup_df.merge(match_df.loc[:, ["date"]].reset_index(), how="inner")
            .assign(dob=lambda df: df["date"] - df[fe_rc.LineupsCols.age] * 365 * 24 * 60 * 60 * 10 ** 9)
            .groupby("fe_player_id")["dob"]
            .mean()
            .reindex(pdf.index)
            .pipe(correct_dob),
            height=lambda df: df[fe_rc.PlayersCols.height].pipe(correct_height),
        )
        .loc[:, [fe_rc.PlayersCols.name, "height", "dob"]]
    )
    return comp_df, season_df, match_df, player_df, team_df, lineup_df


def get_pv_bases():
    country_df = pv_t2.countries_table.get_full_df()
    match_df = (
        pv_t2.match_info_table.get_full_df()
        .assign(
            **{
                pv_rc.CommonCols.season_id: get_pv_season_id,
                "date": lambda df: pd.to_datetime(df[pv_rc.MatchInfoCols.date]).astype(np.int64),
            }
        )
        .loc[lambda df: df["date"] > start_date]
    )

    season_df = pv_t2.seasons_table.get_full_df()
    team_df = (
        pv_t2.team_info_table.get_full_df()
        .assign(
            country=lambda df: pv_t2.countries_table.get_full_df()
            .reindex(df[pv_rc.CommonCols.country_id])[pv_rc.CountriesCols.country_name]
            .fillna("N/A")
            .values
        )
        .loc[:, [pv_rc.TeamInfoCols.name, "country"]]
    )
    lineup_df = pv_t2.match_lineups_table.get_full_df()

    player_df = (
        pv_t2.player_info_table.get_full_df()
        .assign(
            dob=lambda df: pd.to_datetime(df[pv_rc.PlayerInfoCols.date_of_birth])
            .pipe(lambda s: s.fillna(s.mean()))
            .astype(int)
            .pipe(correct_dob),
            height=lambda df: df[pv_rc.PlayerInfoCols.height].pipe(correct_height),
        )
        .loc[:, [pv_rc.PlayerInfoCols.player_name, "height", "dob"]]
    )

    comp_df = (
        season_df.groupby(pv_rc.CommonCols.competition_id)[[pv_rc.CommonCols.country_id]]
        .first()
        .assign(
            area=lambda df: country_df[pv_rc.CountriesCols.country_name]
            .reindex(df[pv_rc.CommonCols.country_id].values)
            .values
        )
        .drop(pv_rc.CommonCols.country_id, axis=1)
        .fillna("International")
    )

    return comp_df, season_df, match_df, player_df, team_df, lineup_df
