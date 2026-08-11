---
title: "에이전트 프레임워크 학습 로드맵: Function Calling에서 프레임워크 비교까지"
description: "지원 포지션이 요구하는 LangChain·LangGraph 역량을 기준으로, 에이전트 프레임워크를 어떤 순서로 왜 그 순서로 익힐지 정리한 단계별 계획"
author: yjs000
published: 2026-08-11
updated: 2026-08-11
reading_time: 약 5분
tags: [langgraph, langchain, agentic-rag, multi-agent, study-roadmap]
---

# 에이전트 프레임워크 학습 로드맵: Function Calling에서 프레임워크 비교까지

| 작성자 | 게시·수정일 | 읽는 시간 | 태그 |
|---|---|---|---|
| yjs000 | 2026-08-11 | 약 5분 | LangGraph · LangChain · Agentic RAG · Multi-Agent · Study Roadmap |

같은 그래프 문법으로 안전 게이트, 도구 루프, human-in-the-loop, 다중 에이전트까지 표현되는 걸 [agent-service-toolkit 코드 읽기](../ai-agent-systems/agent-service-toolkit-langgraph-langchain-walkthrough.md)에서 확인한 뒤, 다음 질문이 남았다. 이 라이브러리들을 처음부터 배운다면 어떤 순서가 맞는가.

## 목차

