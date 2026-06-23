from pathlib import Path
import sys
import pymupdf

pdf_path = sys.argv[1]

with pymupdf.open(pdf_path) as doc:  #open document
    text = "\f".join(page.get_text() for page in doc) 
    """
    above line is same as below block
    texts = []

    for page in doc:
        texts.append(page.get_text())

    text = chr(12).join(texts) #chr(12) is a form feed character(\x0c or \f) used as a separator, merging all the elements
    """
# write as a binary file to support non-ASCII characters
Path(f"{pdf_path}.txt").write_text(text, encoding="utf-8")