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


## Literature Context

Progress in entity coreference resolution (in some contexts, referred to as instance matching, or link discovery) seems rather slow and has not been able to generate much attention in the last few years, at least in academia. Articles are generally published in semantic web related conferences or journals like [Semantic Web][SW] and [Web Semantics][WS]. New algorithms and benchmarks are introduced at the yearly evaluation event of the Ontology Alignment Evaluation Initiative([OAEI]). 

Song and Heflin started outlining a method on a similar scale in [SH2010] and [SH2011], which sparked a few notable extensions towards [machine learning][APEX2012] and [scalability][HOGAN2012]. This framing of the problem is a little more general, in the sense that in our case relationships, are known to be coreferent. So that when a team and a match is connected in one database by a `participated-as-home-team` link, it is known that there is a corresponding type of link in the other dataset that represents this same kind of relationship. In these methods, this knowledge is not assumed, but the requirements from the solutions are adjusted to be more modest, as opposed to having to find a 100% accurate matching for all entities in a dataset. 

In more recent cases, the problem is more frequently framed as _link discovery_, with emphasis on scalability and the ambition of semantically connecting resources on the Linked Open Data (LOD) Cloud. A [survey] of these methods from 2017 gives a decent overview of the tools available, sometimes drifting into more general knowledge graph related issues, that are summarized [here][kgi].

Based on the fact that most papers containing some novelty are published mainly by researches affiliated with companies, not universities, the problem is more prevalent in industry, than academia. It appears that in many cases it is viewed as an engineering issue, not a scientific one. Submitting solutions to evaluation events is a rather convoluted and technical endeavor, and open source tools around graph data and the semantic web are not as mature and popular as ones around tabular data, so the barrier to entry for anyone dealing with social sciences is high.

```
@article{nentwig2017survey,
  title={A survey of current link discovery frameworks},
  author={Nentwig, Markus and Hartung, Michael and Ngonga Ngomo, Axel-Cyrille and Rahm, Erhard},
  journal={Semantic Web},
  volume={8},
  number={3},
  pages={419--436},
  year={2017},
  publisher={IOS Press}
}


@article{paulheim2017knowledge,
  title={Knowledge graph refinement: A survey of approaches and evaluation methods},
  author={Paulheim, Heiko},
  journal={Semantic web},
  volume={8},
  number={3},
  pages={489--508},
  year={2017},
  publisher={IOS Press}
}


@inproceedings{song2010domain,
  title={Domain-independent entity coreference in RDF graphs},
  author={Song, Dezhao and Heflin, Jeff},
  booktitle={Proceedings of the 19th ACM international conference on Information and knowledge management},
  pages={1821--1824},
  year={2010}
}

@inproceedings{song2011automatically,
  title={Automatically generating data linkages using a domain-independent candidate selection approach},
  author={Song, Dezhao and Heflin, Jeff},
  booktitle={International Semantic Web Conference},
  pages={649--664},
  year={2011},
  organization={Springer}
}

@inproceedings{rong2012machine,
  title={A machine learning approach for instance matching based on similarity metrics},
  author={Rong, Shu and Niu, Xing and Xiang, Evan Wei and Wang, Haofen and Yang, Qiang and Yu, Yong},
  booktitle={International Semantic Web Conference},
  pages={460--475},
  year={2012},
  organization={Springer}
}

@article{hogan2012scalable,
  title={Scalable and distributed methods for entity matching, consolidation and disambiguation over linked data corpora},
  author={Hogan, Aidan and Zimmermann, Antoine and Umbrich, J{\"u}rgen and Polleres, Axel and Decker, Stefan},
  journal={Journal of Web Semantics},
  volume={10},
  pages={76--110},
  year={2012},
  publisher={Elsevier}
}


```

[SW]: https://www.scimagojr.com/journalsearch.php?q=21100269620&tip=sid&clean=0
[WS]: https://www.scimagojr.com/journalsearch.php?q=14879&tip=sid&clean=0
[OAEI]: http://oaei.ontologymatching.org/
[survey]: http://semantic-web-journal.org/system/files/swj1029.pdf
[kgi]: http://www.semantic-web-journal.net/system/files/swj1167.pdf
[SH2010]: http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.653.2214&rep=rep1&type=pdf
[SH2011]: http://iswc2011.semanticweb.org/fileadmin/iswc/Papers/Research_Paper/09/70310640.pdf
[APEX2012]: https://link.springer.com/content/pdf/10.1007/978-3-642-35176-1_29.pdf
[HOGAN2012]: http://dit.unitn.it/~p2p/RelatedWork/Matching/entcons_jws_final.pdf