import encoref.core.motif_pair_transformations as mtf
from encoref import SearchRoll


class RollCreator:
    def __init__(self, fixture_link_names, lineup_link_name_dict, comp_weights=[0.2, 0.1, 1, 0.7, 0.7]) -> None:

        self.fixture_links = fixture_link_names
        self.lineup_links_dict = lineup_link_name_dict

        self.base_comp_motif = [
            mtf.MotifExtension("season-comp", source_col=0, inverse=True),
            mtf.MotifExtension("match-season", source_col=1, inverse=True),
            *[mtf.MotifExtension(fln, source_col=2) for fln in self.fixture_links],
        ]
        self.comp_weights = comp_weights

    def get_comp_matcher_roll(self, inner_integrate=True, outer_integrate=False, cutoff=0.79):

        mm = mtf.MotifMatch(weights=self.comp_weights)

        inner_steps = (
            [mtf.IntegrateToResult(cutoff=cutoff, cols=[0], cutoff_only_end=False)] if inner_integrate else []
        )
        outer_steps = (
            [
                mm,
                mtf.IntegrateToResult(cutoff=cutoff, cols=[0]),
            ]
            if outer_integrate
            else []
        )
        return SearchRoll(
            mtf.MotifRoot("competition"),
            [
                *self.base_comp_motif,
                mtf.FilterForFree(0),
                mtf.MotifGroupbySide(
                    0,
                    apply_steps=[
                        mtf.MotifSampler(None, 10),
                        mm,
                        *inner_steps,
                    ],
                    side=1,
                ),
                *outer_steps,
            ],
        )

    def get_season_matcher_roll(self, cutoff=0.79):
        return SearchRoll(
            mtf.MotifRoot("competition"),
            [
                *self.base_comp_motif,
                mtf.FilterForFree(1),
                mtf.MotifGroupbyCorefs(
                    0,
                    apply_steps=[
                        mtf.MotifGroupbySide(
                            1,
                            apply_steps=[
                                mtf.MotifSampler(None, 10),
                                mtf.MotifMatch(weights=self.comp_weights),
                                mtf.IntegrateToResult(cutoff=cutoff, cols=[1], cutoff_only_end=False),
                            ],
                            side=1,
                        )
                    ],
                ),
            ],
        )

    def get_match_roll(self, cutoff=0.99):
        return SearchRoll(
            mtf.MotifRoot("season"),
            [
                mtf.MotifExtension("match-season", source_col=0, inverse=True),
                *[mtf.MotifExtension(lname, source_col=1) for lname in self.fixture_links],
                mtf.MotifGroupbyCorefs(
                    0,
                    apply_steps=[
                        mtf.MotifMatch(),
                        mtf.IntegrateToResult(cutoff=cutoff),
                    ],
                ),
            ],
        )

    def get_player_rolls(self, free_filter=False):
        filters = [mtf.FilterForFree(3)] if free_filter else []
        player_rolls = []
        for flink, luplinks in self.lineup_links_dict.items():
            for luplink in luplinks:
                player_rolls.append(
                    SearchRoll(
                        mtf.MotifRoot("season"),
                        [
                            mtf.MotifExtension("match-season", source_col=0, inverse=True),
                            mtf.MotifExtension(flink, source_col=1),
                            mtf.MotifExtension(luplink, source_col=1),
                            *filters,
                            mtf.MotifGroupbyCorefs(
                                col=0,
                                apply_steps=[
                                    mtf.MotifGroupbyCorefs(
                                        col=2,
                                        apply_steps=[
                                            mtf.MotifGroupbyCorefs(col=1, apply_steps=[mtf.MotifMatch()]),
                                        ],
                                    ),
                                    mtf.IntegrateToResult(cutoff=1),
                                ],
                            ),
                        ],
                    )
                )
        return player_rolls


def get_rolls(fixture_link_names, lineup_link_names):

    rc = RollCreator(fixture_link_names, lineup_link_names)

    return [
        rc.get_comp_matcher_roll(inner_integrate=False, outer_integrate=True, cutoff=0.3),  # 0.3
        rc.get_comp_matcher_roll(inner_integrate=True, outer_integrate=False, cutoff=0.79),  # 0.79
        rc.get_season_matcher_roll(cutoff=0.6),
        rc.get_season_matcher_roll(cutoff=0.79),
        rc.get_match_roll(),
        rc.get_match_roll(0.8),
        *rc.get_player_rolls(),
        *rc.get_player_rolls(free_filter=True),
    ]
