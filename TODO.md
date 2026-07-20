---
title: AI 에이전트 하니스 구현 TODO
description: Codex, Hermes, Orchestra를 실제 프로젝트에서 검증하기 위한 추적 가능한 작업 목록
status: active
version: 1.1.0
created: 2026-07-20
updated: 2026-07-20
owner: yjs000
related_document: docs/ai-agent-systems/harness-engineering-codex-hermes-orchestra.md
---

# AI 에이전트 하니스 구현 TODO

이 목록은 아티클의 제안을 구현과 측정으로 연결한다. 체크박스는 코드, 설정 또는 재현 가능한 검증 기록이 저장소에 남았을 때만 완료한다.

## 작업 기록 규약

모든 작업은 고유한 `task_id`를 가진다. 작업을 구현 저장소로 옮겨도 이 ID를 유지한다.

- `repository`: 변경 또는 증거가 저장될 저장소. 미정이면 `TBD`.
- `depends_on`: 먼저 완료할 작업 ID. 없으면 `none`.
- `deliverable`: 생성할 코드·문서·설정.
- `verification`: 실행할 명령 또는 검토 방법.
- `done`: 완료를 판정하는 조건.
- `evidence`: 완료 증거를 기록할 Wiki 경로.

## P0 — 기준선과 계약

- [ ] `[P0-BASELINE-001]` `law-rag`의 현재 하니스를 Stage 1~4 모델에 매핑한다.
  - `repository`: `yjs000/law-rag`
  - `depends_on`: `none`
  - `deliverable`: `AGENTS.md`, Roadmap, CI, 에이전트 운영 흐름의 현황표와 Mermaid 다이어그램
  - `verification`: 현재 기본 브랜치의 파일·workflow와 표의 각 항목을 대조 검토
  - `done`: 모든 항목이 `implemented / partial / proposed` 중 하나로 분류됨
  - `evidence`: `docs/evidence/P0-BASELINE-001.yml`
- [ ] `[P0-BENCHMARK-001]` 같은 작업을 Codex App, 공식 Codex CLI, Hermes에서 실행하는 비교 실험을 설계한다.
  - `repository`: `yjs000/wiki`
  - `depends_on`: `P0-BASELINE-001`
  - `deliverable`: 통제 변수, 과제 fixture, 측정 schema, 실행 절차
  - `verification`: 동일 커밋·프롬프트·모델·추론 설정·권한·검증 명령이 세 환경에 적용되는지 사전 점검
  - `done`: 완료율, 도구 오류, 재시도, 시간, 테스트, 사람 개입, diff 품질을 기록할 수 있음
  - `evidence`: `docs/evidence/P0-BENCHMARK-001.yml`
- [ ] `[P0-ISSUE-CONTRACT-001]` GitHub Issue 작업 계약 템플릿을 만든다.
  - `repository`: `yjs000/law-rag`
  - `depends_on`: `P0-BASELINE-001`
  - `deliverable`: 목표, 배경, 범위, 비범위, 수용 기준, 신뢰된 `verification_profile` 참조, 관련 파일, 위험을 포함한 Issue Form과 JSON Schema
  - `verification`: 필수 필드 누락, 길이 초과, 자유 형식 shell 명령, prompt injection 문자열, 승인 후 contract 편집 fixture
  - `done`: Issue가 실행 명령을 직접 제공하지 않고 허용된 data만 Agent 입력으로 전달되며, 승인 대상 전체의 contract hash 변경은 기존 승인을 무효화함
  - `evidence`: `docs/evidence/P0-ISSUE-CONTRACT-001.yml`
- [ ] `[P0-RELATED-PROJECTS-001]` 구현 프로젝트 연결 규약을 적용한다.
  - `repository`: `yjs000/wiki`
  - `depends_on`: `none`
  - `deliverable`: 아티클 front matter, 아래 `Related Projects`, 루트 README의 저장소 링크와 상태
  - `verification`: 구현 증거가 새로 생길 때마다 repository URL, commit 또는 PR, 검증 상태가 완료 증거와 일치하는지 확인
  - `done`: 현재 등록된 모든 프로젝트에서 증거가 있는 항목만 `implemented`, 나머지는 `partial / proposed / TODO`로 표시됨
  - `evidence`: `docs/evidence/P0-RELATED-PROJECTS-001.yml`

