"""2026年試験の事前登録ファイルを作る(一度作ったら上書き禁止)。
入力: 05_2026予測/2026_予測_統計.csv, 2026_予測_LLM解釈.csv の上位15論点。
出力: 05_2026予測/2026_予測_事前登録.csv (手法,順位,論点ID,論点名,K5,K10,K15) と 2026_事前登録_ハッシュ.txt(SHA-256とJST日時)。
コミットとgitタグは別途手動(登録後は編集しない)。"""
import csv, os, hashlib, datetime
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
D = "05_2026予測"; OUT = f"{D}/2026_予測_事前登録.csv"; HS = f"{D}/2026_事前登録_ハッシュ.txt"
assert not os.path.exists(OUT) and not os.path.exists(HS), "登録済み。上書き禁止"
def top15(path, rk):
    rows = list(csv.DictReader(open(path, encoding="utf-8-sig")))
    return [(int(r[rk]), r["論点ID"], r["論点名"]) for r in sorted(rows, key=lambda r: int(r[rk]))[:15]]
with open(OUT, "w", encoding="utf-8-sig", newline="") as f:
    w = csv.writer(f); w.writerow(["手法", "順位", "論点ID", "論点名", "K=5に含む", "K=10に含む", "K=15に含む"])
    for m, p, rk in [("統計(全7年の肢数頻度順)", f"{D}/2026_予測_統計.csv", "頻度順位"), ("LLM解釈(法改正内容から)", f"{D}/2026_予測_LLM解釈.csv", "LLM順位")]:
        t = top15(p, rk); assert [x[0] for x in t] == list(range(1, 16)), m
        for r, tid, nm in t: w.writerow([m, r, tid, nm, int(r <= 5), int(r <= 10), int(r <= 15)])
sha = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()
now = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9))).isoformat(timespec="seconds")
files = [OUT, f"{D}/2026_予測_統計.csv", f"{D}/2026_予測_LLM解釈.csv", f"{D}/2026_法改正一覧.csv", f"{D}/2026_論点別_改正影響.csv"]
with open(HS, "w", encoding="utf-8") as f:
    f.write(f"事前登録日時(JST, ローカル時計): {now}\n試験日: 2026-11-29\n登録内容: 統計予測とLLM解釈予測の上位15論点(K=5,10,15)。登録後は編集しない。\nSHA-256:\n")
    for p in files: f.write(f"{sha(p)}  {p}\n")
print(open(HS, encoding="utf-8").read())
