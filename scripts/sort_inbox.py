"""00_受信箱のPDFを表紙(中身)の判定結果に基づき 01_原本/過去問/ へ移動し、仕分け記録.csvを作る。
判定はR0-R5=テキスト抽出、R6=画像PDFのため目視(1ページ目を画像化して確認)。"""
import pymupdf, re, csv, subprocess, hashlib, os
# (元ファイル名, 西暦, 和暦, 判定方法, 判定根拠)
ITEMS = [
 ("pastexam_r0_legal_licensed_condominium_manager.pdf",2019,"R01","text","表紙『令和元年度 マンション管理士試験 問題』"),
 ("pastexam_r2_legal_licensed_condominium_manager.pdf",2020,"R02","text","表紙『令和２年度 マンション管理士試験 問題』"),
 ("pastexam_r3_legal_licensed_condominium_manager.pdf",2021,"R03","text","表紙『令和３年度 マンション管理士試験 問題』"),
 ("pastexam_r4_legal_licensed_condominium_manager.pdf",2022,"R04","text","表紙『令和４年度 マンション管理士試験 問題』"),
 ("pastexam_r5_legal_licensed_condominium_manager.pdf",2023,"R05","text","表紙『令和５年度 マンション管理士試験 問題』"),
 ("pastexam_r6_legal_licensed_condominium_manager.pdf",2024,"R06","visual","画像PDF(テキスト0文字)。1ページ目を画像化し目視で『令和6年度 マンション管理士試験 問題』と確認"),
]
rows=[]
for src,y,r,method,basis in ITEMS:
    path=f"00_受信箱/{src}"
    d=pymupdf.open(path)
    qs=set()
    if method=="text":
        for p in d: qs |= {int(n) for n in re.findall(r"〔問\s*(\d+)\s*〕",p.get_text())}
    qinfo = f"問番号検出{len(qs)}件(1-50欠落:{sorted(set(range(1,51))-qs)})" if method=="text" else "問題数はOCR未実施のため未検証"
    new=f"{y}_{r}_問題.pdf"
    subprocess.run(["git","mv",path,f"01_原本/過去問/{new}"],check=True)
    status="仕分け済(問題のみ・解答なし)"
    rows.append([src,f"{y}年度({r}) 問題",f"{basis}; ページ数{len(d)}; {qinfo}; 末尾は問50で終了し解答ページなし",new,status])
with open("02_マスターデータ/仕分け記録.csv","w",newline="",encoding="utf-8-sig") as f:
    w=csv.writer(f); w.writerow(["元ファイル名","判定した年度と種別","判定根拠","新ファイル名","状態"]); w.writerows(rows)
for r in rows: print(r[3],"|",r[2])