## P1 — 개인 개발자용 최소 하니스

- [ ] `[P1-ROADMAP-001]` Roadmap과 Exec Plan 규약을 적용한다.
  - `repository`: `yjs000/law-rag`
  - `depends_on`: `P0-BASELINE-001`
  - `deliverable`: `ROADMAP.md`, `docs/exec-plans/active/`, `docs/exec-plans/completed/` 규약
  - `verification`: 샘플 작업을 Pick up → 구현 → 완료 증거 이동까지 수행
  - `done`: 재시작한 Agent가 저장소만 읽고 현재 작업과 다음 행동을 찾을 수 있음
  - `evidence`: `docs/evidence/P1-ROADMAP-001.yml`
- [ ] `[P1-AGENTS-MAP-001]` `AGENTS.md`를 짧은 지도 형태로 정리한다.
  - `repository`: `yjs000/law-rag`
  - `depends_on`: `P1-ROADMAP-001`
  - `deliverable`: 핵심 계약과 상세 문서 링크만 남긴 `AGENTS.md`
  - `verification`: 모든 링크와 필수 진입점이 존재하는지 검사
  - `done`: 상세 지식은 `docs/`에 있고 중복·상충 지시가 제거됨
  - `evidence`: `docs/evidence/P1-AGENTS-MAP-001.yml`
- [ ] `[P1-DOC-CI-001]` 문서의 링크·메타데이터·오래된 계획을 검사하는 CI를 추가한다.
  - `repository`: `yjs000/law-rag`
  - `depends_on`: `P1-ROADMAP-001`, `P1-AGENTS-MAP-001`
  - `deliverable`: 문서 검사 스크립트와 GitHub Actions workflow
  - `verification`: 깨진 링크와 오래된 active plan fixture가 CI를 실패시키는지 확인
  - `done`: 정상 fixture는 통과하고 잘못된 fixture는 재현 가능하게 실패함
  - `evidence`: `docs/evidence/P1-DOC-CI-001.yml`
- [ ] `[P1-VERIFY-CONTRACT-001]` 저장소의 검증 명령을 한 곳에 정의한다.
  - `repository`: `yjs000/law-rag`
  - `depends_on`: `P0-BASELINE-001`
  - `deliverable`: 버전 관리되는 검증 profile, 고정 executable·argv runner, sandbox·egress 정책과 완료 증거 schema
  - `verification`: 깨끗한 clone의 정상 profile 실행과 shell operator·저장소 밖 접근·secret·network 거부 fixture
  - `done`: Agent와 CI가 승인된 revision의 같은 profile을 사용하고 Issue의 자유 형식 문자열은 실행되지 않으며 결과가 링크로 남음
  - `evidence`: `docs/evidence/P1-VERIFY-CONTRACT-001.yml`

## P2 — Hermes 승인 계층

- [ ] `[P2-REGISTRY-001]` 프로젝트 레지스트리 스키마를 정의한다.
  - `repository`: `TBD (Hermes approval bridge)`
  - `depends_on`: `P0-ISSUE-CONTRACT-001`
  - `deliverable`: `project_slug`, repository, branch, roadmap, issue policy를 포함한 schema와 validator
  - `verification`: 정상·누락·중복 slug fixture 검증
  - `done`: 잘못된 프로젝트 입력이 실행 전에 거부됨
  - `evidence`: `docs/evidence/P2-REGISTRY-001.yml`
- [ ] `[P2-DEDUP-001]` Roadmap, Issue, PR의 중복 확인 절차를 구현한다.
  - `repository`: `TBD (Hermes approval bridge)`
  - `depends_on`: `P2-REGISTRY-001`
  - `deliverable`: 제안 fingerprint와 중복 후보·근거 반환 로직
  - `verification`: 같은 목표의 Roadmap·Issue·PR fixture에서 중복을 탐지
  - `done`: 새 Issue 생성 전에 중복 후보와 신뢰 근거를 사용자에게 표시함
  - `evidence`: `docs/evidence/P2-DEDUP-001.yml`
