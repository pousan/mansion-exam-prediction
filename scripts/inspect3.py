import pymupdf, glob, os
for f in sorted(glob.glob("00_受信箱/*.pdf")):
    d = pymupdf.open(f)
    t = d[0].get_text()
    print("=====", os.path.basename(f), "pages", len(d), "chars", sum(len(p.get_text()) for p in d))
    print(t[:260].replace("\n"," "))
