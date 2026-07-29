import customtkinter as ctk
from dashboard import Dashboard

root = ctk.CTk()
root.geometry("2000x800")

app = Dashboard(root)

root.mainloop()