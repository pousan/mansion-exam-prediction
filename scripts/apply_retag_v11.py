"""v1.1再タグ付け(74肢)を検証し、最終タグ・肢マスター・問題マスターへ反映する。変化はコードで集計。"""
import json, csv, collections
D="02_マスターデータ/タグ付け/"
valid={r["論点ID"]:r for r in csv.DictReader(open("02_マスターデータ/論点分類表.csv",encoding="utf-8-sig"))}
R={}
for l in open(D+"出力_sonnet_v11再タグ.jsonl",encoding="utf-8"):
    r=json.loads(l); R[r["肢ID"]]=r
tgt=[r["肢ID"] for r in csv.DictReader(open(D+"再タグ付け対象_v1.1案.csv",encoding="utf-8-sig"))]
assert sorted(R)==sorted(tgt) and len(tgt)==len(set(tgt)), "肢ID不一致"
bad=[(i,r["論点ID"]) for i,r in R.items() if r["論点ID"] not in valid and r["論点ID"]!="なし"]
print("74肢/無効ID:",bad,"／確信度:",dict(collections.Counter(r.get("確信度") for r in R.values())))
F=json.load(open(D+"最終タグ.json",encoding="utf-8")); json.dump(F,open(D+"最終タグ_v1.0.json","w",encoding="utf-8"),ensure_ascii=False)
chg=[]
for i,r in R.items():
    old=F[i]["論点"]; new=r["論点ID"]
    if old!=new: chg.append((i,old,new))
    F[i]=dict(論点=new,副論点=r.get("副論点ID") or "",区分="v1.1再タグ",確信度=r.get("確信度","中"),法令=r.get("根拠法令","") or F[i]["法令"])
print("タグが変わった肢:",len(chg),"／変わらず:",74-len(chg))
print("変化の内訳(旧→新 上位):",collections.Counter((a,b) for _,a,b in chg).most_common(12))
print("MN07:",sum(1 for i in F if F[i]["論点"]=="MN07"),"肢／なし:",[i for i in F if F[i]["論点"]=="なし"])
json.dump(F,open(D+"最終タグ.json","w",encoding="utf-8"),ensure_ascii=False)
K=list(csv.DictReader(open("02_マスターデータ/肢マスター.csv",encoding="utf-8-sig")))
cols=list(K[0].keys())
for r in K:
    f=F[r["肢ID"]]; r["論点ID"]=f["論点"]; r["副論点ID"]=f["副論点"]; r["根拠法令"]=f["法令"]; r["タグ付け区分"]=f["区分"]; r["タグ確信度"]=f["確信度"]
with open("02_マスターデータ/肢マスター.csv","w",newline="",encoding="utf-8-sig") as fo:
    w=csv.DictWriter(fo,fieldnames=cols); w.writeheader(); w.writerows(K)
M=list(csv.DictReader(open("02_マスターデータ/問題マスター.csv",encoding="utf-8-sig"))); mc=list(M[0].keys())
BUNYA={"KS":"区分所有法","MN":"民法・借地借家法","TK":"不動産登記法","EK":"円滑化法","KR":"関係法令","KY":"標準管理規約","KZ":"会計・税務","SH":"修繕・診断","SB":"建築・設備","TH":"適正化法"}
byq=collections.defaultdict(list)
for r in K: byq[r["問題ID"]].append(r["論点ID"])
for m in M:
    c=collections.Counter(byq[m["問題ID"]]).most_common(); top=c[0][0]; tie=len(c)>1 and c[0][1]==c[1][1]
    m["論点ID(主)"]=top; m["分野"]=BUNYA.get(top[:2],"なし"); m["肢の論点混在"]="同数(要確認)" if tie else ("混在" if len(c)>1 else "")
with open("02_マスターデータ/問題マスター.csv","w",newline="",encoding="utf-8-sig") as fo:
    w=csv.DictWriter(fo,fieldnames=mc); w.writeheader(); w.writerows(M)
print("問題:混在",sum(m["肢の論点混在"]=="混在" for m in M),"／同数",sum(m["肢の論点混在"].startswith("同数") for m in M),"／主論点『なし』",sum(m["論点ID(主)"]=="なし" for m in M))
samp={r["肢ID"] for r in csv.DictReader(open("03_分析/品質検証_5%抽出.csv",encoding="utf-8-sig"))}
print("5%抽出のうち v1.1でタグが変わった肢:",[(i,a,b) for i,a,b in chg if i in samp])
print("論点別 問題数の最小5:",collections.Counter(m["論点ID(主)"] for m in M).most_common()[-5:])
