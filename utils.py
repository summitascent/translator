import io 
import pyaudiowpatch as pyaudio
import time
import wave
import tempfile
import keyboard

from _secrets import OPEN_AI_API_KEY
import openai

REQUEST_TIMEOUT = 20

client = openai.OpenAI(api_key=OPEN_AI_API_KEY)

send_requests = False


def on_key(event, key="a"):
    global send_requests
    
    if event.name == key and event.event_type == "down":
        send_requests = True


keyboard.on_press(on_key)


def record_audio(
        filename="output.wav",
        chunk_size=512, 
):
    """
    Record audio from the PC's main output device and save it to a file.
    """
    with pyaudio.PyAudio() as p:
        """
        Create PyAudio instance via context manager.
        """
        try:
            # Get default WASAPI info
            wasapi_info = p.get_host_api_info_by_type(pyaudio.paWASAPI)
        except OSError:
            print("Looks like WASAPI is not available on the system. Exiting...")
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
                print("Default loopback output device not found.\n\nRun `python -m pyaudiowpatch` to check available devices.\nExiting...\n")
                exit()
                
        print(f"Recording from: ({default_speakers['index']}){default_speakers['name']}")
        
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
                frames_per_buffer=chunk_size,
                input=True,
                input_device_index=default_speakers["index"],
                stream_callback=callback
        ) as stream:
            """
            Opena PA stream via context manager.
            After leaving the context, everything will
            be correctly closed(Stream, PyAudio manager)            
            """
            while True:
                global send_requests
                
                time.sleep(0.25) # Blocking execution while playing
                
                if send_requests:
                    print("Sending requests...")
                    send_requests = False
                    break
                
            print(f"PC audio output written to {filename}")
        
        wave_file.close()
        

def record_audio_into_tmp_file(
        chunk_size=512, 
):
    """
    Record audio from the PC's main output device and save it to a temporary file.
    """
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_file:
        filename = tmp_file.name
        record_audio(filename, chunk_size)
        
    return filename


def transcribe_audio(file_path, language="ja"):
    with open(file_path, "rb") as audio_file:
        transcription = client.audio.transcriptions.create(
            model="gpt-4o-transcribe", 
            file=audio_file,
            language=language,
            include="punctuations",
            prompt=f"Transcribe the audio file."
                   f"If something is not in the source language '{language}', do not transcribe it at all and leave it out."
                   f"If the audio has no voice, leave the transcription empty.",
            temperature=0.3,
            timeout=REQUEST_TIMEOUT,
        )
    
    return transcription.text


def translate_text(text, source_language="ja", target_language="en"):
    completion = client.chat.completions.create(
        model="gpt-4o",
        temperature=0.3,
        messages=[
            {
                "role": "system",
                "content": f"You are a translator for dialogues from games who will "
                           f"translate from {source_language} to {target_language}."
                           f"If the text is empty, leave the translation empty."
            },
            {
                "role": "user",
                "content": text,
            },
        ],
        timeout=REQUEST_TIMEOUT,
    )
    
    return completion.choices[0].message.content


def generate_audio(
        text,
        voice="alloy", 
        instructions="You are a character in some game.", 
):
    with client.audio.speech.with_streaming_response.create(
        model="gpt-4o-mini-tts",
        voice=voice,
        input=text,
        instructions=instructions,
        response_format="wav",
        timeout=REQUEST_TIMEOUT,
    ) as response:
        audio_bytes = io.BytesIO(response.read())
    
    return audio_bytes


