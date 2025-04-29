import json
import os
from config_loader import load_config

MUSCLE_GROUPS = load_config("muscle_groups.json")
SET_CONFIG = load_config("set_config.json")
RIR_SCHEMES = load_config("rir_schemes.json")

class Mesocycle:
    def __init__(self, name, duration):
        self.name = name
        self.duration = duration
        self.data = {week: {muscle: {"goal": 0, "actual": 0} for muscle in MUSCLE_GROUPS}for week in range(1, duration+1)}

    def set_goal(self, week, muscle, sets):
        self.data[week][muscle]["goal"] = sets

    def log_actual(self, week, muscle, sets):
        self.data[week][muscle]["acutal"] = sets

    def print_week(self, week):
        print(f"\n Week {week} (RIR: {self.rir_scheme[week-1]})")

    def save(self):
        os.makedirs("data", exist_ok=True)
        with open(f"data/{self.name}.json", "w") as f:
            json.dump(self.__dict__, f, indent = 4)

    def load(name):
        with open(f"data/{name}.json", "r") as f:
            obj = json.load(f)
            cycle = Mesocycle(obj['name'], obj['duration'])
            cycle.rir_scheme = obj['rir_scheme']
            cycle.data = obj['data']
            return cycle
        
    def generate_balanced(self, duration, specialization): 
        self.rir_scheme = RIR_SCHEMES[f"{duration}"]
        
        for week in range(1, duration+1):
            self.data[week] = {}
            for muscle in MUSCLE_GROUPS:
                if SET_CONFIG and muscle in SET_CONFIG:
                    start = SET_CONFIG[muscle]["start"]
                    inc_pct = SET_CONFIG[muscle]["increase"]
                    if specialization==muscle:
                        goal = int(start * ((1 + 20 / 100) ** (week - 1)))
                    elif specialization=="None":
                        goal = int(start * ((1 + inc_pct / 100) ** (week - 1)))
                else:
                    goal = 0
                self.data[week][muscle] = {"goal": goal, "actual": 0}

        

