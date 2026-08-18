---
title: "RAG 학습계획"
description: "러프한 RAG 구현을 기준점으로 LlamaIndex, LangChain, LangGraph를 순서대로 적용하는 간단한 학습계획"
author: yjs000
published: 2026-07-22
updated: 2026-08-18
reading_time: 약 1분
tags: [rag, llamaindex, langchain, langgraph, study-roadmap]
---

# RAG 학습계획

| 작성자 | 게시·수정일 | 읽는 시간 | 태그 |
|---|---|---|---|
| yjs000 | 게시 2026-07-22 · 수정 2026-08-18 | 약 1분 | RAG · LlamaIndex · LangChain · LangGraph · Study Roadmap |

law-rag를 현재 기준점으로 두고, 구현 방식을 한 단계씩 바꿔 보며 RAG 시스템을 확장한다.

## 이 주제의 학습목표

1. [x] **러프한 RAG를 구현한다** — law-rag로 법령 원문, 검색, 답변, 근거 표시가 연결된 현재 기준점을 만들었다.
2. [x] **LlamaIndex를 이용해 RAG를 구현한다** — [sec-insights](https://github.com/run-llama/sec-insights)를 8단계(Stage 0~7)로 손으로 재현해 인덱스 저장, 메타데이터 필터, 서브쿼스천, 멀티툴 에이전트, SSE 스트리밍까지 구성과 동작을 비교했다.
3. [ ] **LangChain과 LangGraph를 도입한다** — 필요한 모델·도구 호출과 상태·분기 흐름에만 적용한다.

## 학습 순서

1. [law-rag](https://github.com/yjs000/law-rag)의 현재 RAG 구현을 기준점으로 둔다.
2. LlamaIndex를 이용한 RAG 예제 또는 오픈소스를 분석하고 구현한다.
3. LangChain과 LangGraph를 도입해 모델·도구 호출, 상태·분기 흐름을 확장한다.

## 관련 기록

- [law-rag 1블록 점검](../../learning-records/rag-system/2026-08-11-law-rag-roadmap-block-1-review.md) — 현재 구현과 초기 학습 판정
- [law-rag 현재 기준점과 프레임워크 확장 계획](../../learning-records/rag-system/2026-08-12-law-rag-current-state-and-framework-expansion.md) — 다음 단계의 판단 기준
- [LlamaIndex sec-insights 재현 8단계: Stage 7 SSE 스트리밍 질문·판정 증거](../../learning-records/rag-system/2026-08-18-llamaindex-sec-insights-stage7-sse.md) — 8단계 재현의 마지막 단계, SSE 연결 버그·세션 설계 오답 정정·도구와 에이전트 개수 혼동 정정
