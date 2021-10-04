# Entity Coreference

## Outline

The goal of this version of the entity coreference algorithm is to take two different source datasets which describe the same types of entities and links between them, and figure out which entity descriptions are coreferent - refer to the same real world entity. The foundation of the method is the creation of motif set pairs that are then matched based on the attributes of the entities from the two different source datasets. Using similarities between motifs, coreferent entities are established and the utilized in subsequent steps to narrow down the search when comparing other kinds of motifs to each other.

A motif set pair can be created and altered using a number of different steps:

- **take root**: takes a specific type of entity adds all of its members to both sets of motifs in the pair
- **extend**: take a specific kind of link and use it to extend both sets of motifs
- **match**: find the most similar motifs from the 2 sets and match them, matching at most one to one
  - once a match step is completed, the state of the algorithm is not simply defined by the two sets of motifs, but the relationship between them, possibly with similarity scores or orders.
- **sample**: take a sample from one or both of the motif sets
  - the sample can be random or specific, like taking all motifs that contain at least one entity that is not coreferent ot another, or just taking one motif from both sets where we know all entities are coreferent, etc...

When matching in a motif set pair, a number of factors are considered:
- similarity of attributes of entities
- have entities in the motifs already been matched to each other
- have entities in the motifs already been matched to some other entity

An additional step that alters the state of the coreference seeking system is **integrate to result**. This step does not change the motif set pair, but after the motifs from the two sets have been matched, an integration steps asserts whether entity coreferences can be established. For example if a pair of entities of the same type from the two source datasets are present in a number of matched motifs and only correspond to each other, they are likely to be coreferent and can be recorded so. This influences future motif matching steps. However if several entities from one source dataset have different corresponding entities from the other dataset based on the matched motifs, the whole state might be wrong and no coreferences should be established based on the matched motifs.


## Setup the Dataset pair

A dataset fit for this entity coreference task contains pair of table sets. Each table in the dataset has a pair corresponding

Tables of entities - with attributes in this specific case are:

- **competitions**: name (str)
- **seasons**: seasons have no attributes
- **matches**: score (str), start time (datetime)
- **teams**: name (str), country name (str)
- **players**: name (str), date of birth (str), height (float)

Links between entities are:

- seasons of competitions
- matches of seasons
- home/away team playing in a match
- home/away starter/substitute player in a match

## Creating and Matching Motifs

The steps that create transform and match motifs are intended to first find coreferent competitions and seasons, then find coreferent teams to properly find coreferent matches based on these, then find coreferent players based on all this knowledge. So the first motifs created are `competition - season - match - home_team - away_team`, then four different kinds of matches for `match - home_starter_player`, `match - home_sub_player`, `match - away_starter_player`, and `match - away_sub_player`.



All of this is implemented in the python package [encoref-v0.0.5](https://github.com/endremborza/encoref/tree/v0.0.5)

