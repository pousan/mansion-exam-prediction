#!/usr/bin/env python3
"""
TAC『2026年度版 マンション管理士 項目別 過去8年問題集』
PDFデータ化・統合データベース構築スクリプト
"""

import os
import re
import csv
import json
import fitz

PDF_DIR = "/Volumes/AdobeApps/mankan2026/mankan-pdf"
OUTPUT_JSONL = "02_マスターデータ/過去8年問題集_解説付き.jsonl"
OUTPUT_CSV = "02_マスターデータ/過去8年問題集_解説付き.csv"

ERA_MAP = {
    "平成30": 2018, "H30": 2018,
    "令和元年": 2019, "令和1": 2019, "R元": 2019, "R1": 2019,
    "令和2": 2020, "R2": 2020,
    "令和3": 2021, "R3": 2021,
    "令和4": 2022, "R4": 2022,
    "令和5": 2023, "R5": 2023,
    "令和6": 2024, "R6": 2024,
    "令和7": 2025, "R7": 2025,
}

PDF_FILES = [
    "05mankan-minpou.pdf",
    "06mankan-kubunshoyu.pdf",
    "07fudousantoukihou.pdf",
    "08shusihoukoku.pdf",
    "09tosikeikaku.pdf",
    "10kanrisi.pdf"
]

def load_existing_masters():
    """既存マスターデータをロードする"""
    questions = {}
    if os.path.exists("02_マスターデータ/問題マスター.csv"):
        with open("02_マスターデータ/問題マスター.csv", encoding="utf-8-sig") as f:
            for r in csv.DictReader(f):
                questions[r["問題ID"]] = r
                
    options = {} # q_id -> list of options
    if os.path.exists("02_マスターデータ/肢マスター.csv"):
        with open("02_マスターデータ/肢マスター.csv", encoding="utf-8-sig") as f:
            for r in csv.DictReader(f):
                qid = r["問題ID"]
                if qid not in options:
                    options[qid] = []
                options[qid].append(r)
                
    answers = {}
    if os.path.exists("02_マスターデータ/正解表.csv"):
        with open("02_マスターデータ/正解表.csv", encoding="utf-8-sig") as f:
            for r in csv.DictReader(f):
                answers[r["問題ID"]] = r["正解"]

    return questions, options, answers

def parse_mokuji():
    """目次PDFから全問のメタデータを抽出する"""
    doc = fitz.open(os.path.join(PDF_DIR, "02mankan-mokuji.pdf"))
    full_text = "\n".join([p.get_text() for p in doc])
    
    # パターン: テーマ ... ［令和X年第Y問(改題)?］ 掲載ページ
    pattern = re.compile(r"([^\n\[]+?)\s*[\.．・…\s]*［\s*(令和|平成|R|H)\s*(\d+|元)\s*年\s*第\s*(\d+)\s*問(?:\s*改題)?\s*］\s*(\d+)")
    
    items = []
    seen = set()
    for m in pattern.finditer(full_text):
        raw_theme = m.group(1).strip().replace("・", "").replace("．", "")
        # 先頭の記号を除去
        theme = re.sub(r"^[D図団日国眉田囮困座四梱固囚\d\s]+", "", raw_theme).strip()
        era = m.group(2)
        y = m.group(3)
        q = int(m.group(4))
        p = int(m.group(5))
        
        era_str = f"{era}{y}"
        year = None
        for k, v in ERA_MAP.items():
            if k in era_str:
                year = v
                break
        if not year:
            year = 2018 if "平成" in era else 2019
            
        exam_id = f"{year}-{q:02d}"
        key = (exam_id, p)
        if key not in seen:
            seen.add(key)
            items.append({
                "exam_id": exam_id,
                "year": year,
                "q_num": q,
                "theme": theme,
                "page_num": p
            })
            
    return items

