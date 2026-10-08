# オフライン画像・文書 意味検索 PWA（offline-photo-search）

卒業研究（教育学部 技術・ものづくり教育コース）の開発リポジトリです。
スマートフォンのブラウザだけで動く「完全オフライン意味検索」PWA を開発します。

- 公開URL: https://224096-cmd.github.io/offline-photo-search/
- 検索は4段階構成（BM25 → 静的埋め込み → e5-small／Ruri → EmbeddingGemma 2）で、端末ごとに動く段階を使う
- 登録した文書・ベクトルは端末内（IndexedDB）にのみ保存し、外部へ送信しません

## 現在の状態

**v0.6** — 検索MVP。「文書の登録 → 端末内保存 → 検索」が一通り動きます。

- **① 登録**：本文を追加（サンプル8件の一括投入あり）。IndexedDBに永続保存
- **② 方式・モデル**：
  - 段階0：BM25（文字2-gram方式のキーワード検索。モデル不要・即動作）
  - 段階2：multilingual-e5-small（スマホ標準。iPhone実測で安定）
  - 段階2候補：Ruri v3-30m（日本語特化・約1/4規模。検証中）
  - 段階3：EmbeddingGemma 2（PC向け。iPhoneでは不安定のため測定用）
  - 実行方式は自動（iPhone→WASM／PC等→WebGPU）。ベクトル化は1件ずつ処理し**1件ごとに保存**（中断しても続きから再開）
- **③ 検索**：日本語クエリで上位10件を表示（スコア・所要時間つき）
- **④ 書き出し**：JSONコピー／CSVダウンロード

※ライブラリ（transformers.js）はCDN、モデルはHugging Faceから初回のみ取得します。
完全オフライン化（自前配信＋Service Workerキャッシュ）は後の版で行います。

## 開発フロー

1. 受け取った zip をこのリポジトリのフォルダに展開する
2. `git add -A` → `git commit` → `git push`
3. GitHub Actions が自動で Pages へデプロイ（Actions タブで進行確認）
4. スマホ・PCで公開URLを開いて動作確認

## ファイル構成

| ファイル | 役割 |
| --- | --- |
| `index.html` | アプリ本体（v0.6 は検索MVP） |
| `.github/workflows/pages.yml` | GitHub Pages への自動デプロイ設定 |
| `.nojekyll` | GitHub Pages の Jekyll 処理を無効化 |
