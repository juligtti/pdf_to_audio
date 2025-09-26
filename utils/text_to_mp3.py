#!/usr/bin/env python3
# coding: utf-8

import pathlib
import subprocess
import sys
import tempfile

__all__ = ["pyttsx3_to_mp3", "gtts_to_mp3"]


def pyttsx3_to_mp3(text, filename):
    import pyttsx3
    # engine = None
    engine = pyttsx3.init()
    engine.setProperty('rate', 300)

    # temporäre WAV-Datei erzeugen
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp_wav:
        wav_path = tmp_wav.name

    engine.save_to_file(text, wav_path)
    engine.runAndWait()
    engine.stop()

    # WAV → MP3 konvertieren
    subprocess.run(
        ["ffmpeg", "-y", "-i", wav_path, "-codec:a", "libmp3lame", "-qscale:a", "2", filename],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        check=True
    )

    # temporäre Dateien löschen
    pathlib.Path(wav_path).unlink(missing_ok=True)


def gtts_to_mp3(text, filename):
    from gtts import gTTS
    # tts = None
    tts = gTTS(text, tld="de", lang="de", lang_check=False)
    tts.save(filename)


def main():
    # engine = pyttsx3 | gtts
    # file: str =
    kwargs = dict(arg.split("=", 1) for arg in sys.argv[1:])
    kwargs.setdefault("engine", "pyttsx3")

    file = kwargs.get("file")
    if not file:
        return

    if (filepath := pathlib.Path(file)).exists():
        with open(file, "r", encoding="utf-8") as f:
            text = f.read()
            filename = filepath.with_suffix(".mp3")
            if kwargs["engine"] == "gtts":
                gtts_to_mp3(text, filename)
            else:
                pyttsx3_to_mp3(text, filename)


if __name__ == "__main__":
    main()
