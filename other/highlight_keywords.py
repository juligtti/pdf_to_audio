#!/usr/bin/env python3
# coding: utf-8

import glob
import sys
import fitz
from utils import choose_mult


def main():
    if len(sys.argv) > 1:
        path = sys.argv[1]
    else:
        path = f"*.pdf"

    if len(sys.argv) > 2:
        texte = sys.argv[2:]
    else:
        texte = [" ich ", " man ", " wir ", " uns ", " unser ", " unsere ", " mein ", " meine ", "enorm", "extrem"]

    print("Gesuchte Worte:", " | ".join(texte))

    keyword_end = "FERTIG / ABBRUCH"
    loop = True
    while loop:
        file_list = glob.glob(path)
        file_list.insert(0, keyword_end)
        files = choose_mult(file_list, "Dateien zur Markierung auswählen.")
        if keyword_end in files:
            loop = False
            files.remove(keyword_end)

        for file in files:
            print("Beginne Text auszulesen: ", file)
            doc = fitz.open(file)
            for page in doc:
                for text in texte:
                    text_instances = page.search_for(text)
                    for inst in text_instances:
                        page.add_highlight_annot(inst)
            doc.save(file.replace(".pdf", "_edit.pdf"), garbage=4, deflate=True, clean=True)


if __name__ == "__main__":
    main()
