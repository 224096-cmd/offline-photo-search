# オフライン画像・文書 意味検索 PWA（offline-photo-search）

卒業研究（教育学部 技術・ものづくり教育コース）の開発リポジトリです。
スマートフォンのブラウザだけで動く「完全オフライン意味検索」PWA を開発します。

- 公開URL: https://224096-cmd.github.io/offline-photo-search/
- 中核モデル: EmbeddingGemma 2（テキスト＋画像。初回のみ Hugging Face から取得し、ブラウザ内に保存）
- OCR: PaddleOCR.js（主力）／ Tesseract.js（比較用）
- 登録した画像・テキスト・ベクトルは端末の外へ一切送信しません（クラウドゼロ送信）

## 現在の状態

**v0.2** — EmbeddingGemma 2（テキスト・q4量子化）の実機検証デモ。

- 「① モデルを読み込む」：約180〜210MBをダウンロードし、読み込み時間を計測（2回目以降はブラウザ内キャッシュ）
- 「② 類似度を計算」：日本語クエリと文書3件をベクトル化し、コサイン類似度で順位付け。処理時間を計測
- 「③ 計測結果を書き出す」：JSONコピー／CSVダウンロード（卒論の図表用）
- 「WASMを強制」チェックで WebGPU との速度比較が可能

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
| `index.html` | アプリ本体（v0.2 は埋め込みモデルの実機検証デモ） |
| `.github/workflows/pages.yml` | GitHub Pages への自動デプロイ設定 |
| `.nojekyll` | GitHub Pages の Jekyll 処理を無効化 |
