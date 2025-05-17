import sounddevice as sd
import soundfile as sf
import tempfile
import moviepy as mp

video_path = r"examples/steins_gate_shorter.mkv"

# Extract audio and save to a temporary WAV file
video = mp.VideoFileClip(video_path)
with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmpfile:
    audio_path = tmpfile.name
    video.audio.write_audiofile(audio_path, codec='pcm_s16le')

# Read and play audio
data, samplerate = sf.read(audio_path)
sd.play(data, samplerate)
sd.wait()
