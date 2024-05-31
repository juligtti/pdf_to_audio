#!/usr/bin/env python3
# coding: utf-8

import numpy as np
from collections.abc import Collection
from typing import Union

__all__ = ["choose", "choose_range", "choose_mult"]


def isint(s):
    try:
        return int(s)
    except ValueError:
        return None


def make_dict_and_print(liste: Collection):
    liste_dic = {}
    if isinstance(liste, dict):
        for n, (k, v) in enumerate(liste.items(), start=1):
            print(n, " - ", k, f"({v})")
            liste_dic[n-1] = k
    else:
        for n, i in enumerate(liste, start=1):
            print(n, " - ", i)
            liste_dic[n-1] = i
    return liste_dic


def choose(
        liste: Collection,
        text: str = None,
        element: bool = True,
        default: int = None):

    print("\n===== choose =====\n")

    if not isinstance(liste, Collection) or len(liste) == 0:
        raise ValueError("Keine Liste/Tuple oder leer")

    liste_dic = make_dict_and_print(liste)

    if isinstance(text, str):
        print(f"\n{text}")
    wahl = input("Nummer auswählen:\n>>> ")
    print("\n==========\n")

    if wahl.strip() != "":
        try:
            wahl = int(wahl) - 1
        except ValueError as e:
            print(f"Eingabe ungültig\n\n{e}")
            return choose(liste, text, element, default)

        if element and wahl in liste_dic:
            try:
                return liste_dic[wahl]
            except KeyError as e:
                print(f"Eingabe nicht in Auswahlliste\n\n{e}")
                return choose(liste, text, element, default)
        elif not element and wahl in liste_dic:
            return wahl

    if element and isinstance(default, int):
        try:
            return liste_dic[default]
        except KeyError as e:
            print(f"Defaultwert nicht in Auswahlliste\n\n{e}")
            return choose(liste, text, element)
    elif not element and isinstance(default, int):
        return default
    else:
        print("Auswahl nicht erkannt. Bitte erneut versuchen")
        return choose(liste, text, element)


def choose_range(
        liste: Collection,
        text: str = "BESCHREIBUNG",
        typ: str = "array") -> Union[np.ndarray, tuple]:

    print("\n===== choose_range =====\n")

    if typ not in ["array", "min_max"]:
        raise ValueError("Wiedergabewert falsch definiert")
    if not isinstance(liste, Collection) or len(liste) == 0:
        raise ValueError("Keine Liste/Tuple oder leer")

    min_val = min(liste)
    max_val = max(liste)
    eingabe_min = input(f"\nStartwert ({text}) eingeben (mindestens {min_val}):\n>>> ")
    eingabe_max = input(f"\nEndwert ({text}) eingeben (höchstens {max_val}):\n>>> ")
    eingabe_min = isint(eingabe_min)
    eingabe_max = isint(eingabe_max)

    if isinstance(eingabe_min, int) and isinstance(eingabe_max, int):
        wahl_min = min([eingabe_min, eingabe_max])
        wahl_max = max([eingabe_min, eingabe_max])
        if wahl_min < min_val:
            print("\nStartwert zu klein")
            return choose_range(liste, text, typ)
        elif wahl_max > max_val:
            print(f"\nEndwert zu groß. {max_val} wird als Endwert festgelegt.")
            wahl_max = max_val
        start = wahl_min
        end = wahl_max
    elif isinstance(eingabe_min, int):
        start = eingabe_min
        end = max_val
    elif isinstance(eingabe_max, int):
        start = min_val
        end = eingabe_max
    else:
        print("\nEingabewerte müssen ganze Zahlen sein.")
        return choose_range(liste, text, typ)

    print("\n==========\n")

    if typ == "array":
        return np.arange(start, end+1)
    elif typ == "min_max":
        return start, end


def choose_mult(
        liste: Collection,
        text: str = None,
        nums: bool = False,
        default: Union[int, Collection] = None) -> list:

    print("\n===== choose_mult =====\n")

    if not isinstance(liste, Collection) or len(liste) == 0:
        raise ValueError("Keine Liste/Tuple oder leer")

    liste_dic = make_dict_and_print(liste)

    if isinstance(text, str):
        print(f"\n{text}\n")
    eingabe = input("Bitte Nummern angeben, mit Komma trennen oder mit '-' von / bis eingeben.\n>>> ")

    if len(eingabe.strip()) == 0 and isinstance(default, int):
        try:
            return liste_dic[default]
        except KeyError as e:
            print(f"Defaultwert nicht in Auswahlliste\n\n{e}")
            return choose_mult(liste, text, nums)
    elif len(eingabe.strip()) == 0 and isinstance(default, Collection):
        try:
            return [liste_dic[d] for d in default]
        except KeyError as e:
            print(f"Defaultwerte nicht in Auswahlliste\n\n{e}")
            return choose_mult(liste, text, nums)

    nummern = []
    eingaben = [x.strip() for x in eingabe.split(",") if x.strip() != ""]
    if "-" not in eingabe:
        try:
            nummern = list(map(int, eingaben))
        except ValueError:
            return choose_mult(liste, text, nums)
    else:
        for eintrag in eingaben:
            if "-" in eintrag:
                eintraege = [x.strip() for x in eintrag.split("-")]
                try:
                    val1 = int(eintraege[0])
                    val2 = int(eintraege[-1])
                except ValueError:
                    print("Mindestens eine Eingabe entsprach keiner ganzzahligen Zahl.")
                    return choose_mult(liste, text, nums)
                nummern.extend([x for x in range(val1, val2+1) if x not in nummern])
            else:
                try:
                    if int(eintrag) not in nummern:
                        nummern.append(int(eintrag))
                except ValueError:
                    print("Mindestens eine Eingabe entsprach keiner ganzzahligen Zahl.")
                    return choose_mult(liste, text, nums)

    auswahl = [liste_dic[num-1] for num in nummern if num-1 in liste_dic]
    print("\nAuswahl:\n- ", "\n- ".join(list(map(str, auswahl))), sep="")
    print("\n==========\n")
    if nums:
        return [num-1 for num in nummern if num-1 in liste_dic]
    else:
        return auswahl
