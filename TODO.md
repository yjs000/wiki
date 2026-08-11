# AI 시스템 학습 목표

1. [x] **Codex로 실제 프로젝트를 진행한다** — [law-rag](https://github.com/yjs000/law-rag)에 Codex를 활용했다.
2. [ ] **RAG 검색 시스템을 코드와 평가 결과로 설명한다** — 일반 검색, 벡터 검색, 하이브리드 검색의 차이를 같은 평가셋으로 비교한다.
3. [ ] **AI 오픈소스의 주요 실행 경로를 읽고 축소 재구현한다** — 기능표가 아니라 진입점, 상태, 호출 흐름, 실패 처리를 기준으로 평가한다.
4. [ ] **GitHub Issues와 Symphony로 코딩 작업을 실행한다** — 작은 저장소에서 격리, 재시도, 상태 전이와 PR 검증을 직접 확인한다.
5. [ ] **Discord, Hermes, Symphony를 역할이 겹치지 않게 연결한다** — Hermes는 요청·판단·결과 설명을, Symphony는 Issue dispatch와 Codex 실행을 담당한다.

## 에이전트 프레임워크 학습 순서 (2026-08-11)

지원 포지션이 LangChain·LangGraph를 직접 언급해 다음 순서로 우선 학습한다. LangGraph는 법령 RAG의 `retrieve → rerank → 검증 → generation → verification → retry` 구조를 그래프로 옮겨볼 수 있어 순서상 우선순위를 가장 높게 둔다.

6. [ ] **Function Calling / Tool Calling** — 모델의 툴 호출 메커니즘을 프레임워크 없이 이해한다.
7. [ ] **LangChain Agent** — `agent-service-toolkit-langgraph-langchain-walkthrough.md`에서 정리한 LangChain/LangGraph 역할 구분을 에이전트 실행 관점으로 확장한다.
8. [ ] **LangGraph** — 법령 RAG의 검색·검증·재시도 파이프라인을 그래프로 재구성해본다.
9. [ ] **Agentic RAG 직접 구현** — 프레임워크 없이 최소 구현으로 검증한 뒤 LangGraph 버전과 비교한다.
10. [ ] **Multi-Agent** — 역할 분담과 오케스트레이션 방식을 비교한다.
11. [ ] **CrewAI / OpenAI Agents SDK / ADK 중 하나 비교** — LangGraph와 같은 과제로 비교해 선택 근거를 남긴다.
