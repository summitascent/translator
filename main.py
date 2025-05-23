import sounddevice as sd
import soundfile as sf
from threading import Event
import importlib


def run(stop_event: Event = Event()):
    from utils import (
        record_audio_into_tmp_file,
        transcribe_audio,
        translate_text,
        generate_audio,
    )

    import controls
    importlib.reload(controls) # refresh language selection

    while not stop_event.is_set():
        file_path = record_audio_into_tmp_file(stop_event=stop_event)

        if stop_event.is_set():
            return

        text = transcribe_audio(file_path, language=controls.SOURCE_LANGUAGE)
        print(text, end="\n\n")

        if stop_event.is_set():
            return

        if text.strip() == "":
            continue

        translated_text = translate_text(text, source_language=controls.SOURCE_LANGUAGE, target_language=controls.TARGET_LANGUAGE)
        print(translated_text, end="\n\n")

        if stop_event.is_set():
            return

        if translated_text.strip() == "":
            continue

        audio = generate_audio(translated_text)

        # Read using soundfile
        data, samplerate = sf.read(audio, dtype='float32')

        # Play using sounddevice
        sd.play(data, samplerate)
        sd.wait()  # Wait until audio is finished


if __name__ == "__main__":
    run()