- [배경과 제약](#배경과-제약)
- [학습 순서](#학습-순서)
- [왜 LangGraph를 가장 깊게 보는가](#왜-langgraph를-가장-깊게-보는가)
- [단계별 통과 조건](#단계별-통과-조건)
- [한계와 미검증 가설](#한계와-미검증-가설)
- [결론과 다음 검증](#결론과-다음-검증)
- [참고 자료](#참고-자료)

## 배경과 제약

지원 포지션이 LangChain·LangGraph를 직접 언급한다(**추천** — 특정 상황에 대한 선택이며 공식 기능 확인은 아니다). 이미 진행 중인 [law-rag](https://github.com/yjs000/law-rag) 프로젝트는 검색·생성 파이프라인은 있지만 에이전트 오케스트레이션 계층이 없다. 두 조건을 합치면 "프레임워크 문법을 익히는 것"과 "법령 RAG에 실제로 붙일 수 있는 것"을 분리하지 않고 같은 순서로 다루는 편이 시간을 아낀다.

이 로드맵은 [RAG에서 독립적인 AI 시스템 설계까지: 3년 학습 로드맵](ai-systems-study-roadmap.md)의 하위 갈래다. 상위 로드맵은 에이전트 런타임 구현을 13개월차 이후로 미루지만, 이 문서는 그 전 단계인 "기존 프레임워크의 문법과 설계를 코드 읽기·비교로 이해하는" 범위만 다룬다. 최소 루프를 프레임워크 없이 직접 구현하는 것은 여전히 상위 로드맵의 13~15개월차 몫이다.

## 학습 순서

```text
Function Calling / Tool Calling
→ LangChain Agent
→ LangGraph
→ Agentic RAG 직접 구현
→ Multi-Agent
→ CrewAI / OpenAI Agents SDK / ADK 중 하나 비교
```

| 순서 | 단계 | 목표 |
|---|---|---|
| 1 | Function Calling / Tool Calling | 프레임워크 없이 모델의 툴 호출 메커니즘(스키마 전달 → 모델의 호출 결정 → 파싱 → 실행 → 결과 반환)을 이해한다 |
| 2 | LangChain Agent | `Runnable`, `bind_tools`, 메시지 타입 등 agent-service-toolkit에서 이미 확인한 LangChain 부품을 에이전트 실행 관점으로 확장한다 |
| 3 | LangGraph | `StateGraph`, 조건부 엣지, managed value, 체크포인터로 법령 RAG의 검색·검증·재시도 흐름을 그래프로 재구성한다 |
| 4 | Agentic RAG 직접 구현 | 프레임워크 없이 최소 구현으로 먼저 검증한 뒤 LangGraph 버전과 비교한다 |
| 5 | Multi-Agent | 역할 분담과 오케스트레이션 방식(수동 조립 vs. `create_supervisor` 같은 위임형)을 비교한다 |
| 6 | 프레임워크 비교 | CrewAI, OpenAI Agents SDK, ADK 중 하나를 LangGraph와 같은 과제로 비교해 선택 근거를 남긴다 |

## 왜 LangGraph를 가장 깊게 보는가

**설계 해석**: [agent-service-toolkit 코드 읽기](../ai-agent-systems/agent-service-toolkit-langgraph-langchain-walkthrough.md)에서 rag-assistant는 `guard_input`(안전성 검사) → `model`(검색 tool 호출 여부 판단) → `tools`(벡터 검색) → 다시 `model`로 돌아가는 조건부 루프 하나로 구성돼 있었다. 이 골격은 법령 RAG가 필요로 하는 `retrieve → rerank → 검증 → generation → verification → retry` 흐름과 노드·조건부 엣지 단위로 거의 1대1 대응한다.

- `retrieve`·`rerank`는 rag-assistant의 `tools` 노드에 해당하지만, rag-assistant는 rerank 없이 top-k 유사도 검색만 한다는 한계가 이미 확인돼 있다 — 그 빈 자리를 직접 채워보는 것이 3단계의 구체적인 실습 대상이다.
- `검증`은 rag-assistant에는 없는 노드다. `pending_tool_calls()`가 하는 일은 tool_calls 존재 여부만 보는 라우팅이지, "근거가 충분한가"를 채점하는 별도 노드가 아니었다. 법령 RAG에 검증 노드를 추가하는 것 자체가 LangGraph 조건부 엣지를 새로 설계하는 연습이 된다.
- `retry`는 rag-assistant의 `RemainingSteps` managed value와 같은 계열의 문제다. 무한 루프를 어떻게 막을지, 몇 번째 재시도부터 사과 응답으로 전환할지를 그래프 상태로 표현하는 패턴을 그대로 참고할 수 있다.

다른 단계(1, 2, 4~6)는 개념과 문법을 넓히는 단계이고, LangGraph만 "이미 읽은 코드의 빈 부분을 직접 채우는" 단계라는 점이 우선순위를 높이는 이유다.

## 단계별 통과 조건

각 단계는 [실습·검증 기록 작성 규칙](../learning-evidence/README.md)의 증거 수준 표기를 따라, 최소 **독립 실험** 수준(작은 코드와 실제 출력)까지 도달해야 다음 단계로 넘어간다. 코드를 읽고 설명한 것만으로는(**개념 설명** 수준) 통과로 보지 않는다.

- **1~2단계**: 모델 API 문서의 tool-calling 예제를 그대로 실행해 보고, 모델이 언제 tool_calls를 내는지/안 내는지 최소 5개 프롬프트로 관찰한다.
- **3단계**: 법령 RAG의 검색·검증·재시도를 `StateGraph`로 재구성한 실행 가능한 그래프를 만든다. rag-assistant와 달리 검증 노드가 실제로 재검색을 유발하는 사례를 하나 이상 재현한다.
- **4단계**: 3단계와 동일한 과제를 프레임워크 없이 최소 구현하고, 두 구현의 코드량·재시도 로직 표현 방식·실패 처리 차이를 표로 비교한다.
- **5단계**: 최소 두 가지 오케스트레이션 방식(직접 조건부 엣지 vs. 위임형 supervisor)으로 같은 멀티에이전트 과제를 풀어보고 차이를 설명한다.
- **6단계**: LangGraph로 이미 통과한 과제를 CrewAI·Agents SDK·ADK 중 하나로 재구현해 같은 평가 기준으로 비교한다.

## 한계와 미검증 가설

**미검증 가설**: 이 순서가 실제로 가장 효율적인지는 아직 검증하지 않았다. 특히 1~2단계(Function Calling, LangChain Agent)를 생략하고 3단계(LangGraph)부터 시작해도 학습 결과가 크게 다르지 않을 가능성이 있다 — agent-service-toolkit 읽기에서 이미 `bind_tools`, `Runnable` 같은 LangChain 개념을 코드 근거로 확인했기 때문이다. 이 가설은 1~2단계를 실제로 통과한 뒤에만 검증할 수 있다.

법령 RAG에 검증 노드를 추가하는 것이 rerank 부재보다 우선순위가 높은지도 아직 근거가 없다. 두 개선 모두 rag-assistant에는 없는 기능이며, 어느 쪽이 답변 품질에 더 큰 영향을 주는지는 별도 실험이 필요하다.

## 결론과 다음 검증

이 로드맵은 agent-service-toolkit 코드 읽기에서 나온 관찰 하나 — "그래프 골격은 같은데 검증 노드와 rerank가 빠져 있다" — 를 학습 순서로 바꾼 것이다. 다음 검증은 1단계(Function Calling)를 프레임워크 없이 통과시키는 것부터 시작한다.

## 참고 자료

- [agent-service-toolkit 코드 읽기](../ai-agent-systems/agent-service-toolkit-langgraph-langchain-walkthrough.md) — 이 로드맵의 근거가 된 rag-assistant 구조 분석
- [RAG에서 독립적인 AI 시스템 설계까지: 3년 학습 로드맵](ai-systems-study-roadmap.md) — 상위 로드맵, 에이전트 런타임 직접 구현은 13개월차 이후로 배치
- [LangGraph 공식 문서](https://langchain-ai.github.io/langgraph/)
- [LangChain Runnable 인터페이스](https://python.langchain.com/docs/concepts/runnables/)
