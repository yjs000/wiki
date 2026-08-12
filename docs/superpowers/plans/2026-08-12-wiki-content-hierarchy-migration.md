# Wiki Content Hierarchy Migration Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Wiki 콘텐츠를 학습계획, 학습기록, 읽을거리, 관련 프로젝트의 README 중심 계층으로 재배치한다.

**Architecture:** 새 콘텐츠 경로는 `docs/learning-plans/`, `docs/learning-records/`, `docs/readings/`, `docs/projects/`로 고정한다. 각 계층의 README는 바로 아래 항목만 인덱싱하며, 이전 경로는 외부 링크를 깨지 않도록 새 위치를 가리키는 안내 문서로 남긴다.

**Tech Stack:** Markdown, Git, ripgrep

## Global Constraints

- 루트 README와 영향받는 모든 계층 README는 같은 변경에서 함께 갱신한다.
- 학습목표는 `docs/learning-plans/README.md`에 흡수하고, `TODO.md`는 안내 문서로만 남긴다.
- 학습증거는 `학습계획 주제 → 증거` 경로에 한 번만 둔다.
- 읽을거리와 학습증거는 분리한다. 읽은 뒤의 질문·판정은 학습기록에 둔다.
- 기존 공유 URL의 콘텐츠를 삭제하지 않고 새 위치 링크가 있는 안내 문서로 바꾼다.

---

### Task 1: 새 최상위 콘텐츠 인덱스를 만든다

**Files:**
- Modify: `README.md`
- Create: `docs/learning-plans/README.md`
- Create: `docs/learning-records/README.md`
- Create: `docs/readings/README.md`
- Create: `docs/projects/README.md`

- [x] **Step 1: 루트 README를 네 영역 인덱스로 바꾼다**

`학습계획`, `학습기록`, `읽을거리`, `관련 프로젝트`의 README 링크만 남기고 개별 아티클·증거 링크는 하위 README로 옮긴다.

- [x] **Step 2: 네 최상위 README를 작성한다**

학습계획 README에는 현재 학습목표와 주제별 계획을, 학습기록 README에는 계획 주제별 기록을, 읽을거리 README에는 주제별 아티클을, 프로젝트 README에는 실제 프로젝트와 관계를 둔다.

### Task 2: 학습계획과 목표를 주제별 README로 이동한다

**Files:**
- Move: `docs/learning-roadmaps/ai-systems-study-roadmap.md` → `docs/learning-plans/rag-system/README.md`
- Move: `docs/learning-roadmaps/agent-framework-study-roadmap.md` → `docs/learning-plans/agent-framework/README.md`
- Modify: `TODO.md`
- Create: legacy redirects under `docs/learning-roadmaps/`

- [x] **Step 1: 두 로드맵을 주제 README로 이동하고 상대 링크를 갱신한다**

RAG 시스템과 에이전트 프레임워크 계획은 각각 주제 README가 된다. 학습증거·읽을거리 링크를 새 상대 경로로 고친다.

- [x] **Step 2: 학습목표를 학습계획 README에 흡수한다**

TODO의 여섯 목표를 학습계획 README에 보존하고 주제 README와 연결한다. TODO는 새 인덱스로 이동하는 안내만 둔다.

- [x] **Step 3: 이전 로드맵 URL을 안내 문서로 보존한다**

기존 파일명마다 새 주제 README로 연결하는 짧은 안내 문서를 남긴다.

### Task 3: 학습기록과 읽을거리를 주제별로 이동한다

**Files:**
- Move RAG evidence into `docs/learning-records/rag-system/`
- Move LangGraph evidence into `docs/learning-records/agent-framework/`
- Move foundation article into `docs/readings/ai-foundations/`
- Move agent articles into `docs/readings/agent-systems/`
- Create README indexes at each subject directory
- Create legacy redirects under old content directories

- [x] **Step 1: 학습기록을 계획 주제별 증거 폴더로 이동한다**

RAG 증거는 `learning-records/rag-system/`, LangGraph 증거는 `learning-records/agent-framework/`에 둔다. 해당 주제 README는 증거 목록과 계획 README 링크를 가진다.

- [x] **Step 2: 읽을거리를 주제별 폴더로 이동한다**

임베딩 글은 `readings/ai-foundations/`, 하네스·LangGraph 글은 `readings/agent-systems/`에 둔다. 각 주제 README는 아티클 목록과 관련 학습계획·기록 링크를 가진다.

- [x] **Step 3: 이전 학습증거·읽을거리 URL을 안내 문서로 보존한다**

기존 파일은 새 위치를 링크하는 안내 문서로 바꾸고, 기존 학습자 원문은 새 학습기록의 원문에만 유지한다.

### Task 4: 규칙과 링크를 새 계층에 맞춘다

**Files:**
- Modify: `AGENTS.md`
- Modify: legacy and moved documents with relative links

- [x] **Step 1: AGENTS.md의 저장소 지도와 자동 분류 규칙을 새 경로로 바꾼다**

새 목표·아티클·증거를 배치할 정확한 경로와 `루트 README + 영향받는 모든 계층 README` 동시 갱신 의무를 명시한다.

- [x] **Step 2: 모든 이동 문서의 상대 링크를 새 경로로 갱신한다**

계획·기록·읽을거리·프로젝트 사이 링크가 새 계층을 가리키도록 수정한다.

### Task 5: 구조와 URL 보존을 검증하고 게시한다

**Files:**
- Verify: `README.md`, all new README files, all legacy redirects

- [x] **Step 1: 새 계층과 README 인덱스를 확인한다**

Run: `rg --files -g README.md docs; rg -n "학습계획|학습기록|읽을거리|관련 프로젝트" README.md docs/learning-plans/README.md docs/learning-records/README.md docs/readings/README.md docs/projects/README.md`

Expected: 루트와 네 최상위 영역, 각 주제의 README가 존재한다.

- [x] **Step 2: 새 문서와 이전 URL의 링크를 확인한다**

Run: PowerShell relative-link validation for every Markdown file under `README.md`, `TODO.md`, and `docs/`.

Expected: 모든 내부 Markdown 링크가 존재하는 파일을 가리킨다.

- [x] **Step 3: 변경 범위와 형식을 확인하고 커밋·푸시한다**

Run: `git diff --check && git status -sb && git add -A && git commit -m "docs: restructure wiki content hierarchy" && git push origin main`

Expected: 새 구조, 이전 URL 안내, README 인덱스가 한 커밋에 반영되고 로컬 `HEAD`와 `origin/main`이 일치한다.
