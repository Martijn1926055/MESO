import json
import tkinter as tk
from tkinter import ttk, messagebox
from mesocycle import Mesocycle

def load_muscle_groups():
    with open("muscle_groups.json", "r") as f:
        return json.load(f)
    
MUSCLE_GROUPS = load_muscle_groups()

def load_set_config():
    with open("set_config.json", "r") as f:
        return json.load(f)

SET_CONFIG = load_set_config()

class Meso:
    def __init__(self, root):
        self.root = root
        self.root.title("MESO")
        self.cycle = None

        self.setup_gui()

    def setup_gui(self):
        self.name_entry = ttk.Entry(self.root)
        self.name_entry.insert(0, "Cycle Name")
        self.name_entry.grid(row=0, column=0)

        self.duration_entry = ttk.Entry(self.root)
        self.duration_entry.insert(0, "7")
        self.duration_entry.grid(row=0, column=1)

        ttk.Button(self.root, text="New Cycle", command=self.create_cycle).grid(row=0, column=2)
        ttk.Button(self.root, text="Load", command=self.load_cycle).grid(row=0, column=3)
        ttk.Button(self.root, text="Save", command=self.save_cycle).grid(row=0, column=4)

        #Week & Muscle Select
        self.week_var = tk.IntVar(value=1)
        self.muscle_var = tk.StringVar(value=MUSCLE_GROUPS[0])

        ttk.Label(self.root, text="Week:").grid(row=1, column=0)
        self.week_spin = ttk.Spinbox(self.root, from_=1, to=7, textvariable=self.week_var)
        self.week_spin.grid(row=1, column=1)

        ttk.Label(self.root, text="Muscle:").grid(row=1, column=2)
        self.muscle_menu = ttk.OptionMenu(self.root, self.muscle_var, *MUSCLE_GROUPS)
        self.muscle_menu.grid(row=1, column=3)

        #Goal/Actual input
        self.goal_entry = ttk.Entry(self.root)
        self.goal_entry.grid(row=2, column=0)
        ttk.Button(self.root, text="Set Goal", command=self.set_goal).grid(row=2, column=1)

        self.actual_entry = ttk.Entry(self.root)
        self.actual_entry.grid(row=2, column=2)
        ttk.Button(self.root, text="Log Actual", command=self.set_actual).grid(row=2, column=3)

        #Display
        self.output = tk.Text(self.root, height=10, width=70)
        self.output.grid(row=3, column=0, columnspan=5)

        ttk.Button(self.root, text="View Week", command=self.view_week).grid(row=4, column=0, columnspan=5)

    def create_cycle(self):
        name = self.name_entry.get()
        duration = int(self.duration_entry.get())
        self.cycle = Mesocycle(name, duration)
        messagebox.showinfo("Created", f"New cycle '{name}' created.")

    def generate_balanced_cycle(self):
        name = self.name_entry.get()
        duration = int(self.duration_entry.get())
        self.cycle = Mesocycle(name, duration)
        self.cycle.generate_balanced(duration, SET_CONFIG)
        messagebox.showinfo("Generated", f"New cycle '{name}' created")

    def set_goal(self):
        if not self.cycle: return
        week = self.week_var.get()
        muscle = self.muscle_var.get()
        sets = int(self.goal_entry.get())
        self.cycle.set_goal(week, muscle, sets)

    def set_actual(self):
        if not self.cycle: return
        week = self.week_var.get()
        muscle = self.muscle_var.get()
        sets = int(self.actual_entry.get())
        self.cycle.log_actual(week, muscle, sets)

    def view_week(self):
        if not self.cycle: return
        week = self.week_var.get()
        output = f"Week {week}:\n"
        for m in MUSCLE_GROUPS:
            g = self.cycle.data[week][m]["goal"]
            a = self.cycle.data[week][m]["actual"]    
            output += f"{m:<15} Goal: {g}  |  Actual: {a}\n"
        self.output.delete(1.0, tk.END)
        self.output.insert(tk.END, output)

    def save_cycle(self):
        if self.cycle:
            self.cycle.save()
            messagebox.showinfo("Saved", "Mesocycle saved!")

    def load_cycle(self):
        name = self.name_entry.get()
        try:
            self.cycle = Mesocycle.load(name)
            messagebox.showinfo("Loaded", f"Loaded cycle '{name}'")
        except:
            messagebox.showinfo("Error", f"Could not load cycle: {name}")

if __name__ == "__main__":
    root = tk.Tk()
    app = Meso(root)
    root.mainloop()
