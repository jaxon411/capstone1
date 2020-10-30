# Dota 2: *Dire* Chances at Winning and How to Give your Team the Best Odds

## What is Dota 2?

Dota 2 is a competitive video game in the MOBA grenre (multiplayer online battle arena). As a MOBA, it features two teams of five players each, and both teams are attempting to push down the map in order to destroy the other team's base.

![Image](https://static.wikia.nocookie.net/dota2_gamepedia/images/8/8d/Labelled_Map_7.20.png/revision/latest?cb=20181122205641&format=original)

The image above shows the two sides of the maps that both teams start and spawn in (named Radiant and Dire). I try to keep the color's consistant in the graphs below.

The main focus of this project at first was to detail the impact of having objective/resource control on a a teams chances at winning. However, after modeling the data, I found some unexpected results that changed the direction of my analysis.


## Gold

First, I think it's important to show where the rabbit hole started. I figured I should look at something easy to understand in my first analysis: **gold**.

Gold is a resource in Dota 2 that lets you buy gear to improve your character throughout the game. *Lots* of things give you gold in the game, but those details don't really matter.

Here is the first chart I made, simply plotting the sum of gold for each team over the course of the game, as well as the eventual winner of the match:

![Image]

Not too surprising, the team with more gold (i.e. more resources) won that match. Next, I plotted 16 other matches, selected at random:

![Image]

Again, not surprising. Now that I had a visual, I decided to dive into the raw numbers insted. Below is some print out of code measuring the probabability of winning given more gold at the end of the game taken from the entire sample:

```
{'rad_adv': 25749,
'dire_adv': 24251,
'rad_wins': 25378,
'dire_wins': 23686,
'adv_ties': 0,
'rad_tie_wins': 0,
'dire_tie_wins': 0}

Radiant win-rate given they had most gold at the end of the game = 0.99
Dire win-rate given they had most gold at the end of the game = 0.98
```

Without anymore analysis, we can pretty confidently conclude that having more gold at the end of the game is a fantastic predictor of win-rate. However, it's not very useful to players. You won't know who had the most gold at the end of the game until the game is already over, and obviously at that point it no longer matters.

Looking at the raw probabilities, I was a little curious about the 1% difference between the two teams. Presumably 1% difference is within the variance, but I decided to do a sanity check to make sure...

And I'm glad I did.

## Win-rates of Radiant and Dire

To analyze the overall win-rates of the two teams, I decided to leaverage bootstrapping to give me a normal distribution of win-rates. Here is the result for both Radiant and Dire teams:

![Image]

![Image]

**Woah.** That is very unexpected. I'm not familiar with the nuances of competative Dota 2 play, but I have some general knowledge of MOBAs, and I would expect that the goal is to get it as close to 50/50 as possible.

I'm not sure what exactly could cause this, but after a little bit of research I found that the Radiant and Dire sides of the map are not a perfect mirror; there are quite a few differences, and that could be significant enough to tilt the probabilities. One of those differences is the location of an objective called Roshan.

## Roshan Control

Roshan is the most powerful neutral objective in the game. It gives many benificial affects to a team if they kill it, and the fact that it's neutral means that either team can get it.

However, one important difference is that Roshan's position is nearly all inside of the Dire portion of the map. I decided to run a test to see if this positioning meant that Dire teams who prioritized what I call Roshan Control (killing Roshan more often than your oppoents) would have a better win-rate than the raw probability.

To do this, I treated winning andnot winning as a Bernoulli trial and utilized some Bayesian magic (also known as Bayesian testing) to find the most likely P-Values. I gathered the number of wins for each team *given* that they had Roshan Control and created a binomial distribution with it.

Finally, to accomplish the Bayesian testing, I created two beta distributions for the prior probabilities, which is updated by their wins and losses as alpha and beta respectively. Here are the results after testing:

![Image]

Nope, didn't help at all! In fact, not only did it not help, but the difference between winrates went from ~4% to ~10%. In other words, if both teams prioritize Roshan Control, Radiant benifits more statistically than Dire does if they're successful.

Maybe not a great bet for Dire, then...

## Looking Forward

Unfortunately the week time constraint didn't allow me to delve any deeper on the win-rate disparity I stumbled uppon. Looking forward, I would love to revist this dataset and do the following:
* Look at win rates for teams who have higher gold totals at a given time

```
gold_adv_at_15 = {'rad_adv': 25953,
 'dire_adv': 23962,
 'rad_wins': 18150,
 'dire_wins': 16222,
 'adv_ties': 4,
 'rad_tie_wins': 3,
 'dire_tie_wins': 1}
Radiant win-rate given the most gold at 15 minutes = 0.7
Dire win-rate given the most gold at 15 minutes = 0.68
```

* Look at win rates for teams that score First Blood (first kill of the game)
* Look at win rates for teams that destroy more/less Towers (obticles needed to overcome before destroying the Fountain)
* Then eventually, string some or all of these into a Bayesian test to 
