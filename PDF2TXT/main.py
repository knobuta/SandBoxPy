# convert PDF to text using pdfplumber

import pdfplumber

pdf_file = "/Full/Path/To/file.pdf"
out_file = "/Full/Path/To/output.txt"

with pdfplumber.open(pdf_file) as pdf, open(out_file, "w", encoding="utf-8") as f:
    for page in pdf.pages:
        t = page.extract_text()
        if t:
            f.write(t + '\n')
