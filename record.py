import tkinter as tk
from tkinter import ttk, messagebox
import pyaudio
import wave

def get_input_devices():
    """Get available audio input devices.

    Returns:
        list: List of tuples (device index, device name) with input channels >0
    """
    p = pyaudio.PyAudio()
    devices = []
    for i in range(p.get_device_count()):
        info = p.get_device_info_by_index(i)
        if info.get("maxInputChannels") > 0:
            devices.append((i, info["name"]))
    p.terminate()
    return devices

class AudioRecorderApp:
    """Main application class for audio recording GUI"""
    def __init__(self, root, title="Audio Recorder Tool", geometry="320x150", audio_path="record.wav"):
        """Initialize the main application window

        Args:
            root (tk.Tk): Root tkinter window
            title (str): Window title
            geometry (str): Window size specification
            audio_path (str): Default output file path
        """
        self.root = root
        self.root.title(title)
        self.root.geometry(geometry)
        self.audio_path = audio_path

        self.devices = get_input_devices()
        self.device_names = [f"{i}: {name}" for i, name in self.devices]
        self.selected_device = tk.StringVar()
        self.selected_device.set(self.device_names[0] if self.devices else "No devices available")

        self.rate = tk.StringVar(value="16000")
        self.recording = False
        self.recorder = None

        # UI component creation
        tk.Label(root, text="Select input device:").grid(row=0, column=0, padx=10, pady=5)
        self.device_menu = ttk.Combobox(root, textvariable=self.selected_device,
                                       values=self.device_names)
        self.device_menu.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(root, text="Sample rate (Hz):").grid(row=1, column=0, padx=10, pady=5)
        self.rate_entry = tk.Entry(root, textvariable=self.rate, width=10)
        self.rate_entry.grid(row=1, column=1, padx=10, pady=5)

        self.start_btn = tk.Button(root, text="Start Recording", command=self.start_recording)
        self.start_btn.grid(row=2, column=0, padx=10, pady=10)

        self.stop_btn = tk.Button(root, text="Stop Recording", command=self.stop_recording,
                                 state=tk.DISABLED)
        self.stop_btn.grid(row=2, column=1, padx=10, pady=10)

        self.status_lbl = tk.Label(root, text="", fg="blue")
        self.status_lbl.grid(row=3, column=0, columnspan=2, pady=5)

        self.root.after(100, self.check_recording)

    def start_recording(self):
        """Handle start recording button click"""
        selected = self.selected_device.get()
        if not selected:
            messagebox.showwarning("Warning", "Please select a device first")
            return

        device_index = int(selected.split(":")[0])
        try:
            rate = int(self.rate.get())
        except ValueError:
            rate = 16000
        self.recorder = AudioRecorder(device_index, rate)
        self.recorder.start()
        self.recording = True

        self.status_lbl.config(text="Recording in progress...")
        self.start_btn.config(state=tk.DISABLED)
        self.stop_btn.config(state=tk.NORMAL)

    def stop_recording(self):
        """Handle stop recording button click"""
        if self.recorder:
            self.recorder.stop()
            self.recorder.save(self.audio_path)
            self.status_lbl.config(text=f"Recording saved to {self.audio_path}")
            self.recording = False
            self.start_btn.config(state=tk.NORMAL)
            self.stop_btn.config(state=tk.DISABLED)

    def check_recording(self):
        """Periodically check recording status"""
        if self.recording and self.recorder:
            self.recorder.record()
        self.root.after(100, self.check_recording)

class AudioRecorder:
    """Handles actual audio recording operations"""
    def __init__(self, device_index, rate):
        """Initialize audio recording parameters

        Args:
            device_index (int): Index of input device
            rate (int): Sampling rate in Hz
        """
        self.p = pyaudio.PyAudio()
        self.stream = None
        self.frames = []
        self.recording = False
        self.device_index = device_index
        self.rate = rate
        self.CHUNK = 1024
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = 1

    def start(self):
        """Start audio stream and recording"""
        self.stream = self.p.open(
            format=self.FORMAT,
            channels=self.CHANNELS,
            rate=self.rate,
            input=True,
            frames_per_buffer=self.CHUNK,
            input_device_index=self.device_index
        )
        self.frames = []
        self.recording = True

    def stop(self):
        """Stop current recording stream"""
        self.recording = False
        self.stream.stop_stream()
        self.stream.close()

    def record(self):
        """Read audio data from stream while recording"""
        if self.recording:
            data = self.stream.read(self.CHUNK)
            self.frames.append(data)

    def save(self, filename):
        """Save recorded data to WAV file"""
        with wave.open(filename, 'wb') as wf:
            wf.setnchannels(self.CHANNELS)
            wf.setsampwidth(self.p.get_sample_size(self.FORMAT))
            wf.setframerate(self.rate)
            wf.writeframes(b''.join(self.frames))

    def __del__(self):
        """Cleanup PyAudio resources on destruction"""
        self.p.terminate()

def main_loop():
    """Main application entry point"""
    root = tk.Tk()
    app = AudioRecorderApp(root)
    root.mainloop()

if __name__ == "__main__":
    main_loop()