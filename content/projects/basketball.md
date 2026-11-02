---
title: 농구팀 사이트
summary: 경기 일정, 참석 투표, 팀 구성, 영상 공유를 한곳에서 처리하는 팀 운영 사이트입니다.
card: 회원, 투표, 팀 구성을 다루는 팀 운영 서비스
date: 2026-05-21
period: 2026.05.21–23
stack: [Next.js, Supabase, "@hello-pangea/dnd"]
stackDetail: "Next.js, Supabase Auth, @hello-pangea/dnd"
scale: 파일 66개
repo: https://github.com/ch-park0422/basketball-team
demo: ""
weight: 7
---

## 문제

경기 일정, 참석 투표, 팀 구성, 영상 공유를 한곳에서 처리하는 팀 운영 사이트입니다.

## 설계 결정

- 로그인, 회원 등급, 관리자 회원 관리
- 경기 일정 게시판과 실시간 참석 투표
- 드래그앤드롭 팀 빌더와 투표 변경 자동 동기화
- 영상 게시판, 프로필, 팀 대시보드

## 문제와 해결

{{< fix problem="초기 Prisma와 SQLite 코드가 Vercel 배포에 맞지 않았습니다." >}}레거시 코드를 걷어내고 Supabase로 정리했습니다.{{< /fix >}}
{{< fix problem="회원을 삭제해도 인증 계정이 남았습니다." >}}service role로 auth.users에서 직접 삭제하게 했습니다.{{< /fix >}}

## 링크

- 저장소: [ch-park0422/basketball-team](https://github.com/ch-park0422/basketball-team)