- [ ] `[P2-APPROVAL-001]` Discord 제안 → 사용자 승인 → GitHub Issue 흐름을 구현한다.
  - `repository`: `TBD (Hermes approval bridge)`
  - `depends_on`: `P2-REGISTRY-001`, `P2-DEDUP-001`
  - `deliverable`: 인증된 actor·시각·canonical contract payload와 hash·만료·철회를 기록하는 append-only approval ledger, 승인 handler, Issue creator
  - `verification`: 승인·거절·만료·철회·재전송·인증되지 않은 actor 시나리오 실행
  - `done`: ledger만 승인 원본이며 Issue와 Hermes는 approval_id projection을 사용하고, 승인 후 계약을 갖춘 Issue가 정확히 하나 생성됨
  - `evidence`: `docs/evidence/P2-APPROVAL-001.yml`
- [ ] `[P2-IDEMPOTENCY-001]` 승인 재처리의 중복 Issue 생성을 막는다.
  - `repository`: `TBD (Hermes approval bridge)`
  - `depends_on`: `P2-APPROVAL-001`
  - `deliverable`: 승인 대상 전체 필드를 포함하는 canonical contract hash, 검색용 fingerprint, `(approval_id, contract_hash)` unique constraint, reservation·upsert와 crash recovery
  - `verification`: 범위·비범위·관련 파일·검증 profile·위험 변경, Unicode·null·배열 순서, 동시 승인 전달, 이벤트 재전송, Issue 생성 직후 프로세스 종료 fixture
  - `done`: 모든 재처리가 기존 reservation·Issue를 반환하고 중복 Issue를 만들지 않음
  - `evidence`: `docs/evidence/P2-IDEMPOTENCY-001.yml`
- [ ] `[P2-MESSAGE-HEADER-001]` 메시지에 프로젝트·Issue·상태 헤더를 고정한다.
  - `repository`: `TBD (Hermes approval bridge)`
  - `depends_on`: `P2-REGISTRY-001`
  - `deliverable`: 구조화된 Discord renderer와 snapshot test
  - `verification`: 프로젝트 전환·세션 재시작 fixture의 snapshot 비교
  - `done`: 모든 작업 메시지에서 프로젝트와 외부 작업 ID를 식별할 수 있음
  - `evidence`: `docs/evidence/P2-MESSAGE-HEADER-001.yml`
- [ ] `[P2-ROLE-HARNESS-001]` 제품·마케팅·운영을 역할별 하니스로 라우팅한다.
  - `repository`: `TBD (Hermes approval bridge)`
  - `depends_on`: `P2-REGISTRY-001`
  - `deliverable`: 역할별 prompt, 허용 도구, 평가 rubric, router
  - `verification`: 같은 요청을 역할별 fixture로 평가하고 잘못된 도구 접근을 거부
  - `done`: 각 역할의 출력이 해당 rubric과 권한 정책으로 독립 평가됨
  - `evidence`: `docs/evidence/P2-ROLE-HARNESS-001.yml`

## P3 — Orchestra 실행 계층 파일럿

- [ ] `[P3-PILOT-001]` Orchestra Agent와 Pipeline으로 제한된 파일럿을 만든다.
  - `repository`: `TBD (Orchestra pilot)`
  - `depends_on`: `P0-ISSUE-CONTRACT-001`
  - `deliverable`: 실패한 RAG 평가 분석 또는 작은 코드 수정 PR을 처리하는 Pipeline과 작업·저장소 한정 단기 credential 정책
  - `verification`: Agent Run의 Git 변경·PR·감사 로그 연결, 기본 branch push·merge·secret 조회·임의 egress 거부 확인
  - `done`: 같은 run ID로 입력·실행·PR·결과를 추적하고 Agent 자동화는 PR 생성에서 종료함
  - `evidence`: `docs/evidence/P3-PILOT-001.yml`
- [ ] `[P3-ISSUE-INPUT-001]` GitHub Issue를 Orchestra Pipeline input으로 변환한다.
  - `repository`: `TBD (Orchestra pilot)`
  - `depends_on`: `P3-PILOT-001`, `P2-APPROVAL-001`, `P2-IDEMPOTENCY-001`
  - `deliverable`: signature·delivery replay·repository·actor·label allowlist 검증과 Issue JSON Schema parser를 포함한 trigger adapter
  - `verification`: 유효·누락·비승인·위조 signature·replay·승인 후 편집 Issue fixture 실행
  - `done`: approval ledger의 contract hash와 일치하는 승인된 Issue만 Pipeline Run을 생성함
  - `evidence`: `docs/evidence/P3-ISSUE-INPUT-001.yml`
