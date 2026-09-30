import pymupdf, glob, os, re
for f in sorted(glob.glob("00_受信箱/*answer*.pdf")):
    d = pymupdf.open(f); m = d.metadata
    t = d[0].get_text()
    print("==", os.path.basename(f), "| title:", m.get("title"), "| created:", m.get("creationDate"), "| mod:", m.get("modDate"), "| producer:", m.get("producer"))
    print("   tail:", t[-90:].replace("\n"," "))
d = pymupdf.open("00_受信箱/R6_shiken.pdf")
t = d[-1].get_text()
print("R6_shiken 最終ページ:", t[:140].replace("\n"," "))
