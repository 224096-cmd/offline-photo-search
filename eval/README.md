# 評価セット（公開データセット由来）

アプリの「④ 精度評価」で使う評価セットです。`make_eval.py`（標準ライブラリのみ・乱数シード42）で
元データから機械的に抽出しており、同じ手順で誰でも再生成できます（卒論の再現性確保のため）。

| ファイル | 元データ | ライセンス | 内容 |
| --- | --- | --- | --- |
| `eval-jsquad-50.json` | [JGLUE](https://github.com/yahoojapan/JGLUE) JSQuAD v1.3 valid | CC BY-SA 4.0 | Wikipedia段落50件＋その段落に対する実際の質問20問。質問と文書で語が重なりやすい（単語一致に有利な条件） |
| `eval-stair-50.json` | [STAIR Captions](https://github.com/STAIR-Lab-CIT/STAIR-captions) v1.2 val | CC BY 4.0 | 画像キャプション50件。同じ画像の別キャプション（文字2-gram重複が最小のもの）をクエリにした「純粋な言い換え」20問 |

- JSQuAD抽出条件：1記事につき最初の適合段落（本文120〜380字）のみ。文書は「【記事名】本文」形式
- STAIR抽出条件：キャプション3件以上・各10〜60字の画像から、最長キャプションを文書に、
  文書との文字2-gram重複が最小の別キャプションをクエリにし、重複最小の20問を採用
  （クエリと文書の重複率 中央値 0.082＝語の一致にほぼ頼れない）
- 形式：`{name, source, license, note, docs:[{id,text}], queries:[{q, gold:[id]}]}`
  （アプリは name / docs / queries のみ使用）

再生成方法（元データを取得後）:

```
python3 make_eval.py valid-v1.3.json stair_captions_v1.2_val.json .
```

本フォルダの2つのJSONは、それぞれ元データセットのライセンス（CC BY-SA 4.0 / CC BY 4.0）を引き継ぎます。
