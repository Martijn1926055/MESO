import json
import os

def load_muscle_groups():
    with open("muscle_groups.json", "r") as f:
        return json.load(f)
    
MUSCLE_GROUPS = load_muscle_groups()

def load_set_config():
    with open("set_config.json", "r") as f:
        return json.load(f)

SET_CONFIG = load_set_config()


class Mesocycle:
    def __init__(self, name, duration):
        self.name = name
        self.duration = duration
        self.rir_scheme = [3, 2, 2, 1, 1, 0, "Deload"][:duration]
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
        
    def generate_balanced(self, name, duration, specialization): 
        self.name = name
        
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

        

