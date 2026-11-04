# chpark.dev GitHub Pages 블로그 구축 명세

## 사용법

1. 터미널에서 기존 저장소를 내려받습니다.

```bash
git clone https://github.com/ch-park0422/ch-park0422.github.io.git
cd ch-park0422.github.io
```

2. 이 파일을 저장소 안의 `SPEC.md`로 저장합니다.
3. 함께 받은 파일을 아래 위치에 저장합니다. `reference/`는 저장소에 올리지 않습니다.

| 파일 | 저장 위치 |
|---|---|
| `build-log-career.html` | `reference/build-log-career.html` |
| `profile-dark.jpg` | `reference/profile-dark.jpg` |

4. 그 폴더에서 Claude Code를 열고 아래 문장을 입력합니다.

```text
SPEC.md와 reference/build-log-career.html을 끝까지 읽어줘.
아직 코드는 쓰지 말고 §1의 G0 질문부터 한 번에 물어봐줘.
답을 받으면 Phase 0부터 진행하고, 각 게이트에서 멈춰줘.
```

---

## 0. 만들 것

`reference/build-log-career.html`의 포트폴리오를 GitHub Pages 블로그로 옮긴다.

- 저장소: `ch-park0422/ch-park0422.github.io`
- 1차 주소: `https://ch-park0422.github.io`
- 최종 주소: `https://chpark.dev`
- 정적 사이트 생성기: Hugo
- 배포: `main` 브랜치에 push하면 GitHub Actions가 빌드해 GitHub Pages에 게시

첫 방문자는 채용 담당자와 현업 개발자다.
방문자가 3분 안에 "QA 경력과 역량이 어떠하고, AI 서비스의 품질을 어떻게 다루는가"를 판단할 수 있어야 한다.
이 사이트의 중심은 10년 QA 경력이다. GitHub 프로젝트는 개인 사이드 프로젝트로 표기하고 경력보다 앞세우지 않는다. 커밋 달력은 넣지 않는다.

사이트의 대표 제목은 다음과 같다.

> QA Engineer & AI Builder
>
> 서비스 품질을 검증하고, AI 시대의 품질 기준을 만듭니다

`reference/build-log-career.html`은 내용과 디자인의 구현 기준이다. 프로젝트 사실, 날짜, 수치는 이 파일에서 옮기고, 경력과 학력은 `data/career.yaml`로 관리한다.
전화번호, 이메일, 주소는 G0 승인 없이 게시하지 않는다.

---

## 1. 작업 규칙

### 승인 게이트

아래 시점에는 멈추고 승인을 받는다. 질문은 A/B/C 선택지로 하고, 추천안을 표시한다.

| 게이트 | 시점 | 사람이 확인할 내용 |
|---|---|---|
| G0 | 시작 전 | 공개 프로젝트, 이름 표기, 공개 연락처, 이력서 공개 범위 |
| G1 | Phase 1 뒤 | 로컬 홈 화면과 기준 페이지의 일치 여부 |
| G2 | Phase 3 뒤 | 공개할 글과 사례 연구 초안 |
| G3 | Phase 5 뒤 | 첫 공개 배포 |
| G4 | Phase 6 뒤 | chpark.dev 연결 |

확정된 사항: 직함 표기는 QA Engineer이고 PM 역량을 함께 보여준다. 회사와 프로젝트명은 공개한다. 연락 수단은 GitHub만 쓴다. 석사는 졸업했다.

G0에서 물을 질문:

1. 8개 프로젝트 중 공개할 범위는 어디까지인가? 비공개 저장소 프로젝트의 구조와 버그 사례까지 공개해도 되는가?
2. 공개할 이름, 연락처, 프로필 사진은 무엇인가?
3. 이력서는 웹 페이지만 둘 것인가, 파일도 공개할 것인가?

### 공개 저장소 주의

- 이 저장소의 커밋은 모두 공개된다고 가정한다. 게시되지 않은 초안이라도 커밋하면 볼 수 있다.
- `.gitignore`에 `reference/`, `.env*`, `public/`, `resources/`, `.hugo_build.lock`을 넣는다.
- G0에서 공개 승인되지 않은 프로젝트 내용은 커밋하지 않는다.
- 첫 커밋 전에 비밀값과 비공개 내용을 검사한다.

### 금지 사항

