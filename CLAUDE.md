# CLAUDE.md

박창현의 포트폴리오와 블로그. Hugo로 만들고 GitHub Pages에 배포한다.
전체 명세는 `SPEC.md`, 내용과 디자인의 기준은 `reference/build-log.html`이다.

## G0 결정 (2026-11-02)

- 공개 범위: 8개 프로젝트 전부. 비공개 저장소 프로젝트는 `reference/build-log.html`에 적힌 수준(설계 원칙, 구조, 버그 사례, 수치)까지만 쓴다. 코드, 내부 문서, 환경변수 값은 옮기지 않는다.
- 이름과 연락처: 박창현, GitHub `https://github.com/ch-park0422`만. 프로필 사진은 `static/images/profile.jpg`.
- 이력서: `/resume/` 웹 페이지만. 파일은 공개하지 않는다.

## 명령

```bash
hugo server                              # 로컬 미리보기
hugo --minify                            # 빌드
python3 scripts/check_content.py         # 저장소 내용 검사
python3 scripts/check_content.py --public  # 빌드 결과까지 검사
python3 scripts/check_links.py public      # 깨진 내부 링크
cd tests && npm test                       # Playwright 화면·접근성 테스트
```

## 규칙

- 이 저장소는 공개된다. 커밋한 것은 모두 보인다고 가정한다.
- 사용자가 말하지 않은 경력, 성과, 수치, 동기, 회고를 지어내지 않는다. 수치와 날짜는 `reference/build-log.html`에서만 옮긴다.
- 근거가 없는 곳은 `[TODO-작성자: 질문]`으로 남긴다. 이 표시가 있으면 내용 검사가 실패한다.
- 모든 수치에는 측정일을 붙인다 (`data/figures.yaml`, 프로젝트 `metrics[].measuredAt`).
- 초안을 `draft: true`로 커밋하지 않는다. 승인 전 초안은 `reference/` 아래에만 둔다.
- 비밀값, 비공개 저장소 주소, 로컬 경로를 커밋하지 않는다.
- 외부 테마, 인증, 서버, DB, CMS를 넣지 않는다. 분석 도구와 댓글은 승인 없이 넣지 않는다.
- `git push --force`, 저장소 설정 변경, DNS 변경은 승인 없이 하지 않는다.
- 사람이 해야 할 일(도메인 결제, 계정 로그인, DNS 변경, 캡처)은 `🙋`로 표시하고 대신 하지 않는다.
- 승인 게이트(G1~G4)에서는 멈추고 A/B/C 선택지로 묻는다.

## 디자인

- 흰색, 검정, 빨강만 쓰는 포스터형 라이트 단일 테마. 다크 모드 없음.
- 영문 대제목과 큰 숫자는 Anton, 한글은 IBM Plex Sans KR, 코드와 로그는 IBM Plex Mono.
- 스타일은 `assets/css/main.css`의 CSS 변수와 일반 CSS. 스크립트는 필요한 곳에만 작은 바닐라 JS.
- 본문 너비 약 65자, 모바일 최소 폭 360px, 키보드 포커스 표시, `prefers-reduced-motion` 준수.
- 가짜 로고, 임의의 숙련도 퍼센트, 근거 없는 수치는 쓰지 않는다.
