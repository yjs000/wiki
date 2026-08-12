---
title: "LangGraph·LangChain 코드 읽기: 질문 원문과 개념 설명 증거"
description: "agent-service-toolkit 코드 읽기 아티클에서 나온 학습자 질문, 판정, 한계와 다음 검증을 LangGraph 학습 주제에 연결한 기록"
author: yjs000
published: 2026-08-11
updated: 2026-08-12
reading_time: 약 2분
tags: [langgraph, langchain, learning-evidence, code-reading, agent-service-toolkit]
---

# LangGraph·LangChain 코드 읽기: 질문 원문과 개념 설명 증거

| 작성자 | 게시·수정일 | 읽는 시간 | 태그 |
|---|---|---|---|
| yjs000 | 게시 2026-08-11 · 수정 2026-08-12 | 약 2분 | LangGraph · LangChain · Learning Evidence · Code Reading · Agent Service Toolkit |

학습 계획 위치: [학습계획 → 에이전트 프레임워크](../../learning-plans/agent-framework/README.md) → LangGraph → 실행 경로 코드 읽기

이 기록은 [agent-service-toolkit 코드 읽기 아티클](../../readings/agent-systems/agent-service-toolkit-langgraph-langchain-walkthrough.md)의 8절에서 직접 던진 질문과 판정을 학습증거 형식으로 연결한다. 증거 수준은 **개념 설명**이다. 실제 코드를 읽어 답을 확인했지만, 별도 실행 실험이나 law-rag 적용은 아직 하지 않았다.

## 목차

- [학습자 원문](#학습자-원문)
- [판정과 놓친 경계](#판정과-놓친-경계)
- [기억해야 할 기준](#기억해야-할-기준)
- [다음 검증](#다음-검증)
- [연결 자료](#연결-자료)

## 학습자 원문

아래 질문은 아티클의 대화 기록에서 맞춤법과 표현을 고치지 않고 그대로 옮겼다.

```text
rag-assistant를 파보자. run_service가 service를 호출하고 service가 agents를 호출하고 agents가 rag-assistant를 호출하는건가? rag-assistant는 사용자 입력에 따라 달라지는건가? 어디서주입하지?
```

```text
db에서 근거를 찾았는데 근거가 충분하지 않을경우, 한번더 db찾는 tool로 요청한다는거지? 근거가 충분한지 아닌지는 누가 판단해? db를 불러오는걸 굳이 tool로 할필요가 있어? langgraph를 쓴거야 langChain을 쓴거야? 구분을 명확히해.
```

```text
툴은 뭘사용하지? 툴이 몇번씩작동하고 사용자 응답을 기다리는 로직이 어덯게 되어있지/
```

```text
rag pipeline도 구성되어있어?
```

```text
단순 임베딩으로 되어있어?
```

## 판정과 놓친 경계

- **호출과 조회:** `run_service.py → service.py → agents.py → rag_assistant.py`로 이어지는 큰 방향은 맞았다. 다만 rag-assistant 그래프는 요청마다 새로 호출되는 것이 아니라 서버 시작 때 컴파일·등록되고, 요청에서는 `agent_id`로 조회된다. URL의 `agent_id`로 그래프를 고르는 경계와 `state["messages"]`로 사용자 입력이 들어가는 경계를 분리해야 한다.
- **재검색과 근거 판정:** tool 호출의 존재는 `pending_tool_calls()`가 기계적으로 분기하지만, 다시 검색할지와 검색어는 LLM이 다음 응답에서 정한다. 이 아티클의 rag-assistant에는 근거 충분성을 따로 판정하는 결정론적 검증 노드가 없다.
- **LangGraph와 LangChain:** 그래프 노드·엣지·루프·상태·체크포인터는 LangGraph의 책임이고, 모델 호출 인터페이스·메시지 타입·tool 정의·벡터 저장소 연동은 LangChain의 책임이다. 하나의 라이브러리 이름으로 호출 경로 전체를 설명하면 역할이 섞인다.
- **반복과 중단:** rag-assistant는 LLM이 tool call을 내는 동안 반복하지만 `RemainingSteps`로 상한을 둔다. `interrupt()`가 없어 사람의 응답을 기다리지 않으며, 대화가 이어지는 느낌은 `thread_id` 체크포인터가 요청 사이 상태를 복원하기 때문에 생긴다.
- **인제스천과 검색:** `create_chroma_db.py`의 문서→청크→임베딩→저장 흐름은 오프라인 인제스천이고, 그래프의 tool 호출은 온라인 검색이다. 둘을 하나의 `RAG 파이프라인`으로 뭉치지 않는다.
- **에이전트성과 검색 품질:** LLM이 검색 시점·검색어·횟수를 정하는 것과 검색 방식 자체가 정교한 것은 다르다. 이 사례의 검색은 순수 유사도 top-5 기본형이고, MMR·리랭커·하이브리드·메타데이터 필터·쿼리 재작성은 확인되지 않았다.

## 기억해야 할 기준

- **입력 주입 위치:** 라우팅 입력(`agent_id`)과 그래프 상태 입력(`messages`)을 서로 다른 코드 경로로 추적한다.
- **LLM 판단과 코드 검증:** LLM이 tool을 다시 부를지 결정할 수 있어도, 근거 충분성·인용 허용·안전성 검증이 자동으로 생기지는 않는다. 필요한 경우 별도 노드나 결정론적 검증을 설계한다.
- **반복과 대기:** tool 반복 횟수 제한과 human-in-the-loop 중단은 독립된 기능이다. `RemainingSteps`와 `interrupt()` 존재 여부를 각각 확인한다.
- **RAG의 두 경로:** 인제스천과 질의 시점 검색을 분리해 입력·상태·실패·재시도 경계를 설명한다.

## 다음 검증

1. Function Calling 예제를 프레임워크 없이 실행하고, 최소 5개 프롬프트에서 tool call이 발생하는 조건을 기록한다.
2. law-rag의 검색·검증·재시도를 `StateGraph`로 표현하는 작은 독립 실험을 만들고, 검증 노드가 재검색을 유발하는 사례를 재현한다.
3. 같은 과제를 프레임워크 없이 구현해 코드량, 재시도 표현, 실패 처리의 차이를 비교한다.

현재 기록은 코드 읽기와 설명의 증거다. 위 실험이 생기기 전에는 에이전트 프레임워크 로드맵의 LangGraph 단계를 통과했다고 판정하지 않는다.

## 연결 자료

- [에이전트 프레임워크 학습계획](../../learning-plans/agent-framework/README.md) — 이 기록의 1차 소속과 다음 단계의 통과 조건
- [LangGraph·LangChain 실전 코드 읽기](../../readings/agent-systems/agent-service-toolkit-langgraph-langchain-walkthrough.md) — 코드 파일·함수·상태와 상세 판정
- [RAG 시스템 학습계획](../../learning-plans/rag-system/README.md) — 오픈소스 실행 경로 읽기 주제의 참조 위치
