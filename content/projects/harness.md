---
title: my-harness-app
summary: 역할별 CLAUDE.md로 에이전트 협업 구조를 시험한 Fastify 백엔드입니다.
card: 역할별 규칙 파일로 에이전트 구조를 시험한 백엔드
date: 2026-05-22
period: 2026.05.22
status: 실험
stack: [Fastify, Prisma]
stackDetail: "Fastify, Prisma v7"
scale: 파일 20개, 테스트 케이스 8개(이번 집계에서 미실행)
repo: https://github.com/ch-park0422/my-harness-app
demo: ""
weight: 8
---

## 문제

역할별 CLAUDE.md로 에이전트 협업 구조를 시험한 Fastify 백엔드입니다.

## 설계 결정

루트의 CLAUDE.md는 총괄 아키텍트 역할을 맡아 도메인 간 API와 데이터 흐름을 조율합니다. backend, frontend, tests 폴더에는 각자의 규칙을 두었고, 구현이 끝나면 테스트 쪽 규칙에 따라 검증을 요청하게 했습니다.

## 품질 근거

- 테스트 케이스 8개가 있습니다. 2026-11-02 집계에서는 실행하지 않았습니다.

## 회고

이후 잔흔의 직군 팀 구조로 이어진 초기 실험입니다.

## 링크

- 저장소: [ch-park0422/my-harness-app](https://github.com/ch-park0422/my-harness-app)
