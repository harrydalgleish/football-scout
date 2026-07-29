import customtkinter as ctk
#from playerview import PlayerView
from mplsoccer import Pitch
from utils.data_loader import load_competitions

class Dashboard:
    def __init__(self, root):
        self.root = root

        self.create_sidebar()
        self.create_mainview()
        self.create_formation()

    def create_sidebar(self):
        competitions = load_competitions()
        competition_names = [comp["competition_name"] for comp in competitions]
        self.sidebar = ctk.CTkFrame(
            self.root,
            width = 400
        )
        self.sidebar.pack(
            side="left",
            fill="y"
        )
        self.title = ctk.CTkLabel(
            self.sidebar,
            text="Selection",
            font=("Arial",22,"bold")
        )
        self.competitiontitle = ctk.CTkLabel(
            self.sidebar,
            text="Competition",
        )
        self.competitiondropdown = ctk.CTkOptionMenu(
            self.sidebar,
            values = competition_names
        )

        self.title.pack(pady=20)
        self.competitiontitle.pack(pady=20)
        self.competitiondropdown.pack(pady=10,padx=20)

        

    def create_mainview(self):
        pass

    def create_formation(self):
        pass
