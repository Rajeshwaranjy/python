from tkinter import *
import time

class Stopwatch(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)

        self.start_button =Button(self, text="Start", command=self.start,width=20,height=1,font=("arial", 30),bg='black',fg='white')
        self.stop_button =Button(self, text="Stop", command=self.stop,width=20,height=1,font=("arial", 30),bg='black',fg='white')
        self.reset_button =Button(self, text="Reset", command=self.reset,width=20,height=1,font=("arial", 30),bg='black',fg='white')
        self.time_label = Label(self, text="00:00:00:00",width=20,height=1,font=("arial", 35),bg='black',fg='white')

        self.start_button.pack()
        self.stop_button.pack()
        self.reset_button.pack()
        self.time_label.pack()

        self.is_running = False

    def start(self):
        if not self.is_running:
            self.start_time = time.time()
            self.is_running = True
            self.update_time()

    def stop(self):
        if self.is_running:
            self.is_running = False
            self.stop_time = time.time()

    def reset(self):
        self.is_running = False
        self.start_time = None
        self.stop_time = None
        self.time_label.config(text="00:00:00:00")

    def update_time(self):
        if self.is_running:
            elapsed_time = time.time() - self.start_time
            hours = int(elapsed_time // 3600)
            remaining_seconds = elapsed_time % 3600
            minutes = int(elapsed_time // 60)
            seconds = int(elapsed_time % 60)
            milliseconds = int(elapsed_time * 1000 % 1000)
            self.time_label.config(text="{:02d}:{:02d}:{:02d}:{:03d}".format(hours,minutes, seconds, milliseconds))
            self.after(10, self.update_time)

if __name__ == "__main__":
    root = Tk()
    root.config(bg='blue')
    stopwatch = Stopwatch(root)
    stopwatch.pack()
    root.mainloop()