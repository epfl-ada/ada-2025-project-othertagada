---
layout: page
title: r/GamerGate
subtitle: Misogyny in gamer communities, the case of the kiA subreddit
cover-img: assets/gamergateCollage_thedailycougar.jpg
mathjax: true
---
<style type="text/css" media="screen">
.image_center{
  display: block;
  margin: auto;
  width: 600px;
}
.row_div{
    display: flex;
    justify-content: space-between;
}
.center_div{
    display: grid; 
    justify-content: center; 
    align-items: center;
    width: 100%;
    grid-template-columns: 100%;
    grid-template-rows: auto;
}

.iframe_standard{
    width: 100%;
    height: 400px;
    border: none;
}

#topics-subreddit-iframe {
    height: 1000px;
    margin-left: max(calc(50% - 50vw), calc(50% - 610px));
    width: min(99vw, 1300px);
}

.iframe_75{
    width: 100%;
    height: 1000px;
    border: none;
    zoom: 0.75;
}

.iframe_50{
    width: 100%;
    height: 1000px;
    border: none;
    zoom: 0.50;
}

.iframe-row {
  display: flex;
  gap: 2rem;
  justify-content: center;
}

.iframe-row iframe {
  width: 500px;
  height: 450px;
  border: none;
}

.page-heading {
    background: rgba(50, 100, 255, 0.2);
    backdrop-filter: blur(10px);
    border-radius: 10px;
    padding: 15px !important;
    margin: 13rem 0;
    box-shadow: 0 0 0 3px rgba(50, 100, 255,0.2),
    0 8px 300px rgba(50,100,255,0.15);
}


body {
    font: normal 1rem Verdana, Arial, sans-serif;
    color: black;
    text-align: justify;
}

h1{
    font: Verdana, Arial, sans-serif;
    font-size: 28px;
}
h2 {
    font: Verdana, Arial, sans-serif;
    font-size: 22px;
}
h3{
    font: Verdana, Arial, sans-serif;
    font-size: 18px;
}

table {
    margin: 0 auto;
}


/* Container to show two svg images on the same row */
.svg-container {
    display: flex;
    width: 100%;
    gap: 10px;            /* optional gap between images */
  }

  /* SVG images: equal width, maintain aspect ratio */
  .svg-image {
    flex: 1 1 50%;        /* grow/shrink, base width 50% */
    width: 50%;
    height: auto;
  }

  /* Responsive: stack on small screens */
  @media (max-width: 800px) {
    .svg-image {
      flex: 1 1 100%;     /* full width */
      width: 100%;
    }
    .svg-container {
        flex-wrap: wrap;      /* allows wrapping to next line */
    }
  }

</style>
<script src="https://cdn.plot.ly/plotly-3.3.0.min.js" charset="utf-8"></script>
<!--- Script that closes the menu when clicking a nav link-->
<script src="assets/js/menu_closer.js"></script>

# Introduction
## What are we talking about ?

