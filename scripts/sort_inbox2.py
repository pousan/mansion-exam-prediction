"""第2回仕分け: mankan.org/pdf から取得した問題(R7, R6テキスト版)と正解7年分を、中身の表記に基づき 01_原本/過去問/ へ移動。
正解PDFは1ページ目末尾の『令和X年度マンション管理士試験正解』で年度判定(ファイル名は使わない)。"""
import pymupdf, re, csv, subprocess, os
ROOT_IN="00_受信箱"; OUT="01_原本/過去問"
ERA={"元":1,"２":2,"３":3,"４":4,"５":5,"６":6,"７":7}
rows=[]
def mv(src,new): os.rename(f"{ROOT_IN}/{src}",f"{OUT}/{new}")
# 既存の画像版R6問題を退避し、テキスト版を正本名にする(内容確認: 表紙・問50が一致)
if not os.path.exists(f"{OUT}/2024_R06_問題_画像版.pdf"): os.rename(f"{OUT}/2024_R06_問題.pdf",f"{OUT}/2024_R06_問題_画像版.pdf")
# 問題
for src,y,r in [("R7_shiken.pdf",2025,"R07"),("R6_shiken.pdf",2024,"R06")]:
    d=pymupdf.open(f"{ROOT_IN}/{src}"); t=d[0].get_text()
    m=re.search(r"令和\s*(\d|元)\s*年度",t.replace("　",""))
    era=m.group(1) if m else None
    qs=set()
    for p in d: qs|={int(n) for n in re.findall(r"〔問\s*(\d+)\s*〕",p.get_text())}
    assert "問題" in t
    new=f"{y}_{r}_問題.pdf"; mv(src,new)
    rows.append([src,f"{y}年度({r}) 問題","表紙『令和%s年度 マンション管理士試験 問題』; テキストPDF; ページ数%d; 問番号検出%d件(欠落:%s)%s"%(era,len(d),len(qs),sorted(set(range(1,51))-qs),"; 取得元mankan.org。既存の画像版(2024_R06_問題_画像版.pdf)と表紙・最終ページ(問50)一致を目視確認、全問の一致は未検証" if r=="R06" else "; 取得元mankan.org"),new,"仕分け済(問題)"])
# 正解
for src in ["R01_answer.pdf","R2_answer2.pdf","R03_answer.pdf","R04_answer.pdf","R5_answer.pdf","R6_answer.pdf","R7_answer.pdf"]:
    d=pymupdf.open(f"{ROOT_IN}/{src}"); t=d[0].get_text().replace("\n","")
    m=re.search(r"令和(元|\d|[０-９])年度マンション管理士試験正解",t.translate(str.maketrans("０１２３４５６７８９","0123456789")))
    era=m.group(1); n=1 if era=="元" else int(era); y=2018+n
    note=""
    if n==4: note="; 問4=正解なし、問9=2,3の複数扱い(ページ内の注記あり)"
    if n==2: note="; 問23=1、3の複数扱い"
    new=f"{y}_R{n:02d}_解答.pdf"; mv(src,new)
    rows.append([src,f"{y}年度(R{n:02d}) 解答",f"1ページ目末尾『令和{era}年度マンション管理士試験正解』で判定; PDF作成日{d.metadata.get('creationDate')[2:10]}; 取得元mankan.org{note}",new,"仕分け済(解答)。内容は肢マスター作成時にCSV化・検証"])
with open("02_マスターデータ/仕分け記録.csv","a",newline="",encoding="utf-8-sig") as f:
    csv.writer(f).writerows(rows)
for r in rows: print(r[3],"|",r[2][:110])