def build_page_map():
    """全PDFの各ページから印刷ページ番号をマップする"""
    page_map = {} # printed_page_num -> (filename, page_idx)
    docs = {}
    for f in PDF_FILES:
        path = os.path.join(PDF_DIR, f)
        doc = fitz.open(path)
        docs[f] = doc
        for idx, page in enumerate(doc):
            lines = [l.strip() for l in page.get_text().split("\n") if l.strip()]
            for l in reversed(lines[-5:]):
                if l.isdigit() and int(l) > 0:
                    p_num = int(l)
                    if p_num not in page_map:
                        page_map[p_num] = (f, idx)
                    break
    return page_map, docs

def extract_law_refs(text):
    """解説文から根拠条文を抽出する"""
    refs = []
    matches = re.findall(r"[（\(]([^）\)]*(?:法\s*\d+条|\d+条|判例|指針|告示|規約)[^）\)]*)[）\)]", text)
    for m in matches:
        cleaned = m.strip().replace(" ", "")
        if cleaned and cleaned not in refs:
            refs.append(cleaned)
    return " ; ".join(refs) if refs else ""

def split_expl_text(text):
    """解説テキストから各肢の解説を分割する"""
    lines = [l.strip() for l in text.split("\n") if l.strip()]
    # ヘッダー/フッター除外
    clean = []
    for l in lines:
        if l.startswith("...") or l.isdigit() or l in ["民", "法", "等", "民法等", "_", "区分所有法", "適正化法"]:
            continue
        clean.append(l)
        
    # 区切り判定
    splits = []
    for idx, l in enumerate(clean):
        is_split = False
        if l in ["正しい", "誤り", "適切", "不適切"]:
            is_split = True
        elif l.startswith("正しい") or l.startswith("誤り") or l.startswith("適切") or l.startswith("不適切"):
            is_split = True
        elif ("⇒" in l or "→" in l or "吟" in l or "＊" in l) and ("「" in l or "『" in l):
            is_split = True
            
        if is_split:
            if not splits or (idx - splits[-1] >= 2):
                splits.append(idx)
                
    if len(splits) == 4:
        res = []
        for i in range(4):
            start = splits[i]
            end = splits[i+1] if i < 3 else len(clean)
            chunk = "\n".join(clean[start:end]).strip()
            res.append(chunk)
        return res
    else:
        # 4分割できなかった場合は全文を返す
        full = "\n".join(clean).strip()
        return [full, "", "", ""]

