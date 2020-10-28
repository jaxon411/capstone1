# Only put working code here

# standard imports
import pandas as pd
import matplotlib.pyplot as plt
import scipy.stats as stats
import numpy as np

#reading in data
df_match_out = pd.read_csv('data/match_outcomes.csv')
df_match = pd.read_csv('data/match.csv')
df_player_time = pd.read_csv('data/player_time.csv')


def TeamGoldTotals(match_id, time_index=-1):
    '''
    params:
    match_id = int corresponding to the match_id column
    time_index = index to grab gold totals at, default is the last timestamp of the match
    
    returns:
    2 ints of gold totals of team 1 and 2 at the end of the match.
    '''
    
    match_view = df_player_time[df_player_time['match_id']==match_id]
    team1 = (match_view.iloc[time_index][2] +
            match_view.iloc[time_index][5] +
            match_view.iloc[time_index][8] +
            match_view.iloc[time_index][11] +
            match_view.iloc[time_index][14])
    
    team2 = (match_view.iloc[time_index][17] +
            match_view.iloc[time_index][20] +
            match_view.iloc[time_index][23] +
            match_view.iloc[time_index][26] +
            match_view.iloc[time_index][29])
    
    return team1,team2

def GoldValsThruMatch(match_id):
    '''
    params:
    match_id = int corresponding to the match_id column
    
    returns 2 np.arrays with team gold values at each time interval
    and a np.array of list of time intervals in minutes(for graphing)
    '''
    
    match_df = df_player_time[df_player_time['match_id']==match_id]
    team1 = []
    team2 = []
    
    for i in range(len(match_df.index)):
        t1, t2 = TeamGoldTotals(match_id, i)
        team1.append(t1)
        team2.append(t2)
    
    return np.array(team1),np.array(team2), np.array(match_df['times']//60)


def GetMatchWinner(match_id):
    '''
    params:
    match_id=int of match_id primary key
    
    returns:
    string of team that won and string for plotting color. Team 1 corresponds to radiant, Team 2 corresponds to dire.
    '''
    #the indexes of df_match are idential to the match_id's in ascending order
    specific_match = df_match.iloc[match_id]
    if specific_match['radiant_win']:
        return 'Team 1','blue'
    else:
        return 'Team 2','red'

if __name__ == '__main__':

    #plotting
    example_match = np.random.randint(0,50000)
    winner,win_color = GetMatchWinner(example_match)
    y1,y2,x = GoldValsThruMatch(example_match)

    fig, ax = plt.subplots()

    ax.plot(x,y1, label='Team1',color='blue')
    ax.plot(x,y2, label='Team2',color='red')

    #Formatting
    ax.set_title('Team gold totals over the course of the match \n (match_id={})'.format(example_match),y=1.1,fontsize=18)
    ax.set_xlabel('Match Time (in minutes)')
    ax.set_ylabel('Team Gold Total', rotation=0, labelpad=60)
    ax.text(0.5,.8,"Match Winner: \n" + winner,
            bbox=dict(edgecolor=win_color,facecolor='none',pad=5),
            horizontalalignment='center',
            verticalalignment='center',
            transform=ax.transAxes)
    ax.legend()
    fig.show()