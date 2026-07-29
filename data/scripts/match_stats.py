import json
import pandas as pd

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

    
    with open(f"data/raw/player_stats/{match_id}_player_stats.json", "w") as file:
        json.dump(players, file, indent=4)


match_stats(3749493)