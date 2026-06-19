"""Convert thesis LaTeX and Markdown sources to DOCX via pandoc."""
import pypandoc
import os

THESIS = os.path.dirname(os.path.abspath(__file__))
FINAL  = os.path.join(THESIS, "final")
os.makedirs(FINAL, exist_ok=True)

conversions = [
    (os.path.join(THESIS, "main.tex"),
     os.path.join(FINAL, "Thesis.docx"),
     "latex",
     ["--resource-path=" + THESIS, "--wrap=none"]),

    (os.path.join(THESIS, "PoA_full.tex"),
     os.path.join(FINAL, "Plan_of_Approach.docx"),
     "latex",
     ["--resource-path=" + THESIS, "--wrap=none"]),

    (os.path.join(THESIS, "logbook.md"),
     os.path.join(FINAL, "Logbook.docx"),
     "markdown",
     ["--wrap=none"]),

    (os.path.join(THESIS, "competency_portfolio.tex"),
     os.path.join(FINAL, "Competency_Portfolio.docx"),
     "latex",
     ["--resource-path=" + THESIS, "--wrap=none"]),
]

for src, dst, fmt, args in conversions:
    name = os.path.basename(dst)
    try:
        pypandoc.convert_file(src, "docx", format=fmt, outputfile=dst, extra_args=args)
        size = os.path.getsize(dst)
        print(f"OK  {name}  ({size:,} bytes)")
    except Exception as exc:
        print(f"ERR {name}: {exc}")
