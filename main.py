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
df_objectives = pd.read_csv('data/objectives.csv')


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

def GetRoshanTeamKills ():
    df_objectives[df_objectives['subtype'] == 'CHAT_MESSAGE_ROSHAN_KILL']['player1']
    roshdf = df_objectives[df_objectives['subtype'] == 'CHAT_MESSAGE_ROSHAN_KILL']

    roshkill_wins = {'rad_kills' : 0,
                    'dire_kills': 0,
                    'rad_wins' : 0,
                    'dire_wins' : 0,
                    'kill_ties' : 0,
                    'rad_tie_wins' : 0,
                    'dire_tie_wins': 0}

    for _id in roshdf['match_id'].unique():
        #slice into _id's rows only
        current_match = roshdf[roshdf['match_id']==_id]
        #get number of radiant and dire Roshan kills in current match
        current_rad_kills = len(current_match['player1'][current_match['player1']==2])
        current_dire_kills = len(current_match['player1'][current_match['player1']==3])
        #grabs match winner so i dont have to call it 3 times
        current_winner = GetMatchWinner(_id)[0]
        
        if current_rad_kills == current_dire_kills:
            roshkill_wins['kill_ties'] += 1
            
            if current_winner == 'Team 1':
                roshkill_wins['rad_tie_wins'] += 1
            else:
                roshkill_wins['dire_tie_wins'] += 1
            
        elif current_rad_kills > current_dire_kills:
            roshkill_wins['rad_kills'] += 1
            
            if current_winner == 'Team 1':
                roshkill_wins['rad_wins'] += 1
                
        elif current_dire_kills > current_rad_kills:
            roshkill_wins['dire_kills'] += 1
            
            if current_winner == 'Team 2':
                roshkill_wins['dire_wins'] += 1

    return roshkill_wins

if __name__ == '__main__':

    #plotting grid of 16 random games total gold values
    fig, axs = plt.subplots(4,4, figsize=(18,10))

    for i in range(4):
        for j in range(4):
            example_match = np.random.randint(0,50000)
            winner,win_color = GetMatchWinner(example_match)
            y1,y2,x = GoldValsThruMatch(example_match)

            axs[i,j].plot(x,y1, label='Team1',color='blue')
            axs[i,j].plot(x,y2, label='Team2',color='red')

            #Formatting

            
            axs[i,j].text(0.5,.8,"    ",
                    bbox=dict(facecolor=win_color,pad=5),
                    horizontalalignment='center',
                    verticalalignment='center',
                    transform=axs[i,j].transAxes)
            
            axs[i,j].text(0.3,.8,"winner:",fontsize = 14,
                    bbox=dict(facecolor='none',pad=5),
                    horizontalalignment='center',
                    verticalalignment='center',
                    transform=axs[i,j].transAxes)

    axs[0,0].legend(bbox_to_anchor=(3.9, 1.6), loc='upper left', ncol=1, fontsize = 15)
            
    axs[0,1].set_title('Team gold totals over the course of the match',x=1.1,y=1.1,fontsize=25)
    axs[3,1].set_xlabel('Match Time (in minutes)',x=1.2,fontsize=25)
    axs[2,0].set_ylabel('Team\nGold', rotation=0, labelpad=40, y=1, fontsize= 20)
    fig.show()
    #end of block

    #plot of Roshan Kill Win Likelihood Under Null Hypothesis
    
    #this dict is data from GetRoshanTeamKills()
    #I'm setting it here explicitly so it won't run on __main__ every time
    rosh_kills = {'rad_kills': 16487,
    'dire_kills': 23092,
    'rad_wins': 14550,
    'dire_wins': 18017,
    'kill_ties': 4408,
    'rad_tie_wins': 2494,
    'dire_tie_wins': 1914}

    binomeal_null = stats.binom(n=rosh_kills['rad_kills'], p=.5) #null hypothesis is p of 50% win rate

    fig, ax= plt.subplots(figsize = (12,5))
    x = np.arange(rosh_kills['rad_kills'])

    ax.plot(x,binomeal_null.pmf(x))

    ax.text(0.8,0.8,"P-Value = {}".format(1-binomeal_null.cdf(14550)),fontsize = 14,
                    bbox=dict(facecolor='none',pad=5),
                    horizontalalignment='center',
                    verticalalignment='center',
                    transform=ax.transAxes)

    ax.set_xlim(7900,8600)
    ax.fill_between(x,binomeal_null.pmf(x),
                where=(x>=14550), color='blue', alpha=0.5)
    ax.set_title("Number of Wins Observed Under The Null Hypothesis\n(50/50 chance of winning given more Roshan kills)", y=1.1)
    ax.set_xlabel('Number of Wins')
    ax.set_ylabel('Probability', rotation=0, labelpad=40)
    fig.show()
    #end of block

