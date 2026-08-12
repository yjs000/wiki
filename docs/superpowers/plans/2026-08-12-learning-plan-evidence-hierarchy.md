# Learning Plan and Evidence Hierarchy Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 학습 목표, 로드맵, 관련 아티클, 학습증거를 README 기반의 주제 계층으로 분류하고 같은 주제의 기록을 병합한다.

**Architecture:** `AGENTS.md`는 목표·아티클이 들어올 때의 공통 분류와 병합 트리거를 가진다. `docs/learning-evidence/README.md`는 증거 문서의 1차 소속·세부 주제·병합 방식을 정의하고, 두 로드맵은 각 세부 주제에서 해당 증거를 링크한다.

**Tech Stack:** Markdown, Git, ripgrep

## Global Constraints

- README는 최상위 탐색 인덱스이며, 문서 작성 규칙을 중복하지 않는다.
- 학습자 원문은 맞춤법·표현·순서까지 고치지 않고 보존한다.
- 하나의 학습증거는 하나의 1차 로드맵 주제와 세부 주제를 가진다.
- 여러 주제에 연결되는 증거는 본문을 중복하지 않고 다른 주제에서 링크로 참조한다.
- 기존 RAG의 `부분 충족` 판정과 에이전트 코드 읽기의 `개념 설명` 증거 수준을 높이지 않는다.

---

### Task 1: 자동 분류·병합 규칙을 저장소 계약에 추가한다

**Files:**
- Modify: `AGENTS.md`
- Modify: `docs/learning-evidence/README.md`

**Interfaces:**
- Consumes: README의 카테고리와 `docs/learning-roadmaps/`의 기존 로드맵
- Produces: 새 목표·아티클·증거에 공통 적용되는 계층화와 병합 규칙

- [x] **Step 1: AGENTS.md에 짧은 트리거를 추가한다**

`저장소 지도` 뒤에 `학습 계획과 증거의 자동 분류` 절을 넣는다. 새 목표는 README 카테고리와 로드맵을 먼저 찾고, 겹치는 주제는 기존 로드맵 절에 병합하며, 관련 아티클·질문·실험은 하나의 1차 주제와 세부 주제에 연결한다는 규칙을 적는다.

- [x] **Step 2: 학습증거 README에 문서 단위 규칙을 추가한다**

목차와 `파일과 연결 규칙`을 확장한다. 증거마다 `학습 계획 위치`를 `로드맵 → 학습 주제 → 세부 주제` 형식으로 명시하고, 같은 위치의 새 원문·실험·판정은 기존 문서의 세부 절에 날짜 순으로 병합하며, 다중 관련성은 링크로만 처리한다고 적는다.

- [x] **Step 3: 완료 전 검사에 계층·중복 검사를 추가한다**

학습증거에 1차 소속과 세부 주제가 있는지, 로드맵에서 해당 증거로 이동할 수 있는지, 같은 증거 본문을 여러 문서에 복사하지 않았는지를 검사 항목으로 넣는다.

### Task 2: 기존 RAG 기록을 AI 시스템 로드맵의 세부 주제에 연결한다

**Files:**
- Modify: `docs/learning-roadmaps/ai-systems-study-roadmap.md`
- Modify: `docs/learning-evidence/2026-08-11-law-rag-roadmap-block-1-review.md`

**Interfaces:**
- Consumes: AI 시스템 로드맵의 1블록 `RAG 전체 경로`와 4블록 `오픈소스 실행 경로 읽기`
- Produces: RAG 증거의 1차 위치와 LangGraph 문서의 참조 위치

- [x] **Step 1: AI 시스템 로드맵에 주제별 증거 절을 만든다**

첫 3개월 상세 계획 뒤에 `학습 주제와 증거` 절을 추가한다. `1블록 → RAG 전체 경로 → 데이터 준비·검색·근거 검증`에 law-rag 통합 학습증거를 연결한다.

- [x] **Step 2: 오픈소스 읽기 중복을 참조로 처리한다**

`4블록 → 작은 오픈소스 실행 경로 읽기`에는 LangGraph·LangChain 코드 읽기 아티클과 그 학습증거를 참조로만 연결한다. 1차 소속은 에이전트 프레임워크 로드맵임을 적는다.

