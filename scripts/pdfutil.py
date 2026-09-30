"""問題PDFのページテキスト取得。ページ番号だけを除去する。
- 2019年度: 各ページ末尾の『― N ―』
- 2020年度以降: 各ページ先頭の半角数字のみの行(全角数字の行=選択肢番号は残す)"""
import re, pymupdf
def page_text(p):
    ls=p.get_text().split("\n")
    ls=[l for l in ls if not re.fullmatch(r"\s*[―－\-]\s*\d{1,2}\s*[―－\-]\s*",l)]
    for i,l in enumerate(ls):
        if l.strip():
            if re.fullmatch(r"\s*[0-9]{1,2}\s*",l): ls.pop(i)
            break
    return "\n".join(ls)
def doc_text(path):
    d=pymupdf.open(path); return "\n".join(page_text(p) for p in d)
