#!/usr/bin/env python3
# coding: utf-8

__all__ = ["ABKS", "SATZANFAENGE", "QUOTATIONS"]

ABKS = [
    (r"(\s)S\. (\d+)", r"\1Seite \2"),
    (r"(^|\s)usw\.", r"\1und so weiter"),
    (r"(^|\s)sog\.", r"\1sogenannte"),
    (r"(^|\s)([rR])d\.", r"\1\2und"),
    (r"(\s|\()([zZ])\.\s*B\.", r"\1\2um Beispiel"),
    (r"bspw\.", "beispielsweise"),
    (r"(\s|\()([uU])\.\s*a\.", r"\1\2nter anderem"),
    (r"(\s|\()([gG])gf\.", r"\1\2egebenenfalls"),
    (r"(\s|\()bzw\.", r"\1beziehungsweise"),
    (r"(\s|\()([iI])\.\s?d\.\s?R\.", r"\1\2n der Regel"),
    (r"(\s|\()([gG])em\.", r"\1\2gemäß"),
    (r"Mio(\.|\s)", "Millionen "),
    (r"Mrd(\.|\s)", "Milliarden "),
    (r"(\s|\()([mM])in(d)?\.", r"\1\2indestens"),
    (r"(^|\s)u\.?v\.?m\.", r"\1und viele mehr."),
    (r"\s+, ", ", "),
    (r"EURO|EUR|€", "Euro"),
    (r"zzgl\.", "zuzüglich"),
    (r"(^|\s)ca\.", r"\1circa"),
    (r"Abs\.", "Absatz"),
    (r"o\.\s*g\.", "oben genannte"),
    (r"u\.\s*g\.", "unten genannte"),
    (r"\s*[\[\(](\.+|…)[\)\]]", " "),
    (r"[Vv]gl.(\s)", r"Vergleiche\1"),
    (r"Nr\.", "Nummer"),
    (r"et\.? al\.", "und andere"),
    (r"(\))\d{1,3}(\s)", r"\1\2"),
    (r"<\s*(\d)", r"weniger als \1"),
    (r">\s*(\d)", r"mehr als \1"),
    (r"([dD])\.\s?h\.", r"\1as heißt"),
    (r"etc\.", " et cetera"),
    (r"\s+\.", r"\."),
    (r"([a-zäöü])([A-ZÄÖÜ])", r"\1 \2"),
    (r"Abb\.", "Abbildung "),
    (r"Tab\.", "Tabelle "),
    (r",00(\D)", r"\1")
]

SATZANFAENGE = [
    r"(Der\s)", r"(Die(s)?\s)", r"(Das(s)?\s)", r"(Ein(e|es|er)?\s)", r"(Zu(r|m)?\s)", r"(I(m|n){1}\s)",
    r"(Bei(m)?\s)", r"(Zu(dem)?\s)", r"(Da(raus|bei|her|für|durch)?\s)", r"(Anhand\s)", r"(Diese(r|s)?\s)",
    r"(Demnach\s)", r"(A(n|m){1}\s)", r"(Um\s)", r"(Für\s)", r"(So(wohl|llte)?\s)", r"(Durch\s)",
    r"(Als\s)", r"(Wenn\s)", r"(Lediglich\s)", r"(Wird\s)", r"(Werden\s)", r"(Dem\s)", r"(Sollte(n)?\s)",
    r"(Des(halb| Weiteren)?\s)", r"(Normalerweise\s)", r"(Es\s)", r"(Viel(e|es)?\s)", r"(Außerdem\s)",
    r"(Auch\s)", r"(Nach\s)", r"(Jede(r|s)?\s)", r"(Zwar\s)", r"(Auf(grund)?\s)", r"(Allerdings\s)", r"(Je\s)"
]

QUOTATIONS = [
    '\u0022', '\u00ab', '\u00bb', '\u2018', '\u2019', '\u201a', '\u201b', '\u201c', '\u201d',
    '\u201e', '\u201f', '\u2039', '\u203a', '\u275b', '\u275c', '\u275d', '\u275e', '\u275f',
    '\u2760', '\u276e', '\u276f', '\u301d', '\u301e', '\u301f', '\uff02', '\u0060', '\u0027'
]

if __name__ == "__main__":
    for n, quot in enumerate(QUOTATIONS):
        print(n, quot)
