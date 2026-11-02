#!/usr/bin/env python3
"""빌드 결과(public/)의 내부 링크 검사.

모든 HTML의 href, src와 #앵커가 실제 파일과 id를 가리키는지 확인한다.
깨진 링크가 있으면 종료 코드 1로 끝난다.

사용법:
    python3 scripts/check_links.py [빌드 폴더]   # 기본값 public
"""

import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

SITE_HOSTS = {"ch-park0422.github.io", "chpark.dev", "www.chpark.dev"}


class Collector(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
        self.ids = set()

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if "id" in attrs:
            self.ids.add(attrs["id"])
        for name in ("href", "src"):
            value = attrs.get(name)
            # canonical, og:url처럼 자기 자신을 가리키는 절대 주소도 검사한다.
            if value is not None and not (tag == "link" and attrs.get("rel") in ("preconnect",)):
                self.links.append(value)


def parse(path, cache):
    if path not in cache:
        c = Collector()
        c.feed(path.read_text(encoding="utf-8"))
        cache[path] = c
    return cache[path]


def resolve(root, page, url):
    """링크를 빌드 폴더 안의 파일로 바꾼다. 외부 링크는 None."""
    parts = urlsplit(url)
    if parts.scheme in ("mailto", "tel", "data", "javascript"):
        return None, None
    if parts.scheme or parts.netloc:
        if parts.netloc not in SITE_HOSTS:
            return None, None
    path = unquote(parts.path)
    if not path:
        target = page
    elif path.startswith("/"):
        target = root / path.lstrip("/")
    else:
        target = (page.parent / path).resolve()
    if target.is_dir() or path.endswith("/"):
        target = target / "index.html"
    return target, parts.fragment


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else "public").resolve()
    if not root.is_dir():
        sys.exit("%s이 없습니다. 먼저 hugo --minify를 실행하세요." % root)

    cache = {}
    broken = []
    pages = sorted(root.rglob("*.html"))
    for page in pages:
        for url in parse(page, cache).links:
            target, fragment = resolve(root, page, url)
            if target is None:
                continue
            if not target.is_file():
                broken.append((page, url, "파일 없음"))
            elif fragment and target.suffix == ".html" and unquote(fragment) not in parse(target, cache).ids:
                broken.append((page, url, "앵커 없음"))

    if broken:
        print("깨진 내부 링크: %d개" % len(broken))
        for page, url, why in broken:
            print("  %s → %s (%s)" % (page.relative_to(root), url, why))
        return 1
    print("내부 링크 검사 통과: 페이지 %d개" % len(pages))
    return 0


if __name__ == "__main__":
    sys.exit(main())
