#!/usr/bin/env python3
"""
TAC『2026年度版 マンション管理士 項目別 過去8年問題集』PDFパーサー
全6分野PDFから、問題・選択肢・解答・正誤・詳細解説・根拠条文を抽出し、
JSONL および CSV として出力する。
"""

import os
import re
import csv
import json
import glob
import fitz

# 和暦 -> 西暦
ERA_MAP = {
    "H30": 2018, "平成30": 2018,
    "R元": 2019, "R1": 2019, "令和元": 2019, "令和1": 2019,
    "R2": 2020, "令和2": 2020,
    "R3": 2021, "令和3": 2021,
    "R4": 2022, "令和4": 2022,
    "R5": 2023, "令和5": 2023,
    "R6": 2024, "令和6": 2024,
    "R7": 2025, "令和7": 2025,
}

def parse_exam_id(text):
    """年度・問番号を抽出して (exam_id, year, q_num, raw_str) を返す"""
    pat = re.compile(r"([RH]\s*\d+|R\s*元(?:年)?|平成\s*\d+年?)\s*[\-—ー–〜~]?\s*問\s*(\d+)")
    m = pat.search(text)
    if not m:
        return None, None, None, None
    raw_era = m.group(1).replace(" ", "").replace("年", "")
    q_num = int(m.group(2))
    raw_str = f"{raw_era}-問{q_num}"
    
    year = None
    for k, v in ERA_MAP.items():
        if k in raw_era:
            year = v
            break
    if not year:
        # 数字部分
        num_m = re.search(r"\d+", raw_era)
        if "H" in raw_era and num_m:
            year = 1988 + int(num_m.group(0))
        elif "R" in raw_era and num_m:
            year = 2018 + int(num_m.group(0))
        else:
            year = 2018
    
    exam_id = f"{year}-{q_num:02d}"
    return exam_id, year, q_num, raw_str

def extract_explanations(page_a):
    """解説ページ（偶数P）から4肢の解説ブロックを抽出する"""
    blocks = page_a.get_text("blocks")
    # x 座標が 50 以上のテキストブロックを y 座標順に並べる（左端のアイコン列を除く）
    content_blocks = []
    for b in blocks:
        # b = (x0, y0, x1, y1, text, block_no, block_type)
        x0, y0, x1, y1, text = b[0], b[1], b[2], b[3], b[4].strip()
        if not text:
            continue
        # ヘッダーやフッター、垂直タイトルを除外
        if y1 < 60 or y0 > 560:
            continue
        if x0 > 370: # 右端の縦書き「民法等」など
            continue
        if x1 < 50: # 左端の丸数字アイコン
            continue
        content_blocks.append((y0, text))
    
    content_blocks.sort(key=lambda x: x[0])
    
    # 正誤キーワード ("正しい" / "誤り") で肢を分割
    # 各肢の判定とテキストをまとめる
    options_expl = []
    cur_judge = ""
    cur_texts = []
    
    for y0, text in content_blocks:
        # 先頭に「正しい」「誤り」が含まれているか判定
        m = re.match(r"^(正しい|誤り)(.*)", text, re.DOTALL)
        if m:
            if cur_judge:
                options_expl.append((cur_judge, "\n".join(cur_texts).strip()))
                cur_texts = []
            cur_judge = m.group(1)
            rem = m.group(2).strip()
            if rem:
                cur_texts.append(rem)
        else:
            # 「副」「公」などのOCR誤認識がある場合
            m_sub = re.match(r"^[o0〇\s]*(副|公|誤|正)(.*)", text, re.DOTALL)
            if m_sub and len(options_expl) < 4 and not cur_texts:
                char = m_sub.group(1)
                judge = "誤り" if char in ["副", "公", "誤"] else "正しい"
                if cur_judge:
                    options_expl.append((cur_judge, "\n".join(cur_texts).strip()))
                    cur_texts = []
                cur_judge = judge
                rem = m_sub.group(2).strip()
                if rem:
                    cur_texts.append(rem)
            else:
                cur_texts.append(text)
                
    if cur_judge:
        options_expl.append((cur_judge, "\n".join(cur_texts).strip()))
        
    return options_expl

def extract_law_refs(expl_text):
    """解説文から根拠条文や判例を抽出する"""
    refs = []
    # （民法93条1 項本文）や（区分所有法17条2項）、(94条1項) など
    matches = re.findall(r"[（\(]([^）\)]*(?:法\d+条|\d+条|判例|指針|告示|規約)[^）\)]*)[）\)]", expl_text)
    for m in matches:
        cleaned = m.strip().replace(" ", "")
        if cleaned and cleaned not in refs:
            refs.append(cleaned)
    return " ; ".join(refs) if refs else ""

if __name__ == "__main__":
    print("TAC parser module loaded.")
