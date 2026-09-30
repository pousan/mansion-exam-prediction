"""Sonnet/Opusで論点IDが割れた肢を抽出し、判定用入力を作る(両者の候補・確信度・メモ・肢本文を含む)。"""
import json
D="02_マスターデータ/タグ付け/"
S=json.load(open(D+"統合_sonnet.json",encoding="utf-8")); O=json.load(open(D+"統合_opus.json",encoding="utf-8"))
inp={}
for c in range(1,15):
    for l in open(D+f"入力_{c:02d}.jsonl",encoding="utf-8"):
        r=json.loads(l); inp[r["肢ID"]]=r
rows=[]
for i in sorted(S):
    if S[i]["論点ID"]!=O[i]["論点ID"]:
        r=inp[i]
        rows.append({"肢ID":i,"出題形式":r["出題形式"],"設問文":r["設問文"],"肢本文":r["肢本文"],
            "候補A":{"論点ID":S[i]["論点ID"],"確信度":S[i].get("確信度"),"メモ":S[i].get("メモ",""),"副論点ID":S[i].get("副論点ID","")},
            "候補B":{"論点ID":O[i]["論点ID"],"確信度":O[i].get("確信度"),"メモ":O[i].get("メモ",""),"副論点ID":O[i].get("副論点ID","")}})
with open(D+"判定入力.jsonl","w",encoding="utf-8") as f:
    for r in rows: f.write(json.dumps(r,ensure_ascii=False)+"\n")
print(len(rows),"肢")
