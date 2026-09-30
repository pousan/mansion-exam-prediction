"""問題構造.jsonl + 正解表.csv から 問題マスター.csv / 肢マスター.csv(タグ付け前の骨格)を生成する。
肢=A:選択肢1-4の各文 / B:ア〜エの各文(肢番号1-4=ア-エ) / C:空欄補充の語句の組合せ1-4。
正誤は機械的に導出できる場合のみ付与し、極性が不明・個数問題で確定できない場合は『要確認』『不明(個数)』とする。特殊区分の問題は『別区分』。"""
import json, csv, re
from collections import Counter
S=[json.loads(l) for l in open("02_マスターデータ/問題構造.jsonl",encoding="utf-8")]
A={r["問題ID"]:r for r in csv.DictReader(open("02_マスターデータ/正解表.csv",encoding="utf-8-sig"))}
NEG=r"誤っている|成立しない|有効でない|無効|誤り|適切でない|適当でない|正しくない|できない|認められない|規定されていない|定められていない|該当しない|含まれない|不適切"
POS=r"正しい|であるもの|に当たる|成立する|適切な|適当な|認められる|できる|該当する|規定されている|含まれる"
def polarity(stem):
    # 最初の『どれか/いくつあるか』までを設問の核とみなし、その末尾120字で極性を判定する(表・語句リストの混入対策)
    m=re.search(r"どれか|いくつあるか|１～４のうち|1～4のうち",stem)
    core=stem[:m.end()] if m else stem[-120:]
    tail=core[-120:]
    if re.search(NEG,tail): return "誤"
    if re.search(POS,tail): return "正"
    return None
KAN="アイウエ"; CNT={"一つ":1,"二つ":2,"三つ":3,"四つ":4,"なし":0}
def strip_no(t): return re.sub(r"^[１-４1-4]\s*[　 ]?","",t).strip()
mrows=[]; krows=[]
for s in S:
    qid=s["問題ID"]; a=A[qid]; ans=a["正解"]; sp=a["特殊区分"]; fm=s["形式"]
    pol=polarity(s["設問文"]) if s["形式"]!="C" else "正(空欄補充)"; count_q=bool(re.search(r"いくつ",s["設問文"]))
    items=s["肢"] if s["肢"] else s["選択肢"]
    truth=[None]*4; basis=""
    if sp: truth=["別区分"]*4; basis="特殊区分("+sp+")"
    elif fm=="C":
        truth=["正" if str(i+1)==ans else "誤" for i in range(4)]; basis="空欄補充:正解肢=正"
    elif fm=="A":
        if pol is None: truth=["要確認"]*4; basis="設問極性を判定できない"
        else:
            other="正" if pol=="誤" else "誤"
            truth=[pol if str(i+1)==ans else other for i in range(4)]; basis=f"設問は『{pol}』を選ぶ形式。正解肢={ans}"
    elif fm=="B":
        opts=[strip_no(t) for t in s["選択肢"]]; sel=opts[int(ans)-1]
        if count_q:
            n=CNT.get(sel)
            if pol is None or n is None: truth=["要確認"]*4; basis="個数問題:極性不明"
            elif n==0 or n==4:
                v=(pol if n==4 else ("誤" if pol=="正" else "正")); truth=[v]*4; basis=f"個数問題:{sel}で全肢確定"
            else: truth=["不明(個数)"]*4; basis=f"個数問題:{sel}のため肢別の正誤は確定不能"
        else:
            ks=set(re.findall(r"[アイウエ]",sel))
            if pol is None or not ks: truth=["要確認"]*4; basis="組合せ問題:極性または選択肢を解釈できない"
            else:
                other="正" if pol=="誤" else "誤"
                truth=[pol if KAN[i] in ks else other for i in range(4)]; basis=f"組合せ問題:{sel}=『{pol}』の肢"
    mrows.append([qid,s["年度"],s["問番号"],"","",fm,ans,sp,pol or "要確認",("個数" if count_q else "")])
    for i in range(4):
        krows.append([f"{qid}-{i+1}",qid,i+1,KAN[i] if fm=="B" else "","","",truth[i],"",fm,items[i] if items else "",basis])
with open("02_マスターデータ/問題マスター.csv","w",newline="",encoding="utf-8-sig") as f:
    w=csv.writer(f); w.writerow(["問題ID","年度","問番号","分野","論点ID(主)","出題形式","正解","特殊区分","設問極性","個数問題"]); w.writerows(mrows)
with open("02_マスターデータ/肢マスター.csv","w",newline="",encoding="utf-8-sig") as f:
    w=csv.writer(f); w.writerow(["肢ID","問題ID","肢番号","肢表記","論点ID","根拠条文","正誤","改正影響フラグ","出題形式","肢本文","正誤の導出根拠"]); w.writerows(krows)
print("問題",len(mrows),"肢",len(krows))
print("正誤:",Counter(r[6] for r in krows))
print("設問極性:",Counter(r[8] for r in mrows))
print("極性不明の問題:",[r[0] for r in mrows if r[8]=="要確認"])