- 사용자가 말하지 않은 경력, 성과, 수치, 동기, 회고를 지어내지 않는다.
- 확인이 필요한 곳은 `[TODO-작성자: 질문]`으로 남기고, 이 표시가 있으면 공개 빌드를 실패시킨다.
- 비공개 저장소의 코드, 내부 문서, 환경변수 값을 옮기지 않는다.
- 비밀값을 커밋하지 않는다.
- 인증, 서버, DB, CMS를 추가하지 않는다.
- 분석 도구와 댓글은 승인 없이 넣지 않는다.
- `git push --force`, 저장소 설정 변경, DNS 변경은 승인 없이 하지 않는다.
- 사람이 해야 할 일은 `🙋`로 표시하고 대신 처리하지 않는다. 도메인 결제, 계정 로그인, DNS 변경이 해당한다.

---

## 2. 기술 기준

| 영역 | 선택 |
|---|---|
| 사이트 생성 | Hugo extended 최신 안정 버전 |
| 테마 | 외부 테마 없이 `layouts/`와 `assets/`에 직접 구현 |
| 콘텐츠 | Markdown, `data/`의 YAML |
| 스타일 | CSS 변수와 일반 CSS |
| 스크립트 | 필요한 곳에만 작은 바닐라 JS |
| 검증 | Python 표준 라이브러리 스크립트, Playwright |
| 배포 | GitHub Actions, GitHub Pages |

시작 전에 Hugo와 GitHub Pages 공식 문서로 현재 설치 방법과 Actions 배포 방식을 확인한다.
워크플로에서 Hugo 버전을 정확히 고정한다. `latest`는 쓰지 않는다.
외부 테마를 설치하지 않는다. 이 사이트의 디자인은 기준 페이지를 직접 구현한다.

### 폴더 구조

```text
.github/workflows/hugo.yml
archetypes/
assets/css/main.css
assets/js/main.js
content/
  _index.md
  about.md
  resume.md
  blog/
  projects/
data/
  skills.yaml
  catches.yaml
  prompts.yaml
  figures.yaml
layouts/
  _default/
  partials/
  shortcodes/
  index.html
  404.html
scripts/
  check_content.py
  publish.py
static/images/
tests/
hugo.toml
CLAUDE.md
README.md
```

`hugo.toml`의 `baseURL`은 Phase 5까지 `https://ch-park0422.github.io/`로 두고, Phase 6에서 `https://chpark.dev/`로 바꾼다.

---

## 3. 사이트 구조

| 경로 | 내용 |
|---|---|
| `/` | 히어로, 경력과 학력, QA 핵심 역량, 사이드 프로젝트, 소개, 기술 목록, 연락처 순서 |
| `/projects/` | 프로젝트 목록과 기술 필터 |
| `/projects/[slug]/` | 프로젝트 사례 연구 |
| `/blog/` | 글 목록, 태그 |
| `/blog/[slug]/` | 글 상세, 읽는 시간, 이전·다음 글 |
| `/about/` | 경력, 기술, 일하는 방식, 교육 |
| `/resume/` | 웹 이력서. 파일 공개는 G0 결정을 따른다 |
| `/404.html` | 주요 페이지로 가는 안내 |

자동 생성 파일은 `/index.xml`, `/sitemap.xml`, `/robots.txt`다.
공유 이미지는 프로필 사진을 쓴 기본 이미지 1개로 시작한다.

### 데이터 이관

- 핵심 역량 6개는 `data/skills.yaml`
- AI가 놓친 문제 9개는 `data/catches.yaml`
- 프롬프트 기법 9개는 `data/prompts.yaml`
- 수치와 측정일은 `data/figures.yaml`
- 프로젝트 글은 `content/projects/*.md`

### 프로젝트 front matter

```yaml
---
title: 사회자 퇴근
summary: 진행자 역할을 앱이 맡는 파티게임 앱
date: 2026-10-28
role: 기획, 설계, 구현 검토
status: 개발 중 # 운영 중 | 개발 중 | 중단 | 실험
stack: [Expo, React Native, TypeScript, Supabase]
repo: ""
demo: ""
featured: true
metrics:
  - label: 통과한 테스트
    value: "395"
    measuredAt: 2026-11-02
---
```

모든 수치에는 측정일을 넣는다.
공개 저장소이므로 초안을 `draft: true`로 커밋하지 않는다. 미승인 초안은 커밋하지 않고 `reference/` 아래에만 둔다.

### 사례 연구 구조

