# オフライン画像・文書 意味検索 PWA（offline-photo-search）

卒業研究（教育学部 技術・ものづくり教育コース）の開発リポジトリです。
スマートフォンのブラウザだけで動く「完全オフライン意味検索」PWA を開発します。

- 公開URL: https://224096-cmd.github.io/offline-photo-search/
- 検索は4段階構成（BM25 → 静的埋め込み → e5-small／Ruri → EmbeddingGemma 2）で、端末ごとに動く段階を使う
- 写真・文字・ベクトルは端末内（IndexedDB）にのみ保存し、外部へ送信しません

## 現在の状態

**v0.8** — アプリ内カメラ（無音・ズーム対応）＋OCR読み込みの修正。

- **修正**：v0.7でOCRエンジン（Tesseract.js）のESM読み込みが失敗（createWorker未定義）。
  公式ドキュメント標準のUMD版（scriptタグ読み込み→window.Tesseract）に変更して解消
- **アプリ内カメラ**：従来の「カメラで撮る」はiPhone標準カメラを開く方式で、日本向け端末では
  シャッター音を消せない。本版はページ内カメラ（getUserMedia）に置き換え、**無音撮影**＋
  **ズームスライダー**（端末がズーム機能に対応していれば実ズーム、非対応ならデジタル切り出し）に対応。
  続けて複数枚撮影可。映像・写真は端末外へ送信しない
- ファイル・カメラの両経路を共通の処理（縮小→OCR→文字あり/なし判定→保存→任意でベクトル化）に統一
- e5ベクトルの「消失」は利用者操作（全削除→再投入）由来と判明。読み直し合成の保存強化は保険として維持
- DL型OCRの主力は次版で接続予定：PaddleOCR.js と ppu-paddle-ocr（同じPP-OCR系・MIT・統合が簡単）を
  検証し、確実に動く方を採用する

※ライブラリ・モデル・OCR日本語データは初回のみCDN／Hugging Faceから取得します。
完全オフライン化（自前配信＋Service Workerキャッシュ）は後の版で行います。

## 開発フロー

1. 受け取った zip をこのリポジトリのフォルダに展開する
2. `git add -A` → `git commit` → `git push`
3. GitHub Actions が自動で Pages へデプロイ（Actions タブで進行確認）
4. スマホ・PCで公開URLを開いて動作確認

## ファイル構成

| ファイル | 役割 |
| --- | --- |
| `index.html` | アプリ本体（v0.8 はアプリ内カメラ＋OCR＋検索） |
| `.github/workflows/pages.yml` | GitHub Pages への自動デプロイ設定 |
| `.nojekyll` | GitHub Pages の Jekyll 処理を無効化 |
