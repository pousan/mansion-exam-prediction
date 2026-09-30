"""タグ付け出力(モデル別・14チャンク)の検証。使い方: validate_tags.py sonnet
欠落/重複/想定外ID/無効論点ID、確信度分布、論点別件数、副論点・メモ率、4肢同一論点の問題率を出力。"""
import json, csv, sys, glob, collections
model=sys.argv[1]; D="02_マスターデータ/タグ付け/"
valid={r["論点ID"] for r in csv.DictReader(open("02_マスターデータ/論点分類表.csv",encoding="utf-8-sig"))}
tot=0; rows={}; problems=[]
for c in range(1,15):
    inp=[json.loads(l)["肢ID"] for l in open(D+f"入力_{c:02d}.jsonl",encoding="utf-8")]
    try: out=[json.loads(l) for l in open(D+f"出力_{model}_{c:02d}.jsonl",encoding="utf-8") if l.strip()]
    except FileNotFoundError: problems.append(f"chunk{c:02d}: ファイル無し"); continue
    ids=[o.get("肢ID") for o in out]
    if collections.Counter(ids)!=collections.Counter(inp): problems.append(f"chunk{c:02d}: 肢ID不一致 欠落{sorted(set(inp)-set(ids))[:3]} 余剰{sorted(set(ids)-set(inp))[:3]} 重複{[k for k,v in collections.Counter(ids).items() if v>1][:3]}")
    for o in out:
        if o.get("論点ID") not in valid|{"なし"}: problems.append(f"{o.get('肢ID')}: 無効な論点ID {o.get('論点ID')}")
        sub=o.get("副論点ID","")
        if sub and sub not in valid: problems.append(f"{o.get('肢ID')}: 無効な副論点ID {sub}")
        rows[o["肢ID"]]=o
print(model,"肢数",len(rows),"問題点",len(problems)); [print(" ",p) for p in problems[:20]]
print("確信度:",dict(collections.Counter(o.get("確信度") for o in rows.values())))
print("論点=なし:",sum(o["論点ID"]=="なし" for o in rows.values()),"／副論点あり:",sum(bool(o.get("副論点ID")) for o in rows.values()),"／メモあり:",sum(bool(o.get("メモ")) for o in rows.values()))
qs=collections.defaultdict(set)
for i,o in rows.items(): qs[i.rsplit("-",1)[0]].add(o["論点ID"])
print("4肢が同一論点の問題:",sum(len(v)==1 for v in qs.values()),"/",len(qs))
cnt=collections.Counter(o["論点ID"] for o in rows.values())
print("使われた論点数:",len(cnt),"／未使用の論点:",sorted(valid-set(cnt)))
print("上位:",cnt.most_common(8))
json.dump(rows,open(D+f"統合_{model}.json","w",encoding="utf-8"),ensure_ascii=False)
