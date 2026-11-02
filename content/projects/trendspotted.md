---
title: TrendSpotted
summary: 트렌드를 수집해 Claude로 정제하고 매일 자동으로 갱신하는 큐레이션 서비스입니다.
card: 수집, Claude 정제, 저장을 자동화한 큐레이션 서비스
date: 2026-05-25
period: 2026.05.25
stack: [Next.js, Supabase, Anthropic SDK, Vercel Cron]
scale: 파일 33개
repo: https://github.com/ch-park0422/TrendSpotted
demo: ""
weight: 6
---

## 문제

트렌드를 수집해 Claude로 정제하고 매일 자동으로 갱신하는 큐레이션 서비스입니다.

## 설계 결정

- Vercel Cron이 수집 작업을 호출하고, 수집 결과를 Claude가 정제해 Supabase에 저장합니다.

## 문제와 해결

{{< fix problem="Vercel Hobby 플랜에서 6시간 주기 크론을 쓸 수 없었습니다." >}}매일 1회로 변경했습니다.{{< /fix >}}
{{< fix problem="한국어 전문 검색 인덱스에서 오류가 났습니다." >}}pg_trgm으로 교체했습니다.{{< /fix >}}
{{< fix problem="스트리밍 응답에서 tool_use 처리가 불안정했습니다." >}}messages.create 호출로 전환했습니다.{{< /fix >}}

## 링크

- 저장소: [ch-park0422/TrendSpotted](https://github.com/ch-park0422/TrendSpotted)
