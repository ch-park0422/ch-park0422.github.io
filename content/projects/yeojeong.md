---
title: 여정
summary: 항공권, 숙박, 일정, 경비, 지도, 추천을 한곳에 모은 여행 계획 서비스입니다. 한국어와 영어를 지원합니다.
date: 2026-08-31
period: 2026.08.31–09.02
stack: [Next.js, Prisma, PostgreSQL, Auth.js, next-intl, Mapbox GL, Anthropic SDK, Playwright]
stackDetail: "Next.js, Prisma, PostgreSQL(Neon), Auth.js, next-intl, Mapbox GL, Anthropic SDK, Playwright"
scale: 파일 325개, 단위·통합 테스트 299개 통과
repo: ""
demo: ""
weight: 2
featured: true
tile: { style: light, lines: [여정], label: 웹 · 데이터 모델링 · LLM 추천 }
metrics:
  - label: 통과한 테스트
    value: "299"
    measuredAt: 2026-11-02
---

## 문제

항공권, 숙박, 일정, 경비, 지도, 추천을 한곳에 모은 여행 계획 서비스입니다. 한국어와 영어를 지원합니다.

## 내 역할

SPEC.md에 기술 스택, 데이터 모델, 화면 원칙을 고정하고 Phase 0부터 10까지 나눠 진행했습니다. 뼈대, 인증, 일정, 경비, 티켓, 지도, 추천, LLM, 공유, 체크리스트 순서입니다.

이후 경쟁 서비스 트리플을 분석해 문서로 남기고, 거기서 꼽은 개선 항목을 우선순위대로 구현했습니다. 디자인은 시안을 비교해 유리 재질의 '맑음' 컨셉을 적용했습니다.

## 설계 결정

- 모바일은 여행 중에 쓰는 화면, 데스크톱은 여행 전에 계획하는 화면으로 나눴습니다.
- 계획 금액과 실제 지출을 데이터 모델에서 분리해 비교할 수 있게 했습니다.

## 문제와 해결

{{< fix problem="Neon CLI가 .env.local의 DB 주소를 덮어써, 시드나 E2E 실행이 원격 데이터를 지울 수 있었습니다." >}}원격 DB 사고 방지 가드를 넣고, DB 명령의 대상을 한 곳에서 정하게 했습니다.{{< /fix >}}
{{< fix problem="서버리스 환경에서는 업로드한 티켓 파일이 디스크에 남지 않습니다." >}}S3 호환 저장소를 쓰고, 설정이 없으면 프로덕션 업로드를 막았습니다.{{< /fix >}}
{{< fix problem="지도가 그려지지 않거나 움직이지 않았습니다." >}}원인별로 나눠 수정했습니다.{{< /fix >}}

## 품질 근거

- 단위·통합 테스트 299개 통과 (2026-11-02 실행, E2E 제외)
- E2E 테스트도 있으며, 이번 집계에서는 제외했습니다.

## 링크

- 저장소: 비공개
