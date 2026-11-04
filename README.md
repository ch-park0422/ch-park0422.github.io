# ch-park0422.github.io

박창현의 포트폴리오와 블로그입니다.

> QA Engineer & AI Builder
>
> 서비스 품질을 검증하고, AI 시대의 품질 기준을 만듭니다

- 주소: https://ch-park0422.github.io
- 사이트 생성기: [Hugo](https://gohugo.io/) 0.169.0 extended
- 배포: `main`에 push하면 GitHub Actions가 빌드해 GitHub Pages에 게시합니다.

## 로컬 실행

```bash
brew install hugo
hugo server
```

## 검사

```bash
hugo --minify
python3 scripts/check_content.py --public
```

```bash
python3 scripts/check_links.py public           # 깨진 내부 링크
python3 -m unittest discover -s tests            # 검사 스크립트 테스트
cd tests && npm install && npm test              # Playwright 화면·접근성 테스트
```

`check_content.py`는 작성자 확인 표시(`[TODO-작성자: …]`), 비밀값 패턴, 비공개 저장소 주소, 사이트에 싣지 않기로 한 개인 정보, 올리면 안 되는 파일을 찾습니다. 하나라도 있으면 CI가 실패합니다.
측정 결과는 [docs/quality.md](docs/quality.md)에 있습니다.

## 구조

| 경로 | 내용 |
|---|---|
| `content/` | 홈, 소개, 이력서, 블로그 글, 프로젝트 사례 연구 |
| `data/` | 경력과 학력, 첫 화면 문구, QA·사이드 프로젝트 역량, AI가 놓친 문제, 프롬프트 기법, 수치 |
| `layouts/`, `assets/` | 직접 구현한 템플릿, CSS, JS (외부 테마 없음) |
| `scripts/` | 내용 검사, 글 발행 |
| `.github/workflows/hugo.yml` | 빌드와 배포 |
