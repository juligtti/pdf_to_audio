#!/usr/bin/env python3
# coding: utf-8

"""
Ansatz hat leider viele Schwächen. Code zu undurchsichtig und unkommentiert.

"""

import re

import pdfplumber

from utils import match_sentences_constants
from utils.choose_functions import *

__all__ = ["pdf_to_text"]


def pdf_to_text(file, save_text=False):
    with pdfplumber.open(file) as pdf:
        start_inhalt, ende_inhalt = choose_range([page.page_number for page in pdf.pages],
                                                 "Seitennummer der PDF-Datei", "min_max")

        crop_tuple = compute_crop_area(pdf)
        verz = detect_inhaltsverzeichnis(pdf, crop_tuple, start_inhalt)

        texts = extract_texts(pdf, crop_tuple, start_inhalt, ende_inhalt)

        processed_texts = process_texts(texts, verz)
        full_text = " ".join([line for no, lines in processed_texts.items() for line in lines])
        full_text = full_text.replace("#LB#", "\n")

        # text_lines = finalize_text(processed_texts)
        # full_text = finalize_lines(text_lines, verz)

        if save_text:
            save_extracted_text(file, full_text)

    return full_text


def compute_crop_area(pdf):
    breite = float(pdf.pages[0].width)
    hoehe = float(pdf.pages[0].height)
    return breite * 0.08, hoehe * 0.075, breite * 0.92, hoehe * 0.9


def extract_texts(pdf, crop_tuple, start_inhalt, ende_inhalt):
    texts = {}
    for n, page in enumerate(pdf.pages[start_inhalt - 1:ende_inhalt]):
        try:
            texts[page.page_number] = page.crop(crop_tuple).extract_text()
        except ValueError:
            print(f"Seite {page.page_number} konnte nicht zugeschnitten werden.")
    return texts


def process_texts(texts, verz):
    for no, text in texts.items():
        # finde Fußnotenkennziffern
        text = re.sub(r"\)\d+", r")", text)
        text = re.sub(r"(\D)\.\d+(?![\d.,])", r"\1.", text)
        text = edit_text_basics(text, verz)
        lines = detect_footnote(text.strip().split("\n"))
        lines = clean_lines(lines)
        lines = leading_ending_newlines(lines)
        texts[no] = lines

    texts = detect_header_lines(texts)
    return texts


def clean_lines(lines):
    return [
        " " if re.search(r"^\s*$", line) else line.replace("\uf0b7", " ")
        for line in lines
    ]


def finalize_text(processed_texts):
    all_lines = [line for no, lines in processed_texts.items() for line in lines]
    all_lines = detect_word_bindings(all_lines)
    full_text = re.sub(r"( )+\n", ".\n", " ".join(all_lines))
    full_text = re.sub(r"(\n){2,}", "\n", full_text)

    return [re.sub("( ){2,}", " ", line).strip() for line in full_text.split("\n")]


def save_extracted_text(file, full_text):
    with open(file.replace(".pdf", "_text.txt"), "w", encoding="utf-8") as f:
        f.write(full_text)


