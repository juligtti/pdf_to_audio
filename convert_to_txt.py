#!/usr/bin/env python3
# coding: utf-8

import tkinter.filedialog as fd

from utils import pdf_to_text


def main():
    files = fd.askopenfilenames(title="Dateien zur Textumwandlung auswählen.")

    for file in files:
        pdf_to_text(file, save_text=True)


if __name__ == "__main__":
    main()
