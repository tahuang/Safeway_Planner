import tkinter as tk
from tkinter import ttk
import time
import winsound

class MasterChefTimer:
    def __init__(self, master):
        self.master = master
        self.master.title("MasterChef Tag Team Timer")

        ttk.Label(master, text="Total Time (min:sec):").grid(row=0, column=0)
        self.total_time_min_entry = ttk.Entry(master, width=5)
        self.total_time_min_entry.grid(row=0, column=1)
        self.total_time_sec_entry = ttk.Entry(master, width=5)
        self.total_time_sec_entry.grid(row=0, column=2)

        ttk.Label(master, text="Switch Time (min:sec):").grid(row=1, column=0)
        self.switch_time_min_entry = ttk.Entry(master, width=5)
        self.switch_time_min_entry.grid(row=1, column=1)
        self.switch_time_sec_entry = ttk.Entry(master, width=5)
        self.switch_time_sec_entry.grid(row=1, column=2)

        self.start_button = ttk.Button(master, text="Start", command=self.start_timer)
        self.start_button.grid(row=2, column=0, columnspan=2)

        self.total_time_left_label = ttk.Label(master, text="", font=("Helvetica", 72))
        self.total_time_left_label.grid(row=3, column=0, columnspan=2)

        self.switch_time_left_label = ttk.Label(master, text="", font=("Helvetica", 72))
        self.switch_time_left_label.grid(row=4, column=0, columnspan=2)
        
        self.timer_running = False
        self.after_id = None

    def start_timer(self):
        if self.timer_running:
            self.reset()
            
        total_min = int(self.total_time_min_entry.get())
        total_sec = int(self.total_time_sec_entry.get())
        self.total_time_left = total_min * 60 + total_sec

        switch_min = int(self.switch_time_min_entry.get())
        switch_sec = int(self.switch_time_sec_entry.get())
        self.switch_time_left = switch_min * 60 + switch_sec
        self.switch_time = self.switch_time_left

        self.timer_running = True
        self.update_timer()
        self.start_button.config(text="Reset")
            
    def reset(self):
        if self.after_id:
            self.master.after_cancel(self.after_id)        
        self.timer_running = False
        self.total_time_left = 0
        self.switch_time_left = 0
        self.total_time_left_label.config(text="")
        self.switch_time_left_label.config(text="")
        self.start_button.config(text="Start")    

    def update_timer(self):
        if self.total_time_left > 0:
            self.total_time_left -= 1
            min_left, sec_left = divmod(self.total_time_left, 60)
            self.total_time_left_label.config(text=f"Total Time: {min_left}:{sec_left:02d}")

            self.switch_time_left -= 1
            switch_min_left, switch_sec_left = divmod(self.switch_time_left, 60)
            self.switch_time_left_label.config(text=f"Switch Time: {switch_min_left}:{switch_sec_left:02d}")

            if self.switch_time_left == 0:
                winsound.Beep(1000, 1000)
                self.switch_time_left = self.switch_time

            self.after_id = self.master.after(1000, self.update_timer)
        else:
            self.total_time_left_label.config(text="Time's Up!")
            self.switch_time_left_label.config(text="")

if __name__ == "__main__":
    root = tk.Tk()
    app = MasterChefTimer(root)
    root.mainloop()
