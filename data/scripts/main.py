#Documentation
"""
grab_competitions:
    Goal - Prints information about the competitions (SeasonID, CompetitionID, Year, Competition etc.)
download_season(CompID - Selected competition, SeasonID - Selected Season):
    Goal - Download the matches for the selected season and competition.
season_overview(CompID, SeasonID):
    Goal - Prints the different matches available from the season
download_events(match_id)
    Goal - Downloads the events of the match
match_stats(match_id)
    Goal - Create the match_stats json file
visualisation(match_id)
    Goal - Creates the gif of the game
"""

#Modules
import json
import requests
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from mplsoccer import Pitch


#Commands

def grab_competitions(): #Prints the information about competitions
    with open("/workspaces/football-scout/data/raw/competitions.json", "r") as file:
        competitions = json.load(file)
    print("Competition Name | Season Name | Competition ID | Season ID | Country Name")
    for competition in competitions:
        print(competition["competition_name"],"|", competition["season_name"],"|", competition["competition_id"],"|", competition["season_id"],"|", competition["country_name"])

def download_season(competition_id, season_id):
    specific_url = f"https://raw.githubusercontent.com/statsbomb/open-data/refs/heads/master/data/matches/{competition_id}/{season_id}.json"
    specific_file = f"{competition_id}_{season_id}.json"

    response = requests.get(specific_url)
    with open(f"data/raw/matches/{specific_file}", "w") as file:
        file.write(response.text)

def season_overview(competition_id, season_id):
    with open(f"/workspaces/football-scout/data/raw/matches/{competition_id}_{season_id}.json", "r") as file:
        matches = json.load(file)
    for game in matches:
        print(game["match_id"]," - ",(game["home_team"])["home_team_name"]," vs ",(game["away_team"])["away_team_name"])

def download_events(match_id):
    specific_url = f"https://raw.githubusercontent.com/statsbomb/open-data/refs/heads/master/data/events/{match_id}.json"
    specific_file = f"{match_id}.json"

    response = requests.get(specific_url)

    with open(f"data/raw/events/{specific_file}", "w") as file:
        file.write(response.text)

