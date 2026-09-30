import pymupdf, glob, os, re
for f in sorted(glob.glob("00_受信箱/*.pdf")):
    d = pymupdf.open(f)
    if sum(len(p.get_text()) for p in d)==0: continue
    hits=[i+1 for i,p in enumerate(d) if re.search(r"正\s*解|解\s*答\s*一\s*覧|正解番号", p.get_text())]
    print(os.path.basename(f), "pages with 正解/解答一覧:", hits)
    print("  last page text:", d[-1].get_text()[:200].replace("\n"," "))
d = pymupdf.open("00_受信箱/pastexam_r6_legal_licensed_condominium_manager.pdf")
for n in (0,31):
    d[n].get_pixmap(dpi=70).save(f"/tmp/r6/p{n+1}.png")
