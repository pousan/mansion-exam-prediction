"""問題PDFを、改行を保持したまま 設問文/肢/選択肢 に分解して 02_マスターデータ/問題構造.jsonl に保存(試作)。
形式: A=4択の各文が肢(1-4) / B=ア〜エの各文が肢＋1-4は組合せ・個数の選択肢 / C=空欄補充(〔ア〕〜〔エ〕)＋1-4は語句の組合せ / X=解析不能(要目視)"""
import sys, re, json, glob, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pdfutil import doc_text
from collections import Counter
NUM="１２３４1234"; KANA="アイウエ"
def norm(s): return s.translate(str.maketrans("１２３４","1234"))
out=[]
for f in sorted(glob.glob("01_原本/過去問/*_問題.pdf")):
    y=int(os.path.basename(f)[:4])
    txt=doc_text(f)
    parts=re.split(r"〔問\s*(\d+)\s*〕",txt)
    for k in range(1,len(parts),2):
        n=int(parts[k]); raw=parts[k+1]
        lines=[l.rstrip() for l in raw.split("\n")]
        # 行頭マーカー位置を収集
        def find(marks, pat):
            pos=[]
            for i,l in enumerate(lines):
                m=re.match(pat,l)
                if m and norm(m.group(1)) in marks: pos.append((i,norm(m.group(1))))
            return pos
        nums=find("1234", r"^\s*([１-４1-4])\s*(?:[　 ].*)?$")
        # 1,2,3,4が順に現れる最後の系列を採用
        seq=[];want=1
        for i,mk in nums:
            if int(mk)==want: seq.append(i); want+=1
            elif int(mk)==1: seq=[i]; want=2
        numok=(len(seq)==4)
        kanas=[(i,m) for i,l in enumerate(lines) for m in [re.match(r"^\s*([アイウエ])\s*(?:[　 ].*)?$",l)] if m]
        ks=[];want=0
        for i,(idx,mk) in enumerate(kanas):
            mk=mk.group(1)
            if mk==KANA[want]: ks.append(idx); want+=1
            elif mk=="ア": ks=[idx]; want=1
        kanaok=(len(ks)==4)
        blank=bool(re.search(r"〔\s*ア\s*〕",raw))
        def seg(idxs,end):
            res=[]
            for a,b in zip(idxs,idxs[1:]+[end]):
                ls=[l.strip() for l in lines[a:b] if l.strip()]
                # マーカーだけの行から始まる表形式の肢は、セルをスペースで連結する
                res.append(" ".join(ls[1:]) if ls and len(ls[0])<=2 else "".join(ls))
            return res
        rec={"問題ID":f"{y}-{n:02d}","年度":y,"問番号":n}
        if numok and not kanaok and not blank:
            rec["形式"]="A"; rec["設問文"]="".join(lines[:seq[0]]).strip(); rec["肢"]=seg(seq,len(lines)); rec["選択肢"]=None
        elif kanaok and numok and not blank:
            rec["形式"]="B"; rec["設問文"]="".join(lines[:ks[0]]).strip(); rec["肢"]=seg(ks,seq[0]); rec["選択肢"]=seg(seq,len(lines))
        elif blank and numok:
            rec["形式"]="C"; rec["設問文"]="".join(lines[:seq[0]]).strip(); rec["肢"]=None; rec["選択肢"]=seg(seq,len(lines))
        else:
            rec["形式"]="X"; rec["設問文"]="".join(lines).strip(); rec["肢"]=None; rec["選択肢"]=None
            rec["メモ"]=f"num={numok} kana={kanaok} blank={blank}"
        out.append(rec)
with open("02_マスターデータ/問題構造.jsonl","w",encoding="utf-8") as fo:
    for r in out: fo.write(json.dumps(r,ensure_ascii=False)+"\n")
print(Counter(r["形式"] for r in out))
print("X:",[ (r["問題ID"],r["メモ"]) for r in out if r["形式"]=="X"])
print("肢数分布:",Counter(len(r["肢"]) for r in out if r["肢"]))
