import pandas as pd
from colassigner.core import allcols
from encoref import CoReferenceLock, EntitySetPair, RelationPair

from ..constants import sides
from ..data_management import fe_raw_cols as fe_rc
from ..data_management import fe_trepos as fe_t2
from ..data_management import pv_raw_cols as pv_rc
from ..data_management import pv_trepos as pv_t2
from ..data_management.data_outputs import (
    match_coref,
    player_coref,
    season_coref,
    team_coref,
)
from ..pipereg import pipereg
from .create_bases import CorefCols, get_fe_bases, get_pv_bases
from .create_rolls import get_rolls


@pipereg.register(
    outputs=[season_coref, player_coref, team_coref, match_coref],
    dependencies=[
        fe_t2.teams_table,
        fe_t2.matches_table,
        fe_t2.seasons_table,
        fe_t2.lineups_table,
        fe_t2.players_table,
        pv_t2.countries_table,
        pv_t2.player_info_table,
        pv_t2.match_info_table,
        pv_t2.seasons_table,
        pv_t2.team_info_table,
        pv_t2.match_lineups_table,
        get_rolls,
        get_fe_bases,
    ],
)
def run_entity_coreference():

    (
        fe_comp_df,
        fe_season_df,
        fe_match_df,
        fe_player_df,
        fe_team_df,
        fe_lineup_df,
    ) = get_fe_bases()
    (
        pv_comp_df,
        pv_season_df,
        pv_match_df,
        pv_player_df,
        pv_team_df,
        pv_lineup_df,
    ) = get_pv_bases()

    es_pairs = [
        EntitySetPair(
            fe_match_df.loc[:, ["score", "date"]],
            pv_match_df.loc[:, ["score", "date"]],
            "match",
        ),
        EntitySetPair(fe_team_df, pv_team_df, "team"),
        EntitySetPair(
            fe_season_df.loc[:, [fe_rc.SeasonsCols.competition_name]],
            pv_season_df.loc[:, [pv_rc.SeasonInfoCols.competition_name]],
            "season",
        ),
        EntitySetPair(fe_player_df, pv_player_df, "player"),
        EntitySetPair(fe_comp_df, pv_comp_df, "competition"),
    ]

    rel_pairs = [
        RelationPair(
            fe_match_df.loc[:, [fe_rc.CommonCols.season_id]].reset_index(),
            pv_match_df.loc[:, [pv_rc.CommonCols.season_id]].reset_index(),
            name="match-season",
            entity_types_of_columns=["match", "season"],
        ),
        RelationPair(
            fe_season_df.loc[:, fe_comp_df.index.name].reset_index(),
            pv_season_df.loc[:, pv_comp_df.index.name].reset_index(),
            name="season-comp",
            entity_types_of_columns=["season", "competition"],
        ),
    ]

    fixture_names = []
    lup_names = {}

    # here the order is assumed to be the same
    # for sides and the 2 colaccessors
    for side, fecol, pvcol in zip(sides, allcols(fe_rc.MatchesCols.TeamId), allcols(pv_rc.MatchInfoCols.TeamId)):
        name = f"match-team-{side}"
        fixture_names.append(name)
        rel_pairs.append(
            RelationPair(
                fe_match_df.loc[:, [fecol]].reset_index(),
                pv_match_df.loc[:, [pvcol]].reset_index(),
                name=name,
                entity_types_of_columns=["match", "team"],
            )
        )
        lup_names[name] = []
        for starter in ["starter", "sub"]:
            lupname = f"lup-{side}-{starter}"
            lup_names[name].append(lupname)
            rel_pairs.append(
                RelationPair(
                    fe_lineup_df.loc[
                        lambda df: (df["starter"] == starter) & (df[fe_rc.LineupsCols.side] == side),
                        [fe_rc.CommonCols.match_id, fe_rc.CommonCols.player_id],
                    ],
                    pv_lineup_df.loc[
                        lambda df: (df["starter"] == starter) & (df[pv_rc.MatchLineupsCols.side] == side),
                        [pv_rc.CommonCols.match_id, pv_rc.CommonCols.player_id],
                    ],
                    name=lupname,
                    entity_types_of_columns=["match", "player"],
                )
            )

    crl = CoReferenceLock(
        es_pairs,
        rel_pairs,
        progress_bar=True,
    )

    all_rolls = get_rolls(fixture_names, lup_names)

    crl.run_searches(all_rolls)

    (
        fe_lineup_df.assign(
            season=lambda df: fe_match_df.reindex(df[fe_rc.CommonCols.match_id])[fe_rc.CommonCols.season_id].values,
            missing=lambda df: ~df[fe_rc.CommonCols.player_id].isin(crl.results["player"][0].keys()),
        )
        .groupby("season")["missing"]
        .sum()
        .loc[lambda s: s < 6_000_001]
        .pipe(
            lambda s: pd.Series(crl.results["season"][0], name=pv_rc.CommonCols.season_id)
            .reindex(s.index)
            .reset_index()
            .rename(columns={"season": fe_rc.CommonCols.season_id})
            .assign(**CorefCols(pv_season_df))
        )
        .pipe(season_coref.replace_all)
    )

    (
        pd.DataFrame(
            crl.results["player"][0].items(),
            columns=[fe_rc.CommonCols.player_id, pv_rc.CommonCols.player_id],
        ).pipe(player_coref.replace_all)
    )

    (
        pd.DataFrame(
            crl.results["team"][0].items(),
            columns=[fe_rc.CommonCols.team_id, pv_rc.CommonCols.team_id],
        ).pipe(team_coref.replace_all)
    )

    (
        pd.DataFrame(
            crl.results["match"][0].items(),
            columns=[fe_rc.CommonCols.match_id, pv_rc.CommonCols.match_id],
        ).pipe(match_coref.replace_all)
    )