- [ ] `[P3-CORRELATION-001]` Issue, Pipeline Run, Agent Session, PR의 상관관계 ID를 정의한다.
  - `repository`: `TBD (Orchestra pilot)`
  - `depends_on`: `P3-ISSUE-INPUT-001`
  - `deliverable`: correlation schema와 로그·artifact 표준
  - `verification`: run ID에서 Issue와 PR을 양방향 조회
  - `done`: 어느 시스템에서 시작해도 관련 실행과 변경을 찾을 수 있음
  - `evidence`: `docs/evidence/P3-CORRELATION-001.yml`
- [ ] `[P3-RETRY-OWNERSHIP-001]` 계층별 재시도 책임을 구현한다.
  - `repository`: `TBD (Orchestra pilot)`
  - `depends_on`: `P3-PILOT-001`
  - `deliverable`: Pipeline·Agent·CI 실패 분류와 최대 재시도 정책
  - `verification`: infrastructure timeout, 테스트 실패, CI 실패 fixture
  - `done`: 한 실패를 둘 이상의 계층이 동시에 재시도하지 않고 무한 반복이 차단됨
  - `evidence`: `docs/evidence/P3-RETRY-OWNERSHIP-001.yml`
- [ ] `[P3-LAWRAG-DAG-001]` `law-rag` 데이터·평가·배포 흐름을 DAG로 모델링한다.
  - `repository`: `yjs000/law-rag`
  - `depends_on`: `P0-BASELINE-001`, `P3-PILOT-001`
  - `deliverable`: 수집 → 정규화 → 청킹 → 임베딩 → 검색 평가 → 배포 승인 Pipeline
  - `verification`: sample dataset으로 성공·회귀 실패·재시도 경로 실행
  - `done`: 각 task의 입력, 출력, 소유자, 실패 정책이 문서와 실행 정의에 일치함
  - `evidence`: `docs/evidence/P3-LAWRAG-DAG-001.yml`
- [ ] `[P3-COST-REVIEW-001]` Orchestra 도입 전후의 비용과 복구율을 비교한다.
  - `repository`: `yjs000/wiki`
  - `depends_on`: `P3-PILOT-001`, `P3-RETRY-OWNERSHIP-001`
  - `deliverable`: 운영 코드량, 장애 지점, 비용, 사람 개입, 복구율 비교 보고서
  - `verification`: 동일 기간 또는 동일 fixture의 before/after 데이터 검토
  - `done`: 확대·유지·제거 중 하나의 결정과 근거가 decision log에 기록됨
  - `evidence`: `docs/evidence/P3-COST-REVIEW-001.yml`

## P4 — 독립 검증과 운영

- [ ] `[P4-CI-GATE-001]` PR에 독립 검증 gate를 적용한다.
  - `repository`: `TBD (first implementation repo)`
  - `depends_on`: `P1-VERIFY-CONTRACT-001`
  - `deliverable`: full commit SHA로 고정한 action, 최소 권한, checkout credential 비유지를 적용한 lint·unit·integration·security·docs jobs
  - `verification`: 정상·검사 실패·fork PR fixture와 secret·OIDC·쓰기 권한 부재 확인
  - `done`: 필수 check가 모두 통과해야 병합 가능하고 신뢰하지 않는 PR 코드는 배포 credential에 접근할 수 없음
  - `evidence`: `docs/evidence/P4-CI-GATE-001.yml`
- [ ] `[P4-BRANCH-PROTECTION-001]` Agent가 우회할 수 없는 보호 브랜치 정책을 설정한다.
  - `repository`: `TBD (first implementation repo)`
  - `depends_on`: `P4-CI-GATE-001`
  - `deliverable`: branch protection 또는 ruleset 설정 기록
  - `verification`: 필수 check 미통과 PR의 병합 거부 확인
  - `done`: Agent credential로 기본 branch 직접 push와 gate 우회가 불가능함
  - `evidence`: `docs/evidence/P4-BRANCH-PROTECTION-001.yml`
