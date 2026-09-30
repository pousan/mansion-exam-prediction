"""01_原本/過去問/*_問題.pdf(テキスト版)から問題ごとに本文を抽出し 02_マスターデータ/問題テキスト.jsonl に保存。
問題ID=年度-問番号(2桁)。画像版は対象外。"""
import pymupdf, re, json, glob, os
out=[]
for f in sorted(glob.glob("01_原本/過去問/*_問題.pdf")):
    y=os.path.basename(f)[:4]
    d=pymupdf.open(f)
    txt="\n".join(p.get_text() for p in d)
    # ページ番号行のノイズ除去(単独の数字行)
    txt=re.sub(r"\n\s*[\-－―]?\s*\d{1,2}\s*[\-－―]?\s*\n","\n",txt)
    parts=re.split(r"〔問\s*(\d+)\s*〕",txt)
    found=0
    for i in range(1,len(parts),2):
        n=int(parts[i]); body=re.sub(r"\s+","",parts[i+1]) if False else re.sub(r"[ 　]*\n[ 　]*","",parts[i+1]).strip()
        out.append({"問題ID":f"{y}-{n:02d}","年度":int(y),"問番号":n,"本文":body}); found+=1
    print(y,found,"問")
with open("02_マスターデータ/問題テキスト.jsonl","w",encoding="utf-8") as f:
    for o in out: f.write(json.dumps(o,ensure_ascii=False)+"\n")
print("total",len(out))
