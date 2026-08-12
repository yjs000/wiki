# RAG Learning Evidence Consolidation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 초기 RAG 개념 게이트와 law-rag 1블록 점검을 하나의 최신 학습증거 흐름으로 통합한다.

**Architecture:** 8월 11일 문서를 기준 통합본으로 확장해 7월 22일의 학습자 원문과 핵심 정정을 포함한다. 7월 22일 문서는 삭제하지 않고, 통합본으로 연결하는 원문 보존 안내 문서로 축소한다.

**Tech Stack:** Markdown, Git, ripgrep

## Global Constraints

- 학습자가 직접 쓴 질문과 답변은 요약하거나 교정하지 않고 코드 블록으로 보존한다.
- 1블록의 기존 `부분 충족` 판정은 변경하지 않는다.
- law-rag 코드와 로드맵 문서는 변경하지 않는다.
- 7월 문서의 기존 URL은 유지한다.

---

### Task 1: 통합본에 초기 개념 게이트를 흡수한다

**Files:**
- Modify: `docs/learning-evidence/2026-08-11-law-rag-roadmap-block-1-review.md`

**Interfaces:**
- Consumes: `2026-07-22-rag-pipeline-concept-gate.md`의 초기 원문과 정정
- Produces: 초기 학습부터 최신 구현 판정까지 이어지는 기준 학습증거 문서

- [x] **Step 1: 초기 학습자 원문을 확인한다**

Run: `rg -n -A 96 "^## 학습자 원문" docs/learning-evidence/2026-07-22-rag-pipeline-concept-gate.md`

Expected: 단계별 첫 설명, 네 질문 답변, 이어진 질문의 원문 블록을 확인한다.

- [x] **Step 2: 통합본에 원문과 핵심 정정 절을 추가한다**

`학습자 재설명과 판정` 앞에 `초기 개념 게이트: 원문과 정정` 절을 넣는다. 원문 블록은 문자·오탈자·줄바꿈을 바꾸지 않는다. 피드백은 파싱/청크 구분, 청킹 목적, 임베딩의 한계, 질문 문자열과 벡터, 재시도, 기술 실패와 품질 실패, 메타데이터의 식별·검증 역할로 압축한다.

- [x] **Step 3: 통합본 탐색 요소를 갱신한다**

front matter의 `updated`를 `2026-08-12`로 유지하고, 목차에 새 상위 절을 추가한다. 참고 자료에서 7월 문서를 `통합 전 원본`으로 표시한다.

### Task 2: 7월 문서를 원문 보존 안내본으로 바꾼다

**Files:**
- Modify: `docs/learning-evidence/2026-07-22-rag-pipeline-concept-gate.md`

**Interfaces:**
- Consumes: 통합본 상대 링크 `2026-08-11-law-rag-roadmap-block-1-review.md`
- Produces: 기존 URL을 유지하면서 통합본으로 안내하는 짧은 문서

- [x] **Step 1: 문서의 역할을 안내문으로 교체한다**

제목과 설명에 `통합 안내`를 명시한다. 본문에는 이 문서의 학습자 원문과 정정이 통합본에 보존됐다는 사실, 통합본 링크, 원문을 삭제하지 않는 이유만 남긴다.

- [x] **Step 2: 날짜와 목차를 정리한다**

`updated`와 표시 날짜를 `2026-08-12`로 바꾸고, 불필요한 기존 목차는 제거한다.

### Task 3: 문서 통합을 검증하고 게시한다

**Files:**
- Verify: `docs/learning-evidence/2026-07-22-rag-pipeline-concept-gate.md`
- Verify: `docs/learning-evidence/2026-08-11-law-rag-roadmap-block-1-review.md`

**Interfaces:**
- Consumes: 통합된 Markdown 문서
- Produces: 링크·원문 보존·형식 검증 결과와 Git 커밋

- [x] **Step 1: 원문 보존과 링크를 확인한다**

Run: `rg -n "법령 원문|문서를 왜 청킹하는가|그러면 1항이 원문문서라면|2026-08-11-law-rag-roadmap-block-1-review" docs/learning-evidence/2026-07-22-rag-pipeline-concept-gate.md docs/learning-evidence/2026-08-11-law-rag-roadmap-block-1-review.md`

Expected: 세 종류의 초기 학습자 원문은 통합본에서, 통합 링크는 안내본에서 발견된다.

- [x] **Step 2: Markdown 변경을 확인한다**

Run: `git diff --check && git diff -- docs/learning-evidence/2026-07-22-rag-pipeline-concept-gate.md docs/learning-evidence/2026-08-11-law-rag-roadmap-block-1-review.md`

Expected: 공백 오류가 없고, 변경은 두 학습증거 문서와 계획 문서에만 한정된다.

- [x] **Step 3: 커밋하고 푸시한다**

Run: `git add docs/superpowers/plans/2026-08-12-rag-learning-evidence-consolidation.md docs/learning-evidence/2026-07-22-rag-pipeline-concept-gate.md docs/learning-evidence/2026-08-11-law-rag-roadmap-block-1-review.md && git commit -m "docs: consolidate rag learning evidence" && git push origin main`

Expected: 로컬 `HEAD`와 `origin/main`이 같은 새 커밋 SHA를 가리킨다.
