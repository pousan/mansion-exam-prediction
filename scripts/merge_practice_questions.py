"""4つの練習問題セット(各scriptで根拠原文の照合済み)を1冊の問題集にまとめる。内容は変更しない(通し番号の付与と整形のみ)。
入力: 06_練習問題/練習問題_{改正区分所有法,標準管理規約,民法,給排水設備告示}.csv
出力: 06_練習問題/練習問題_全集.csv / .md(問題編→正解と解説編。通し番号+元の問題ID)"""
import csv, os
from collections import Counter
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
SETS = [("改正区分所有法", "第1部 区分所有法(令和8年4月1日施行の改正を含む)", "根拠:e-Gov法令検索(2026-09-30取得)"),
        ("標準管理規約", "第2部 マンション標準管理規約(単棟型・令和7年10月17日改正)", "根拠:国交省公表の規約本文(コメントは不使用)"),
        ("民法", "第3部 民法(意思表示・代理・時効・債権・不法行為)", "根拠:e-Gov法令検索(2026-10-01取得)"),
        ("給排水設備告示", "第4部 給排水設備の構造方法(建設省告示第1597号)", "根拠:国交省公表の告示。試験で頻出の数値の多くは告示に無く対象外")]
rows = []; n = 0; part_range = []
for key, title, src in SETS:
    rs = list(csv.DictReader(open(f"06_練習問題/練習問題_{key}.csv", encoding="utf-8-sig")))
    first = n + 1
    for r in rs:
        n += 1
        rows.append(dict(通し番号=n, 部=title, 元の問題ID=r["問題ID"], 論点ID=r["論点ID"], 関連改正ID=r.get("関連改正ID") or r.get("関連改正ID(2026_法改正一覧)") or "",
                         問題文=r["問題文"], 肢1=r["肢1"], 肢2=r["肢2"], 肢3=r["肢3"], 肢4=r["肢4"], 正解=int(r["正解"]), 解説=r["解説(肢別)"],
                         根拠=r.get("根拠条文") or r.get("根拠"), 根拠原文=r["根拠原文(抜粋)"], 検証=r["検証"]))
    part_range.append((title, src, first, n))
assert len({r["元の問題ID"] for r in rows}) == len(rows) == n
cols = ["通し番号", "部", "元の問題ID", "論点ID", "関連改正ID", "問題文", "肢1", "肢2", "肢3", "肢4", "正解", "解説", "根拠", "根拠原文", "検証"]
with open("06_練習問題/練習問題_全集.csv", "w", encoding="utf-8-sig", newline="") as f:
    w = csv.DictWriter(f, fieldnames=cols); w.writeheader(); w.writerows(rows)
topics = Counter(r["論点ID"] for r in rows); ans = Counter(r["正解"] for r in rows)
md = [f"# マンション管理士 練習問題集(全{n}問)\n",
      "- 作成:AI(Sonnet)。**本試験の過去問ではなく、練習用の創作問題**。試験日:2026-11-29。出題基準日:令和8年4月1日施行の法令等。",
      "- 全肢について、根拠の条・項(または告示の節)と原文の一部が、一次資料の原文に含まれることをコードで検証済み。ただし言い換えの妥当性はコードでは確認できないため、人の確認を推奨。",
      "- 範囲の偏り:改正論点(区分所有法・標準管理規約)を厚くした。設備・修繕・会計・税務・適正化法などは含まない。",
      "- 詳細な根拠原文・検証は `練習問題_全集.csv` の「根拠原文」列。個別版は同フォルダの各セットを参照。\n",
      "## 構成\n", "| 部 | 問題番号 | 出典 |", "|---|---|---|"]
md += [f"| {t} | 問{a}〜問{b} | {s} |" for t, s, a, b in part_range]
md += ["", "論点別の問題数:" + "、".join(f"{k} {v}" for k, v in sorted(topics.items())), "正解位置の分布(1〜4):" + "、".join(f"{k}={ans[k]}" for k in sorted(ans)) + "\n", "## 問題編\n"]
cur = None
for r in rows:
    if r["部"] != cur: cur = r["部"]; md.append(f"### {cur}\n")
    md.append(f"**問{r['通し番号']}**({r['元の問題ID']}・{r['論点ID']})\n\n{r['問題文']}\n\n" + "\n".join(f"{j}. {r['肢'+str(j)]}" for j in range(1, 5)) + "\n")
md += ["---\n", "## 正解一覧\n", "| 問 | 正解 | 問 | 正解 | 問 | 正解 | 問 | 正解 | 問 | 正解 |", "|---|---|---|---|---|---|---|---|---|---|"]
for i in range(0, n, 5):
    cells = []
    for r in rows[i:i + 5]: cells += [str(r["通し番号"]), str(r["正解"])]
    cells += [""] * (10 - len(cells)); md.append("| " + " | ".join(cells) + " |")
md += ["", "## 解説編\n"]
cur = None
for r in rows:
    if r["部"] != cur: cur = r["部"]; md.append(f"### {cur}\n")
    md.append(f"**問{r['通し番号']} 正解:{r['正解']}**({r['元の問題ID']})\n")
    md += [f"- {p.strip()}" for p in r["解説"].split(" / ")]
    md.append(f"- 根拠:{r['根拠']}\n")
open("06_練習問題/練習問題_全集.md", "w", encoding="utf-8").write("\n".join(md))
print("問題数", n, "論点", dict(topics), "正解位置", dict(sorted(ans.items())))
