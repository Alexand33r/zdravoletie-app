#!/usr/bin/env python3
"""Convert logbook.md to logbook_temp.tex for pdflatex compilation."""
import re

INPUT  = r"C:\Users\AleksandarTanev\Downloads\Fontys\Code\thesis\logbook.md"
OUTPUT = r"C:\Users\AleksandarTanev\Downloads\Fontys\Code\thesis\logbook_temp.tex"


def escape(text):
    """Escape LaTeX special characters in a plain-text segment."""
    text = text.replace("\\", r"\textbackslash{}")
    text = text.replace("&",  r"\&")
    text = text.replace("%",  r"\%")
    text = text.replace("$",  r"\$")
    text = text.replace("#",  r"\#")
    text = text.replace("^",  r"\textasciicircum{}")
    text = text.replace("_",  r"\_")
    text = text.replace("{",  r"\{")
    text = text.replace("}",  r"\}")
    text = text.replace("~",  r"\textasciitilde{}")
    text = text.replace("²", r"$^{2}$")   # ²
    text = text.replace("°", r"$^{\circ}$")  # °
    return text


def inline(text):
    """Process inline markdown (bold, italic) on raw markdown text."""
    out = []
    i = 0
    n = len(text)
    while i < n:
        # Bold: **...**
        if text[i:i+2] == "**":
            end = text.find("**", i + 2)
            if end != -1:
                out.append(r"\textbf{" + escape(text[i+2:end]) + "}")
                i = end + 2
                continue
        # Italic: *...* (not **)
        if text[i] == "*" and text[i:i+2] != "**":
            end = text.find("*", i + 1)
            # Make sure the closing * is not part of **
            if end != -1 and text[end:end+2] != "**":
                out.append(r"\textit{" + escape(text[i+1:end]) + "}")
                i = end + 1
                continue
        # Accumulate plain characters up to the next *
        j = i + 1
        while j < n and text[j] != "*":
            j += 1
        out.append(escape(text[i:j]))
        i = j
    return "".join(out)


PREAMBLE = r"""\documentclass[11pt,a4paper]{article}
\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}
\usepackage[expansion=false]{microtype}
\usepackage[a4paper, margin=2.5cm]{geometry}
\usepackage{setspace}
\usepackage{parskip}
\usepackage[hidelinks]{hyperref}
\onehalfspacing
\setcounter{secnumdepth}{0}
\begin{document}
"""

POSTAMBLE = r"\end{document}" + "\n"


def convert(md_text):
    lines = md_text.splitlines()
    out = [PREAMBLE]

    for line in lines:
        s = line.strip()

        # H1 title
        if re.match(r"^# [^#]", s):
            out.append(r"{\LARGE\bfseries " + inline(s[2:]) + r"\par}")
            out.append(r"\medskip")

        # H2 week headings
        elif re.match(r"^## ", s):
            out.append(r"\section{" + inline(s[3:]) + "}")

        # Horizontal rule
        elif s == "---":
            out.append(r"\noindent\rule{\textwidth}{0.4pt}" + "\n")

        # Blank line
        elif s == "":
            out.append("")

        # Normal paragraph line
        else:
            out.append(inline(s))

    out.append(POSTAMBLE)
    return "\n".join(out)


with open(INPUT, encoding="utf-8") as f:
    md = f.read()

tex = convert(md)

with open(OUTPUT, "w", encoding="utf-8") as f:
    f.write(tex)

print(f"Written {OUTPUT} ({len(tex.splitlines())} lines)")
