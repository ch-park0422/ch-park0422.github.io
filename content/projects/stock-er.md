---
title: Stock-er
summary: 주식 밸류에이션, 시장 흐름, 암호화폐 온체인 지표를 다루는 한영 분석 대시보드입니다.
card: 밸류에이션, 온체인 지표, 백테스트 분석 대시보드
date: 2026-05-26
period: 2026.05.26–06.05
stack: [Next.js, Recharts, 한국투자증권 Open API, Yahoo Finance, Finnhub, Alpha Vantage]
scale: 파일 36개
repo: https://github.com/ch-park0422/stock-er
demo: ""
weight: 5
---

## 문제

주식 밸류에이션, 시장 흐름, 암호화폐 온체인 지표를 다루는 한영 분석 대시보드입니다.

## 내 역할

초기에 시나리오 생성기, 검증 엔진, 모니터로 구성한 QA 하네스를 만들고 /admin/test-harness로 분리했습니다.

## 설계 결정

- DCF, EPS-PER 순으로 시도하는 하이브리드 밸류에이션
- PEG, Piotroski F-Score, Magic Formula를 적용한 구루 전략 탭
- 움직임 큰 종목과 섹터를 보여주는 Market Pulse
- 시장 국면 감지, 동적 가중 점수, 백테스트를 갖춘 Quant Engine

## 문제와 해결

{{< fix problem="Finnhub 캔들 API가 403을 반환했습니다." >}}OHLCV 데이터를 Yahoo Finance로 교체했습니다.{{< /fix >}}
{{< fix problem="Alpha Vantage 사용량이 초과됐습니다." >}}Finnhub로 자동 전환하게 했습니다.{{< /fix >}}
{{< fix problem="API 실패 시 mock 데이터가 실제 값처럼 보일 수 있었습니다." >}}폴백을 없애고 호출 불가 화면을 표시했습니다.{{< /fix >}}
{{< fix problem="암호화폐 백테스트 적중률이 0%로 나왔습니다." >}}조회 기간과 목표치를 조정하고, 신호 없음 상태를 따로 처리했습니다.{{< /fix >}}

## 품질 근거

- 시나리오 생성기, 검증 엔진, 모니터로 구성한 QA 하네스(/admin/test-harness)

## 링크

- 저장소: [ch-park0422/stock-er](https://github.com/ch-park0422/stock-er)
