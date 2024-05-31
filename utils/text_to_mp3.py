#!/usr/bin/env python3
# coding: utf-8

import sys
import os

__all__ = ["pyttsx3_to_mp3", "gtts_to_mp3"]


def pyttsx3_to_mp3(text, filename):
    import pyttsx3
    # engine = None
    engine = pyttsx3.init()
    engine.setProperty('rate', 300)
    engine.save_to_file(text, filename)
    engine.runAndWait()


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
    if os.path.isfile(file):
        with open(file, "r", encoding="utf-8") as f:
            text = f.read()
            if kwargs["engine"] == "gtts":
                gtts_to_mp3(text, f'{file.rsplit(".", 1)[0]}.mp3')
            else:
                pyttsx3_to_mp3(text, f'{file.rsplit(".", 1)[0]}.mp3')


if __name__ == "__main__":
    main()
