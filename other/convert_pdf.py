import fitz
import os

__all__ = ["pdf_to_html", "pdf_to_dict"]


def pdf_to_html(file):
    html_file_split = os.path.split(file.replace(".pdf", ".html"))
    html_file = os.path.join(html_file_split[0], "HTML-Dateien", html_file_split[1])
    os.makedirs(os.path.dirname(html_file), exist_ok=True)
    with fitz.open(file) as doc:
        with open(html_file, "w") as new_file:
            for page in doc.pages():
                new_file.write(page.getText("html"))


def pdf_to_dict(file):
    txt_file_split = os.path.split(file.replace(".pdf", "_DICT.txt"))
    txt_file = os.path.join(txt_file_split[0], "Textdateien", txt_file_split[1])
    os.makedirs(os.path.dirname(txt_file), exist_ok=True)
    with fitz.open(file) as doc:
        with open(txt_file, "w") as new_file:
            for page in doc.pages():
                new_file.write(page.getText("json"))
