# Only put working code here

# standard imports
import pandas as pd
import matplotlib.pyplot as plt
import scipy.stats as stats
import numpy as np

#reading in data
match_out = pd.read_csv('data/match_outcomes.csv')
match = pd.read_csv('data/match.csv')
player_time = pd.read_csv('data/player_time.csv')


def TeamGoldTotals(match_id,num_of_points=1):
    '''
    params:
    int of the match_id
    
    returns:
    np.array of gold totals for team 1 and 2 at the end of the match.
    
    TODO:
    take num_of_pts to make a np.linspace range and pull points from that as an evenly-spaced index range
    '''
    match_df = player_time[player_time['match_id']==match_id]
    team1 = (match_df.iloc[-1][2] +
            match_df.iloc[-1][5] +
            match_df.iloc[-1][8] +
            match_df.iloc[-1][11] +
            match_df.iloc[-1][14])
    
    team2 = (match_df.iloc[-1][17] +
            match_df.iloc[-1][20] +
            match_df.iloc[-1][23] +
            match_df.iloc[-1][26] +
            match_df.iloc[-1][29])
    
    return np.array([team1,team2])

def GoldValsThruMatch(match_id):
    '''
    params:
    match_id = int corresponding to the match_id column
    
    returns a (2 x n) np.array 
    '''
    
    match_df = player_time[player_time['match_id']==match_id]
    team1 = []
    team2 = []
    
    for i in range(len(match_df.index)):
        t1, t2 = TeamGoldTotals(match_id, i)
        team1.append(t1)
        team2.append(t2)
    
    return np.array([team1,team2])


if __name__ == '__main__':

    #plotting
    fig, ax = plt.subplots()

    ax.plot(GoldValsThruMatch(50)[0], label='Team1')
    ax.plot(GoldValsThruMatch(50)[1], label='Team2')

    #Formatting
    ax.set_title('Team gold totals over the course of the match')
    ax.set_xlabel('Match Time')
    ax.set_ylabel('Team Gold Total')
    ax.legend()
    fig.show();