Our datastory is about [Gamergate](https://en.wikipedia.org/wiki/Gamergate), an online harassement campaign against feminism, diversity, and progressivism in video game culture that was present on multiple online platforms including reddit. \
The trigger for this event was a blog post published in August 2014 by Eron Gjoni, the ex-partner of game developer Zoë Quinn, in which he made allegations about their personal relationship. Conspiracy theories regarding Quinn having affairs with journalists in exchange for positive reviews on her new game "Depression Quest" were the perfect argument for far-right activists to create a large-scale bullying campaign disguised as scandal about ethics in games journalism. \
In practice, the movement became dominated by coordinated harassment, particularly targeting women in gaming, including Quinn, Anita Sarkeesian, and Brianna Wu, through doxxing, threats, and sustained online abuse.

Two subreddits were created in response: r/KotakuInAction and r/GamerGhazi, which are exclusively about this topic.

>Anyone else having seen the cultural insanity of SJW's spreading far enough that they are considering just giving up on the first world?

Posted on r/KiAChatroom


<div class="center_div">

<div class="plotly-chart">
  {% include_relative assets/posts_per_day_gamerghazi.html %}
</div>


<div class="plotly-chart">
  {% include_relative assets/posts_per_day_kotakuinaction.html %}
</div>

</div>

These two graphs show the number of posts in each of the subreddits created during the Gamer gate, we can see that peak activity was around the end of october. The post volume on r/GamerGhazi stayed elevated until march of 2015, where it declined and stabilized. r/KotakuInAction saw a rapid peak and decline, and subsequent stabilization after the initial burst of posting.

## Why this topic ?
Reddit’s semi-anonymous structure and inconsistent moderation practices have historically made it a fertile environment for the rapid spread of hostility and harassment. In this datastory, we examine the evolution of one such episode, using data to uncover how the event unfolded across the platform, how various communities were involved, which tools were used, and the political implications of such a large scale drama at the dawn of the 2016  US presidential elections, with the aim of being aware of these propaganda patterns if they happen again in the future, and possible moderation tools that could be developped to fight against them.
## The datasets
### Reddit Hyperlink Network
The main dataset (available [here](https://snap.stanford.edu/data/soc-RedditHyperlinks.html)) used for this project was created by a group at Stanford. It is composed of two separate datasets with the same structure, with the only difference being that the first is extracted from post titles and the second one from the post bodies :

| Label | Description |
| ------- | ------- |
| **SOURCE_SUBREDDIT** | The subreddit where the link was posted | 
| **TARGET_SUBREDDIT** | The subreddit that the link links to | 
| **POST_ID** | Unique id of the post |
| **TIMESTAMP** | Time of the post |
| **LINK_SENTIMENT** | 1 for positive or neutral intent, -1 for negative intent |
|**PROPERTIES**| Multiple integer fields grouped in a csv, visit the dataset source for more information|

This data represents a hyperlink network and was extracted from publicly available Reddit data of 2.5 years from Jan 2014 to April 2017.

### Pushshift
The second dataset we used has been generated by pushshift, which uses the Reddit API to extract and save post data to create a snapshot of Reddit accessible to the public (obtained [here](https://academictorrents.com/details/ba051999301b109eab37d16f027b3f49ade2de13)). We selected the same period of time as the first dataset (Jan 2014 to April 2017). It contains a log and metadata of all posts made during the time period, including usernames, titles, post bodies and more!  

### Events
The major events of the conflict with their time stamps were scraped from [this reddit timeline](https://www.reddit.com/r/GamerGhazi/wiki/timeline/).

## Data processing
We noticed that the reddit hyperlink dataset has some issues :
1. The post id's sometimes have an 's' appended to them, which we had to remove to be able to match the posts with the ones we got from the pushshift dataset. Since all valid id's are of length 6, we could drop the last character in the ones that where longer.
2. The timestamps of the reddit hyperlink are quite innacurate, we could not figure out why this is the case. After manual review, we determined that the timestamps of the pushshift dataset are acccurate and we replaced the timestamps of the hyperlink dataset with these, matching on the post id's.

Additionally, to make it easier to work with the Pushshift dataset, we only kept the following attributes:

| Label | Description |
| ------- | ------- |
| **SUBREDDIT** | The subreddit of the post | 
| **USERNAME** | Username of the post author | 
| **POST_ID** | Unique id of the post |
| **TIMESTAMP** | Time of the post |
| **TITLE** | Text of the post title |
| **BODY_TEXT** | Text of the post body|
| **NUM_COMMENTS** | Number of comments under the post |

We chose to reduce our dataset to the subreddits that interact the most with either r/kotakuinaction (main pro-GamerGate subreddit) or r/gamerghazi (main counterpart of kotakuinaction) between 2014-07-01 and 2016-09-30.


<div class="iframe-row">
  <iframe src="assets/top50_interactions_kotakuinaction.html" class="iframe_standard"></iframe>
  <iframe src="assets/top50_interactions_gamerghazi.html" class="iframe_standard"></iframe>
</div>


# Look at the players
We want to understand how users interact with the reddit platform to better analyze the gamergate. First let's look how strongly power users (users that posted a lot in the subreddits related to the gamergate) dominate the discourse. In the graph below we see the number of posts per user in the 15 subreddits of interest. While the graph seems to follow a power law distribution at first sight, statistical analysis shows that it follows a lognormal distribution, as one can infer from the graphs below.

<div class="svg-container">
  <img src="assets/histogram_nbposts_per_user.svg" alt="Histogram of number of posts per user" class="svg-image">
  <img src="assets/userposts_ccdf.svg" alt="CCDF number of posts per user plot" class="svg-image">
</div>

Power-law distributions are extremely unequal. For example, the number of references to websites follows a power-law distribution. Most websites are linked very little, while a tiny number (like google.com) can become overwhelmingly dominant. This kind of pattern is often described as scale-free, because the same imbalance appears at every level. Lognormal distributions are also heavy-tail, but not scale-free. This makes sense, as human users are constrained by time and attention. This in turns shows that power users are very important but do not fully dominate the discourse as might be the case with a pure power law.

"Light users", while rare posters, might also still look at a lot of posts and might be very active in the act of reading and could therefore be considered more as spectators. Power users could be seen more like the leaders of the subreddits.

We also were interested to analyze if on the posts that contain hyperlinks, power users are overall less negative than "light" users. While the initial graphs we drew seemed to suggest that, the statistical analysis revealed no statistical significance, so we can conclude that power users and light users have the same probability to start attacks.

## Which subreddits are more moderated?

Let's look which subreddits do more strongly moderate their users. In reddit, a post can be deleted either by the user itself (in this case in the body the text "\[deleted]" appears) or by moderators or admins (in this case in the post body the text "\[removed]" appears).

Most of the moderation is done by the moderators. Users who create subreddits automatically become their moderators. They can define the rules of the subreddit, can nominate other users to become moderators, and can delete posts. Moderators in general have lots of freedom in the way they do moderation. Admins on the contrary are reddit employees. Until around 2014, they only did the most basic moderation to be able to keep the site running, like deleting spam or removing illegal content. By 2014 however, reddit admins began to moderate a bit more strictly and imposed some new moderation rules. This change of policy was also due to events like the Gamergate happening. Posts can also be deleted by bots, but the bots are in turn controlled by one of these two groups. \[2]

This chart shows the percentage of posts with bodies removed by moderators or admins per subreddit. To interpret this graph, it is probably safe to assume that most posts were removed by moderators (and not admins).

<div class="plotly-chart">
  {% include_relative assets/deleted_posts_per_subreddit.html %}
</div>

This plot is very interesting. On the right side we see the subreddits that are mostly unmoderated. r/kiachatroom (kia=kotakuinaction), r/amrsucks (amr=againstmensright), r/srssucks (srs=shitredditsays) and r/shitghazisays (ghazi=gamerghazi) are all subreddits on the side of "r/kotakuinaction", the side of the attackers and initiators of the gamergate.
On the contrary, most strongly moderated subreddits e.g. r/shitredditsays, r/gamerghazi, r/againstgamersgate are on the side of the defenders. This makes lots of sense, as the subreddits who fight against harassment will moderate their own posts, while the attackers will not. 

<div class="center_div">

To understand better how the selected subreddits interact we first need to understand how their communities of users overlap (or don't!) We compute the Jaccard Similarity between each subreddit to construct a heatmap of user similarity between subreddits in a very intuitive way.

The Jaccard index measures the similarity between two sets by dividing the intersection of the sets by their union.
</div>

$$J(A,B)= \frac{A\cap B}{A\cup B}$$


<div class="center_div">
So subreddits with a higher proportion of overlapping users will have a higer Jaccard index.
<br><br>

<img src="assets/heatmap_users.png" class="image_center"/>

We can look into the interactions of these subreddits to see if they link towards or get linked, by either gamerghazi or kotakuinaction, to better understand their relationships within the Gamergate network.
<iframe src="assets/stacked_bar_transition.html" class="iframe_standard"></iframe>

We can clearly see that most subreddits send more links than they receive from KiA and Ghazi.  <br> 

This also helps us better understand the nature of one of our actors. Gamerghazi presents much more links towards Kia than from them, which is in explained by its nature of G"counter-attack" to gamergate. They are not the direct target of the gamergaters, but more like an opposition. <br> <br>


Together, these two plots give us insights on which side of the conflict each subreddit stand.  <br> <br>

Here is a parctical summary of where their "side". They are noted as either pro-gamergate or anti-gamergate. <br> <br>
Some of these are pretty general subreddits that are involved in all sorts of interactions and are by no means exclusive to the gamergate drama. If they didn't strictly agree to one side, they were marked as neutral. <br> <br> <br>
  
</div>


| **<span style="color:red">kotakuinaction</span>** | Pro |
| **amrsucks** | Pro |
| **kiachatroom** | Pro |
| **srssucks** | Pro |
| **shitghazisays** | Pro |
| **ggfreeforall** | Neutral/pro |
| **shitliberalssay** | Political/Pro |
| **<span style="color:blue">gamerghazi</span>** | Anti |
| **topmindsofreddit** | Anti |
| **againstgamergate** | Neutral/anti |
| **bestofoutrageculture** | Political/anti |
| **drama** | Neutral |
| **subredditdrama** | Neutral |
| **shitredditsays** | Neutral |
| **circlebroke2** | Neutral |
| **panichistory** | Political/Neutral |

# How it played out
Here is an overview of how the Gamergate events unraveled. Use the slider to navigate. Look at the week of Dec 15, 2014 for a fun example, which gives a glimpse at the magnitude of the drama just after its peak !

<div class="center_div">

<iframe class="iframe_75" src="assets/slider_graph_and_bar_chart.html"></iframe>

</div>

# Can negativity be predicted ?

As mentioned before, this story is one of intense harassment, a huge part of managing these types of hate compaigns is content moderation. Nowadays content moderation relies mainly on models trained to detect hateful speach. Considering the cleaving topics discussed in gamergate, here we chose to consider a negative link from a subreddit to another as a sign of hate.

### So much negativity...

Gamergate led to a massive hate campaign so as we could expect, the subreddits involved in the conflict spreaded a lot of negativity compared to the the platform as a whole and the link sentiment confirms it very well. 



The two sides of the conflict confronted each other vividly on the subject but, like in almost every quarrel, some side can attack with more energy. We determined in a naive way which subreddits are more aggressive in their speach and the one that are more victims of this aggressivity. Here we simplify and classify the "bullies" and the "bullied" by observing which fraction is higher between the outgoing and incomig negative links for each subreddit.

#plot in/out negative link per subs#

The plot is clear : 
- Bullies : r/amrsucks, r/circlebroke2, r/drama, r/srssucks, r/subredditdrama.
- Bullied : r/panichistory, r/shitredditsays, r/bestofoutrageculture, r/againstgamergate, r/gamerghazi.

Considering the bullies count among them two of clearly pro-gamergate subreddits i.e. r/amrsucks and r/srssucks and that we find among the bullied four anti-gamergater i.e. r/shitredditsays, r/bestofoutrageculture, r/againstgamergate, r/gamerghazi, it makes a lot of sense. The attackers leading a harassment campain would surely spread negativity in the communities the most and the defenders would also collect more of this negativity.

Obviously, it is never as simple as that but we still get a global picture of the most hostile groups involved.


### Let's build our negativity detector

Predicting the negativity of a post is the best way to moderate the content of a platform in a machine learning manner and it also tells us a lot about the content of the text, if you ask the write questions. The Gamergate involved, as already stated, a lot of hostility, but how exactly was this hostility expressed ? Do we see some patterns in hateful speech ? If so, whcih ones ? That's what we tried to figure out. So let's get to it !
For this purpose, we used our good old logistic regression that will help us classify some link posts as positive or negative, given their attributes. The ones that we chose were related to the stylistic linguistic





For this analysis, we used the following text properties of the posts : 

"chars_no_ws", "frac_special","num_words","num_long_words",\
"avg_word_len", "frac_stopwords", "num_sentences", "num_long_sentences", \
"avg_chars_sentence","avg_words_sentence", "automated_readability"\
"vader_pos","vader_neg",\
"LIWC_Swear","LIWC_Affect","LIWC_Anger", "LIWC_Sexual"

The first 11 stylistic linguistic features would help us show how relevant the structure of a speech is in the prediction of its sentiment. We could determine if a text with an attributed sentiment tend to follow a specific structure or to have a certain complexity.

VADER values are used as well. Valence Aware Dictionary and sEntiment Reasoner is a sentiment analysis tool which is designed to analyze social media text and informal language. It is best at detecting sentiment in short pieces of text like tweets, product reviews or user comments which contain slang, emojis and abbreviations. 

Linguistic Inquiry and Word Count (LIWC) Analysis is a computational method that categorizes text into validated linguistic and psychological dimensions. It offers 118 categories for which the statistical outputs of a text is represented as :  

$$
\text{Category Score} =
\frac{\text{Number of words in category}}
     {\text{Total number of words in text}}
\times 100\%
$$

In our dataset, only 65 categories are available and we chose to select four of them which have the most potential to be indicators of a negative sentiment in our selected communities.

Plotting pairwise relationships in the dataset to see if we can identify any correlation, the observation is as follow :

We find the obvious correlation between features such as the number of words in a sentence with the number of characters in a sentence.
But we notice one correlation between automated readability with the average number of characters in sentences and the average number of words in a sentence as well. It seems to tell that sentences with more words tend to be more complicated to understand and needs for someone to have a better level of language to comprehend the text.\
The Automated Readability Index is indeed a readability test that that gauges the level of education needed to understand a piece of writing and looking at its formula :

$$
ARI = 4.71 \left( \frac{\text{characters}}{\text{words}} \right)
+ 0.5 \left( \frac{\text{words}}{\text{sentences}} \right)
- 21.43,
$$

it confirms our observation. We find the average number of words in a sentence and the average word length which is just an affine (linear) function of the average number of characters in a word.\
Other than the ones we just discussed, we are not able to identify any other correlation clearly.



Let's train our regression model and see how well we can predict the link sentiment of our dataset.

#### Logistic Regression for link prediction


Training on the whole dataset, we get an prediction accuracy of 0.807 which is pretty satisfying. Now let's see how well the model predict the outgoing link sentiment of each of our selected subreddits.

<iframe src="assets/pred_accuracy_per_subs_hl_data.html" class="iframe_standard"></iframe>

It is clearly less satisfying... 
The accuracy is less than 0.8 for all subreddits and even less than 0.5 for three of them. 
Since we trained on the whole dataset, our model is not fitting all the data from the selected subreddits very well. It represents only a small fraction of the whole dataset.
However, among the subreddits with the most accurate predictions, we can find drama, circlebroke2 and subredditdrama, the same that were classified as "bullies" in our previous analysis but were actually not in a particular side. Why is that ?

Let's look at this next plot to get a better understanding.

#plot of nb posts pos/neg#

The answer is actually very simple. They are among the most active subreddits of our selection, which means that they will have more impact on the model that we trained than the other smaller subreddits with only a few posts on their account.


To go futher with this analysis we want to figure out which feature had the most weight in the decision making of our model. This is where we introduce the feature coefficient of the model that will help us determine the importance of each feature and in which direction they lead us (positive or negative). 
\
\
But, to keep things a little bit more interesting, let's train an other model but with only the large_gamergate_df. That way we can compare the importance of the features in the link sentiment prediction of our chosen gamergate-related subreddits and of Reddit as a whole.

#plot accuracy per subs (gamergate_subs)#

The overall accuracy is lower (0.742) than the previous one but the accuracy per subreddit shows a little improvement : only 4 are under 0.7 against 10 in the previous model.

### 3.3 What are signs of negativity on reddit?


##### Feature importance and significance

The logistic regression model is useful not only to classify a link as negative or positive but also to give us a glimpse into which features are the most useful in the classification and if their presence has a positive or negative impact on the link sentiment.

#plot coef bar plot#

#significance grid#

Here we have the following :

- A bar plot of the logistic regression feature coefficient in a descending order,
- A grid of these coefficient also indicating the significance of the feature in the model.

Among the most important features in a positive prediction we have : automated readability, num_words, vader_pos\
For a negative prediction there are : LIWC_Anger, avg_words_sentence, LIWC_Swear

Knowing the VADER indicator definition, it is not surprising to observe its weight in the positive top 3. The automated readability being top 1, we could make the asssumption that links containing more "complicated" text tend to be classified as positive. It could be that the texts written with negative intent are incline to be less elaborated and complex. Probably because the majority of the negatively classified posts contains insulting and aggressive speech with swears and are not negative in a constructive way like a negative review might be for example. This could explain the strong negative weight that the LIWC_Anger and LIWC_Swear features gained in the trained model. \
Only 4 features are here considered to be insignificant (char_no_ws, num_long_sentences, num_sentences, avg_chars_sentence).

### 3.4 Linguistic characteristics of Gamergaters 

Let's evaluate the features of our second model now.

#plot coef bar plot#

#significance grid#

Among the most important features in a positive prediction we have : automated readability, avg_chars_sentence, num_words\
For a negative prediction there are :  avg_words_sentence, avg_word_len, LIWC_Anger

Again without any surprise, anger is a good predictor of negative sentiment in a link. Gamergate involved a lot of threats and abuse as we previously stated. It triggered a very vivid reaction which was aggressive. The average number of words in a sentence appears as well once again in the negative prediction. It indicates a characteristic of the negative posts : the more words in a sentence, the more negative it gets.

Automated readability still plays an important role in the decision of a positive link sentiment. As the positive link sentiment also include neutral posts, the large weight of automated readability could be explained by the role of some subreddits such as r/subredditdrama that might just report some drama that occurs on the platform without taking part. Just stating some facts and sharing the newest conflicts there might be which would be categorized as neutral posts.

It's intriguing to notice LIWC_Swear has now a small positive weight. We have to remind ourselves that a positive link sentiment do not necessarily means that the post's text is friendly. It could also mean that it is neutral, it doesn't have any good or bad intentions. We could interpret that as a way of speaking and writing that is just more crude but not mean in our subreddits of interest.


<div class="center_div">

<iframe src="assets/feature_coef_hl_data.html" class="iframe_standard"></iframe>

<iframe src="assets/feature_significance_hl_data.html" class="iframe_standard"></iframe>

<iframe src="assets/pred_accuracy_per_subs_hl_data.html" class="iframe_standard"></iframe>

<iframe src="assets/feature_coef_gamergate_subs.html" class="iframe_standard"></iframe>

<iframe src="assets/feature_significance_gamergate_subs.html" class="iframe_standard"></iframe>

<iframe src="assets/pred_accuracy_gamergate_subs.html" class="iframe_standard"></iframe>

</div>

# Gamergate users and the alt-right sphere
GamerGate has been widely analysed post mortem and is now considered a text book exmaple of manifactured online outrage. Pushing communinities to more extrem views, more precisely more extrem political views. Gamergate is inherently political in its premice of harassement compagne agains women in gamer spaces.\
As pointed out by numerous medias covering the drama, Gamergate was a conspiracy theory created by alt-right extremists to rally people to their cause. 
As Donald Trump's former political advisor Steve Bannon [stated here](https://eu.usatoday.com/story/tech/talkingtech/2017/07/18/steve-bannon-learned-harness-troll-army-world-warcraft/489713001/) : “You can activate that army. They come in through Gamergate or whatever and then get turned onto politics and Trump.”  
Let's see if that worked out.\
We look at users from what we consider 'attacker' subreddits and at users from political subreddits, in particular right to alt-right subreddits.

{% include_relative assets/gamergate_proportion_politics.html %}

But is this high proportion really more elevated than for the communuty of a 'regular' subredit. We decided to test the proportion of alt-right users in r/gaming, a less polarizing subreddit.

{% include_relative assets/gaming_proportion_politics.html %}


# What Happens in the aftermath ?
While r/kotakuinaction and r/gamerghazi where created expressively with the goal of discussing the subject of GamerGate, these subreddits (like many others) do not die down suddenly after the events. These subreddits continue posting years after the peak of the conflict. But what topics are still discussed in the aftermath of the main events, is the actual gamergate still the most important theme are do communities once united by a conflict build new interest?\
To try to respond to these interrogations we utilized [Empath](https://arxiv.org/pdf/1602.06979) a NLP tool that relies on deep learning to infer lexicon from some given seed words. Here we created 4 topic categories: 
* Gamergate : Everything related to the actual events that sparked gamergate
* Mysogyny : Signs of mysogyny, sexims and violence against women.
* Legal : Legal speech, trial 
* Incel : Incel retoric

{% include_relative assets/kia_topics_monthly.html %}

For the topic of 'gamergate' we can see a high starting point that slowly goes down as time passes and the drama looses relevance, we have a real decline in interest in main topic. From the start misogyny is quite high and slowly goes up. The topic of 'incel' and 'legal' start quite low and also go up with time. These last two topics are way more precise than the two others we analyze so it is not surpising that they have lower value overall. 

{% include_relative assets/gia_topics_monthly.html %}

R/gamerghazi tells a different story, the topic of 'gamergate' is from the start not as relevant and 'misogyny' is globally higher. The subreddit r/gamergahzi is not as much invested in tha actual events but more on discussing what came of the hate compaign. These is even more seen in the aftermath, where r/gamerghazi is mostly used to discuss the incel movement that has come up from the events. Legal picks up significantly in importance as the legal ramifications of GamerGate slowly surface.

Just to be sure that our technic using Empath is working properly, let's see what happens when we compute the same values for a subreddit that is not part of the gamergate drama. We chose the very active r/gaming subreddit.

{% include_relative assets/gaming_topics_monthly.html %}

The topic of gamergate are very high, this is explained by the fact that one of the seed word given for this category was 'gaming', which is a word that is most certainly well found in r/gaming. In contrast, the other topics look almost irrelevant for this subreddit, this confirm that the sudreddits r/kotakuinaction and r/gamerghazi have a high value for the topic of misogyny and incel behaviour than a subreddit not linked to the events. 


# Conclusion
Our story is one of successful manufactured outrage. A political agenda disguised as a simple 'gaming scandal'. 
We trained a logistic regression model with the aim of better understanding what makes a message negative with the bigger goal of having better moderation on reddit. Better moderation to prevent such harassement and hate compaign from happening again, but not only.\
With better moderation from the platforms that host these online communites, we could hope to see an improved responsiveness to the creation of extreme online communities.\
Still we need to keep in mind that it is very often difficult to put in action, one cannot just apply a threshold to justify closing a subreddit, it is often a delicate situation. 

# References 
- Cover image: [https://thedailycougar.com/wp-content/uploads/2014/11/gamergate.jpg](https://thedailycougar.com/wp-content/uploads/2014/11/gamergate.jpg)

- \[2] Moderation in reddit [https://www.theguardian.com/technology/2015/dec/30/reddit-ellen-pao](https://www.theguardian.com/technology/2015/dec/30/reddit-ellen-pao)