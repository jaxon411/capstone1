# Dota 2: *Dire* Chances at Winning and How to Give your Team the Best Odds

## Resources
**Dota 2 Matches kaggle dataset:**

https://www.kaggle.com/devinanzelmo/dota-2-matches

**Other useful resources that informed my understanding of the data:**

Web API Wiki - https://wiki.teamfortress.com/wiki/WebAPI#Dota_2

Web API Developer forum - https://dev.dota2.com/forum/dota-2/spectating/replays/webapi

Dota 2 Gameplay Wiki - https://dota2.gamepedia.com/Dota_2_Wiki

## What is Dota 2?

Dota 2 is a competitive video game in the **MOBA** grenre (**multiplayer online battle arena**). As a MOBA, it features two teams of five players each, with both teams attempting to push down the map in order to destroy the other team's base (known as an **Ancient**).

![Image](https://static.wikia.nocookie.net/dota2_gamepedia/images/8/8d/Labelled_Map_7.20.png/revision/latest?cb=20181122205641&format=original)

The image above shows the two sides of the map that both teams (named **Radiant** and **Dire**) spawn into. I try to keep the colors (green and red respectively) consistant in the graphs below.

The main focus of this project at first was to detail the impact of having objective/resource control on a a team's chances at winning. However, after modeling the data, I found some unexpected results that changed the direction of my analysis.


## Gold

First, I think it's important to show where the rabbit hole started. I figured I should look at something easy to understand in my first analysis: **gold**.

Gold is a resource in Dota 2 that lets you buy gear to improve your character throughout the game. *Lots* of things give you gold in the game, but those details don't really matter.

Here is the first chart I made, simply plotting the sum of gold for each team over the course of the game, as well as the eventual winner of the match:

![Image](https://i.imgur.com/Or1Wq1h.png)

Not too surprising, the team with more gold (i.e. more resources) won that match. Next, I plotted 16 other matches, selected at random:

![Image](https://i.imgur.com/LOiykX6.png)

Again, not surprising. Now that I had a visual, I decided to dive into the raw numbers insted. Below is some print out of code measuring the probabability of winning given more gold at the end of the game taken from the entire sample:

```
Radiant Gold Advantage: 25749
Dire Gold Advantage: 24251
Radiant Wins | Gold Advantage: 25378
Dire Wins | Gold Advantage: 23686

Radiant win-rate given they had most gold at the end of the game = 0.99
Dire win-rate given they had most gold at the end of the game = 0.98
```

Without anymore analysis, we can pretty confidently conclude that having more gold at the end of the game is a fantastic predictor of win-rate. However, it's not very useful to players. You won't know who had the most gold at the end of the game until the game is already over, and obviously at that point it no longer matters.

Looking at the raw probabilities, I was a little curious about the 1% difference between the two teams. Presumably 1% difference is within the variance, but I decided to do a sanity check to make sure...

And I'm glad I did.

## Win-rates of Radiant and Dire

To analyze the overall win-rates of the two teams, I started with the raw probabilities:

```
Radiant Overall Winrate = 0.52
Dire Overall Winrate = 0.48
```

These two numbers don't give us much information other than what we would tend to expect; about a 50/50 split.

To give some visual representation, and to potentially do a hypothesis test, I decided to leaverage bootstrapping to give me a normal distribution of win-rates. Here is the result for both Radiant and Dire teams:

![Image](https://i.imgur.com/VPfH2by.png)

![Image](https://i.imgur.com/VEkpjAT.png)

**Woah.** That is very unexpected. I'm not familiar with the nuances of competative Dota 2 play, but I have some general knowledge of MOBAs, and I would expect that the goal is to get it as close to 50/50 as possible.

I'm not sure what exactly could cause this, but after a little bit of research I found that the Radiant and Dire sides of the map are not a perfect mirror; there are quite a few differences, and that could be significant enough to tilt the probabilities. One of those differences is the location of an objective called Roshan.

## Roshan Control

**Roshan** is the most powerful neutral objective in the game. It gives many benificial effects to a team if they kill it, and the fact that it's neutral means that either team can get it.

However, one important difference is that Roshan's position is nearly all inside of the Dire portion of the map. I decided to run a test to see if this positioning meant that Dire teams who prioritized what I call **Roshan Control** (killing Roshan more often than your oppoents) would have a better win-rate than the raw probability.

To do this, I came up with this hypothesis test:

```
H0 = Roshan Control gives no better statistical advantage to Dire relative to the raw win probability (>=4%)
Ha = Roshan Control improves Dire's chances of winning relative to the raw win probability (<4%)
alpha = 0.05
```

I treated winning and not winning as a Bernoulli trial and utilized some Bayesian magic (also known as Bayesian testing) to find the most likely P-Values. I gathered the number of wins for each team *given* that they had Roshan Control and created a binomial distribution with it.

Finally, to accomplish the Bayesian testing, I created two beta distributions for the prior probabilities, which is updated by their wins and losses as alpha and beta respectively. Here are the results after testing:

![Image](https://i.imgur.com/scfckoi.png)

Nope, it didn't help at all! We can't reject the null unfortunately. In fact, not only did iy **not** help, but the difference between winrates went from **~4%** to **~10%**. In other words, if both teams prioritize Roshan Control, Radiant benifits more statistically than Dire does if they're successful.

Maybe not a great bet for Dire, then...

## Conclusion

**Takeaways**
* Gold is a major predictor for win-rates in every game, but it's essentially useless for player information.
* Dire teams, for all metrics I've tested for so far, have an overall lower win-rate.
* Roshan Control (killing Roshan more than the opposing team) gives a *significant* boost to win-rate, but Radiant benifits more than Dire.

Since team selection in Dota 2 is random, a player doesn't have the option to always play Radiant. Given what we see from the analysis above, the only bit of advice I can give for a player drafted onto the Dire team is:

**Get as much gold as you can**


## Looking Forward

Unfortunately the week time constraint didn't allow me to delve any deeper on the win-rate disparity I stumbled uppon. Looking forward, I would love to revist this dataset and do the following:
* Look at win rates for teams who have higher gold totals at a given time

```
Radiant Gold Advantage @ 15 min: 25953
Dire Gold Advantage @ 15 min: 23962
Radiant Wins | Gold Advantage @ 15 min: 18150
Dire Wins | Gold Advantage @ 15 min: 16222
Gold Ties @ 15 min: 4
Radiant Wins | Gold Tie @ 15 min: 3
Dire Wins | Gold Tie @ 15 min: 1

Radiant win-rate given the most gold at 15 minutes = 0.7
Dire win-rate given the most gold at 15 minutes = 0.68
```

* Look at win rates for teams that score First Blood (first kill of the game)
* Look at win rates for teams that destroy more/less Towers (obtacles that need to be destroyed before destroying the enemy Ancient)
* Then eventually, string some or all of these into a Bayesian test to 
