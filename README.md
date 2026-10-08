# オフライン画像・文書 意味検索 PWA（offline-photo-search）

卒業研究（教育学部 技術・ものづくり教育コース）の開発リポジトリです。
スマートフォンのブラウザだけで動く「完全オフライン意味検索」PWA を開発します。

- 公開URL: https://224096-cmd.github.io/offline-photo-search/
- 主構成モデル: EmbeddingGemma 2（初回のみ Hugging Face から取得し、ブラウザ内に保存）
- 軽量フォールバック: multilingual-e5-small（RQ3 の軽量構成を兼ねる）
- OCR: PaddleOCR.js（主力）／ Tesseract.js（比較用）
- 登録した画像・テキスト・ベクトルは端末の外へ一切送信しません（クラウドゼロ送信）

## 現在の状態

**v0.5** — テキスト埋め込みの実機検証デモ（モデル切替つき）。

- モデルを2種から選択可能：
  - **EmbeddingGemma 2**（主構成・270M。WebGPU時 q4f16=157MB）
  - **multilingual-e5-small**（軽量・118Mパラメータ。WebGPU時 q4f16=205MB／WASM時 q8=118MB。クエリ接頭辞は `query:`／`passage:` に自動切替）
- 実機での判明事項（iPhone 17e / iOS 26.6.2・EmbeddingGemma 2）：
  - WebGPU＋q4f16 … v0.3 で1回完走（1文あたり約60〜90ms）したが、以後はメモリ不足とみられるページ再読み込みが再発。**動作が成功と失敗の境界線上にある**
  - WebGPU＋q4、WASM＋q4 … 読み込み／推論段階で再読み込み発生
  - → 本端末の安定運用には軽量モデルの併用が必要（この比較自体が RQ3・RQ4 の測定データ）
- 中断（ページ再読み込み）の段階を localStorage に自動記録し、再訪時に表示＋書き出しに含める

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
| `index.html` | アプリ本体（v0.5 は埋め込みモデルの実機検証デモ・2モデル切替） |
| `.github/workflows/pages.yml` | GitHub Pages への自動デプロイ設定 |
| `.nojekyll` | GitHub Pages の Jekyll 処理を無効化 |
