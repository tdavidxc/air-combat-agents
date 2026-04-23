#This class handles the running of the experiments and the collection of the results
import tkinter as tk
from tkinter import ttk, scrolledtext, filedialog
# import yaml
import os

#defining colours and style to match the colour scheme of the designed UI or similar
BG_DARK = "#2b2b2b"
BG_MID = "#3c3c3c"
BG_PANEL = "#333333"
BG_INPUT = "#4a4a4a"
FG_WHITE = "#ffffff"
FG_GREEN = "#00cc44"
FG_RED_LOG = "#ff4444"
ACCENT_GREEN = "#4caf50"
ACCENT_RED = "#e53945"
DIVIDER = "#555555"

FONT_LABEL   = ("Courier New", 9)
FONT_BOLD    = ("Courier New", 9, "bold")
FONT_TITLE   = ("Courier New", 10, "bold")
FONT_LOG     = ("Courier New", 8)
FONT_LIVE    = ("Courier New", 9)
FONT_LIVE_B  = ("Courier New", 9, "bold")


class SimulationApp(tk.Tk):
    
    def __init__(self):
        super().__init__() #initialising the main window
        self.title("Simulation Configuration")
        self.resizable(False, False)
        self.configure(bg=BG_DARK)

        #the top level layout for the config panel and the log panel on the right side
        #this is handled with frames and grids to make it easier for me
        left_frame = tk.Frame(self, bg=BG_DARK, padx=10, pady=10)
        right_frame = tk.Frame(self, bg=BG_DARK, padx=6, pady=10)
        left_frame.grid(row=0, column=0, sticky="nsew")
        right_frame.grid(row=0, column=1, sticky="nsew")
        #having methods to build the different panels
        self.build_global_settings(left_frame)
        self.build_team_panels(left_frame)
        self.build_start_stop(left_frame)
        self.build_log_panel(right_frame)
        self.build_live_panel(right_frame)

    #defining helpers with the UI creation because there is a lot of repetitiveness
    def create_label_entry(self, parent, row, col, text, default="", width=6):
        #make a label and a small entry pair and return the String Variablle
        tk.Label(parent, text=text, bg=BG_DARK, fg=FG_WHITE, font=FONT_LABEL, anchor="w").grid(row=row, column=col, sticky="w", pady=2)
        var = tk.StringVar(value=str(default))
        e = tk.Entry(parent, textvariable=var, width=width, bg=BG_INPUT, fg=FG_WHITE, insertbackground=FG_WHITE, relief="flat", font=FONT_LABEL)
        e.grid(row=row, column=col+1, sticky="w", padx=(4,10), pady=2)
        return var
    
    def create_label_dropdown(self, parent, row, col, text, choices, default=None, width=10):
        #make a label and an option menu pair then return the String Variable again
        tk.Label(parent, text=text, bg=BG_DARK, fg=FG_WHITE, font=FONT_LABEL, anchor="w").grid(row=row, column=col, sticky="w", pady=2)
        var = tk.StringVar(value=default if default else choices[0]) #the default value is either the one provided or the first choice
        om = tk.OptionMenu(parent, var, *choices) #the * is to unpack the list of choices into inputs for the option menu
        om.config(bg=BG_INPUT, fg=FG_WHITE, relief="flat", font=FONT_LABEL, width=width, indicatoron=True, highlightthickness=0)
        om["menu"].config(bg=BG_INPUT, fg=FG_WHITE, font=FONT_LABEL)
        om.grid(row=row, column=col+1, sticky="w", padx=(4, 10), pady=2)
        return var
    
    def create_section_divider(self, parent, row, colspan=4):
        #a vertical line to divide sections of the UI which can just be a simple frame
        tk.Frame(parent, bg=DIVIDER, height=1).grid(row=row, column=0, columnspan=colspan, sticky="ew", pady=(6,6))

    
    #global settings panel for things like number of runs and time per sim etc.

    def build_global_settings(self, parent):
        f = tk.Frame(parent, bg=BG_DARK)
        f.pack(fill="x", pady=(0,4))
        self.var_num_runs = self.create_label_entry(f, 0, 0, "Number of Simulation Runs", default=1, width=5)
        self.var_time_per_sim = self.create_label_entry(f, 1, 0, "Time per Simulation (s)", default=30, width=5)
        self.var_show_env = self.create_label_dropdown(f, 2, 0, "Show Environment", ["True", "False"], default="True", width=8)
        self.var_seed = self.create_label_entry(f, 3, 0, "Seed", default=67, width=5)
        self.create_section_divider(f, 4, colspan=4)

    #now making the friendly and enemy team panels which are basically the same
    def build_team_panels(self, parent):
        container = tk.Frame(parent, bg=BG_DARK)
        container.pack(fill="x")
        #the divier between the two panels
        friendly_frame = tk.Frame(container, bg=BG_DARK)
        div = tk.Frame(container, bg=DIVIDER, width=1)
        enemy_frame = tk.Frame(container, bg=BG_DARK)
        
        friendly_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 6))
        div.grid(row=0, column=1, sticky="ns")
        enemy_frame.grid(row=0, column=2, sticky="nsew", padx=(6, 0))

        #columnconfigure is a method to set the resizing behaviour of the columns in the grid
        container.columnconfigure(0, weight=1)
        container.columnconfigure(2, weight=1)
        #the things inside the friendly and enemy panels
        self.build_friendly_panel(friendly_frame)
        self.build_enemy_panel(enemy_frame)

    #methods to make the items inside the friendly and enemy panels
    def build_friendly_panel(self, parent):
        tk.Label(parent, text="Friendly", bg=BG_DARK, fg=FG_WHITE, font=FONT_TITLE).grid(row=0, column=0, columnspan=2, pady=(0,6))
        self.var_f_jets = self.create_label_entry(parent, 1, 0, "Number of Jets", default = 1)
        self.var_f_missiles = self.create_label_entry(parent, 2, 0, "Number of Missiles\nPer Jet", default = 5)
        movement_choices_jet = ["Dynamic"]
        self.var_f_jet_movement = self.create_label_dropdown(parent, 3, 0, "Jet Movement Strategy", movement_choices_jet, default=movement_choices_jet[0], width=8)
        target_choices_missile = ["direct", "predictive"]
        self.var_f_target_missile = self.create_label_dropdown(parent, 4, 0, "Missile Target\nStrategy", target_choices_missile, default=target_choices_missile[0], width=8)
        self.var_f_datalink = self.create_label_dropdown(parent, 5, 0, "Datalink", ["True", "False"], default="True", width=8)
        #missile configuration file picker
        self.build_file_picker(parent, 6, "Select\nMissile Config", "missile_config")
        self.build_file_picker(parent, 7, "Select\nJet Config", "jet_config_friendly")

    def build_enemy_panel(self, parent):
        tk.Label(parent, text="Enemy", bg=BG_DARK, fg=FG_WHITE, font=FONT_TITLE).grid(row=0, column=0, columnspan=2, pady=(0,6))
        self.var_e_jets = self.create_label_entry(parent, 1, 0, "Number of Jets", default = 3)
        self.var_e_missiles = self.create_label_entry(parent, 2, 0, "Number of Missiles\nPer Jet", default = 5)
        movement_choices_jet = ["Dynamic"]
        self.var_e_jet_movement = self.create_label_dropdown(parent, 3, 0, "Jet Movement Strategy", movement_choices_jet, default=movement_choices_jet[0], width=8)
        target_choices_missile = ["direct", "predictive"]
        self.var_e_target_missile = self.create_label_dropdown(parent, 4, 0, "Missile Target\nStrategy", target_choices_missile, default=target_choices_missile[0], width=8)
        self.var_e_datalink = self.create_label_dropdown(parent, 5, 0, "Datalink", ["True", "False"], default="True", width=8)
        #missile configuration file picker
        self.build_file_picker(parent, 6, "Select\nMissile Config", "missile_config")
        self.build_file_picker(parent, 7, "Select\nJet Config", "jet_config_enemy")

    def build_file_picker(self, parent, row, label_text, attr_name, default_label="Missile1.yaml"):
        #a drop down style button that opens a file dialog
        tk.Label(parent, text=label_text, bg=BG_DARK, fg=FG_WHITE, font=FONT_LABEL, anchor="w", justify="left").grid(row=row, column=0, sticky="w", pady=2)
        var = tk.StringVar(value=default_label)
        setattr(self, f"var_{attr_name}", var) #this is a bit of dynamic attribute setting to avoid having to write separate code for friendly and enemy missile and jet configs because the naming will just be enemy or friendly after var_
        btn = tk.Button(parent, textvariable=var, bg=BG_INPUT, fg=FG_WHITE, relief="flat", font=FONT_LABEL, width=12, anchor="w", command=lambda a=attr_name: self.on_select_config_file(a))
        btn.grid(row=row, column=1, sticky="w", padx=(4,10), pady=2)

    
    #the start and stop buttons
    def build_start_stop(self, parent):
        f = tk.Frame(parent, bg=BG_DARK)
        f.pack(fill="x", pady=(6,0))
        self.btn_start = tk.Button(f, text="Start Simulation", bg=ACCENT_GREEN, fg=FG_WHITE, font=FONT_BOLD, relief="flat", activebackground="#388e3c", width=18, command=self.on_start_simulation)
        self.btn_stop = tk.Button(f, text="Stop Simulation", bg=ACCENT_RED, fg=FG_WHITE, font=FONT_BOLD, relief="flat", activebackground="#c62828", width=18, command=self.on_stop_simulation)
        self.btn_start.pack(side="left", padx=(0, 8))
        self.btn_stop.pack(side="left")


        
    #the right side of the UI panel with the simulation log and the live information

    def build_log_panel(self, parent):
        self.log_text = scrolledtext.ScrolledText(parent, width=42, height=14, bg=BG_PANEL, fg=FG_GREEN, insertbackground=FG_GREEN, font=FONT_LOG, relief="flat", state="disabled", wrap="word")
        self.log_text.pack(fill="both", expand=True, pady=(0, 6))
        self.log('>Simulation Log. Start by clicking the "Start Simulation" Button')
        
    def build_live_panel(self, parent):
        live = tk.Frame(parent, bg=BG_PANEL, padx=8, pady=6)
        live.pack(fill="x")

        tk.Label(live, text="Live Information", bg=BG_PANEL, fg=FG_WHITE,
                font=FONT_LIVE_B).grid(row=0, column=0, columnspan=2,
                                        sticky="w", pady=(0, 4))

        stats = [
            ("Interceptions:",          "0"),
            ("Friendly Casualty:",      "0"),
            ("Friendly Fire Incidents:","0"),
            ("Interception Rate:",      "0%"),
            ("Average Interception Time:", "0s"),
            ("Kills per missile:",      "0"),
            ("Missile's out of fuel:",  "0"),
        ]

        self.live_vars = {}
        for i, (label, default) in enumerate(stats):
            tk.Label(live, text=label, bg=BG_PANEL, fg=FG_WHITE,
                    font=FONT_LIVE, anchor="w").grid(row=i+1, column=0,
                                                    sticky="w", pady=1)
            var = tk.StringVar(value=default)
            self.live_vars[label] = var
            tk.Label(live, textvariable=var, bg=BG_PANEL, fg=FG_WHITE,
                    font=FONT_LIVE).grid(row=i+1, column=1, sticky="w",
                                        padx=(6, 0), pady=1)
            

            

        
    #---------------------------------------------------------------------------
    #The actual methods that handle the button presses and all the functionality

    def on_start_simulation(self):
        #Called when the user clicks start simulation
        pass

    def on_stop_simulation(self):
        #called when the user clicks stop simulation
        pass

    def on_select_config_file(self, attr_name):
        #called when the user clicks one of the config file buttons to open a file dialog and select a new config for either the missile or the jets
        pass

    def run_single_simulation(self, run_index):
        #This is where the simulation would need to be run for a single run only
        pass

    def collect_config(self):
        #this is to Read all the UI widgets and returns a dict (or object) containing the full simulation configuration.
        pass

    def update_live_stats(self, stats_dict):
        #This is to update the live information panel when running the simulation
        pass

    def log(self, message):
        #Appends a line to the simulation log box
        self.log_text.config(state="normal")
        self.log_text.insert("end", message + "\n")
        self.log_text.see("end")
        self.log_text.config(state="disabled")

    def clear_log(self):
        #Used to clear the simulation log box
        pass

    def reset_live_stats(self):
        #Used to reset the live stats box to the default values
        pass

    def validate_config(self):
        #This checks if every config entered is valid and can be run. It needs to return a boolean to decide whether the simulation should run or not
        pass

    def on_simulation_finished(self, results):
        #Decides what to do when the simulation finishes
        #Need to save the results to C:\Users\tom24\Documents\University\Yr3\Designing Intelligent Agents\Coursework\air-combat-agents\experiments\results

        pass
 
 
#This is where this file is run
 
if __name__ == "__main__":
    app = SimulationApp()
    app.mainloop()
 

