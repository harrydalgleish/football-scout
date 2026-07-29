import customtkinter as ctk
from playerview import PlayerView
from mplsoccer import Pitch

class Dashboard:
    def __init__(self, root)
        self.root = root

        self.create_sidebar()
        self.create_mainview()
        self.create_formation()

    def create_sidebar(self):
        self.sidebar = ctk.CTkFrame(
            self.root,
            width = 400
        )
        self.sidebar.pack(
            side="left",
            fill="y"
        )
        title = ctk.CTkLabel(
            self.sidebar,
            text="Selection",
            font=("Arial",22,"bold")
        )
        competitiontitle = ctk.CTkLabel(
            self.sidebar,
            text="Competition",
        )
        competitiondropdown = ctk.CTkOptionMenu(
            self.sidebar,
            values = competition_names
        )
        

    def create_mainview(self):

    def create_formation(self):
