#!/usr/bin/env python3
"""공개 전 내용 검사.

저장소에 올라갈 파일과 빌드 결과(public/)에서 아래를 찾는다.
하나라도 찾으면 종료 코드 1로 끝나 CI를 실패시킨다.

- [TODO-작성자: ...] 표시
- 비밀값 패턴 (API 키, 토큰, 개인 키, 비밀번호가 든 DB 주소)
- 비공개 저장소 주소와 로컬 주소
- 올리면 안 되는 파일 (.env, 개인 키, reference/)
- draft: true인 콘텐츠 (미승인 초안은 reference/에만 둔다)
- 사이트에 싣지 않기로 한 개인 정보 (이메일, 전화번호, 학점, 생년월일, 병역)

사용법:
    python3 scripts/check_content.py            # 저장소에 올라갈 파일 검사
    python3 scripts/check_content.py --public   # 빌드 결과까지 검사
"""

import argparse
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# 이 파일은 패턴 자체를 담고 있어 검사에서 뺀다.
SELF = Path(__file__).resolve().relative_to(ROOT).as_posix()

# TODO 표시를 허용하는 곳: 작성 규칙 문서와 새 글 틀.
TODO_ALLOWED = ("SPEC.md", "CLAUDE.md", "README.md", "archetypes/")

TEXT_SUFFIXES = {
    ".md", ".html", ".htm", ".xml", ".txt", ".toml", ".yaml", ".yml", ".json",
    ".css", ".js", ".mjs", ".py", ".svg", ".webmanifest", ".sh", ".cfg", ".ini",
}

TODO = re.compile(r"\[TODO-작성자")
DRAFT = re.compile(r"^draft\s*[:=]\s*true\b", re.I)

SECRETS = [
    ("Anthropic API 키", re.compile(r"sk-ant-[A-Za-z0-9_\-]{20,}")),
    ("OpenAI API 키", re.compile(r"\bsk-(?:proj-)?[A-Za-z0-9]{32,}")),
    ("GitHub 토큰", re.compile(r"\b(?:ghp|gho|ghu|ghs|ghr)_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{40,}")),
    ("AWS 액세스 키", re.compile(r"\b(?:AKIA|ASIA)[0-9A-Z]{16}\b")),
    ("Google API 키", re.compile(r"\bAIza[0-9A-Za-z_\-]{35}\b")),
    ("Slack 토큰", re.compile(r"\bxox[abprs]-[A-Za-z0-9\-]{10,}")),
    ("Telegram 봇 토큰", re.compile(r"\b\d{8,10}:AA[A-Za-z0-9_\-]{33}\b")),
    ("JWT", re.compile(r"\beyJ[A-Za-z0-9_\-]{10,}\.eyJ[A-Za-z0-9_\-]{10,}\.[A-Za-z0-9_\-]{10,}")),
    ("개인 키", re.compile(r"-----BEGIN (?:[A-Z]+ )?PRIVATE KEY-----")),
    ("비밀번호가 든 DB 주소", re.compile(r"\b(?:postgres(?:ql)?|mysql|mongodb(?:\+srv)?|redis)://[^\s:/@]+:[^\s@/]+@")),
    ("비밀값 대입", re.compile(r"(?i)\b(?:api[_-]?key|secret|token|password|service[_-]?role)[\"']?\s*[:=]\s*[\"'][A-Za-z0-9_\-+/=]{16,}[\"']")),
]

# 비공개 저장소 이름. 공개 승인을 받아도 저장소 주소는 링크하지 않는다.
PRIVATE_REPOS = ("hostoff", "yeojeong", "aftermark", "stock_alam", "stock-alam", "my-game")
PRIVATE_URLS = [
    ("비공개 저장소 주소", re.compile(
        r"github\.com/ch-park0422/(?:%s)\b" % "|".join(re.escape(r) for r in PRIVATE_REPOS), re.I)),
    ("로컬 주소", re.compile(r"https?://(?:localhost|127\.0\.0\.1|0\.0\.0\.0|\[::1\])(?::\d+)?", re.I)),
    ("로컬 파일 경로", re.compile(r"/Users/[A-Za-z0-9_.\-]+/")),
]

