import os
import threading
import tkinter as tk
import edge_tts
from openai import OpenAI
from playsound import playsound

from record import AudioRecorderApp
from asr import SenseVoiceSmall as ASR

# Configuration parameters
TEMP_PATH = os.path.abspath("temp")
AUDIO_PATH = os.path.join(TEMP_PATH, "record.wav")   # Recorded audio file path
SPEECH_PATH = os.path.join(TEMP_PATH, "speech.mp3")  # Generated speech file path
ASR_MODEL_PATH = os.path.abspath("SenseVoiceSmall")
OPENAI_API_KEY = "YOUR_OPENAI_API_KEY"
OPENAI_BASE_URL = "https://openrouter.ai/api/v1"  # Base URL for OpenRouter API, for free


def process_text_with_openai(text, base_url=OPENAI_BASE_URL, api_key=OPENAI_API_KEY):
    """Process input text with OpenAI API to generate response

    Args:
        text (str): Input user query

    Returns:
        str: Processed response text
    """
    client = OpenAI(base_url=base_url, api_key=api_key)
    response = client.completions.create(
        model="google/gemini-2.0-flash-exp:free",  # Specify LLM model
        prompt="(你的回答将经过中文TTS转换为音频，请仅回复用于音频的对话内容)" + text,
        max_tokens=1000
    )
    return response.choices[0].text.strip()

def text_to_speech(text, character="zh-CN-XiaoyiNeural"):
    """Convert text to speech using Edge TTS and save audio file

    Args:
        text (str): Text to convert
        character (str): Voice character model
    """
    communicate = edge_tts.Communicate(text, character)
    communicate.save_sync(SPEECH_PATH)
    print(f"Speech generated and saved to {SPEECH_PATH}")

class App(AudioRecorderApp):
    def _llm_process(self):
        """Main processing flow for audio -> text -> LLM -> speech"""
        asr = ASR()

        # Step 1: Audio-to-text conversion using ASR
        self.update_status("Calling ASR...")
        text = asr.convert(
            audio_path=self.audio_path,
            language="auto"  # Auto detect language
        )
        print("ASR Output:", text)

        # Step 2: Process text with LLM
        self.update_status("Processing LLM...")
        output_text = process_text_with_openai(text)
        print("LLM Output:", output_text)

        # Step 3: Text-to-speech conversion
        self.update_status("Generating speech...")
        text_to_speech(output_text)

        # Step 4: Play the generated audio
        self.update_status("Playing speech...")
        playsound(SPEECH_PATH)

        # Final status updates
        self.update_status("Complete")
        self.start_btn.config(state=tk.NORMAL)

    def update_status(self, text):
        """Update status label asynchronously in main thread"""
        self.status_lbl.after(0, lambda: self.status_lbl.config(text=text))

    def stop_recording(self):
        """Handle recording stop and start processing"""
        if self.recorder:
            self.recorder.stop()
            self.recorder.save(self.audio_path)
            self.status_lbl.config(text=f"Recording saved to {self.audio_path}")
            self.recording = False
            threading.Thread(target=self._llm_process).start()
            self.stop_btn.config(state=tk.DISABLED)


def main_loop():
    """Main application setup and execution"""
    os.makedirs(TEMP_PATH, exist_ok=True)
    root = tk.Tk()
    app = App(
        root,
        title="Voice LLM Assistant",
        geometry="320x150",
        audio_path=AUDIO_PATH
    )
    root.mainloop()


if __name__ == "__main__":
    main_loop()
