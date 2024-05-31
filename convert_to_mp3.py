#!/usr/bin/env python3
# coding: utf-8

import os
import tkinter.filedialog as fd
from utils import choose, pyttsx3_to_mp3, gtts_to_mp3, pdf_to_text


def main():
    files = fd.askopenfilenames(title="Dateien zur Audioumwandlung auswählen.")

    tts_engine_wahl = choose(["pyttsx3 (größere Datei)", "gtts (kleinere Datei)"], element=False,
                             text="Welche TTS-Engine soll verwendet werden?", default=0)
    if tts_engine_wahl == 0:
        tts_engine = pyttsx3_to_mp3
    else:
        tts_engine = gtts_to_mp3

    save_text = choose(["nein (standard)", "ja"], element=False,
                       text="Ausgelesenen Text als Textdatei speichern?", default=0)

    for file in files:
        file_prozess(file, tts_engine, bool(save_text))


def file_prozess(file, tts_engine, save_text=False):
    print(f"\n=====\n\nBeginne Umwandlung von Datei:\n>>> {file}")

    filename_mp3 = file.replace(".pdf", ".mp3")
    if os.path.isfile(filename_mp3):
        existiert_bereits = choose(["Weiter machen", "Nächste Datei / Abbrechen (standard)"], element=False,
                                   text="Datei existiert bereits!", default=1)
        if existiert_bereits == 1:
            return

    print("Beginne Text auszulesen...")
    text = pdf_to_text(file)
    if save_text:
        filename_txt = file.replace(".pdf", ".txt")
        with open(filename_txt, "w", encoding="utf-8") as f:
            f.write(text)

    print("Beginne mp3-Datei zu generieren...")
    tts_engine(text, filename_mp3)


if __name__ == "__main__":
    main()
