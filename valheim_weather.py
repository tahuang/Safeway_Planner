import tkinter as tk
from tkinter import ttk
from datetime import timedelta, datetime
import math
import time

from valheim_wind_forecast import forecast_wind

GAME_HOUR_PER_REAL_MINUTE = 24.0 / 30.0

def game_time_to_real_time(game_time_hrs):
    # Converts game time to real time.
    # A 24 hour day in the game equals 30 min of real time.
    return game_time_hrs / GAME_HOUR_PER_REAL_MINUTE
    
def real_time_to_game_time(real_time_mins):
    # Converts real time to game time
    return real_time_mins * GAME_HOUR_PER_REAL_MINUTE



class Valheim_Forecast:
    def __init__(self, root):
        
        self.root = root
        
        # Create default start time
        self.start_time = time.time()
        self.day = 1

        self.root.title("Timer Application")
        
        # Creating widgets
        self.day_label = tk.Label(root, text="Day")
        self.day_entry = tk.Entry(root)
        
        self.game_time_label = tk.Label(root, text="Est. Game Time")
        self.game_time_entry = tk.Entry(root)
        
        self.set_day_button = tk.Button(root, text="Set Day", command=self.set_day)
        self.set_dawn_button = tk.Button(root, text="Set Dawn", command=self.set_dawn)
        self.set_game_time_button = tk.Button(root, text="Set Game Time", command=self.set_game_time)
        
        self.real_time_label = tk.Label(root, text="Real Time: 0:00")
        self.game_time_timer_label = tk.Label(root, text="Game Time: 0:00")
        self.time_til_night_label = tk.Label(root, text="Time til Night: 20:00")
        
        # Define the for a weather readout
        columns = ('Current','Real Time', 'Direction', 'Game Time')
        
        self.wind_table = ttk.Treeview(root, columns=columns, show='headings', height=20)
        
        
        # Layout
        self.day_label.pack()
        self.day_entry.pack()
        self.game_time_label.pack()
        self.game_time_entry.pack()
        self.set_day_button.pack()
        self.set_dawn_button.pack()
        self.set_game_time_button.pack()
        self.real_time_label.pack()
        self.game_time_timer_label.pack()
        self.time_til_night_label.pack()
        self.wind_table.pack(side='bottom', fill='x')
        
        self.update_timers()        

        
    def update_timers(self):
        elapsed_min = (time.time() - self.start_time)/60
        if elapsed_min > 30:
            self.start_time = time.time()
            elapsed_min = (time.time() - self.start_time)/60
            self.set_day(new_day=self.day+1)
            
        self.day_label.config(text="Day: {:d}".format(self.day))  
        
        # Real Time Timer: Loop every 30 minutes
        real_time_str = self.get_time_str(elapsed_min)
        self.real_time_label.config(text=f"Real Time: {real_time_str}")
        
        real_minutes_decimal = elapsed_min
        
        game_time_decimal = real_time_to_game_time(real_minutes_decimal)
        
        # Real Time Timer: Loop every 24 hours
        game_time_str = self.get_time_str(game_time_decimal)
        self.game_time_timer_label.config(text=f"Game Time: {game_time_str}")  
        
        # Convert real to time til night
        # dawn is 4.5 minutes in real time after midnight
        time_til_next_dawn = (34.5 - elapsed_min) % 30
        is_night = elapsed_min < 4.5 or elapsed_min > 25.5
        if not is_night:
            ttn_time_str = self.get_time_str(time_til_next_dawn - 9)
            self.time_til_night_label.config(text=f"Time til Night: {ttn_time_str}")
        else:
            ttn_time_str = self.get_time_str(time_til_next_dawn)
            self.time_til_night_label.config(text=f"Time til Dawn: {ttn_time_str}")            
        self.elasped_min = elapsed_min
        
        self.color_current_time_row()
        
        root.after(1000, self.update_timers)
    
    def set_dawn(self):
        self.start_time = time.time() - 4.5*60
        if self.elasped_min > 20:
            self.set_day(new_day=self.day+1)
        
        ## Set the game time to morning (03:36).
        #self.game_time_timer_label.config(text="Game Time: 03:36")
        #self.game_time_entry.insert(0, "03:36")
        
        ## Set the real time to the corresponding time.
        #game_time_hours = 3 + 36.0 / 60.0
        #real_time_min = game_time_to_real_time(game_time_hours)
        #real_minutes = math.trunc(real_time_min)
        #real_sec = (real_time_min - real_minutes) * 60
        #real_time_str = f"{real_minutes:02d}:{real_sec:02d}"    
        #self.real_time_label.config(text=f"Real Time: {real_time_str}")
        
    def get_time_str(self, minutes_decimal):
        # can also be used for hours/minutes
        minutes = math.trunc(minutes_decimal)
        seconds = (minutes_decimal - minutes) * 60
        if seconds < 0:
            seconds *= -1
        time_str = f"{minutes:02d}:{int(seconds):02d}"    
        return time_str
    
    def set_game_time(self):
        # Logic to set game time based on user input
        game_time_string = self.game_time_entry.get()
        try:
            hrs, mins = game_time_string.split(':')
            game_time_hrs = float(hrs) + float(mins)/60
            real_time_min = game_time_to_real_time(game_time_hrs)
            self.start_time = time.time() - real_time_min * 60
        except ValueError:
            pass
    
    def set_day(self, new_day = None):
        if new_day is None:
            try:
                self.day = int(self.day_entry.get())
            except ValueError:
                self.day = 1
        else:
            self.day = new_day
            
        self.update_wind_table()
            
    def update_wind_table(self):
        times, winds = forecast_wind(self.day)
        
        for item in self.wind_table.get_children():
            self.wind_table.delete(item)        
        
        for time, wind in zip(times, winds):
            time_str = self.get_time_str(time)
            game_time_str = self.get_time_str(real_time_to_game_time(time))
            self.wind_table.insert('', 'end', values=('',time_str, str(round(wind)), game_time_str))
        
        aa = 0
        
    def color_current_time_row(self):
        # Example function to add a row to the table
        # Replace with your actual data retrieval logic
        children = self.wind_table.get_children()
        for i, child in enumerate(children):
            mins, secs = [int(val) for val in self.wind_table.item(child)['values'][1].split(':')]
            real_time_start = mins + secs/60
            child_vals = self.wind_table.item(child)['values']
            self.wind_table.item(child, values=['']+child_vals[1:])
            self.wind_table.item(child, tags=())
            if real_time_start > self.elasped_min and i != 0:
                mark_child = children[i-1]
                mark_child_vals = self.wind_table.item(mark_child)['values']
                self.wind_table.item(mark_child, values=['x']+mark_child_vals[1:])   
                self.wind_table.item(mark_child, tags=('colored',))
                self.wind_table.tag_configure('colored', background='lightblue')
                break
            aa = 0
    
if __name__ == "__main__":
    root = tk.Tk()
    app = Valheim_Forecast(root)
    root.mainloop()