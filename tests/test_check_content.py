"""scripts/check_content.py가 공개하면 안 되는 내용을 잡는지 확인한다.

    python3 -m unittest discover -s tests
"""

import importlib.util
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
spec = importlib.util.spec_from_file_location("check_content", ROOT / "scripts" / "check_content.py")
check = importlib.util.module_from_spec(spec)
spec.loader.exec_module(check)


# 이 파일이 내용 검사에 걸리지 않게 표본 값을 조각으로 나눠 둔다.
TODO = "[TODO-" + "작성자: 질문]"
PRIVATE_REPO = "https://github.com/ch-park0422/" + "hostoff"
LOCAL_URL = "http://local" + "host:3000/x"
LOCAL_PATH = "/Us" + "ers/someone/project"
DB_URL = "postgres://user:" + "pass@db.example.com/x"
PRIVATE_KEY = "-----BEGIN PRIVATE" + " KEY-----"


def labels(rel, text):
    return [p[2] for p in check.scan_text(rel, text)]


class CheckContentTest(unittest.TestCase):
    def test_todo_marker_fails_in_content(self):
        self.assertEqual(labels("content/blog/a.md", TODO), ["작성자 확인 필요"])

    def test_todo_marker_allowed_in_archetypes_and_docs(self):
        self.assertEqual(labels("archetypes/projects.md", TODO), [])
        self.assertEqual(labels("CLAUDE.md", TODO), [])

    def test_draft_fails(self):
        self.assertEqual(labels("content/blog/a.md", "---\ndraft: true\n---"), ["초안 커밋 금지"])
        self.assertEqual(labels("content/blog/a.md", "draft: false"), [])

    def test_private_repo_url_fails(self):
        self.assertEqual(labels("content/projects/a.md", PRIVATE_REPO), ["비공개 저장소 주소"])
        self.assertEqual(labels("content/projects/a.md", "https://github.com/ch-park0422/stock-er"), [])

    def test_local_address_and_path_fail(self):
        self.assertEqual(labels("content/a.md", LOCAL_URL), ["로컬 주소"])
        self.assertEqual(labels("content/a.md", LOCAL_PATH), ["로컬 파일 경로"])
        self.assertEqual(labels("tests/playwright.config.js", LOCAL_URL), [])

    def test_secrets_fail(self):
        samples = {
            "sk-ant-api03-" + "A" * 30: "Anthropic API 키",
            "ghp_" + "a" * 36: "GitHub 토큰",
            "AKIA" + "B" * 16: "AWS 액세스 키",
            DB_URL: "비밀번호가 든 DB 주소",
            PRIVATE_KEY: "개인 키",
        }
        for value, label in samples.items():
            with self.subTest(label=label):
                self.assertIn(label, labels("data/x.yaml", value))

    def test_found_value_is_masked(self):
        value = check.scan_text("data/x.yaml", "sk-ant-api03-" + "A" * 30)[0][3]
        self.assertEqual(value, "sk-ant-a…")

    def test_forbidden_files(self):
        for rel in (".env.local", "reference/build-log.html", "keys/id_rsa"):
            with self.subTest(rel=rel):
                problems = []
                check.scan(rel, problems)
                self.assertTrue(problems)

    def test_clean_text_passes(self):
        self.assertEqual(labels("content/blog/a.md", "Supabase RLS로 본인 정보만 읽게 했습니다."), [])


if __name__ == "__main__":
    unittest.main()