def match_stats(match_id):
    notable_events = ['Duel', 'Pass', 'Block', 'Clearance', 'Dribble', 'Foul Committed', 'Foul Won', 'Interception', 'Shot', 'Goal Keeper', 'Substitution', 'Bad Behaviour', 'Dispossessed']

    with open(f"/workspaces/football-scout/data/raw/events/{match_id}.json", "r") as file:
        result = json.load(file)

    #Enables the dictionary
    players = {}
    for i in [0,1]:
        tactic = result[i]["tactics"]
        for dictionary in tactic["lineup"]:
            players[(dictionary['player']['id'])] = {'name':(dictionary['player']['name']),
                                                    'position':dictionary['position']['name'],
                                                    'minutes':0,
                                                    'goals':0,
                                                    'assists':0,
                                                    'yellow_cards':0,
                                                    'red_cards':0,
                                                    'shots':0,
                                                    'shots_on_target':0,
                                                    'xG':0,
                                                    'passes':0,
                                                    'successful_passes':0,
                                                    'ground_pass':0,
                                                    'high_pass':0,
                                                    'low_pass':0,
                                                    'cross':0,
                                                    'successful_crosses':0,
                                                    'fouls_committed':0,
                                                    'fouls_won':0,
                                                    'saves':0,
                                                    'goals_conceded':0,
                                                    'dribble':0,
                                                    'successful_dribble':0,
                                                    'times_dispossessed':0,
                                                    'interceptions':0,
                                                    'tackles':0,
                                                    'successful_tackles':0,
                                                    'block': 0,
                                                    'clearance': 0
                                                    }

    for event in result:
        event_type = event["type"]["name"]
        if event_type in notable_events:
            if event_type == "Substitution":
                players[((event['substitution']['replacement'])['id'])] = {'name':((event['substitution']['replacement'])['name']),
                                                    'position':event['position']['name'], #Question Here
                                                    'minutes':0,
                                                    'goals':0,
                                                    'assists':0,
                                                    'yellow_cards':0,
                                                    'red_cards':0,
                                                    'shots':0,
                                                    'shots_on_target':0,
                                                    'xG':0,
                                                    'passes':0,
                                                    'successful_passes':0,
                                                    'ground_pass':0,
                                                    'high_pass':0,
                                                    'low_pass':0,
                                                    'cross':0,
                                                    'successful_crosses':0,
                                                    'fouls_committed':0,
                                                    'fouls_won':0,
                                                    'saves':0,
                                                    'goals_conceded':0,
                                                    'dribble':0,
                                                    'successful_dribble':0,
                                                    'times_dispossessed':0,
                                                    'interceptions':0,
                                                    'tackles':0,
                                                    'successful_tackles':0,
                                                    'block': 0,
                                                    'clearance': 0
                                                    }
                
    
    for event in result:
        event_type = event["type"]["name"]
        if event_type in notable_events:
            player_id = event['player']['id']
            """Code for Passes"""
            if event_type == "Pass":
                crosscount = False
                players[player_id]['passes'] += 1
                pass_type = (event['pass']['height'])['name']
                if event['pass'].get("goal_assist"):
                    players[player_id]["assists"] += 1
                if pass_type == 'Ground Pass':
                    players[player_id]['ground_pass'] += 1
                elif pass_type == 'High Pass':
                    if event['pass'].get("cross"):
                        crosscount = True
                        players[player_id]['cross'] += 1
                    else:
                        players[player_id]['high_pass'] += 1
                elif pass_type == 'Low Pass':
                    players[player_id]['low_pass'] += 1
                if event['pass'].get("outcome"):
                    if (event['pass']['outcome'])['name'] == 'Incomplete':
                        pass
                    else:
                        if crosscount:
                            players[player_id]['successful_crosses'] += 1
                            players[player_id]['passes'] -= 1
                        else:
                            players[player_id]['successful_passes'] += 1
                else:
                    if crosscount:
                        players[player_id]['successful_crosses'] += 1
                        players[player_id]['passes'] -= 1
                    else:
                        players[player_id]['successful_passes'] += 1

            elif event_type == "Shot":
                players[player_id]['shots'] += 1
                ontarget = True
                if event['shot'].get("outcome"):
                    if event['shot']['outcome']['name'] in ["Off T","Wayard","Blocked"]:
                        ontarget = False
                        pass
                    elif event['shot']['outcome']['name'] == "Goal":
                        players[player_id]['goals'] += 1
                players[player_id]['xG'] += event['shot']['statsbomb_xg']
                if ontarget:
                    players[player_id]['shots_on_target'] += 1
            
            elif event_type == "Dribble":
                players[player_id]['dribble'] += 1
                dribble_dict = event['dribble']
                if dribble_dict['outcome']['name'] == "Complete":
                    players[player_id]['successful_dribble'] += 1

            elif event_type == "Foul Committed":
                players[player_id]['fouls_committed'] += 1
                if event.get('foul_committed'):
                    if event['foul_committed'].get('card'):
                        card = event['foul_committed']['card']['name']
                        if card == "Yellow Card":
                            players[player_id]['yellow_cards'] += 1
                        elif card == "Red Card":
                            if players[player_id]['minutes'] == 0:
                                players[player_id]['minutes'] = event['minute']
                            else:
                                players[player_id]['minutes'] = event['minute'] - (90 - players[player_id]['minutes'])
                            
                            players[player_id]['red_cards'] += 1
                        elif card == "Second Yellow":
                            if players[player_id]['minutes'] == 0:
                                players[player_id]['minutes'] = event['minute']
                            else:
                                players[player_id]['minutes'] = event['minute'] - (90 - players[player_id]['minutes'])
                            players[player_id]['yellow_cards'] += 1
                            players[player_id]['red_cards'] += 1

            elif event_type == "Bad Behaviour":
                if event.get("bad_behaviour"):
                    if event["bad_behaviour"].get("card"):
                        card = event["bad_behaviour"]["card"]["name"]

                        if card == "Yellow Card":
                            players[player_id]["yellow_cards"] += 1

                        elif card == "Red Card":
                            players[player_id]["red_cards"] += 1

                        elif card == "Second Yellow":
                            players[player_id]["yellow_cards"] += 1
                            players[player_id]["red_cards"] += 1
                
            elif event_type == "Foul Won":
                players[player_id]["fouls_won"] += 1

            elif event_type == "Interception":
                if (event['interception']['outcome'])['name'] in ['Success In Play', 'Won']:
                    players[player_id]["interceptions"] += 1            
            
            elif event_type == "Clearance":
                players[player_id]["clearance"] += 1

            elif event_type == "Block":
                players[player_id]["block"] += 1

            elif event_type == "Goal Keeper":
                if (event['goalkeeper']['type'])['name'] == "Shot Saved":
                    players[player_id]['saves'] += 1
                elif (event['goalkeeper']['type'])['name'] == "Goal Conceded":
                    players[player_id]['goals_conceded'] += 1
                
            elif event_type == "Duel":
                dueldict = event["duel"]["type"]
                if (dueldict)["name"] == "Tackle":
                    players[player_id]['tackles'] += 1
                    if event["duel"]["outcome"]["name"] in ["Success Out", "Won"]:
                        players[player_id]['successful_tackles'] += 1            

            elif event_type == "Dispossessed":
                players[player_id]['times_dispossessed'] += 1

            elif event_type == "Substitution":
                time_on_pitch = 0
                half = event['period']
                minute_off = event['minute']
                if players[player_id]['minutes'] != 0:
                    time_on_pitch = minute_off - (90 - players[player_id]['minutes'])
                else:
                    if half == 1 and minute_off > 45:
                        time_on_pitch = 46
                        players[player_id]['minutes'] = 45
                    else:
                        time_on_pitch = 90 - minute_off
                players[player_id]['minutes'] = minute_off
                sub_id = event['substitution']['replacement']['id']
                players[sub_id]['minutes'] = time_on_pitch
                

    for player in players:
        if players[player]['minutes'] == 0:
            players[player]['minutes'] = 90
        else:
            pass
    for player in players:
        print(players[player])

    
    with open(f"data/player_stats/{match_id}_player_stats.json", "w") as file:
        json.dump(players, file, indent=4)

