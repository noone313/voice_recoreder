import os
import wave
import pyaudio
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk

class VoiceRecorderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Voice Recorder")
        self.root.geometry("400x300")
        self.root.configure(bg='#2C3E50')

        # Style configuration
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("TButton", font=("Helvetica", 12), padding=10)
        style.configure("TLabel", font=("Helvetica", 12), background='#2C3E50', foreground="white")
        style.configure("TEntry", font=("Helvetica", 12))

        # Frames
        self.top_frame = ttk.Frame(root)
        self.top_frame.pack(pady=20)

        self.middle_frame = ttk.Frame(root)
        self.middle_frame.pack(pady=10)

        self.bottom_frame = ttk.Frame(root)
        self.bottom_frame.pack(pady=20)

        # Status label
        self.status_label = ttk.Label(self.top_frame, text='Press "Start" to record')
        self.status_label.pack()

        # File name entry
        self.file_name_label = ttk.Label(self.middle_frame, text='File Name:')
        self.file_name_label.grid(row=0, column=0, padx=5, pady=5)

        self.file_name_entry = ttk.Entry(self.middle_frame)
        self.file_name_entry.grid(row=0, column=1, padx=5, pady=5)

        # Buttons
        self.start_button = ttk.Button(self.bottom_frame, text='Start Recording', command=self.start_recording)
        self.start_button.grid(row=0, column=0, padx=10)

        self.stop_button = ttk.Button(self.bottom_frame, text='Stop Recording', command=self.stop_recording, state=tk.DISABLED)
        self.stop_button.grid(row=0, column=1, padx=10)

        self.save_button = ttk.Button(self.bottom_frame, text='Save Recording', command=self.save_recording, state=tk.DISABLED)
        self.save_button.grid(row=0, column=2, padx=10)

        # Audio recording setup
        self.p = pyaudio.PyAudio()
        self.stream = None
        self.frames = []
        self.recording = False

    def start_recording(self):
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        self.save_button.config(state=tk.DISABLED)
        self.status_label.config(text='Recording...')

        self.frames = []
        self.stream = self.p.open(format=pyaudio.paInt16, channels=1, rate=44100, input=True, frames_per_buffer=1024)
        self.recording = True
        self.root.after(1, self.record)

    def record(self):
        if self.recording:
            data = self.stream.read(1024)
            self.frames.append(data)
            self.root.after(1, self.record)

    def stop_recording(self):
        self.recording = False
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        self.save_button.config(state=tk.NORMAL)
        self.status_label.config(text='Recording stopped')

        self.stream.stop_stream()
        self.stream.close()

    def save_recording(self):
        file_name = self.file_name_entry.get()
        if not file_name:
            messagebox.showwarning("Input Error", "Please enter a file name.")
            return

        file_path = filedialog.asksaveasfilename(defaultextension=".wav", filetypes=[("Wave files", "*.wav")], initialfile=file_name)
        if not file_path:
            return

        with wave.open(file_path, 'wb') as wf:
            wf.setnchannels(1)
            wf.setsampwidth(self.p.get_sample_size(pyaudio.paInt16))
            wf.setframerate(44100)
            wf.writeframes(b''.join(self.frames))

        self.status_label.config(text=f'Saved to {file_path}')

if __name__ == '__main__':
    root = tk.Tk()
    app = VoiceRecorderApp(root)
    root.mainloop()
