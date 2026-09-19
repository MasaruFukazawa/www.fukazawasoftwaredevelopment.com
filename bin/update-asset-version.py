#!/usr/bin/env python3
"""docs/index.html の CSS/JS リンクに内容ハッシュ (?v=...) を振り直す。

アセットを編集したら必ず実行すること。これを忘れると、
ブラウザが古い CSS をキャッシュから読み続けて表示が崩れる。

    python3 bin/update-asset-version.py
"""
import hashlib
import pathlib
import re
import sys

DOCS = pathlib.Path(__file__).resolve().parent.parent / "docs"
HTML = DOCS / "index.html"
PATTERN = re.compile(r'(?:href|src)="(\./assets/[^"?]+\.(?:css|js))(\?v=[0-9a-f]+)?"')


def main() -> int:
    html = HTML.read_text(encoding="utf-8")
    changed = []

    def repl(m: "re.Match[str]") -> str:
        asset = DOCS / m.group(1).lstrip("./")
        if not asset.exists():
            sys.exit(f"参照先が見つかりません: {asset}")
        digest = hashlib.md5(asset.read_bytes()).hexdigest()[:8]
        new = m.group(0).replace(m.group(0), m.group(0).split('="')[0] + f'="{m.group(1)}?v={digest}"')
        if new != m.group(0):
            changed.append(f"{m.group(1)} -> ?v={digest}")
        return new

    updated = PATTERN.sub(repl, html)
    if updated == html:
        print("変更なし（すべて最新のハッシュ）")
        return 0
    HTML.write_text(updated, encoding="utf-8")
    for line in changed:
        print(line)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