모든 프로젝트 글은 아래 순서를 따른다. 근거가 없는 항목은 `[TODO-작성자: 질문]`으로 남긴다.

1. 문제: 왜 만들었고 누구를 위한 것인가
2. 내 역할: 내가 판단한 것과 Claude Code에 맡긴 것
3. 설계 결정: 대안과 선택 이유
4. 가장 어려웠던 문제: 증상, 원인, 해결, 검증
5. 품질 근거: 테스트, CI, 배포, 측정 결과
6. 회고: 다시 한다면 바꿀 점
7. 링크: 저장소, 데모, 영상

---

## 4. 디자인 기준

- 구현 기준은 `reference/build-log-career.html`이다. 시각 방향은 https://www.behance.net/gallery/199132655/Portfolio-Full-stack-Developer 를 참고하되 그 작품의 이미지와 문구를 복제하지 않는다.
- 다크 단일 테마의 리퀴드 글래스 UI다. 고정된 색상 배경 위에 `backdrop-filter`를 쓴 반투명 패널과 밝은 가장자리를 올린다.
- `backdrop-filter` 미지원 브라우저에서는 불투명 패널로 대체하고, 글자 대비를 유지한다.
- 엇갈린 대제목, 얇은 원형 선, 둥근 벤토 타일, 알약형 태그, `... /Projects ...` 형식의 섹션 표시를 쓴다.
- 영문 제목, 숫자, 코드는 Fira Code, 한글 제목과 본문은 IBM Plex Sans KR로 통일한다.
- 프로필 사진은 `reference/profile-dark.jpg`를 `static/images/profile.jpg`로 복사해 쓴다.
- 가짜 로고, 임의의 숙련도 퍼센트, 근거 없는 수치는 쓰지 않는다.
- 본문 너비는 약 65자, 모바일 최소 폭은 360px로 한다.
- 키보드 포커스를 보이게 하고 `prefers-reduced-motion`을 지킨다.
- 애니메이션은 배경의 느린 이동, 첫 화면 등장, 스크롤 시 가벼운 등장, 카드 호버만 쓴다. 내용은 애니메이션 없이도 읽을 수 있어야 한다.

기준 페이지의 base64 이미지는 Hugo 사이트로 옮길 때 일반 이미지 파일로 바꾼다.
비공개 프로젝트 캡처는 민감한 값이 없는 것만 쓴다. 캡처는 `🙋`로 요청한다.

---

## 5. Phase

### Phase 0: 저장소와 뼈대

- 기존 저장소가 비어 있는지 확인한다. 내용이 있으면 멈추고 보고한다.
- Hugo 설치 확인과 사이트 초기화
- `.gitignore`, `CLAUDE.md`, `README.md` 작성
- `.github/workflows/hugo.yml` 작성
- `scripts/check_content.py` 작성

완료 기준: `hugo --minify`와 내용 검사가 로컬에서 통과한다. 아직 push하지 않는다.

### Phase 1: 레이아웃과 홈

- 기준 페이지의 CSS를 `assets/css/main.css`로 옮긴다.
- 헤더, 푸터, 홈 섹션을 partial로 분리한다.
- 해시 라우팅은 제거하고 프로젝트 상세를 실제 URL로 만든다.
- `hugo server`로 띄운 데스크톱과 모바일 화면 캡처를 제공한다.

완료 기준: 기준 페이지와 주요 배치가 일치하고 가로 스크롤이 없다. **G1에서 멈춘다.**

### Phase 2: 콘텐츠 모델

- `data/` 파일과 템플릿 연결
- 프로젝트, 블로그 목록과 상세
- 태그와 프로젝트 기술 필터
- `[TODO-작성자]`, 비공개 URL, 비밀값 패턴을 찾는 검사

완료 기준: 내용 검사가 문제를 찾으면 CI가 실패한다.

### Phase 3: 콘텐츠 이관

- G0에서 승인된 프로젝트만 §3 구조로 이관
- 첫 글 작성: "AI가 놓친 문제를 어떻게 찾고 규칙으로 남겼나"
- `/about/`, `/resume/` 초안 작성
- 추측한 내용이 없는지 기준 페이지와 대조

완료 기준: 수치와 날짜가 원본과 일치한다. **G2에서 멈춘다.**

### Phase 4: 검색과 공유

- 페이지별 title, description, canonical
- Open Graph 태그와 공유 이미지
- RSS, sitemap, robots
- 구조화 데이터(Person, BlogPosting)

