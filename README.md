# オフライン画像・文書 意味検索 PWA（offline-photo-search）

卒業研究（教育学部 技術・ものづくり教育コース）の開発リポジトリです。
スマートフォンのブラウザだけで動く「完全オフライン意味検索」PWA を開発します。

- 公開URL: https://224096-cmd.github.io/offline-photo-search/
- 中核モデル: EmbeddingGemma 2（テキスト＋画像。初回のみ Hugging Face から取得し、ブラウザ内に保存）
- OCR: PaddleOCR.js（主力）／ Tesseract.js（比較用）
- 登録した画像・テキスト・ベクトルは端末の外へ一切送信しません（クラウドゼロ送信）

## 現在の状態

**v0.3** — EmbeddingGemma 2（テキスト）の実機検証デモ・安定化版。

v0.2 で「② 類似度を計算」実行時にメモリ不足とみられるページ再読み込みが発生したため、次の対策を実装：

- **1件ずつ直列処理**：クエリと文書をまとめず1件ずつベクトル化し、メモリのピークを抑制
- **省メモリ量子化**：WebGPU では q4f16（約157MB）を既定に
- **ウォームアップ**：初回推論（GPU準備で負荷が大きい）を①の読み込み段階で実行
- **中断の検知と記録**：処理の直前に段階名を localStorage に記録し、ページが再読み込みされた場合は次回起動時に「どの段階で中断したか」を表示・書き出しに含める
- **実行方式（WebGPU/WASM）と量子化（q4f16/q4/q8）を画面で切替可能**（比較測定＝RQ3・RQ4用）

※この版はライブラリ（transformers.js）をCDNから、モデルをHugging Faceから取得するため、
初回はオンラインが必要です。完全オフライン化（自前配信＋Service Workerキャッシュ）は後の版で行います。

## 開発フロー

1. 受け取った zip をこのリポジトリのフォルダに展開する
2. `git add -A` → `git commit` → `git push`
3. GitHub Actions が自動で Pages へデプロイ（リポジトリの Actions タブで進行を確認）
4. スマホで公開URLを開いて動作確認

## ファイル構成

| ファイル | 役割 |
| --- | --- |
| `index.html` | アプリ本体（v0.3 は埋め込みモデルの実機検証デモ・安定化版） |
| `.github/workflows/pages.yml` | GitHub Pages への自動デプロイ設定 |
| `.nojekyll` | GitHub Pages の Jekyll 処理を無効化 |