def main():
    print("1. Loading existing masters...")
    q_master, opt_master, ans_master = load_existing_masters()
    print(f"Loaded {len(q_master)} questions from master.")
    
    print("2. Parsing mokuji...")
    mokuji_items = parse_mokuji()
    print(f"Extracted {len(mokuji_items)} items from mokuji.")
    
    print("3. Building PDF page map...")
    page_map, docs = build_page_map()
    print(f"Mapped {len(page_map)} printed pages.")
    
    all_records = []
    
    for item in mokuji_items:
        exam_id = item["exam_id"]
        year = item["year"]
        q_num = item["q_num"]
        theme = item["theme"]
        p_num = item["page_num"]
        
        # 該当ページを探す
        mapping = page_map.get(p_num)
        if not mapping:
            # 近接ページを探す
            for delta in [-1, 1, -2, 2]:
                if (p_num + delta) in page_map:
                    mapping = page_map[p_num + delta]
                    break
                    
        q_text = ""
        expl_text = ""
        expl_chunks = ["", "", "", ""]
        source_file = ""
        q_page_idx = -1
        a_page_idx = -1
        
        if mapping:
            source_file, q_page_idx = mapping
            doc = docs[source_file]
            page_q = doc[q_page_idx]
            q_text = page_q.get_text().strip()
            
            # 解説ページは通常次のページ
            a_page_idx = q_page_idx + 1
            if a_page_idx < len(doc):
                page_a = doc[a_page_idx]
                expl_text = page_a.get_text().strip()
                expl_chunks = split_expl_text(expl_text)
                
        # 既存マスター情報とマージ
        master_q = q_master.get(exam_id, {})
        master_opts = opt_master.get(exam_id, [])
        correct_ans = ans_master.get(exam_id, "")
        
        category = master_q.get("分野", "")
        if not category:
            if "minpou" in source_file: category = "民法・借地借家法"
            elif "kubun" in source_file: category = "区分所有法"
            elif "fudousan" in source_file: category = "不動産登記法・標準管理規約"
            elif "shusi" in source_file: category = "会計・税務"
            elif "tosi" in source_file: category = "都市計画・建築設備・維持修繕"
            elif "kanri" in source_file: category = "適正化法"
            else: category = "その他"
            
        taxonomy_id = master_q.get("論点ID(主)", "")
        polarity = master_q.get("設問極性", "")
        
        # 4肢の構築
        options_data = []
        for i in range(1, 5):
            opt_body = ""
            judge = ""
            law_ref = ""
            
            # 既存肢マスターにあればそれを使用
            if master_opts and len(master_opts) >= i:
                opt_row = master_opts[i-1]
                opt_body = opt_row.get("肢本文", "")
                judge = opt_row.get("正誤", "")
                
            chunk = expl_chunks[i-1] if len(expl_chunks) >= i else ""
            if not judge:
                if "正しい" in chunk or "適切" in chunk: judge = "正"
                elif "誤り" in chunk or "不適切" in chunk: judge = "誤"
                
            law_ref = extract_law_refs(chunk) if chunk else ""
            
            options_data.append({
                "option_num": i,
                "option_text": opt_body,
                "judgement": judge,
                "explanation": chunk,
                "law_ref": law_ref
            })
            
        record = {
            "exam_id": exam_id,
            "year": year,
            "question_num": q_num,
            "source_file": source_file,
            "source_page_q": p_num,
            "category": category,
            "taxonomy_id": taxonomy_id,
            "theme": theme,
            "question_polarity": polarity,
            "correct_answer": correct_ans,
            "question_text": q_text,
            "options": options_data,
            "full_explanation": expl_text
        }
        all_records.append(record)
        
    print(f"4. Saving {len(all_records)} records to {OUTPUT_JSONL}...")
    with open(OUTPUT_JSONL, "w", encoding="utf-8") as f:
        for r in all_records:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
            
    print(f"5. Saving to {OUTPUT_CSV}...")
    with open(OUTPUT_CSV, "w", encoding="utf-8", newline="") as f:
        fieldnames = [
            "問題ID", "年度", "問番号", "分野", "論点ID", "テーマ", "設問極性", "正解",
            "肢1本文", "肢1正誤", "肢1解説", "肢1根拠条文",
            "肢2本文", "肢2正誤", "肢2解説", "肢2根拠条文",
            "肢3本文", "肢3正誤", "肢3解説", "肢3根拠条文",
            "肢4本文", "肢4正誤", "肢4解説", "肢4根拠条文",
            "出典ファイル", "掲載ページ"
        ]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for r in all_records:
            opts = r["options"]
            row = {
                "問題ID": r["exam_id"],
                "年度": r["year"],
                "問番号": r["question_num"],
                "分野": r["category"],
                "論点ID": r["taxonomy_id"],
                "テーマ": r["theme"],
                "設問極性": r["question_polarity"],
                "正解": r["correct_answer"],
                "出典ファイル": r["source_file"],
                "掲載ページ": r["source_page_q"]
            }
            for i in range(1, 5):
                o = opts[i-1] if len(opts) >= i else {}
                row[f"肢{i}本文"] = o.get("option_text", "")
                row[f"肢{i}正誤"] = o.get("judgement", "")
                row[f"肢{i}解説"] = o.get("explanation", "").replace("\n", " ")
                row[f"肢{i}根拠条文"] = o.get("law_ref", "")
            writer.writerow(row)
            
    print("Done! Database successfully built.")

if __name__ == "__main__":
    main()