def finalize_lines(all_lines: list[str], verz):
    sentence = re.compile(r"(^|(?<=[.!?:] ))([A-ZÄÖÜ0-9].+?[.!?:])((?= [A-ZÄÖÜ0-9])|$)", re.UNICODE)

    # skip = None
    # for n, line in enumerate(all_lines):
    #     match = False
    #     if "###" in line:
    #         line_ = line.split("###", 1)
    #         l0 = line_[0].strip()
    #         l1 = line_[1].strip()
    #         v_match = [v for v in verz if v.startswith(l1[:7])]
    #         if v_match and re.sub(r"( )*\.+$", "", l1) == v_match[0]:
    #             line = f"\n\nKapitel {v_match[0]}\n\n"
    #             if l0 != "":
    #                 line = f"{l0}{line}"
    #         else:
    #             print("(#)", line_)
    #             print("(###)", v_match)
    #             line = line.replace("###", "\n\nKapitel ")
    #             line = re.sub(r"\.$", "\n\n", line)
    #         match = True
    #     if "___" in line:
    #         line = line.replace("___", ">>>")
    #         line = re.sub(r"([a-zäöü])\d+([A-ZÄÖÜ])", r"\1\n\2", line, re.UNICODE)
    #         line = detect_satzanfaenge(line, False)
    #         # if line.endswith(":") and n+2 <= len(all_lines):
    #         #     line = f"{line} {all_lines[n+1]}"
    #         match = True
    #     if match:
    #         all_lines[n] = line.split("\n")
    #         continue
    #     saetze = [t_[1] for t_ in sentence.findall(line)]
    #     if len(saetze) > 1:
    #         line = saetze
    #     all_lines[n] = line

    new_lines = []
    for line in all_lines:
        if isinstance(line, str):
            new_lines.append(line)
        elif isinstance(line, list):
            new_lines.extend(line)
    new_lines = ["\n" if line == "" else line for line in new_lines]
    new_lines = [line for line in new_lines if line != "."]

    new_text = re.sub(r"(\.){2,}", ".", "\n".join(new_lines))
    new_text = re.sub(r"(\n){3,}", "\n\n", new_text)
    new_text = new_text.replace("\n, AUS", "\nAUS")
    new_text = re.sub(r"(,\s*,)+", ",", new_text)
    new_text = re.sub(r"(Seite( )?\d+)\.?([A-ZÄÖÜ])", r"\1.\n\3", new_text, re.UNICODE)
    new_text = re.sub(r"(AUSSETZER,\s*){2,}", "AUSSETZER, ", new_text)
    new_text = new_text.replace("#LB#", "\n")

    return new_text


def detect_inhaltsverzeichnis(pdf, crop_tuple, start_inhalt):
    auto_inhalt = choose(["erkennen", "Seiten angeben"],
                         text="Inhaltsverzeichnis selbst erkennen oder Seiten festlegen?",
                         default=0)
    if auto_inhalt == "erkennen":
        iv_pages = None
        for n, page in enumerate(pdf.pages[1:start_inhalt - 1]):
            text = page.crop(crop_tuple).extract_text()
            lines = text.split("\n")[:3]
            if any(line.startswith("Inhalt") for line in lines):
                iv_pages = [text]
                break
        if iv_pages is None:
            seite_iv = input("Seitennummer des IV angeben:\n>>> ")
            if int(seite_iv) not in range(0, start_inhalt):
                raise ValueError("Falsche Seitenzahl für das IV!")
            else:
                iv_pages = [pdf.pages[int(seite_iv) - 1].crop(crop_tuple).extract_text()]
    else:
        start_verz, ende_verz = choose_range(
            [page.page_number for page in pdf.pages if page.page_number < start_inhalt],
            "Seitennummer der PDF-Datei",
            "min_max")
        iv_pages = [page.crop(crop_tuple).extract_text() for page in pdf.pages[int(start_verz) - 1:int(ende_verz)]]
    verz = []
    for page in iv_pages:
        iv = page.split("\n")
        pattern_line_end = re.compile(r"([…_ .])+(\d+|Fehler!.*?)$")
        for n, line in enumerate(iv):
            if line.strip() != "" and line.lstrip()[0].isnumeric():
                full_line = re.match(r"[0-9.]+\s*\w+.*?$", line.strip())
                if not full_line:
                    continue
                full_line = re.sub("( ){2,}", " ", full_line.group(0))
                if pattern_line_end.search(full_line):
                    full_line = re.sub(pattern_line_end, "", full_line)
                    # full_line = re.sub("( )?\.{2,}$", "", full_line)
                elif n + 2 <= len(iv):
                    next_line = iv[n + 1].strip()
                    print(">", full_line)
                    print(">>> ", next_line)
                    if not next_line[0].isnumeric() and pattern_line_end.search(next_line):
                        full_line = f"{full_line} {next_line}"
                        full_line = re.sub("( ){2,}", " ", full_line)
                        full_line = re.sub(pattern_line_end, "", full_line)
                        # full_line = re.sub("( )?\.{2,}$", "", full_line)
                verz.append(full_line)
    return verz


