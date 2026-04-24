# TOH Roles Guide

Among Us本家MOD **TownOfHost** (tukasa0001/TownOfHost) 全役職の日本語早見表。

## 公開サイト

GitHub Pagesで閲覧できます（有効化後に反映）:
https://ryuto-alt.github.io/toh-roles-guide/

## 構成

- `index.html` — 単一HTML。Tailwind CDNでスタイリング、役職データを内蔵
- `images/` — 陣営ヘッダー画像（OpenAI `gpt-image-1` 生成）
- `scripts/gen_image.py` — 画像再生成用スクリプト（Python stdlibのみ）

## 再生成

```bash
py scripts/gen_image.py images/impostor.png "<prompt>" 1024x1024 medium
```

`OPENAI_API_KEY` は Windows User 環境変数から自動読み込みされます。

## 出典

- [tukasa0001/TownOfHost](https://github.com/tukasa0001/TownOfHost) v5.1.14 README
- [Among Us Wiki (Fandom)](https://among-us.fandom.com/wiki/Mod:Town_Of_Host)
