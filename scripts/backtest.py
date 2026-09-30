"""フェーズ4: 統計モデルのみのウォークフォワード・バックテスト(LLM不使用)。
単位=肢の論点ID(主)。年tの予測は t未満の年だけを使う。学習3年以上(テスト年 2022-2025)。
手法: random / frequency / periodic(頻出×間隔超過)。(d)法改正フラグはフェーズ5で追加。
指標: coverage=その年の肢のうち、予測上位K論点に属する肢の割合 / hit=上位K論点のうち実際に出題された論点の割合。"""
import csv, os, random, statistics
from collections import defaultdict
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
OUT = "03_分析/バックテスト結果"; os.makedirs(OUT, exist_ok=True)

rows = list(csv.DictReader(open("02_マスターデータ/肢マスター.csv", encoding="utf-8-sig")))
years = sorted({int(r["問題ID"][:4]) for r in rows})
topics = sorted({r["論点ID"] for r in rows})
cnt = {y: defaultdict(int) for y in years}          # 年×論点の肢数
for r in rows: cnt[int(r["問題ID"][:4])][r["論点ID"]] += 1

# 論点×年 行列を保存
with open(f"{OUT}/論点年行列.csv", "w", encoding="utf-8-sig", newline="") as f:
    w = csv.writer(f); w.writerow(["論点ID"] + years + ["合計"])
    for t in topics: w.writerow([t] + [cnt[y][t] for y in years] + [sum(cnt[y][t] for y in years)])

def scores(method, train, rng):
    """train=学習年のリスト(昇順)。論点→スコア。"""
    if method == "random": return {t: rng.random() for t in topics}
    tot = {t: sum(cnt[y][t] for y in train) for t in topics}
    if method == "frequency": return {t: tot[t] + 1e-3 * sum(cnt[y][t] > 0 for y in train) for t in topics}
    if method == "periodic":   # 出題年率 ×(1+最終出題からの経過年数)。未出題は経過=学習年数
        s = {}
        for t in topics:
            pres = [y for y in train if cnt[y][t] > 0]
            p = len(pres) / len(train)
            gap = train[-1] - pres[-1] if pres else len(train)
            s[t] = p * (1 + gap) + 1e-3 * tot[t]
        return s

def evaluate(method, test, K, nsim=1000):
    train = [y for y in years if y < test]
    actual = {t for t in topics if cnt[test][t] > 0}; n = sum(cnt[test].values())
    def one(rng):
        sc = scores(method, train, rng)
        top = sorted(topics, key=lambda t: (-sc[t], t))[:K]
        return sum(cnt[test][t] for t in top) / n, len(set(top) & actual) / K
    if method == "random":
        rng = random.Random(20261129); res = [one(rng) for _ in range(nsim)]
        return statistics.mean(a for a, _ in res), statistics.mean(b for _, b in res)
    return one(None)

METHODS = ["random", "frequency", "periodic"]; KS = [5, 10, 15]; TESTS = [y for y in years if len([z for z in years if z < y]) >= 3]
detail = []
for m in METHODS:
    for K in KS:
        for y in TESTS:
            c, h = evaluate(m, y, K); detail.append([m, K, y, round(c, 4), round(h, 4)])
with open(f"{OUT}/バックテスト_年別.csv", "w", encoding="utf-8-sig", newline="") as f:
    w = csv.writer(f); w.writerow(["手法", "K", "テスト年", "カバー率", "的中率"]); w.writerows(detail)
summ = []
for m in METHODS:
    for K in KS:
        d = [r for r in detail if r[0] == m and r[1] == K]
        summ.append([m, K, len(d), round(statistics.mean(r[3] for r in d), 4), round(statistics.mean(r[4] for r in d), 4)])
with open(f"{OUT}/バックテスト_サマリー.csv", "w", encoding="utf-8-sig", newline="") as f:
    w = csv.writer(f); w.writerow(["手法", "K", "テスト年数", "平均カバー率", "平均的中率"]); w.writerows(summ)

# SVG棒グラフ(K別、手法比較。上=カバー率、下=的中率)
cols = {"random": "#999999", "frequency": "#1f77b4", "periodic": "#ff7f0e"}
W, H = 720, 520; svg = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" font-family="sans-serif" font-size="12">',
                        '<rect width="100%" height="100%" fill="white"/>']
for pi, (idx, title) in enumerate([(3, "平均カバー率(肢ベース)"), (4, "平均的中率(論点ベース)")]):
    y0 = 40 + pi * 230; h = 160
    svg.append(f'<text x="20" y="{y0-15}" font-size="14">{title}  テスト年 {TESTS[0]}-{TESTS[-1]}({len(TESTS)}年)</text>')
    for g in range(0, 11, 2):
        yy = y0 + h - g / 10 * h; svg.append(f'<line x1="50" y1="{yy}" x2="{W-20}" y2="{yy}" stroke="#ddd"/><text x="10" y="{yy+4}">{g/10:.1f}</text>')
    for ki, K in enumerate(KS):
        for mi, m in enumerate(METHODS):
            v = [r for r in summ if r[0] == m and r[1] == K][0][idx]
            x = 80 + ki * 200 + mi * 50; bh = v * h
            svg.append(f'<rect x="{x}" y="{y0+h-bh}" width="42" height="{bh}" fill="{cols[m]}"/><text x="{x}" y="{y0+h-bh-4}">{v:.2f}</text>')
        svg.append(f'<text x="{110+ki*200}" y="{y0+h+16}">K={K}</text>')
for mi, m in enumerate(METHODS):
    svg.append(f'<rect x="{80+mi*130}" y="{H-25}" width="12" height="12" fill="{cols[m]}"/><text x="{96+mi*130}" y="{H-14}">{m}</text>')
svg.append("</svg>"); open(f"{OUT}/バックテスト.svg", "w", encoding="utf-8").write("\n".join(svg))

print("年:", years, "論点数:", len(topics), "テスト年:", TESTS)
for r in summ: print(r)
print("年別 出題された論点数:", {y: sum(1 for t in topics if cnt[y][t] > 0) for y in years})
