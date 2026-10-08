# オフライン画像・文書 意味検索 PWA（offline-photo-search）

卒業研究（教育学部 技術・ものづくり教育コース）の開発リポジトリです。
スマートフォンのブラウザだけで動く「完全オフライン意味検索」PWA を開発します。

- 公開URL: https://224096-cmd.github.io/offline-photo-search/
- 中核モデル: EmbeddingGemma 2（テキスト＋画像。初回のみ Hugging Face から取得し、ブラウザ内に保存）
- OCR: PaddleOCR.js（主力）／ Tesseract.js（比較用）
- 登録した画像・テキスト・ベクトルは端末の外へ一切送信しません（クラウドゼロ送信）

## 現在の状態

**v0.4** — EmbeddingGemma 2（テキスト）実機検証デモ。類似度計算のバグ修正版。

- **修正**：v0.3 では文プーリング（トークン列を1本の文ベクトルに平均する処理）の指定が漏れており、
  ベクトル次元が 17、類似度が null になっていた。`pooling: "mean", normalize: true` を指定し、
  保険として自前の平均・正規化処理と、次元・数値の妥当性チェックを追加。
- **実機での判明事項（iPhone 17e / iOS 26.6.2）**：
  - WebGPU＋q4f16 … 動作（読み込み約2秒※キャッシュ後、ウォームアップ約0.1秒、1文あたり約60〜90ms）
  - WebGPU＋q4 … 類似度計算時にメモリ不足とみられるページ再読み込みが発生
  - WASM＋q4 … モデル読み込み段階でページ再読み込みが発生
  - → 本端末での安定構成は **WebGPU＋q4f16**（この比較自体が RQ3・RQ4 の測定データ）

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
| `index.html` | アプリ本体（v0.4 は埋め込みモデルの実機検証デモ） |
| `.github/workflows/pages.yml` | GitHub Pages への自動デプロイ設定 |
| `.nojekyll` | GitHub Pages の Jekyll 処理を無効化 |
