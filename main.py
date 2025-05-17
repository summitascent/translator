import sounddevice as sd
import soundfile as sf
from utils import (
    record_audio_into_tmp_file,
    transcribe_audio,
    translate_text,
    generate_audio,
)


def run():
    while True:
        file_path = record_audio_into_tmp_file()

        text = transcribe_audio(file_path)
        print(text)
        print()

        translated_text = translate_text(text)
        print(translated_text)
        print()

        audio = generate_audio(translated_text)

        # Read using soundfile
        data, samplerate = sf.read(audio, dtype='float32')

        # Play using sounddevice
        sd.play(data, samplerate)
        sd.wait()  # Wait until audio is finished
        

if __name__ == "__main__":
    run()