# 공개 연락처는 GitHub만 쓴다. 사이트 소스와 빌드 결과에만 적용한다(규칙 문서는 이 단어를 설명한다).
PRIVATE_INFO = [
    ("이메일 주소", re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)*\.[A-Za-z]{2,}")),
    ("전화번호", re.compile(r"(?<!\d)(?:01[016789]|0[2-6]\d?)[-. ]?\d{3,4}[-. ]?\d{4}(?!\d)")),
    ("학점", re.compile(r"학점|\b\d\.\d{1,2}\s*/\s*4\.[35]\b")),
    ("생년월일·병역", re.compile(r"생년월일|병역|군필|전역")),
]
PRIVATE_INFO_SCOPE = ("content/", "data/", "layouts/", "static/", "assets/", "public/", "hugo.toml")
# 공개해도 되는 주소: 커밋 작성자용 GitHub noreply
EMAIL_ALLOWED = re.compile(r"@users\.noreply\.github\.com$")

FORBIDDEN_FILES = [
    ("환경변수 파일", re.compile(r"(?:^|/)\.env(?:\..*)?$")),
    ("개인 키 파일", re.compile(r"(?:^|/)(?:id_rsa|id_ed25519)$|\.(?:pem|p12|key)$")),
    ("reference/ 파일", re.compile(r"^reference/")),
]


def repo_files():
    """git이 올릴 수 있는 파일: 추적 중이거나, 무시되지 않은 새 파일."""
    try:
        out = subprocess.run(
            ["git", "ls-files", "--cached", "--others", "--exclude-standard", "-z"],
            cwd=ROOT, check=True, capture_output=True,
        ).stdout.decode("utf-8")
    except (OSError, subprocess.CalledProcessError):
        sys.exit("git ls-files를 실행하지 못했습니다.")
    return [p for p in out.split("\0") if p and (ROOT / p).is_file()]


def public_files():
    public = ROOT / "public"
    if not public.is_dir():
        sys.exit("public/이 없습니다. 먼저 hugo --minify를 실행하세요.")
    return [p.relative_to(ROOT).as_posix() for p in public.rglob("*") if p.is_file()]


def scan(rel, problems):
    for label, pattern in FORBIDDEN_FILES:
        if pattern.search(rel):
            problems.append((rel, 0, label, rel))

    if rel == SELF or Path(rel).suffix.lower() not in TEXT_SUFFIXES:
        return
    try:
        text = (ROOT / rel).read_text(encoding="utf-8")
    except (UnicodeDecodeError, OSError):
        return
    problems.extend(scan_text(rel, text))


def scan_text(rel, text):
    """파일 하나의 내용을 검사해 (경로, 줄, 종류, 값) 목록을 돌려준다."""
    problems = []
    check_todo = not rel.startswith(TODO_ALLOWED)
    check_draft = rel.startswith("content/") and rel.endswith(".md")
    for lineno, line in enumerate(text.splitlines(), 1):
        found = []
        if check_todo and TODO.search(line):
            found.append(("작성자 확인 필요", TODO.search(line)))
        if check_draft and DRAFT.search(line):
            found.append(("초안 커밋 금지", DRAFT.search(line)))
        for label, pattern in SECRETS + PRIVATE_URLS:
            # 테스트 설정은 로컬 서버 주소를 쓴다. 비밀값 검사는 그대로 한다.
            if label == "로컬 주소" and rel.startswith("tests/"):
                continue
            m = pattern.search(line)
            if m:
                found.append((label, m))
        if rel.startswith(PRIVATE_INFO_SCOPE):
            for label, pattern in PRIVATE_INFO:
                for m in pattern.finditer(line):
                    if label == "이메일 주소" and EMAIL_ALLOWED.search(m.group(0)):
                        continue
                    found.append((label, m))
                    break
        for label, m in found:
            problems.append((rel, lineno, label, mask(m.group(0))))
    return problems


def mask(value):
    """찾은 값을 출력할 때 비밀값이 다시 새지 않게 가린다."""
    value = value.strip()
    if len(value) <= 12:
        return value
    return value[:8] + "…"


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--public", action="store_true", help="public/ 빌드 결과도 검사")
    args = parser.parse_args()

    files = repo_files()
    if args.public:
        files += public_files()

    problems = []
    for rel in sorted(set(files)):
        scan(rel, problems)

    if problems:
        print("내용 검사 실패: %d건" % len(problems))
        for rel, lineno, label, value in problems:
            where = "%s:%d" % (rel, lineno) if lineno else rel
            print("  %s  [%s]  %s" % (where, label, value))
        return 1

    print("내용 검사 통과: 파일 %d개" % len(set(files)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
