---
title: "RAG·에이전트 프레임워크 학습 로드맵: LlamaIndex에서 프레임워크 비교까지"
description: "law-rag 확장을 목표로 LlamaIndex·LangChain·LangGraph의 실행 경로를 분석하고, 필요한 경계만 채택하는 단계별 계획"
author: yjs000
published: 2026-08-11
updated: 2026-08-12
reading_time: 약 4분
tags: [llamaindex, langgraph, langchain, agentic-rag, multi-agent, study-roadmap]
---

# RAG·에이전트 프레임워크 학습 로드맵: LlamaIndex에서 프레임워크 비교까지

| 작성자 | 게시·수정일 | 읽는 시간 | 태그 |
|---|---|---|---|
| yjs000 | 게시 2026-08-11 · 수정 2026-08-12 | 약 4분 | LlamaIndex · LangGraph · LangChain · Agentic RAG · Multi-Agent · Study Roadmap |

같은 그래프 문법으로 안전 게이트, 도구 루프, human-in-the-loop, 다중 에이전트까지 표현되는 걸 [agent-service-toolkit 코드 읽기](../../readings/agent-systems/agent-service-toolkit-langgraph-langchain-walkthrough.md)에서 확인한 뒤, 다음 질문이 남았다. 이 라이브러리들을 처음부터 배운다면 어떤 순서가 맞는가.

## 목차

