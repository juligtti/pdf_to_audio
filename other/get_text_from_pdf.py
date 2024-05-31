#!/usr/bin/env python3
# coding: utf-8

import glob
import os
import sys
from utils import choose_mult, pdf_to_text


def run():
    if len(sys.argv) > 1:
        path = sys.argv[1]
        print(path)
    else:
        path = f"../*.pdf"

    keyword_end = "FERTIG / ABBRUCH"
    loop = True
    while loop:
        file_list = glob.glob(path)
        file_list.insert(0, keyword_end)
        files = choose_mult(file_list, "Dateien zur Textextraktion auswählen.")
        if keyword_end in files:
            loop = False
            files.remove(keyword_end)

        for file in files:
            print(f"{file}\nBeginne Text auszulesen...")
            text = pdf_to_text(file)
            filename_txt = os.path.join("Textdateien", os.path.basename(file).replace(".pdf", ".txt"))
            with open(filename_txt, "w", encoding="utf-8") as f:
                f.write(text)


if __name__ == "__main__":
    run()
