"""全350問を問題ID順に25問(100肢)ずつ14チャンクに分割し、タグ付け入力を作る。正解・正誤は含めない。"""
import json
S=[json.loads(l) for l in open("02_マスターデータ/問題構造.jsonl",encoding="utf-8")]
S.sort(key=lambda s:s["問題ID"])
assert len(S)==350
n=0
for c in range(14):
    part=S[c*25:(c+1)*25]
    with open(f"02_マスターデータ/タグ付け/入力_{c+1:02d}.jsonl","w",encoding="utf-8") as f:
        for s in part:
            items=s["肢"] if s["肢"] else s["選択肢"]
            for i in range(4):
                f.write(json.dumps({"肢ID":f"{s['問題ID']}-{i+1}","問題ID":s["問題ID"],"出題形式":s["形式"],"設問文":s["設問文"],"肢本文":items[i]},ensure_ascii=False)+"\n"); n+=1
    print(c+1,part[0]["問題ID"],"〜",part[-1]["問題ID"])
print("肢",n)