- [x] **Step 3: RAG 통합본에 1차 계획 위치를 적는다**

`기록의 범위와 증거 수준`에 `학습 계획 위치: AI 시스템 학습 로드맵 → 1블록 → RAG 전체 경로 → 데이터 준비·검색·근거 검증`을 추가한다.

### Task 3: 기존 LangGraph 아티클을 1차 학습증거로 연결한다

**Files:**
- Modify: `docs/learning-roadmaps/agent-framework-study-roadmap.md`
- Modify: `docs/ai-agent-systems/agent-service-toolkit-langgraph-langchain-walkthrough.md`
- Create: `docs/learning-evidence/2026-08-11-langgraph-langchain-code-reading.md`

**Interfaces:**
- Consumes: agent-service-toolkit 코드 읽기 아티클의 8절 질문 원문과 판정
- Produces: `에이전트 프레임워크 → LangGraph → 실행 경로 코드 읽기`의 1차 학습증거

- [x] **Step 1: LangGraph 단계에 관련 아티클과 증거 링크를 둔다**

에이전트 프레임워크 로드맵에 `학습 주제와 증거` 절을 만들고, `LangGraph → 실행 경로 코드 읽기` 세부 주제에서 아티클과 새 학습증거를 함께 연결한다.

- [x] **Step 2: 코드 읽기 아티클에 1차 계획 위치를 표시한다**

리드 아래에 `학습 계획 위치: 에이전트 프레임워크 학습 로드맵 → LangGraph → 실행 경로 코드 읽기`를 넣고, AI 시스템 4블록은 중복 없는 관련 참조임을 명시한다.

- [x] **Step 3: 새 학습증거를 작성한다**

아티클 8절의 질문 원문을 그대로 보존하고, 아티클에서 확인한 판정·기억 기준·증거 수준 `개념 설명`·다음 검증을 구조화한다. 아티클의 전체 내용을 복제하지 않고 원문·판정·한계·링크만 기록한다.

### Task 4: 계층과 병합 결과를 검증하고 게시한다

**Files:**
- Verify: `AGENTS.md`
- Verify: `docs/learning-evidence/README.md`
- Verify: `docs/learning-roadmaps/ai-systems-study-roadmap.md`
- Verify: `docs/learning-roadmaps/agent-framework-study-roadmap.md`
- Verify: `docs/learning-evidence/2026-08-11-law-rag-roadmap-block-1-review.md`
- Verify: `docs/learning-evidence/2026-08-11-langgraph-langchain-code-reading.md`

**Interfaces:**
- Consumes: 변경된 규칙·로드맵·아티클·학습증거
- Produces: 원문 보존, 1차 소속, 링크와 Git 반영 결과

- [x] **Step 1: 분류와 원문 보존을 확인한다**

Run: `rg -n "학습 계획 위치|1차 소속|RAG 전체 경로|LangGraph.*실행 경로 코드 읽기|rag-assistant를 파보자" AGENTS.md docs/learning-evidence docs/learning-roadmaps docs/ai-agent-systems`

Expected: RAG와 LangGraph 증거는 각각 하나의 1차 위치를 가지며, LangGraph 첫 질문 원문은 새 학습증거에 존재한다.

- [x] **Step 2: 형식과 변경 범위를 확인한다**

Run: `git diff --check && git diff --name-only`

Expected: 공백 오류가 없고, 변경은 규칙·로드맵·관련 아티클·학습증거·설계·계획 문서에 한정된다.

- [ ] **Step 3: 커밋하고 푸시한다**

Run: `git add AGENTS.md docs/learning-evidence docs/learning-roadmaps docs/ai-agent-systems/agent-service-toolkit-langgraph-langchain-walkthrough.md docs/superpowers/specs/2026-08-12-learning-plan-evidence-hierarchy-design.md docs/superpowers/plans/2026-08-12-learning-plan-evidence-hierarchy.md && git commit -m "docs: organize learning plans and evidence" && git push origin main`

Expected: 로컬 `HEAD`와 `origin/main`이 같은 새 SHA를 가리킨다.
