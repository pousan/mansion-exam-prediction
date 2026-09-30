import pymupdf, glob, os
for f in sorted(glob.glob("00_受信箱/*.pdf")):
    d = pymupdf.open(f)
    chars = [len(p.get_text()) for p in d]
    print("=====", os.path.basename(f))
    print("pages:", len(d), "| meta title:", d.metadata.get("title"), "| created:", d.metadata.get("creationDate"))
    print("text chars per page (first 8):", chars[:8], "| total:", sum(chars), "| images p1:", len(d[0].get_images()))
    print("--- p1 text ---")
    print(d[0].get_text()[:400])
