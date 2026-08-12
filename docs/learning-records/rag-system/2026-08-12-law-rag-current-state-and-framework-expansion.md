---
title: "law-rag 현재 기준점과 프레임워크 확장 계획"
description: "law-rag를 현재 프로젝트 적용 기준점으로 기록하고, LlamaIndex·LangChain·LangGraph의 실행 경로 분석 후 한 경계만 확장하기로 한 학습 계획"
author: yjs000
published: 2026-08-12
updated: 2026-08-12
reading_time: 약 2분
tags: [law-rag, llamaindex, langchain, langgraph, learning-evidence]
---

# law-rag 현재 기준점과 프레임워크 확장 계획

| 작성자 | 게시·수정일 | 읽는 시간 | 태그 |
|---|---|---|---|
| yjs000 | 2026-08-12 | 약 2분 | Law RAG · LlamaIndex · LangChain · LangGraph · Learning Evidence |

law-rag의 현재 개발 수준을 다음 학습의 출발점으로 삼고, 프레임워크의 이름이 아니라 실제로 필요한 경계를 분석으로 확인한 뒤 확장한다.

## 학습 맥락과 증거 수준

- **학습 계획 위치:** [학습계획 → RAG 시스템](../../learning-plans/rag-system/README.md) → 오픈소스 실행 경로 분석 → law-rag 확장 판단
- **증거 수준:** 프로젝트 적용의 현재 기준점과 다음 학습 계획을 남긴 기록이다. 이 기록 자체는 LlamaIndex·LangChain·LangGraph를 law-rag에 적용했다는 증거가 아니다.
- **기존 근거:** 현재 파이프라인과 1블록 판정은 [law-rag 로드맵 1블록 점검](2026-08-11-law-rag-roadmap-block-1-review.md)에 보존한다.

## 학습자 원문

> rag은 지금 law rag정도로 개발했다는걸 짧게 기록으로 남기고 다음 계획으로
> 앞으로는 law rag를 llamaindex와 langchain langgraph이용해서 확장할거야.
> 그과정에서 랭그래프 랭체인 라마인덱스 활용한 오픈소스 또는 예제 분석할거야

## 현재 판단

- **현재 기준점:** law-rag는 법령 RAG의 고정 파이프라인을 적용한 프로젝트다. 이를 RAG 학습 전체의 완료로 쓰지 않고, 비교 가능한 현재 상태로 둔다.
- **다음 계획:** LlamaIndex·LangChain·LangGraph를 사용한 오픈소스 또는 최소 예제에서 한 요청의 실행 경로를 분석한다.
- **확장 순서:** 분석 → 현재 law-rag와의 차이 정리 → 필요한 경계 한 가지 선택 → 작은 적용 → 기존 질문과 근거 검증 기준으로 전후 비교.

## 기억해야 할 기준

- **분석과 도입을 분리한다:** 예제가 동작하거나 코드 흐름을 이해한 것만으로 law-rag에 프레임워크를 넣지 않는다.
- **경계별로 판단한다:** LlamaIndex는 데이터·인덱싱, LangChain은 모델·도구 호출, LangGraph는 상태·분기·재시도 문제를 각각 해결하는 후보로 비교한다.
- **한 번에 하나만 바꾼다:** 세 도구를 함께 도입하면 품질 변화와 실패 원인을 구분할 수 없다.

## 다음 검증

1. 각 도구를 활용한 작은 예제 또는 오픈소스 하나씩을 선정한다.
2. 각 대상에서 입력, 주요 상태, 검색·모델·도구 호출, 출력과 오류 처리의 실제 파일·함수를 기록한다.
3. law-rag에 필요한 경계 한 가지와 채택하지 않을 경계를 나눠 적는다.
4. 선택한 한 경계만 작게 적용하고 기존 평가 질문으로 전후를 비교한다.
