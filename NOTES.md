# NOTES
Here are some notes about the project. 

## Resources
### LLM
- [OpenAI Text-to-Speech Guide](https://platform.openai.com/docs/guides/text-to-speech)
- [OpenAI Speech-to-Text Guide](https://platform.openai.com/docs/guides/speech-to-text)
    - only can use 11 preset voices (no custom option)

### Python
- [python-soundfile](https://github.com/bastibe/python-soundfile)
    - A library for reading and writing sound files in Python, supporting various formats via libsndfile.
- [python-sounddevice](https://github.com/spatialaudio/python-sounddevice) 
    - Provides bindings for the PortAudio library, enabling real-time audio input/output and recording/playback in Python.
- [moviepy](https://github.com/Zulko/moviepy) 
    - A Python library for video editing, allowing for cutting, concatenation, effects, and audio/video processing with a simple API.

## Goals
- create for demo a command line tool that can work with an example game (ex. Steins;Gate)

## Things to Consider
- the game audio should be "replaced" with the generated audio (can't have both outputted or else it will be chaos) so we need to figure out how to get rid of the voice from the original game while keeping the music in the output
    - might be too difficult; for the demo, maybe just outputting the final voice is sufficient
- the intervals that we translate at
    - we want to minimze latency during translation but translating some languages might require hearing the whole/multiple sentences first before making the translation

## Code Snippets
Play an audio file.
```python
import sounddevice as sd
import soundfile as sf
import tempfile
import moviepy as mp

video_path = r"C:\Users\weiha\OneDrive\Documents\code\personal-projects\translator\examples\steins_gate_shorter.mkv"

# Extract audio and save to a temporary WAV file
video = mp.VideoFileClip(video_path)
with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmpfile:
    audio_path = tmpfile.name
    video.audio.write_audiofile(audio_path, codec='pcm_s16le')

# Read and play audio
data, samplerate = sf.read(audio_path)
sd.play(data, samplerate)
sd.wait()
```

A simple example of recording from speakers ('What you hear') using the WASAPI loopback device
```python
"""A simple example of recording from speakers ('What you hear') using the WASAPI loopback device"""

from _spinner_helper import Spinner
# Spinner is a helper class that is in the same examples folder.
# It is optional, you can safely delete the code associated with it.

import pyaudiowpatch as pyaudio
import time
import wave

DURATION = 5.0
CHUNK_SIZE = 512

filename = "loopback_record.wav"
    
    
if __name__ == "__main__":
    with pyaudio.PyAudio() as p, Spinner() as spinner:
        """
        Create PyAudio instance via context manager.
        Spinner is a helper class, for `pretty` output
        """
        try:
            # Get default WASAPI info
            wasapi_info = p.get_host_api_info_by_type(pyaudio.paWASAPI)
        except OSError:
            spinner.print("Looks like WASAPI is not available on the system. Exiting...")
            spinner.stop()
            exit()
        
        # Get default WASAPI speakers
        default_speakers = p.get_device_info_by_index(wasapi_info["defaultOutputDevice"])
        
        if not default_speakers["isLoopbackDevice"]:
            for loopback in p.get_loopback_device_info_generator():
                """
                Try to find loopback device with same name(and [Loopback suffix]).
                Unfortunately, this is the most adequate way at the moment.
                """
                if default_speakers["name"] in loopback["name"]:
                    default_speakers = loopback
                    break
            else:
                spinner.print("Default loopback output device not found.\n\nRun `python -m pyaudiowpatch` to check available devices.\nExiting...\n")
                spinner.stop()
                exit()
                
        spinner.print(f"Recording from: ({default_speakers['index']}){default_speakers['name']}")
        
        wave_file = wave.open(filename, 'wb')
        wave_file.setnchannels(default_speakers["maxInputChannels"])
        wave_file.setsampwidth(pyaudio.get_sample_size(pyaudio.paInt16))
        wave_file.setframerate(int(default_speakers["defaultSampleRate"]))
        
        def callback(in_data, frame_count, time_info, status):
            """Write frames and return PA flag"""
            wave_file.writeframes(in_data)
            return (in_data, pyaudio.paContinue)
        
        with p.open(format=pyaudio.paInt16,
                channels=default_speakers["maxInputChannels"],
                rate=int(default_speakers["defaultSampleRate"]),
                frames_per_buffer=CHUNK_SIZE,
                input=True,
                input_device_index=default_speakers["index"],
                stream_callback=callback
        ) as stream:
            """
            Opena PA stream via context manager.
            After leaving the context, everything will
            be correctly closed(Stream, PyAudio manager)            
            """
            spinner.print(f"The next {DURATION} seconds will be written to {filename}")
            time.sleep(DURATION) # Blocking execution while playing
        
        wave_file.close()
```