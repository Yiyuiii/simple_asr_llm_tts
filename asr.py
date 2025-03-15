import os
from funasr import AutoModel
from funasr.utils.postprocess_utils import rich_transcription_postprocess
from modelscope import snapshot_download


class SenseVoiceSmall:
    def __init__(self, model_dir=None, model_id="iic/SenseVoiceSmall", device="cuda:0"):
        """Initialize speech-to-text model
        Args:
            model_dir (str, optional): Model storage path (defaults to current script directory's 'models' folder)
            device (str): Compute device (default: "cuda:0")
        """
        if model_dir is None:
            model_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "models")
        os.makedirs(model_dir, exist_ok=True)
        if not os.path.exists(os.path.join(model_dir, model_id)):
            print(f"Downloading model to {model_dir}")
            snapshot_download(model_id, cache_dir=model_dir)

        self.model = AutoModel(
            model=os.path.join(model_dir, model_id),
            trust_remote_code=True,
            remote_code="./model.py",
            vad_model="fsmn-vad",
            vad_kwargs={"max_single_segment_time": 30000},
            device=device,
        )

    def convert(self, audio_path, language="auto", batch_size_s=60, merge_length_s=15):
        """Convert audio file to text
        Args:
            audio_path (str): Audio file path
            language (str): Language setting (options: "auto", "zn", "en", "yue", "ja", "ko", "nospeech")
            batch_size_s (int): Batch processing size in seconds (default: 60)
            merge_length_s (int): Text merging length in seconds (default: 15)
        Returns:
            str: Processed text output
        """
        res = self.model.generate(
            input=audio_path,
            cache={},
            language=language,
            use_itn=True,
            batch_size_s=batch_size_s,
            merge_vad=True,
            merge_length_s=merge_length_s,
        )
        text = rich_transcription_postprocess(res[0]["text"])
        return text


# Example usage
if __name__ == "__main__":
    audio_path = "path/to/your/audio.mp3"  # Replace with actual audio file path
    asr = SenseVoiceSmall()
    result = asr.convert(
        audio_path=audio_path,
        language="auto"  # Options: "auto", "en", "zn", etc.
    )
    print(result)