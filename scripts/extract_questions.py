"""01_原本/過去問/*_問題.pdf(テキスト版)から問題ごとに本文を抽出し 02_マスターデータ/問題テキスト.jsonl に保存。
問題ID=年度-問番号(2桁)。画像版は対象外。"""
import sys, re, json, glob, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pdfutil import doc_text
out=[]
for f in sorted(glob.glob("01_原本/過去問/*_問題.pdf")):
    y=os.path.basename(f)[:4]
    txt=doc_text(f)
    parts=re.split(r"〔問\s*(\d+)\s*〕",txt)
    found=0
    for i in range(1,len(parts),2):
        n=int(parts[i]); body=re.sub(r"[ 　]*\n[ 　]*","",parts[i+1]).strip()
        out.append({"問題ID":f"{y}-{n:02d}","年度":int(y),"問番号":n,"本文":body}); found+=1
    print(y,found,"問")
with open("02_マスターデータ/問題テキスト.jsonl","w",encoding="utf-8") as f:
    for o in out: f.write(json.dumps(o,ensure_ascii=False)+"\n")
print("total",len(out))
