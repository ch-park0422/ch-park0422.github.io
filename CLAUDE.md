# CLAUDE.md

박창현의 포트폴리오와 블로그. Hugo로 만들고 GitHub Pages에 배포한다.
전체 명세는 `SPEC.md`, 내용과 디자인의 기준은 `reference/build-log-career.html`이다.
사이트의 중심은 10년 QA 경력이고, GitHub 프로젝트 8개는 개인 사이드 프로젝트로 표기해 경력보다 앞세우지 않는다.

## 결정 사항

G0 (2026-11-02)

- 공개 범위: 사이드 프로젝트 8개 전부. 비공개 저장소 프로젝트는 기준 페이지에 적힌 수준(설계 원칙, 구조, 버그 사례, 수치)까지만 쓴다. 코드, 내부 문서, 환경변수 값은 옮기지 않는다.
- 이름과 연락처: 박창현, GitHub `https://github.com/ch-park0422`만. 프로필 사진은 `static/images/profile.jpg`.
- 이력서: `/resume/` 웹 페이지만. 파일은 공개하지 않는다.

QA 개편 (2026-11-04)

- 직함은 QA Engineer이고 QA PM 역량을 함께 보여준다. 대제목은 `QA Engineer & AI Builder`, 부제는 "서비스 품질을 검증하고, AI 시대의 품질 기준을 만듭니다".
- QA 경력은 10년으로 쓴다. 경력은 KT, 위메이드, 스트리미, 엔글 4곳이며 잡위드는 넣지 않는다. 석사는 졸업으로 표기한다.
- 회사와 프로젝트명은 공개한다.
- 전화번호, 이메일, 주소, 생년월일, 학점, 병역은 넣지 않는다. `check_content.py`가 사이트 소스와 빌드 결과에서 검사한다.
- 경력, 학력, 자격은 `data/career.yaml`, 첫 화면과 소개 문구는 `data/hero.yaml`에서 관리한다.
- 공개 주소(프로젝트 상세, 글)는 바꾸지 않는다. 바꿔야 하면 먼저 묻는다.

## 명령

```bash
hugo server                              # 로컬 미리보기
hugo --minify                            # 빌드
python3 scripts/check_content.py         # 저장소 내용 검사
python3 scripts/check_content.py --public  # 빌드 결과까지 검사
python3 scripts/check_links.py public      # 깨진 내부 링크
python3 -m unittest discover -s tests      # 검사 스크립트 테스트
cd tests && npm test                       # Playwright 화면·접근성 테스트 (1280, 768, 360px)
```

## 규칙

- 이 저장소는 공개된다. 커밋한 것은 모두 보인다고 가정한다.
- 사용자가 말하지 않은 경력, 성과, 수치, 동기, 회고를 지어내지 않는다. 수치와 날짜는 `reference/build-log-career.html`에서만 옮긴다.
- 근거가 없는 곳은 `[TODO-작성자: 질문]`으로 남긴다. 이 표시가 있으면 내용 검사가 실패한다.
- 모든 수치에는 측정일을 붙인다 (`data/figures.yaml`, 프로젝트 `metrics[].measuredAt`).
- 초안을 `draft: true`로 커밋하지 않는다. 승인 전 초안은 `reference/` 아래에만 둔다.
- 비밀값, 비공개 저장소 주소, 로컬 경로를 커밋하지 않는다.
- 외부 테마, 인증, 서버, DB, CMS를 넣지 않는다. 분석 도구와 댓글은 승인 없이 넣지 않는다.
- `main`에 직접 push하지 않는다. 브랜치에서 작업해 PR로 병합하고, 병합은 승인을 받은 뒤에 한다.
- `git push --force`, 저장소 설정 변경, DNS 변경은 승인 없이 하지 않는다.
- 사람이 해야 할 일(도메인 결제, 계정 로그인, DNS 변경, 캡처)은 `🙋`로 표시하고 대신 하지 않는다.
- 승인 게이트에서는 멈추고 A/B/C 선택지로 묻는다.

## 디자인

- 다크 단일 테마의 리퀴드 글래스 UI. 천천히 움직이는 색 배경 위에 `backdrop-filter` 반투명 패널과 밝은 가장자리를 올린다.
- `backdrop-filter` 미지원 브라우저에서는 불투명 패널(`@supports not`)로 대체하고 글자 대비를 유지한다.
- 엇갈린 대제목, 얇은 원형 선, 둥근 벤토 타일, 알약형 태그, `... /Projects ...` 형식의 섹션 표시를 쓴다.
- 영문 제목, 숫자, 코드는 Fira Code, 한글 제목과 본문은 IBM Plex Sans KR.
- 스타일은 `assets/css/main.css`의 CSS 변수와 일반 CSS. 스크립트는 필요한 곳에만 작은 바닐라 JS(`assets/js/main.js`).
- 움직임은 배경 이동, 첫 화면 등장, 스크롤 등장, 카드 호버만 쓴다. 등장 효과는 위치만 움직이고 투명도는 바꾸지 않는다(첫 표시 지연과 글자 대비 저하를 막기 위해).
- 본문 너비 약 65자, 모바일 최소 폭 360px, 키보드 포커스 표시, `prefers-reduced-motion` 준수.
- 가짜 로고, 임의의 숙련도 퍼센트, 근거 없는 수치는 쓰지 않는다.
