import sounddevice as sd
import soundfile as sf
from threading import Event
from utils import (
    record_audio_into_tmp_file,
    transcribe_audio,
    translate_text,
    generate_audio,
)
from controls import (
    SOURCE_LANGUAGE,
    TARGET_LANGUAGE,
)


def run(stop_event: Event = Event()):
    while not stop_event.is_set():
        file_path = record_audio_into_tmp_file(stop_event=stop_event)

        text = transcribe_audio(file_path, language=SOURCE_LANGUAGE)
        print(text, end="\n\n")

        if text.strip() == "" or stop_event.is_set():
            return

        translated_text = translate_text(text, source_language=SOURCE_LANGUAGE, target_language=TARGET_LANGUAGE)
        print(translated_text, end="\n\n")

        if translated_text.strip() == "" or stop_event.is_set():
            return

        audio = generate_audio(translated_text)

        # Read using soundfile
        data, samplerate = sf.read(audio, dtype='float32')

        # Play using sounddevice
        sd.play(data, samplerate)
        sd.wait()  # Wait until audio is finished


if __name__ == "__main__":
    run()
