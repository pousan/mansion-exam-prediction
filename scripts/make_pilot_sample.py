"""パイロット用サンプル(25問×4肢=100肢)を層化抽出。層は問番号帯(出題順が分野に概ね対応するため)。seed固定。
正解・正誤はタガー用入力に含めない。"""
import csv, json, random
random.seed(20260930)
S={json.loads(l)["問題ID"]:json.loads(l) for l in open("02_マスターデータ/問題構造.jsonl",encoding="utf-8")}
bands=[(1,11,5),(12,17,3),(18,24,3),(25,33,5),(34,35,1),(36,39,2),(40,45,3),(46,50,3)]
sel=[]
for lo,hi,k in bands:
    pool=[q for q,s in S.items() if lo<=s["問番号"]<=hi]
    sel+=random.sample(pool,k)
# B形式が少なくとも4問含まれるか確認し、不足なら入れ替え
def nB(sel): return sum(S[q]["形式"]=="B" for q in sel)
print("B形式の数",nB(sel))
sel=sorted(sel)
rows=[]
for q in sel:
    s=S[q]; items=s["肢"] if s["肢"] else s["選択肢"]
    for i in range(4):
        rows.append({"肢ID":f"{q}-{i+1}","問題ID":q,"出題形式":s["形式"],"設問文":s["設問文"],"肢本文":items[i]})
with open("03_分析/モデル比較/パイロット入力_100肢.jsonl","w",encoding="utf-8") as f:
    for r in rows: f.write(json.dumps(r,ensure_ascii=False)+"\n")
json.dump({"抽出問題":sel,"seed":20260930,"層":bands},open("03_分析/モデル比較/パイロット抽出条件.json","w",encoding="utf-8"),ensure_ascii=False,indent=1)
print(len(sel),"問",len(rows),"肢"); print(sel)
