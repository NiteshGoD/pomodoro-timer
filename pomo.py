import time
import sys
from playsound import playsound
import tkinter as tk
from tkinter import ttk

DEFAULT_FOCUS_TIME = 25.0 * 60
DEFAULT_REST_TIME = 5.0 * 60
DEFAULT_LONG_REST_TIME = 30.0 * 60

class PomodoroTimer():
    """Pomodoro Timer Class"""
    def __init__(self,focus_time = DEFAULT_FOCUS_TIME, rest_time = DEFAULT_REST_TIME, long_rest_time = DEFAULT_LONG_REST_TIME):
        self.focus_interval = focus_time
        self.rest_interval = rest_time
        self.long_rest_interval = long_rest_time
        self.start = 0.0
        self.elapsedtime = 0.0

    def set_starttime(self, starttime : float):
        """set start time"""
        self.start = starttime

    def set_elapsedtime(self, elapsedtime: float):
        """set elapsed time"""
        self.elapsedtime = elapsedtime

    def edit_time(self, focus_time, rest_time = None, long_rest_time = None):
        """edit focus time , rest_time and long_rest_time will be used when the project is updated"""
        if focus_time:
            self.focus_interval = focus_time
        elif rest_time:
            self.rest_interval = rest_time
        elif long_rest_time:
            self.long_rest_interval = long_rest_time

    def get_time_format(self, time_in_seconds):
        """gets the minutes , seconds format"""
        minutes = int(time_in_seconds/60)
        seconds = int(time_in_seconds - minutes * 60.0)
        hseconds = int((time_in_seconds - minutes * 60.0-seconds) * 100)
        return (minutes,seconds,hseconds)
    
    def time_decrement(self, elapsed_time_in_seconds):
        """Reduce the elapsed seconds from the focus interval"""
        time_decreased = self.focus_interval - elapsed_time_in_seconds
        if time_decreased >= 0:
            return time_decreased
        return 0.0
        # sys.exit()
    
    def play_alarm(self):
        """Sounds the alarm"""
        print("Alarm playing")
        playsound("electric_alarm.mp3")
        print("Alarm played!!")


class PomodoroTimerWidget(tk.Frame):
    """Implements a Pomodoro timer frame widget"""

    def __init__(self, parent = None , **kw):
        tk.Frame.__init__(self,parent,kw)
        self.pomo_timer = PomodoroTimer()
        self.time_str = tk.StringVar()
        self._start = 0.0
        self._elapsed_secs = 0.0
        self._running = False
        self.count_down = None
        # make widget
        self.columnconfigure(0,weight=1)
        self.columnconfigure(1,weight=1)
        # self.columnconfigure(2,weight=1)
        self._timer = None
        self.make_widget()

    def set_intervals(self, mins :str="0", seconds : str ="0"):
        """Sets the new interval provided by user"""
        if mins == "":
            mins = "0"
        if seconds == "":
            seconds = "0"
        if mins.isnumeric() and seconds.isnumeric():
            new_interval = int(mins) * 60 + int(seconds)
            self.pomo_timer.edit_time(focus_time=float(new_interval))
            self.set_time_str(float(new_interval))
        else:
            sys.exit()

    def set_time_str(self, elapsed_secs):
        """String representation of the time"""
        minutes, seconds, hseconds = self.pomo_timer.get_time_format(elapsed_secs)
        self.time_str.set('%02d:%02d' % (minutes, seconds))

    def make_widget(self):
        """Creates widgets"""
        padding = {
            "padx":5,
            "pady":5
        }
        time_label = tk.Label(self, textvariable=self.time_str, font=("Arial", 20))
        self.set_time_str(DEFAULT_FOCUS_TIME)
        # time_label.pack(fill=tk.X, expand = tk.NO, pady= 10 , padx =2)
        ttk.Label(self, text="Timer:").grid(column=0, row=0, **padding)
        time_label.grid(column=1, row=0, **padding)

    def _update(self):
        """Update the timer value after every 50 milliseconds"""
        self._elapsed_secs = time.time() - self._start
        self.count_down = self.pomo_timer.time_decrement(self._elapsed_secs)
        self.set_time_str(self.count_down)
        if self.count_down == 0.0:
            #Sound the alarm
            self.pomo_timer.play_alarm()
            self._running = False
            self._elapsed_secs = 0.0
            self._start = 0.0
            return
        self._timer = self.after(50, self._update)

    def reset(self):
        """ Reset the pomodoro session """
        self._start = 0.0
        self._elapsed_secs = 0.0
        self.count_down = self.pomo_timer.time_decrement(self._elapsed_secs)
        self.set_time_str(self.count_down)

    def start(self):
        """Starts the pomodoro timer"""
        if self._running is False:
            self._start = time.time() - self._elapsed_secs
            self._update()
            self._running = True

    def stop(self):
        """Stops or pauses the pomodoro timer"""
        if self._running is True:
            self.after_cancel(self._timer)
            self._elapsed_secs = time.time() - self._start
            # self.set_time_str(self._elapsed_secs)
            self.count_down = self.pomo_timer.time_decrement(self._elapsed_secs)
            self.set_time_str(self.count_down)
            self._running = False
        
class App(tk.Tk):
    """Main App Widget"""
    def __init__(self):
        super().__init__()
        self.title("Pomodoro Timer")
        self.geometry("400x200")
        # self.pomodoro_widget = PomodoroTimerWidget(self)
        self.user_mins = tk.StringVar()
        self.user_secs = tk.StringVar()
        # self.pomodoro_widget.pac
        # self.interval_setting_widget = tk.Frame(self)
        self.columnconfigure(0,weight=1)
        self.columnconfigure(1,weight =1)
        self.columnconfigure(2, weight= 1)
        self.create_widgets()

    def create_widgets(self):
        """Creates widgets"""
        self.pomodoro_widget = PomodoroTimerWidget(self)
        padding = {
            "padx" : 2,
            "pady" : 2
        }
        self.pomodoro_widget.grid(column=1,row=0,**padding)
        settings_frame = tk.Frame(self)
        settings_frame.grid(column=1,row=1,**padding)
        ttk.Label(settings_frame,text="minutes:").grid(column=0,row=0,**padding)
        min_entry = ttk.Entry(settings_frame,textvariable=self.user_mins)
        min_entry.grid(column=1,row=0,**padding)
        ttk.Label(settings_frame,text="seconds").grid(column=0,row=1, **padding)
        sec_entry = ttk.Entry(settings_frame,textvariable=self.user_secs)
        sec_entry.grid(column = 1, row = 1,**padding)
        entry_btn = ttk.Button(settings_frame,text="set timer",command= lambda : self.pomodoro_widget.set_intervals(mins=self.user_mins.get(),seconds=self.user_secs.get()))
        entry_btn.grid(column=1,row=2, **padding)
        operation_frame = ttk.Frame(self)
        operation_frame.grid(column=1,row=2,**padding)
        tk.Button(operation_frame, text='Start', command=self.pomodoro_widget.start).grid(column=0,row=0,**padding)
        tk.Button(operation_frame, text='Pause', command=self.pomodoro_widget.stop).grid(column=1,row =0,**padding)
        tk.Button(operation_frame, text="Reset", command=self.pomodoro_widget.reset).grid(column=2,row=0,**padding) 


if __name__ == "__main__":
    # main()
    app = App()
    app.mainloop()