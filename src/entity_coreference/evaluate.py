import pandas as pd

from ..data_management import fe_raw_cols as fe_rc
from ..data_management import fe_trepos as fe_t2
from ..data_management import pv_trepos as pv_t2
from ..data_management.data_outputs import (
    match_coref,
    player_coref,
    season_coref,
    team_coref,
)
from ..pipereg import pipereg
from ..report_setup import coref_eval_md


def getrate(df, match_df, prefix):
    fits = df.index.isin(match_df[df.index.name])
    return {
        f"{prefix}_fit_rate": fits.mean(),
        f"{prefix}_miss_count": (~fits).sum(),
        f"{prefix}_misses": set(df.index[~fits]),
        f"{prefix}_found": set(df.index[fits]),
    }


@pipereg.register(dependencies=[match_coref, player_coref, season_coref, team_coref], outputs_nocache=[coref_eval_md])
def evaluate_coreference():

    corefs_found_records = []
    for tr1, tr2, coref_tr in [
        (pv_t2.seasons_table, fe_t2.seasons_table, season_coref),
        (pv_t2.match_info_table, fe_t2.matches_table, match_coref),
        (pv_t2.team_info_table, fe_t2.teams_table, team_coref),
        (pv_t2.player_info_table, fe_t2.players_table, player_coref),
    ]:
        mdf = coref_tr.get_full_df()
        rec = {"name": coref_tr.name}
        for pref, tr in zip(["pv", "fe"], [tr1, tr2]):
            rec.update(tr.get_full_df().pipe(getrate, match_df=mdf, prefix=pref))
        corefs_found_records.append(rec)

    res_df = pd.DataFrame(corefs_found_records).set_index("name")

    misses = []
    miss_types = []

    for _df in fe_t2.events_table.dfs:
        miss_ind = ~(_df[fe_rc.CommonCols.player_id].dropna().astype(int).isin(res_df.loc["players", "fe_found"]))
        misses.append(
            {
                "season": _df[fe_rc.CommonCols.season_id].iloc[0],
                **miss_ind.value_counts().to_dict(),
            }
        )
        miss_types.append(
            _df.loc[miss_ind.reindex(_df.index).fillna(False), fe_rc.EventsCols.event_type].value_counts().to_dict()
        )

    md_out = tables_to_md(
        "Evaluation of Entity Coreference",
        {
            "Coreferences found and missed": res_df.loc[:, lambda df: df.dtypes != object],
            "Rates of matches": res_df.loc[:, lambda df: df.columns.str.endswith("rate")]
            .max(axis=1)
            .pipe(lambda s: (s * 100).round(2).astype(str) + "%")
            .rename("rate")
            .to_frame(),
            "Event count of missing players": pd.DataFrame(misses),
            "Missing event count by type": pd.DataFrame(miss_types).sum().to_frame(),
        },
    )

    coref_eval_md.write_text(md_out)


def tables_to_md(title, tab_dic):
    s = [f"# {title}"]
    for tab_title, df in tab_dic.items():
        s += [f"## {tab_title}", df.to_html()]
    return "\n\n".join(s)