def markerdecision(event_type):
    markerdict = {"Block":"s","Foul Committed":"x","Dribble":"o","Interception":"D","Clearance":"^"}
    return markerdict[event_type]

def arrowdecision(event_type):
    arrowdict = {"Pass":"->","Clearance":"-","Shot":"fancy"}
    return arrowdict[event_type]

def visualise(match_id):
    combination = [True, True, True, True, True, True, True]
    notable_events = []
    #Input Separation
    result = input("Do you want Passes to be recorded? (Yes/No) ")
    if result.upper() == "YES":
        pass
    else:
        combination[0] = False
    result = input("Do you want Clearances to be recorded? (Yes/No) ")
    if result.upper() == "YES":
        pass
    else:
        combination[1] = False
    result = input("Do you want Blocks to be recorded? (Yes/No) ")
    if result.upper() == "YES":
        pass
    else:
        combination[2] = False
    result = input("Do you want Dribbles to be recorded? (Yes/No) ")
    if result.upper() == "YES":
        pass
    else:
        combination[3] = False
    result = input("Do you want Fouls to be recorded? (Yes/No) ")
    if result.upper() == "YES":
        pass
    else:
        combination[4] = False
    result = input("Do you want Interceptions to be recorded? (Yes/No) ")
    if result.upper() == "YES":
        pass
    else:
        combination[5] = False
    result = input("Do you want Shots to be recorded? (Yes/No) ")
    if result.upper() == "YES":
        pass
    else:
        combination[6] = False

    if combination[0]:
        notable_events.append("Pass")
    if combination[1]:
        notable_events.append("Clearance")
    if combination[2]:
        notable_events.append("Block")
    if combination[3]:
        notable_events.append("Dribble")
    if combination[4]:
        notable_events.append("Foul Committed")
    if combination[5]:
        notable_events.append("Interception")
    if combination[6]: 
        notable_events.append("Shot")
    file = f"{match_id}.json"
    with open(f"/workspaces/football-scout/data/raw/events/{file}", "r") as file:
        match = json.load(file)
    animation_events = [
        event for event in match
        if event["type"]["name"] in notable_events]
    

    pitch = Pitch(pitch_type="statsbomb")
    fig, ax = pitch.draw()
    
    def update(frame):
        ax.clear()
        pitch.draw(ax=ax)
        event=animation_events[frame]
        event_type = event["type"]["name"]

        if event_type not in notable_events:
            return

        counter = 0
        start = event["location"]

        goalcheck = 0
        if event_type == "Shot":
            end = event["shot"]["end_location"]
            if (event["shot"]["outcome"])["name"] == "Goal":
                goalcheck = 1

        if event_type == "Pass":
            end = event["pass"]["end_location"]

        elif event_type == "Clearance":
            if "end_location" not in event["clearance"]:
                end = start
                counter = 1
            else:
                end = event["clearance"]["end_location"]


        elif event_type in ["Block", "Dribble", "Foul Committed", "Interception"]:
            end = start
        
        if event_type in ["Pass", "Clearance", "Shot"] and counter == 0:
            ax.annotate("",
                        xy=(end[0], end[1]),
                        xytext=(start[0], start[1]),
                        arrowprops={
                            "arrowstyle": arrowdecision(event_type),
                            "linewidth": 2
                        })
        else:
            ax.scatter(start[0], start[1], marker=markerdecision(event_type))
            counter = 0

        ax.text(
            start[0],
            start[1] + 1,
            event["player"]["name"],
            fontsize=8
        )
        if goalcheck == 0:
            ax.set_title(
                f"{event['minute']}' - {event['player']['name']} - {event['type']['name']}"  
            ) 
        elif goalcheck == 1:
            ax.set_title(
                f"{event['minute']}' - {event['player']['name']} - {(event["shot"]["outcome"])["name"]}"
            )
            goalcheck = 0

    animation = FuncAnimation(
        fig,
        update,
        frames=len(animation_events),
        interval=200,
        repeat=False
    )

    animation_name = f"{match_id}_"
    wholegame = True
    if combination[0]:
        animation_name += "p"
    if combination[1]:
        animation_name += "c"
    if combination[2]:
        animation_name += "b"
    if combination[3]:
        animation_name += "d"
    if combination[4]:
        animation_name += "f"
    if combination[5]:
        animation_name += "i"
    if combination[6]:
        animation_name += "s"
    for i in combination:
        if i == False:
            wholegame = False
    if wholegame:
        animation_name = match_id
    animation.save(f"/workspaces/football-scout/data/animations/{animation_name}.gif", writer="pillow")

    plt.close(fig)





#Order of Commands
print(" ----- WELCOME TO FOOTBALL SCOUT ----- ")
grab_competitions()
print("Select Your CompetitionID and SeasonID")
competition_id = int(input("Please select which competition you want: "))
season_id = int(input("Please select the SeasonID for your chosen competition: "))
download_season(competition_id, season_id)
combo_id = f"{competition_id}_{season_id}"
season_overview(competition_id, season_id)
print("Select Your MatchID")
match_id = int(input("Please select the MatchID for your chosen Match: "))
download_events(match_id)
print(" ----- Match Stats ----- ")
match_stats(match_id)
print(" ----- Starting Visualisation Creation ----- ")
visualise(match_id)
print(" ----- Natch Animation Created ----- ")



