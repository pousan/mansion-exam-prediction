"""解答PDF(7年分)から 問番号→正解 を抽出し 02_マスターデータ/正解表.csv に保存。
正解は文字列のまま保持(例: '3', '正解なし', '2,3', '1,3')。特殊区分は正解が単一数字でないもの。"""
import pymupdf, re, csv, glob, os
rows=[]
for f in sorted(glob.glob("01_原本/過去問/*_解答.pdf")):
    y=int(os.path.basename(f)[:4]); d=pymupdf.open(f)
    t=d[0].get_text().replace("　"," ")
    # 表部分(『問題 正解 問題 正解』以降、合格最低点/注記の手前)を1トークン列にする
    body=t.split("正解",2)[-1] if False else t
    toks=[x for x in re.split(r"\s+",body) if x]
    # 数字(問番号) + 正解(数字|正解なし|数字[、,]数字) のペアを1〜50の順で探す
    ans={}
    i=0
    while i<len(toks)-1:
        if re.fullmatch(r"\d{1,2}",toks[i]) and 1<=int(toks[i])<=50 and int(toks[i]) not in ans:
            n=int(toks[i]); v=toks[i+1]
            if re.fullmatch(r"[1-4]([、,][1-4])?|正解なし",v):
                ans[n]=v.replace("、",","); i+=2; continue
        i+=1
    miss=sorted(set(range(1,51))-set(ans))
    print(y,"抽出",len(ans),"欠落",miss)
    for n in range(1,51):
        v=ans.get(n,"")
        sp="" if re.fullmatch(r"[1-4]",v) else ("正解なし" if v=="正解なし" else ("複数正解" if v else "未抽出"))
        rows.append([f"{y}-{n:02d}",y,n,v,sp])
with open("02_マスターデータ/正解表.csv","w",newline="",encoding="utf-8-sig") as fo:
    w=csv.writer(fo); w.writerow(["問題ID","年度","問番号","正解","特殊区分"]); w.writerows(rows)
print("特殊:",[r[0]+":"+r[3] for r in rows if r[4]])
