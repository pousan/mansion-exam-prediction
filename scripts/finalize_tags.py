"""Sonnet/Opusのタグと判定結果を統合し、肢マスター・問題マスターに反映、5%抽出を作る。
最終論点 = 2者一致ならそれ、割れた肢は判定結果。すべてコードで集計。"""
import json, csv, random, collections
D="02_マスターデータ/タグ付け/"
valid={r["論点ID"]:r for r in csv.DictReader(open("02_マスターデータ/論点分類表.csv",encoding="utf-8-sig"))}
S=json.load(open(D+"統合_sonnet.json",encoding="utf-8")); O=json.load(open(D+"統合_opus.json",encoding="utf-8"))
J={}
for l in open(D+"判定結果.jsonl",encoding="utf-8"):
    r=json.loads(l); J[r["肢ID"]]=r
dis=[i for i in S if S[i]["論点ID"]!=O[i]["論点ID"]]
assert set(J)==set(dis) and len(J)==50, (len(J),len(dis))
bad=[(i,J[i]["最終論点ID"]) for i in J if J[i]["最終論点ID"] not in valid and J[i]["最終論点ID"]!="なし"]
print("判定結果:無効ID",bad)
print("選んだ候補:",collections.Counter(J[i]["選んだ候補"] for i in J))
final={}
for i in sorted(S):
    if i in J:
        j=J[i]; sub=j.get("副論点ID") or ""
        final[i]=dict(論点=j["最終論点ID"],副論点=sub,区分="判定",確信度="判定",法令=O[i].get("根拠法令","") or S[i].get("根拠法令",""))
    else:
        sub=O[i].get("副論点ID") or S[i].get("副論点ID") or ""
        final[i]=dict(論点=S[i]["論点ID"],副論点=sub,区分="2者一致",確信度=min([S[i].get("確信度","中"),O[i].get("確信度","中")],key={"高":2,"中":1,"低":0}.get),法令=O[i].get("根拠法令","") or S[i].get("根拠法令",""))
print("最終『なし』:",[i for i,v in final.items() if v["論点"]=="なし"])
# 肢マスター更新
K=list(csv.DictReader(open("02_マスターデータ/肢マスター.csv",encoding="utf-8-sig")))
cols=["肢ID","問題ID","肢番号","肢表記","論点ID","副論点ID","根拠法令","根拠条文","正誤","改正影響フラグ","出題形式","肢本文","タグ付け区分","タグ確信度","正誤の導出根拠"]
out=[]
for r in K:
    f=final[r["肢ID"]]
    out.append({**r,"論点ID":f["論点"],"副論点ID":f["副論点"],"根拠法令":f["法令"],"根拠条文":"要確認(条番号はe-Gov照合後に付与)","タグ付け区分":f["区分"],"タグ確信度":f["確信度"]})
with open("02_マスターデータ/肢マスター.csv","w",newline="",encoding="utf-8-sig") as fo:
    w=csv.DictWriter(fo,fieldnames=cols); w.writeheader(); [w.writerow({c:r.get(c,"") for c in cols}) for r in out]
# 問題マスター: 主論点=4肢の最頻(同数は肢番号の小さい順で先勝ち・要確認フラグ)
M=list(csv.DictReader(open("02_マスターデータ/問題マスター.csv",encoding="utf-8-sig")))
byq=collections.defaultdict(list)
for r in out: byq[r["問題ID"]].append(r["論点ID"])
BUNYA={"KS":"区分所有法","MN":"民法・借地借家法","TK":"不動産登記法","EK":"円滑化法","KR":"関係法令","KY":"標準管理規約","KZ":"会計・税務","SH":"修繕・診断","SB":"建築・設備","TH":"適正化法"}
mix=0
for m in M:
    t=byq[m["問題ID"]]; c=collections.Counter(t).most_common()
    top=c[0][0]; tie=len(c)>1 and c[0][1]==c[1][1]
    m["論点ID(主)"]=top; m["分野"]=BUNYA.get(top[:2],"なし"); m["肢の論点混在"]=("同数(要確認)" if tie else ("混在" if len(c)>1 else "")); mix+=len(c)>1
mc=["問題ID","年度","問番号","分野","論点ID(主)","肢の論点混在","出題形式","正解","特殊区分","設問極性","個数問題"]
with open("02_マスターデータ/問題マスター.csv","w",newline="",encoding="utf-8-sig") as fo:
    w=csv.DictWriter(fo,fieldnames=mc); w.writeheader(); [w.writerow({c:r.get(c,"") for c in mc}) for r in M]
print("問題:肢の論点が混在",mix,"／同数",sum(m["肢の論点混在"].startswith("同数") for m in M))
print("論点別 問題数(主論点)上位:",collections.Counter(m["論点ID(主)"] for m in M).most_common(6),"／最小:",collections.Counter(m["論点ID(主)"] for m in M).most_common()[-5:])
# 5%抽出(70肢)
random.seed(20261115)
ids=sorted(final); samp=sorted(random.sample(ids,70))
inp={}
for c in range(1,15):
    for l in open(D+f"入力_{c:02d}.jsonl",encoding="utf-8"):
        x=json.loads(l); inp[x["肢ID"]]=x
with open("03_分析/品質検証_5%抽出.csv","w",newline="",encoding="utf-8-sig") as fo:
    w=csv.writer(fo); w.writerow(["肢ID","設問文(冒頭120字)","肢本文(冒頭200字)","付与された論点ID","論点名","副論点ID","タグ付け区分","人の確認(○/×)","×の場合の正しい論点ID","メモ"])
    for i in samp:
        f=final[i]; x=inp[i]
        w.writerow([i,x["設問文"][:120],x["肢本文"][:200],f["論点"],valid.get(f["論点"],{}).get("論点名","なし"),f["副論点"],f["区分"],"","",""])
json.dump(final,open(D+"最終タグ.json","w",encoding="utf-8"),ensure_ascii=False)
print("5%抽出",len(samp),"肢 うち判定肢",sum(final[i]["区分"]=="判定" for i in samp))
# 境界の要検討
sug=[(i,J[i]["境界の要検討"]) for i in J if J[i].get("境界の要検討")]
print("判定者の境界提案",len(sug)); [print(" ",i,t[:110]) for i,t in sug[:14]]
