# -*- coding: utf-8 -*-
"""公開データセットから検索ベンチ用の小型評価セットJSONを作る（決定論的・標準ライブラリのみ）
使い方: python3 -I make_eval.py <jsquad_valid.json> <stair_val.json> <outdir>
出力: eval-jsquad-50.json / eval-stair-50.json
形式: {name, source, license, note, docs:[{id,text}], queries:[{q,gold:[id]}]}
"""
import json, random, re, sys, unicodedata

def grams2(s):
    t = re.sub(r"\s+", "", unicodedata.normalize("NFKC", s)).lower()
    return set(t[i:i+2] for i in range(len(t)-1)) if len(t) > 1 else {t}

def overlap(a, b):
    A, B = grams2(a), grams2(b)
    return len(A & B) / max(1, min(len(A), len(B)))

jsq_path, stair_path, outdir = sys.argv[1], sys.argv[2], sys.argv[3]

# ---------- JSQuAD ----------
d = json.load(open(jsq_path, encoding="utf-8"))
rng = random.Random(42)
by_title = []
for art in d["data"]:
    title = art.get("title", "")
    for p in art["paragraphs"]:
        ctx = p["context"]
        if " [SEP] " in ctx:
            t2, body = ctx.split(" [SEP] ", 1)
        else:
            t2, body = title, ctx
        body = body.strip()
        if not (120 <= len(body) <= 380):
            continue
        qs = [q["question"].strip() for q in p["qas"] if len(q["question"].strip()) >= 8]
        if not qs:
            continue
        by_title.append({"title": t2.strip(), "body": body, "qs": qs})
        break  # 1記事につき最初の適合段落のみ（同一記事内の紛らわしい段落を避ける）
rng.shuffle(by_title)
pick = by_title[:50]
docs, queries = [], []
for i, p in enumerate(pick):
    did = "j%02d" % (i + 1)
    docs.append({"id": did, "text": "【" + p["title"] + "】" + p["body"]})
qidx = list(range(50)); rng.shuffle(qidx)
for i in qidx[:20]:
    queries.append({"q": pick[i]["qs"][0], "gold": ["j%02d" % (i + 1)]})
jsq = {
    "name": "JSQuAD抜粋50（Wikipedia段落＋実際の質問）",
    "source": "JGLUE JSQuAD v1.3 valid（yahoojapan/JGLUE）から機械的に抽出",
    "license": "CC BY-SA 4.0（JGLUEに従う）",
    "note": "1記事1段落（本文120-380字）を乱数シード42で50件抽出。うち20件についてその段落に対する実際の質問1問をクエリとし、元段落を正解とした。",
    "docs": docs, "queries": queries,
}
json.dump(jsq, open(outdir + "/eval-jsquad-50.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("JSQuAD: docs", len(docs), "queries", len(queries),
      "doc字数", min(len(x["text"]) for x in docs), "-", max(len(x["text"]) for x in docs))

# ---------- STAIR Captions ----------
sv = json.load(open(stair_path, encoding="utf-8"))
caps = {}
for a in sv["annotations"]:
    caps.setdefault(a["image_id"], []).append(a["caption"].strip())
imgs = sorted(k for k, v in caps.items() if len(v) >= 3 and all(10 <= len(c) <= 60 for c in v[:5]))
rng2 = random.Random(42)
rng2.shuffle(imgs)
pick2 = imgs[:50]
docs2, queries2 = [], []
qpool = []
for i, im in enumerate(pick2):
    did = "s%02d" % (i + 1)
    cs = caps[im][:5]
    doc = max(cs, key=len)  # 最長キャプションを文書に
    rest = [c for c in cs if c != doc]
    # 文書との文字2-gram重複が最小のキャプションをクエリ候補に（言い換え性が最も高い）
    qc = min(rest, key=lambda c: overlap(c, doc))
    docs2.append({"id": did, "text": doc})
    qpool.append({"q": qc, "gold": [did], "ov": overlap(qc, doc)})
qpool.sort(key=lambda x: x["ov"])  # 重複が小さい順＝言い換えが強い順に20問
queries2 = [{"q": x["q"], "gold": x["gold"]} for x in qpool[:20]]
stair = {
    "name": "STAIR Captions抜粋50（同一画像の別キャプション＝言い換え検索）",
    "source": "STAIR Captions v1.2 val（STAIR-Lab-CIT/STAIR-captions）から機械的に抽出",
    "license": "CC BY 4.0（STAIR Captionsに従う）",
    "note": "キャプション3件以上の画像を乱数シード42で50件抽出。最長キャプションを文書、同じ画像の別キャプション（文書との文字2-gram重複が最小のもの）をクエリとし、重複最小の20問を採用。語の一致に頼らない『言い換え』検索の難易度が高い。",
    "docs": docs2, "queries": queries2,
}
json.dump(stair, open(outdir + "/eval-stair-50.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
import statistics
print("STAIR: docs", len(docs2), "queries", len(queries2),
      "クエリ-文書重複率 中央値", round(statistics.median(x["ov"] for x in qpool[:20]), 3))