- [배경과 제약](#배경과-제약)
- [학습 순서](#학습-순서)
- [왜 LangGraph를 가장 깊게 보는가](#왜-langgraph를-가장-깊게-보는가)
- [단계별 통과 조건](#단계별-통과-조건)
- [학습 주제와 증거](#학습-주제와-증거)
- [한계와 미검증 가설](#한계와-미검증-가설)
- [결론과 다음 검증](#결론과-다음-검증)
- [참고 자료](#참고-자료)

## 배경과 제약

이미 진행 중인 [law-rag](https://github.com/yjs000/law-rag)는 법령 원문·검색·생성·근거 검증의 고정 파이프라인을 현재 적용 기준점으로 둔다. 다음 확장은 LlamaIndex·LangChain·LangGraph를 한꺼번에 도입하는 일이 아니라, 각 도구를 쓴 오픈소스 또는 예제의 실행 경로를 분석하고 필요한 경계만 채택하는 일이다.

이 계획은 [RAG 시스템 학습계획](../rag-system/README.md)과 연결되는 별도 주제다. 현재 범위는 "기존 프레임워크의 문법과 설계를 코드 읽기·비교로 이해하는 것"과, 그 분석을 근거로 law-rag의 한 경계만 작게 확장하는 것까지다. 전체 에이전트 런타임이나 멀티에이전트 구현으로 범위를 넓히지 않는다.

### 이 주제의 학습목표

- [ ] **law-rag 확장에 필요한 프레임워크 경계를 순서대로 검증한다** — LlamaIndex 분석 → Function Calling → LangChain 분석 → LangGraph 분석 → 한 경계의 작은 확장 → 비교.

## 학습 순서

```text
LlamaIndex RAG 예제 또는 오픈소스 분석
→ Function Calling / Tool Calling
→ LangChain 예제 또는 오픈소스 분석
→ LangGraph 예제 또는 오픈소스 분석
→ law-rag의 한 경계만 작은 확장
→ 비교와 채택 판단
```

| 순서 | 단계 | 목표 |
|---|---|---|
| 1 | LlamaIndex 분석 | 데이터 적재·인덱싱·검색 경계가 law-rag의 현재 파싱·청킹·검색 계약과 어디서 만나고 달라지는지 추적한다 |
| 2 | Function Calling / Tool Calling | 프레임워크 없이 모델의 툴 호출 메커니즘(스키마 전달 → 모델의 호출 결정 → 파싱 → 실행 → 결과 반환)을 이해한다 |
| 3 | LangChain 분석 | `Runnable`, `bind_tools`, 메시지 타입 등 LangChain 부품이 모델·프롬프트·도구 호출 경계를 어떻게 묶는지 실제 예제 또는 오픈소스 경로로 분석한다 |
| 4 | LangGraph 분석 | `StateGraph`, 조건부 엣지, 상태 저장이 검색·검증·재시도 흐름을 어떻게 표현하는지 실제 예제 또는 오픈소스 경로로 분석한다 |
| 5 | law-rag 작은 확장 | 세 분석 결과를 비교해 데이터·도구·상태 경계 중 하나만 선택하고, 기존 고정 파이프라인과 같은 평가 질문으로 전후를 비교한다 |
| 6 | 채택 판단 | 도입한 부분, 도입하지 않은 부분, 근거와 되돌릴 방법을 기록한다 |

## 왜 LangGraph를 가장 깊게 보는가

**설계 해석**: [agent-service-toolkit 코드 읽기](../../readings/agent-systems/agent-service-toolkit-langgraph-langchain-walkthrough.md)에서 rag-assistant는 `guard_input`(안전성 검사) → `model`(검색 tool 호출 여부 판단) → `tools`(벡터 검색) → 다시 `model`로 돌아가는 조건부 루프 하나로 구성돼 있었다. 이 골격은 법령 RAG가 필요로 하는 `retrieve → rerank → 검증 → generation → verification → retry` 흐름과 노드·조건부 엣지 단위로 거의 1대1 대응한다.

- `retrieve`·`rerank`는 rag-assistant의 `tools` 노드에 해당하지만, rag-assistant는 rerank 없이 top-k 유사도 검색만 한다는 한계가 이미 확인돼 있다 — 그 빈 자리를 직접 채워보는 것이 3단계의 구체적인 실습 대상이다.
- `검증`은 rag-assistant에는 없는 노드다. `pending_tool_calls()`가 하는 일은 tool_calls 존재 여부만 보는 라우팅이지, "근거가 충분한가"를 채점하는 별도 노드가 아니었다. 법령 RAG에 검증 노드를 추가하는 것 자체가 LangGraph 조건부 엣지를 새로 설계하는 연습이 된다.
- `retry`는 rag-assistant의 `RemainingSteps` managed value와 같은 계열의 문제다. 무한 루프를 어떻게 막을지, 몇 번째 재시도부터 사과 응답으로 전환할지를 그래프 상태로 표현하는 패턴을 그대로 참고할 수 있다.

다른 단계(1, 2, 4~6)는 개념과 문법을 넓히는 단계이고, LangGraph만 "이미 읽은 코드의 빈 부분을 직접 채우는" 단계라는 점이 우선순위를 높이는 이유다.

## 단계별 통과 조건

각 분석 단계는 [학습기록 작성 규칙](../../learning-records/README.md)의 증거 수준 표기를 따라, 코드 읽기에서는 최소 **개념 설명**, law-rag 확장에서는 최소 **독립 실험** 수준(작은 코드와 실제 출력)까지 도달해야 한다. 코드를 읽고 설명한 것만으로 프레임워크 도입을 통과로 보지 않는다.

- **1단계**: LlamaIndex 예제 또는 오픈소스 한 경로에서 입력, 인덱스 생성, 검색, 출력의 실제 파일·함수를 기록한다.
- **2단계**: 모델 API 문서의 tool-calling 예제를 실행하고, 모델이 언제 tool_calls를 내는지/안 내는지 최소 5개 프롬프트로 관찰한다.
- **3~4단계**: LangChain·LangGraph 예제 또는 오픈소스 한 경로마다 입력, 상태, 모델·도구 호출, 분기·오류 처리의 실제 코드를 기록한다.
- **5단계**: 분석 결과가 가리키는 한 경계만 law-rag에 작게 적용하고, 기존과 같은 질문·근거 검증 기준으로 전후를 비교한다.
- **6단계**: 프레임워크를 사용한 부분과 사용하지 않은 부분을 각각 설명하고, 제거 또는 되돌릴 조건을 남긴다.

## 학습 주제와 증거

### LangGraph → 실행 경로 코드 읽기

- [LangGraph·LangChain 실전 코드 읽기](../../readings/agent-systems/agent-service-toolkit-langgraph-langchain-walkthrough.md) — **1차 관련 아티클**. agent-service-toolkit의 실제 파일·함수·상태를 따라간 코드 읽기다.
- [LangGraph·LangChain 코드 읽기 학습증거](../../learning-records/agent-framework/2026-08-11-langgraph-langchain-code-reading.md) — **1차 학습증거**. 아티클의 질문 원문, 판정, 기억 기준과 다음 검증을 보존한다. 증거 수준은 `개념 설명`이며, 이 단계의 독립 실험 통과를 뜻하지 않는다.

AI 시스템 학습 로드맵의 4블록은 이 기록을 참조할 수 있지만, 본문과 판정은 이 위치에만 둔다.

## 한계와 미검증 가설

**미검증 가설**: 이 순서가 실제로 가장 효율적인지는 아직 검증하지 않았다. 특히 1~2단계(Function Calling, LangChain Agent)를 생략하고 3단계(LangGraph)부터 시작해도 학습 결과가 크게 다르지 않을 가능성이 있다 — agent-service-toolkit 읽기에서 이미 `bind_tools`, `Runnable` 같은 LangChain 개념을 코드 근거로 확인했기 때문이다. 이 가설은 1~2단계를 실제로 통과한 뒤에만 검증할 수 있다.

법령 RAG에 검증 노드를 추가하는 것이 rerank 부재보다 우선순위가 높은지도 아직 근거가 없다. 두 개선 모두 rag-assistant에는 없는 기능이며, 어느 쪽이 답변 품질에 더 큰 영향을 주는지는 별도 실험이 필요하다.

## 결론과 다음 검증

이 로드맵은 law-rag를 현재 기준점으로 두고, 프레임워크 이름이 아니라 데이터·도구·상태 경계의 필요성을 먼저 검증하는 계획이다. 다음 검증은 LlamaIndex를 활용한 작은 예제 또는 오픈소스 하나에서 입력부터 검색 결과까지의 실행 경로를 실제 파일과 함수로 설명하는 것이다.

## 참고 자료

- [agent-service-toolkit 코드 읽기](../../readings/agent-systems/agent-service-toolkit-langgraph-langchain-walkthrough.md) — 이 계획의 근거가 된 rag-assistant 구조 분석
- [RAG 시스템 학습계획](../rag-system/README.md) — 상위 계획, 에이전트 런타임 직접 구현은 13개월차 이후로 배치
- [LlamaIndex 공식 문서](https://docs.llamaindex.ai/en/stable/) — 데이터·인덱싱·검색 경계 분석의 공식 출발점
- [LangChain 공식 문서](https://python.langchain.com/docs/introduction/) — 모델·프롬프트·도구 호출 경계 분석의 공식 출발점
- [LangGraph 공식 문서](https://langchain-ai.github.io/langgraph/)
- [LangChain Runnable 인터페이스](https://python.langchain.com/docs/concepts/runnables/)