def edit_text_basics(text, verz):
    text = re.sub(r"\s*(?:\(cid:(\s|\d)*\))+(\w\s)*", r", AUSSETZER, ", text)

    # Finde Überschriften, Abbildungen, Tabellen etc.
    lines = []
    old_lines = text.split("\n")
    n = 0
    while n < len(old_lines):
        line = old_lines[n]
        line = re.sub(r"\s+", " ", line.strip()).strip()
        if len(line) <= 1:
            line = "\n"
        elif line[0].isnumeric() and len(line) >= 7 and any(v.startswith(line[:7]) for v in verz):
            if line in verz:
                line = f"#LB##LB#Kapitel {line}#LB#"
            else:
                line = f"#LB##LB#Kapitel {line} {old_lines[n+1].strip()}#LB#"
                n += 1
        else:
            line = search_objekt(line)
        lines.append(line)
        n += 1
    text = "\n".join(lines)

    for q in match_sentences_constants.QUOTATIONS:
        text = text.replace(q, "")

    text = re.sub(r"[\t\r\f\v]", " ", text).strip()

    for pat, repl in match_sentences_constants.ABKS:
        text = re.sub(pat, repl, text, re.UNICODE)

    text = re.sub(r"( ){2,}", " ", text)
    return text


def search_objekt(t):
    re_objekt = re.compile(r"^(?:(?:Abbildung|Abb\.|Tabelle|Tab\.|Formel)[ ]*\d{1,3}|Quelle:).+?$")
    if re_objekt.match(t.strip()):
        t = f"#LB#>>> {t.strip()}#LB#"
    return t


# def detect_satzanfaenge(text, mult_newlines=True):
#     if mult_newlines:
#         for sa in SATZANFAENGE:
#             text = re.sub(sa, r"\n\1", text)
#     else:
#         for sa in SATZANFAENGE:
#             text = re.sub(fr"(?<!:) {sa}", r"\n\1", text)
#     return text


# def detect_word_bindings(all_lines):
#     footnote = re.compile(r"(\D\.|[!?:])\d{1,3}(\s*)")
#     all_lines = [re.sub(footnote, r"\1\n", line) if re.search(footnote, line) else line for line in all_lines]
#     satzende = re.compile(r"([.!?:])( )+$")
#     for n, t in enumerate(all_lines[:-1]):
#         t2 = all_lines[n + 1]
#         t2_first_word = t2.split(" ", 1)[0]
#         if (
#                 t.endswith("-") and
#                 t2[0].islower() and not
#         any(x in t2_first_word for x in ("und", "oder", "beziehungsweise", "/", "&"))
#         ):
#             line = t[:-1]
#         elif satzende.search(t):
#             line = re.sub(satzende, r"\1\n", t)
#         else:
#             line = t
#         all_lines[n] = line
#     return all_lines


# def match_objekt(all_lines):
#     for n, t in enumerate(all_lines[:-1]):
#         if len(t.strip()) == 0:
#             continue
#         t_neu, t_match = search_objekt(t)
#         if t_match:
#             all_lines[n] = t_neu
#     return all_lines


def detect_footnote(lines):
    stop = len(lines)
    if stop < 2:
        return lines
    count = 0
    lines = lines[::-1]
    for n, line in enumerate(lines[:-1]):
        line = line.strip()
        if re.search(r"^\d+[^.]", line) or re.search(r"^\d+[^.]", lines[n+1].strip()):
            # findet in dieser oder der folgenden Zeile eine Fußnote
            count = 0
        elif line == "":
            count += 1
            if count >= 2:
                stop = -n
                break
        else:
            if n != 0:
                stop = -n
            break
    return lines[::-1][:stop]


def leading_ending_newlines(lines):
    start = 0
    stop = None
    for n, line in enumerate(lines, start=1):
        if line == "\n":
            start = n
            continue
        else:
            break
    for n, line in enumerate(lines[::-1], start=1):
        if line == "\n":
            stop = -n
            continue
        else:
            break
    return lines[start:stop]


def detect_header_lines(texts):
    while True:
        first_lines = set()
        for no, lines in texts.items():
            if len(lines) == 0:
                print(f"Leere Seite: {no}")
            else:
                first_lines.add(lines[0])
        if len(first_lines) == 1:
            for no, lines in texts.items():
                texts[no] = lines[1:]
        else:
            break
    return texts
