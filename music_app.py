import os
import glob
import tkinter as tk
from tkinter import filedialog, messagebox
from pygame import mixer
import time

def scan_audio_files(directory):
    audio_extensions = ['.mp3', '.wav', '.ogg', '.flac']
    audio_files = []
    for ext in audio_extensions:
        audio_files.extend(glob.glob(os.path.join(directory, f'**/*{ext}'), recursive=True))
    return audio_files

class MusicApp:
    def __init__(self, root):
        mixer.init()  # Must be first

        self.root = root
        self.root.title("🎵 Music Player")
        self.root.geometry("800x640")
        self.root.configure(bg="#121212")

        self.file_list = []
        self.filtered_list = []
        self.current_index = None
        self.paused = False
        self.song_length = 0
        self.seek_offset = 0
        self.user_dragging = False

        self.search_entry = tk.Entry(root, font=('Segoe UI', 12), width=40, bg="#1e1e1e", fg="#ffffff", insertbackground="white")
        self.search_entry.pack(pady=10)
        self.search_entry.bind("<KeyRelease>", self.search_audio)

        self.playlist = tk.Listbox(root, width=85, height=15, font=('Segoe UI', 11),
                                   bg="#1e1e1e", fg="white", selectbackground="#03DAC6", borderwidth=0)
        self.playlist.pack(pady=5)

        self.seek_slider = tk.Scale(root, from_=0, to=100, orient=tk.HORIZONTAL, length=600,
                                    bg="#121212", fg="white", troughcolor="#03DAC6", highlightthickness=0)
        self.seek_slider.pack(pady=10)
        self.seek_slider.bind("<Button-1>", self.on_slider_press)
        self.seek_slider.bind("<ButtonRelease-1>", self.on_slider_release)

        self.now_playing = tk.Label(root, text="Now Playing: ", font=('Segoe UI', 12), fg="#BB86FC", bg="#121212")
        self.now_playing.pack()

        self.button_frame = tk.Frame(root, bg="#121212")
        self.button_frame.pack(pady=10)

        self.make_button("⏮ Previous", self.play_previous, 0)
        self.make_button("▶ Play", self.play_audio, 1)
        self.make_button("⏸ Pause", self.pause_audio, 2)
        self.make_button("⏭ Next", self.play_next, 3)
        self.make_button("🗑️ Delete", self.delete_audio, 4)
        self.make_button("🔤 Sort A-Z", self.sort_audio, 5)
        self.make_button("📁 Choose Folder", self.choose_directory, 6)

        # 🎚️ Volume control
        self.volume_frame = tk.Frame(root, bg="#121212")
        self.volume_frame.pack(pady=5)

        tk.Label(self.volume_frame, text="🔊 Volume", font=('Segoe UI', 10), bg="#121212", fg="white").pack()
        self.volume_slider = tk.Scale(self.volume_frame, from_=0, to=100, orient=tk.HORIZONTAL,
                                      length=150, command=self.set_volume,
                                      bg="#121212", fg="white", troughcolor="#03DAC6", highlightthickness=0)
        self.volume_slider.set(70)  # Default volume
        self.volume_slider.pack()
        mixer.music.set_volume(0.7)

        self.status = tk.Label(root, text="Ready", font=('Segoe UI', 10), bg="#121212", fg="gray")
        self.status.pack(side=tk.BOTTOM, fill=tk.X)

        self.root.after(1000, self.track_position)
        self.root.after(2000, self.check_song_end)
        self.time_label = tk.Label(root, text="00:00 / 00:00", font=('Segoe UI', 10), fg="white", bg="#121212")
        self.time_label.pack()


    def make_button(self, text, command, col):
        btn = tk.Button(self.button_frame, text=text, font=('Segoe UI', 10, 'bold'), width=12, height=2,
                        bg="#03DAC6", fg="#000000", activebackground="#018786", command=command,
                        relief="flat", borderwidth=0, cursor="hand2")
        btn.grid(row=0, column=col, padx=4)

    def choose_directory(self):
        folder = filedialog.askdirectory()
        if folder:
            self.file_list = scan_audio_files(folder)
            self.filtered_list = self.file_list.copy()
            self.update_playlist()
            self.status.config(text=f"Loaded {len(self.filtered_list)} files")

    def update_playlist(self):
        self.playlist.delete(0, tk.END)
        for file in self.filtered_list:
            self.playlist.insert(tk.END, os.path.basename(file))

    def play_audio(self):
        selected = self.playlist.curselection()
        if selected:
            index = selected[0]
            self.current_index = index
            file_path = self.filtered_list[index]
            try:
                mixer.music.load(file_path)
                mixer.music.play()
                self.seek_offset = 0
                self.song_length = self.get_song_length(file_path)
                self.seek_slider.config(to=int(self.song_length))
                self.paused = False
                self.now_playing.config(text="Now Playing: " + os.path.basename(file_path))
                self.status.config(text="Playing")
            except Exception as e:
                messagebox.showerror("Error", f"Could not play the file.\n{e}")
                self.status.config(text="Error while playing")

    def pause_audio(self):
        if not self.paused:
            mixer.music.pause()
            self.paused = True
            self.status.config(text="Paused")
        else:
            mixer.music.unpause()
            self.paused = False
            self.status.config(text="Resumed")

    def play_next(self):
        if self.current_index is not None and self.current_index < len(self.filtered_list) - 1:
            self.playlist.selection_clear(0, tk.END)
            self.current_index += 1
            self.playlist.selection_set(self.current_index)
            self.play_audio()

    def play_previous(self):
        if self.current_index is not None and self.current_index > 0:
            self.playlist.selection_clear(0, tk.END)
            self.current_index -= 1
            self.playlist.selection_set(self.current_index)
            self.play_audio()

    def delete_audio(self):
        selected = self.playlist.curselection()
        if selected:
            index = selected[0]
            file_path = self.filtered_list[index]
            confirm = messagebox.askyesno("Confirm Delete", f"Delete '{os.path.basename(file_path)}'?")
            if confirm:
                try:
                    os.remove(file_path)
                    self.file_list.remove(file_path)
                    self.filtered_list.remove(file_path)
                    self.update_playlist()
                    self.now_playing.config(text="")
                    self.status.config(text="File deleted")
                except Exception as e:
                    messagebox.showerror("Error", f"Could not delete the file.\n{e}")

    def sort_audio(self):
        self.filtered_list.sort(key=lambda x: os.path.basename(x).lower())
        self.update_playlist()
        self.status.config(text="Sorted A-Z")

    def search_audio(self, event=None):
        query = self.search_entry.get().lower()
        self.filtered_list = [file for file in self.file_list if query in os.path.basename(file).lower()]
        self.update_playlist()
        self.status.config(text=f"{len(self.filtered_list)} results found")

    def seek_position(self, value):
        try:
            new_pos = float(value)
            self.seek_offset = new_pos
            mixer.music.play(start=new_pos)
            self.paused = False
            self.status.config(text=f"Jumped to {int(new_pos)} sec")
        except:
            pass

    def on_slider_press(self, event):
        self.user_dragging = True

    def on_slider_release(self, event):
        self.user_dragging = False
        self.seek_position(self.seek_slider.get())

    def get_song_length(self, file_path):
        try:
            from mutagen.mp3 import MP3
            from mutagen.wave import WAVE
            if file_path.endswith(".mp3"):
                return MP3(file_path).info.length
            elif file_path.endswith(".wav"):
                return WAVE(file_path).info.length
        except:
            return 100
        return 100

    def track_position(self):
        if mixer.music.get_busy() and not self.paused and not self.user_dragging:
            try:
                current_pos = mixer.music.get_pos() // 1000
                actual_pos = int(self.seek_offset + current_pos)
                if actual_pos <= self.song_length:
                    self.seek_slider.set(actual_pos)

                # Format time as MM:SS
                def format_time(seconds):
                    mins = int(seconds // 60)
                    secs = int(seconds % 60)
                    return f"{mins:02d}:{secs:02d}"

                current_str = format_time(actual_pos)
                total_str = format_time(self.song_length)
                self.time_label.config(text=f"{current_str} / {total_str}")

            except:
                pass
        self.root.after(1000, self.track_position)


    def check_song_end(self):
        if not mixer.music.get_busy() and not self.paused and self.current_index is not None:
            self.play_next()
        self.root.after(2000, self.check_song_end)

    def set_volume(self, val):
        volume = float(val) / 100
        mixer.music.set_volume(volume)
        self.status.config(text=f"Volume: {int(float(val))}%")

# Run app
if __name__ == "__main__":
    root = tk.Tk()
    app = MusicApp(root)
    root.mainloop()