- [ ] `[P4-CI-REPAIR-001]` CI 실패를 제한된 Agent 수정 입력으로 변환한다.
  - `repository`: `TBD (Orchestra pilot)`
  - `depends_on`: `P3-RETRY-OWNERSHIP-001`, `P4-CI-GATE-001`
  - `deliverable`: 실패 로그 normalizer, trusted verification profile의 command ID resolver, repair trigger, 반복 제한
  - `verification`: 비신뢰 로그·proposal의 shell 문자열이 runner 입력으로 승격되지 않고, 같은 실패가 최대 횟수 뒤 사람에게 escalation되는지 확인
  - `done`: Agent 입력에는 check URL과 `(verification_profile, immutable revision, command_id)`만 포함되고 무한 루프가 없음
  - `evidence`: `docs/evidence/P4-CI-REPAIR-001.yml`
- [ ] `[P4-FAILURE-TAXONOMY-001]` 실패를 공통 taxonomy로 기록한다.
  - `repository`: `TBD (shared schema)`
  - `depends_on`: `P3-CORRELATION-001`
  - `deliverable`: `provider / harness / tool / code / verification / orchestration / infrastructure`의 `primary_failure_class`와 `contributing_factors[]`, 관측 계층, 소유자, 재시도 가능 여부 schema
  - `verification`: 원인 사슬이 있는 과거·fixture 실패를 분류하고 동일 사건의 계층별 중복 재시도가 없는지 확인
  - `done`: 모든 실패 이벤트가 주 원인, 기여 요인, 소유 계층, retry owner, 다음 행동을 포함함
  - `evidence`: `docs/evidence/P4-FAILURE-TAXONOMY-001.yml`
- [ ] `[P4-METRICS-001]` 작업·복구 품질 지표를 기록한다.
  - `repository`: `TBD (observability)`
  - `depends_on`: `P3-CORRELATION-001`, `P4-FAILURE-TAXONOMY-001`
  - `deliverable`: 완료율, 사람 개입, 재시도, 평균 복구 시간, 회귀율 dashboard 또는 report
  - `verification`: sample runs의 원시 이벤트와 집계값 대조
  - `done`: 각 지표의 정의·분모·수집 주기와 원시 증거 링크가 있음
  - `evidence`: `docs/evidence/P4-METRICS-001.yml`
- [ ] `[P4-GC-001]` 문서·규약·중복 코드의 정기 가비지 컬렉션을 만든다.
  - `repository`: `TBD (first implementation repo)`
  - `depends_on`: `P1-DOC-CI-001`, `P4-METRICS-001`
  - `deliverable`: drift 검사, 정리 PR 생성, 품질 등급 갱신 작업
  - `verification`: 의도적으로 만든 오래된 문서와 중복 패턴을 탐지하는 fixture
  - `done`: 정기 실행 결과가 PR 또는 명시적인 no-change report로 남음
  - `evidence`: `docs/evidence/P4-GC-001.yml`

## Related Projects

| 프로젝트 | 연결 목적 | 현재 상태 | 증거 |
|---|---|---|---|
| [yjs000/law-rag](https://github.com/yjs000/law-rag) | RAG 개발·데이터·평가 하니스 사례 | 기존 프로젝트, 본 문서의 목표 구조 구현 여부는 `proposed` | `P0-BASELINE-001` 예정 |
| Hermes 승인·Issue 브리지 | 대화형 판단과 실행 계약 분리 | `TODO`, repository 미정 | `P2-APPROVAL-001` 예정 |
| Orchestra Agent Pipeline | 승인된 작업의 실행·관측 파일럿 | `TODO`, repository 미정 | `P3-PILOT-001` 예정 |
| Codex/Hermes 비교 하니스 | 동일 조건 성능 비교 | `TODO`, repository 미정 | `P0-BENCHMARK-001` 예정 |

## 완료 증거 규약

각 TODO를 완료할 때 실제 `task_id`와 저장소의 검증 증거를 기록한다.

```yaml
task_id: P2-APPROVAL-001
status: completed
repository: https://github.com/example/repository
commit: "<full commit SHA>"
evidence:
  tests:
    - command: "pytest tests/integration/test_approval_flow.py -q"
      result: passed
  pull_request: "https://github.com/example/repository/pull/123"
  run_url: "https://github.com/example/repository/actions/runs/123456"
verified_at: "YYYY-MM-DD"
limitations:
  - "실제 Orchestra 운영 계정에서는 아직 검증하지 않음"
```

`완료`는 아이디어 정리가 아니라 실제 산출물과 검증 증거가 연결된 상태를 뜻한다.
