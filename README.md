# TITLE PROPS:
- Please be nice: A deep dive into inter-subreddit communication
- The extroverts: Analyzing the most interacting subreddits on the platform
- The bubbleverse: How do different spheres on Reddit communicate?

## The aim of this analysis will be to visualize the dialogues that take place within a frequently communicating portion of subreddits, by unraveling causes, consequences, attacks and responses between these groups that oftenly interact together.
# Research question
## What can we learn about conflicts and friendships from analyzing the dynamics that occur within a frequently interacting set of groups ?

# Description
This project explores how Reddit communities interact, collaborate, and clash within a densely connected network of subreddits. By focusing on the most active and communicative groups, we aim to uncover the dynamics that shape inter-community relationships — whether friendly alliances or hostile exchanges. Using network analysis and time-windowed tracking of subreddit behavior, we visualize how patterns of sentiment and interaction evolve over time, identifying clusters of related topics and potential “troublemakers” who ignite chains of negative exchanges. Alongside network-based insights, we also examine linguistic properties of posts — such as word complexity, sentence length, or number of words used — to see whether communication style influences sentiment and group dynamics. Ultimately, this study investigates whether the mechanisms driving conflict and cooperation between online communities mirror those found in human social groups, revealing how both structure and language shape the evolving landscape of discourse on Reddit. (la dernière phrase rejoint la cinquième question de la section d'en-dessous mais jsp si on veut s'aventurer là-dedans vraiment même si c'est mega intéressant)
ou on met ça idk:
Ultimately, this study seeks to provide a deeper understanding of how communities on Reddit organize, influence one another, and evolve through cycles of cooperation and conflict within the broader ecosystem of online discourse.

# Specific questions and methods
Q° : What seems to bring these subreddits together ? Are they closely related or completely different ?
-> subreddit embeddings

Q° : Can we identify "troublemakers" within the population ?
-> time analysis of the initiators : find the first negative links sent that trigger a series of events
    Do they have similatities (in size, graph-based structure, topic etc.)?

Q° : Are alliances made to coordonate/face attacks ? Are they temporary or long lasting friendships ?
-> graph analysis  ??

Q° : How long does it take for an attack to be forgiven by the receiving end ? Meaning that they start interacting positively together again.
-> temporal analysis of the sentiment of individual subreddits for other subreddits that attacked them

Q° : Can we find mechanisms that group conflicts follow that are similar to the ones in conflicts between individuals ? (peut etre too far haha)
->

Q° : Can conflicts within the population spark seemingly unrelated conflicts between other members ??
->

# Proposed timeline
| **Week** |**Dates**| **Tasks** |
| :------: | :------: | ------ |
|**1** |6.11-12.11| <ul><li>Find target population for deeper analysis </li><li> Make more utils for time analysis, plotting and other general functionalities needed for the project</li></lu>|
|**2** |13.11-19.11| <ul><li>Start in-depth time analysis of our target population </li><li> Define attack/interaction window (to be able to relate interactions between two subreddits)</li></lu>|
|**3** |20.11-26.11|<ul><li>Start work on the datastory (probably with a github.io website) </li><li> Use a classifier to try to create groups for our target population (by topic, size, other metrics...) </li><li> Continue working on analyzing the target population with focus on "troublemakers" </li></lu> |
|**4** |27.11-03.12|<ul><li>Look for conflict sparking trends and possible alliances </li><li> Continue work on both data story and further analysis of the target population (bulk of our work should be this week)</li></lu>|
|**5** |4.12-10.12|<ul><li>Finalize the datastory, including text, interactive graphs and images </li><li> Wrap up analysis of our target population (time allocated for ideas not part of our initial planning) </li><li> Make sure all helpers and supporting code is mostly finalized</li></lu>|
|**6** |11.12-17.12|<ul><li>Fix bugs (if any) </li><li> Verify website layout and code clarity </li><li> Avoid adding new features/content, focus on correctness of the project</li></lu>|

# Internal milestones
- [ ] Found our target population
- [ ] Defined robust interaction window
- [ ] Found troublemakers (or proved that there are none ) 
- [ ] Datastory content complete