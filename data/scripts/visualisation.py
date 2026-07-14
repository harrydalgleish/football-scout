import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import json
from mplsoccer import Pitch

def markerdecision(event_type):
    markerdict = {"Block":"s","Foul Committed":"x","Dribble":"o","Interception":"D","Clearance":"^"}
    return markerdict[event_type]

def arrowdecision(event_type):
    arrowdict = {"Pass":"->","Clearance":"-","Shot":"fancy"}
    return arrowdict[event_type]

def visualise(match_id):
    file = f"{match_id}.json"
    with open(f"/workspaces/football-scout/data/raw/events/{file}", "r") as file:
        match = json.load(file)
    notable_events = ["Pass",
                      "Clearance",
                      "Block",
                      "Dribble",
                      "Foul Committed",
                      "Interception",
                      "Shot"]
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

        if event_type == "Pass":
            end = event["pass"]["end_location"]

        elif event_type == "Clearance":
            if "end_location" not in event["clearance"]:
                end = start
                counter = 1
            else:
                end = event["clearance"]["end_location"]

        elif event_type == "Shot":
            end = event["shot"]["end_location"]

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

        ax.set_title(
            f"{event['minute']}' - {event['player']['name']} - {event['type']['name']}"  
        ) 

    animation = FuncAnimation(
        fig,
        update,
        frames=len(animation_events),
        interval=200,
        repeat=False
    )

    animation.save(f"/workspaces/football-scout/data/animations/{match_id}.gif", writer="pillow")

    plt.close(fig)


visualise(3749493)
print("Match Animation Created")