완료 기준: 공유 미리보기 태그와 RSS가 정상 생성된다.

### Phase 5: 품질 검증과 첫 배포

- Playwright: 홈, 프로젝트 상세, 글 상세, 404
- 깨진 링크 검사와 접근성 검사
- 모바일 Lighthouse 측정

완료 기준:

- Performance 90 이상, Accessibility·Best Practices·SEO 95 이상
- 깨진 내부 링크 0개
- 360px 폭에서 가로 스크롤 없음
- 저장소와 빌드 결과에서 비밀값 미검출

측정 결과를 `docs/quality.md`에 남긴다. **G3에서 멈춘다.**

승인 후 진행:

- 🙋 GitHub 저장소 **Settings → Pages → Source**를 **GitHub Actions**로 설정
- 커밋 후 `main`에 push
- Actions 성공을 확인하고 `https://ch-park0422.github.io`를 점검

### Phase 6: chpark.dev 연결

**G4 승인 뒤 진행한다.** 도메인을 구매할 수 없으면 대체 이름을 3개 제안하고 멈춘다.

1. 🙋 `chpark.dev` 구매
2. 🙋 GitHub 프로필 **Settings → Pages**에서 도메인을 추가하고 안내된 TXT 레코드로 검증
3. 🙋 DNS에 아래 레코드 추가

| 종류 | 이름 | 값 |
|---|---|---|
| A | `@` | `185.199.108.153` |
| A | `@` | `185.199.109.153` |
| A | `@` | `185.199.110.153` |
| A | `@` | `185.199.111.153` |
| AAAA | `@` | `2606:50c0:8000::153` |
| AAAA | `@` | `2606:50c0:8001::153` |
| AAAA | `@` | `2606:50c0:8002::153` |
| AAAA | `@` | `2606:50c0:8003::153` |
| CNAME | `www` | `ch-park0422.github.io` |

4. 🙋 저장소 **Settings → Pages → Custom domain**에 `chpark.dev` 입력
5. 🙋 인증서 발급 뒤 **Enforce HTTPS** 활성화. 최대 24시간이 걸릴 수 있다.
6. `hugo.toml`의 `baseURL`을 `https://chpark.dev/`로 바꾸고 배포
7. 주요 페이지, RSS, sitemap, `www` 이동, HTTPS를 확인

GitHub Actions 배포에서는 `CNAME` 파일이 필요하지 않다. 만들지 않는다.
`.dev`는 HTTPS 전용이므로 인증서가 준비되기 전에는 접속이 실패할 수 있다.

### Phase 7: 글 발행 자동화

`scripts/publish.py`를 만든다.

```bash
python scripts/publish.py "post: 글 제목"
```

- 변경 파일을 보여주고 `content/`, `data/`, `static/images/` 외 변경이 있으면 멈춘다.
- `hugo --minify`와 `scripts/check_content.py`를 실행한다.
- 통과하면 대상 파일만 add, commit, push한다.
- 강제 push는 쓰지 않고, 원격이 앞서 있으면 멈춘다.
- 토큰을 코드에 넣지 않고 기존 Git 인증을 쓴다.

자동 실행 일정은 만들지 않는다. 사람이 글을 확인한 뒤 실행한다.

---

## 6. 후속 작업: 공개 저장소 정리

사이트 배포 뒤 별도 작업으로 진행한다. 코드는 바꾸지 않고, 저장소별로 PR을 만든다.

대상은 `stock-er`, `TrendSpotted`, `basketball-team`, `my-harness-app`이다.

```text
이 저장소의 README를 채용 담당자가 읽을 수 있게 다시 써줘.
코드와 커밋 기록에서 확인한 사실만 쓰고, 모르는 내용은 질문으로 남겨줘.
구성: 프로젝트 소개, 화면 캡처 자리, 주요 기능, 기술 스택, 구조, 실행 방법, 환경변수 이름, 테스트 방법, 배운 점.
비밀값은 넣지 말고, 시작 전에 커밋 기록의 비밀값 노출 여부도 점검해줘.
```

## 7. 완료 보고

작업을 마치면 다음을 보고한다.

- 배포 URL과 저장소
- 품질 측정 결과
- 남은 `🙋` 작업
- 공개하지 않은 프로젝트 목록
- 다음에 쓰면 좋은 글 3개
