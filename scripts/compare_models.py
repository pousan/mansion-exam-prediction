"""パイロット(100肢)の3モデル出力を検証・比較する。すべてコードで集計。
出力: 03_分析/モデル比較/{一致率.csv, 不一致一覧.csv, 混同ペア.csv, 検証結果.txt}"""
import json, csv, itertools, os
from collections import Counter
D="03_分析/モデル比較/"
models=["haiku","sonnet","opus"]
inp=[json.loads(l) for l in open(D+"パイロット入力_100肢.jsonl",encoding="utf-8")]
ids=[r["肢ID"] for r in inp]; IN={r["肢ID"]:r for r in inp}
valid={r["論点ID"] for r in csv.DictReader(open("02_マスターデータ/論点分類表_案_v0.2.csv",encoding="utf-8-sig"))}
name={r["論点ID"]:r["論点名"] for r in csv.DictReader(open("02_マスターデータ/論点分類表_案_v0.2.csv",encoding="utf-8-sig"))}
out={}; log=[]
for m in models:
    p=D+f"出力_{m}.jsonl"
    if not os.path.exists(p): log.append(f"{m}: 出力ファイル無し"); continue
    rows=[json.loads(l) for l in open(p,encoding="utf-8") if l.strip()]
    got=[r.get("肢ID") for r in rows]
    dup=[k for k,c in Counter(got).items() if c>1]; miss=sorted(set(ids)-set(got)); extra=sorted(set(got)-set(ids))
    badid=[(r.get("肢ID"),r.get("論点ID")) for r in rows if r.get("論点ID") not in valid and r.get("論点ID")!="なし"]
    log.append(f"{m}: 行数{len(rows)} 重複{dup} 欠落{miss} 想定外ID{extra} 無効な論点ID{badid}")
    out[m]={r["肢ID"]:r for r in rows if r.get("肢ID") in IN}
    log.append(f"   確信度: {dict(Counter(r.get('確信度') for r in rows))}  論点ID=なし: {sum(r.get('論点ID')=='なし' for r in rows)}")
ms=[m for m in models if m in out]
def kappa(a,b):
    n=len(a); po=sum(x==y for x,y in zip(a,b))/n
    ca,cb=Counter(a),Counter(b); pe=sum(ca[k]*cb[k] for k in set(ca)|set(cb))/(n*n)
    return (po-pe)/(1-pe) if pe<1 else 1.0
rows_a=[]
for x,y in itertools.combinations(ms,2):
    A=[out[x].get(i,{}).get("論点ID") for i in ids]; B=[out[y].get(i,{}).get("論点ID") for i in ids]
    pa=sum(a==b for a,b in zip(A,B)); fa=sum((a or "")[:2]==(b or "")[:2] for a,b in zip(A,B))
    rows_a.append([f"{x}-{y}","論点",pa,len(ids),round(pa/len(ids),3),round(kappa(A,B),3)])
    rows_a.append([f"{x}-{y}","分野(ID頭2字)",fa,len(ids),round(fa/len(ids),3),""])
if len(ms)==3:
    T=[tuple(out[m][i]["論点ID"] for m in ms) for i in ids]
    a3=sum(len(set(t))==1 for t in T); maj=sum(len(set(t))<3 for t in T)
    rows_a.append(["3者一致","論点",a3,len(ids),round(a3/len(ids),3),""]); rows_a.append(["3者のうち2者以上一致","論点",maj,len(ids),round(maj/len(ids),3),""])
with open(D+"一致率.csv","w",newline="",encoding="utf-8-sig") as f:
    w=csv.writer(f); w.writerow(["組","粒度","一致数","総数","一致率","Cohen_kappa"]); w.writerows(rows_a)
dis=[]; pairs=Counter()
for i in ids:
    tags=[out[m][i]["論点ID"] for m in ms]
    if len(set(tags))>1:
        dis.append([i,IN[i]["問題ID"],IN[i]["出題形式"],*tags,*[out[m][i].get("確信度","") for m in ms],IN[i]["肢本文"][:80],"; ".join(f"{m}:{out[m][i].get('メモ','')}" for m in ms if out[m][i].get("メモ"))[:160]])
        for a,b in itertools.combinations(sorted(set(tags)),2): pairs[(a,b)]+=1
with open(D+"不一致一覧.csv","w",newline="",encoding="utf-8-sig") as f:
    w=csv.writer(f); w.writerow(["肢ID","問題ID","形式",*[f"論点_{m}" for m in ms],*[f"確信度_{m}" for m in ms],"肢本文(冒頭80字)","メモ"]); w.writerows(dis)
with open(D+"混同ペア.csv","w",newline="",encoding="utf-8-sig") as f:
    w=csv.writer(f); w.writerow(["論点A","論点A名","論点B","論点B名","不一致肢数"]); [w.writerow([a,name.get(a,""),b,name.get(b,""),c]) for (a,b),c in pairs.most_common()]
open(D+"検証結果.txt","w",encoding="utf-8").write("\n".join(log))
print("\n".join(log)); [print(r) for r in rows_a]; print("不一致肢",len(dis)); print("混同ペア上位",pairs.most_common(12))
