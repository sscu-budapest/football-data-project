# Entity Coreference

## The Concrete Task

We have player valuation with transfer history data from one source and match event data from another source, and we need to find out which records in the two different datasets describe the same player - are coreferent.

### Baseline Solution

Fuzzy matching. Use simply the names of the players, with any additional information available, like date of birth, height, nationality and match them based on similarity. 

### The Complications

#### Resources

Takes a lot of effort to calculate all possible similarities and find the best ones. A space of only ten thousand players means one hundred million possible pairs and optimizing that to fit into a reasonable amount of time and memory just to find out that it does not work is not ideal.

#### Precision in the Face of Noise

More importantly, simply matching the players by themselves is not precise enough, mostly due to the noise in the data. Names of teams, leagues or players, dates and scores are mostly similar but do not always match and sometimes the data is just wrong. Sometimes players are simply referred to by their first name in one dataset and their full name in another. This problem can be demonstrated with an example of teams: in one dataset the names of two clubs are *Athletic* and *Atletico Madrid*, while in the other *Athletic Bilbao* and simply *Atletico*. So the solution must be open to the possibility, that the two entities, *Athletic* and *Atletico* even though are very similar in name - more similar than any other team name to either, ar not in fact coreferent. 

Also, some players might have two or more different records in one dataset, due to simple data errors, that messes up a strict one-to-one matching.

#### Too Much Data for Manual Corrections

Re-examining and correcting the possible matches for over ten thousand players is simply not feasible, so a solution needs to be able to improve upon itself iteratively, without human help.

### Improved Solution

Introducing motifs. The core concept of the improved solution is not to match simply players, but match motifs in a network of players, matches, seasons and teams. This way, already discovered coreferences can be utilized to narrow the search space, and noise in the data can be mitigated by relying on more than one similarity to establish a coreference. Also, the links in the data can be utilized az validation and evaluation to iteratively improve the solution, or reject certain possible coreferences, as described in more detail below.

### Measuring Improvement

Due to the network nature of the data a possible mismatch is not difficult to detect. If we know that two players from the two datasets are coreferent, and so are two matches, if one dataset indicates that the player played in the corresponding match while the other does not, there is a problem. Ideally, if there are no errors in the datasets, there should be zero such cases. 

## Setup of the Dataset Pair

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


## General Outline of the Solution

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

## Creating and Matching Motifs

The steps that create transform and match motifs are intended to first find coreferent competitions and seasons, then find coreferent teams to properly find coreferent matches based on these, then find coreferent players based on all this knowledge. So the first motifs created are `competition - season - match - home_team - away_team`, then four different kinds of matches for `match - home_starter_player`, `match - home_sub_player`, `match - away_starter_player`, and `match - away_sub_player`.



All of this is implemented in the python package [encoref-v0.0.5](https://github.com/endremborza/encoref/tree/v0.0.5)

