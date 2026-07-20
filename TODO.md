---
title: AI 에이전트 하니스 구현 TODO
description: Codex, Hermes, Orchestra를 실제 프로젝트에서 검증하기 위한 작업 목록
status: active
version: 1.0.0
created: 2026-07-20
updated: 2026-07-20
owner: yjs000
related_document: docs/ai-agent-systems/harness-engineering-codex-hermes-orchestra.md
---

# AI 에이전트 하니스 구현 TODO

이 목록은 아티클의 제안을 구현과 측정으로 연결한다. 체크박스는 코드, 설정 또는 재현 가능한 검증 기록이 저장소에 남았을 때만 완료한다.

## P0 — 기준선과 계약

- [ ] `law-rag`의 현재 `AGENTS.md`, `ROADMAP`, CI, 에이전트 운영 흐름을 문서의 Stage 1~4 모델에 매핑한다.
  - 산출물: 아키텍처 현황표와 Mermaid 다이어그램
  - 관련 저장소: <https://github.com/yjs000/law-rag>
  - 완료 조건: 현재 구현과 목표 구조를 `implemented / partial / proposed`로 구분
- [ ] 같은 작업을 Codex App, 공식 Codex CLI, Hermes에서 각각 실행하는 비교 실험을 설계한다.
  - 통제 변수: 동일 커밋, 프롬프트, 모델, 추론 설정, 권한, 검증 명령
  - 측정값: 완료율, 도구 오류, 재시도, 소요 시간, 테스트 결과, diff 품질
  - 완료 조건: 원시 로그와 결과표를 공개 가능한 형태로 저장
- [ ] GitHub Issue 작업 계약 템플릿을 만든다.
  - 필수 필드: 목표, 배경, 범위, 비범위, 수용 기준, 검증 명령, 관련 파일, 위험
  - 완료 조건: Issue Form 또는 Markdown 템플릿과 샘플 Issue 작성

## P1 — 개인 개발자용 최소 하니스

- [ ] `ROADMAP.md`와 `docs/exec-plans/` 규약을 실제 사이드프로젝트에 적용한다.
- [ ] `AGENTS.md`를 짧은 지도 형태로 정리하고 상세 지식은 `docs/`로 분리한다.
- [ ] 문서 링크, 메타데이터, 오래된 계획을 검사하는 CI를 추가한다.
- [ ] 완료 선언 전에 실행할 검증 명령을 저장소별로 한 곳에 정의한다.

## P2 — Hermes 승인 계층

- [ ] 프로젝트 레지스트리 스키마를 정의한다.
  - 필드: `project_slug`, `repository`, `default_branch`, `roadmap_path`, `issue_policy`
- [ ] Hermes가 기존 Roadmap, Issue, PR과 중복을 확인하는 절차를 구현한다.
- [ ] Discord에서 제안 → 사용자 승인 → GitHub Issue 생성 흐름을 구현한다.
- [ ] 중복 Issue를 막는 `approval_id`와 `issue_fingerprint`를 저장한다.
- [ ] 메시지마다 프로젝트, Issue, 상태를 구조화된 헤더로 표시한다.
- [ ] 제품, 마케팅, 운영 작업에 각각 다른 프롬프트·평가 기준을 적용하는 라우팅 실험을 한다.

## P3 — Orchestra 실행 계층 파일럿

- [ ] Orchestra Runtime의 Agent와 Pipeline 기능으로 제한된 파일럿을 만든다.
  - 첫 범위: 실패한 RAG 평가 결과 분석 또는 작은 코드 수정 PR
  - 완료 조건: Agent Run, Git 변경, PR, 감사 로그를 한 실행 ID로 추적
- [ ] GitHub Issue 입력을 Orchestra Pipeline input으로 변환한다.
- [ ] Pipeline Run, Agent Session, GitHub Issue, PR의 상관관계 ID 규약을 정의한다.
- [ ] 재시도 책임을 구분한다.
  - Orchestra: 파이프라인·인프라 재시도
  - 코딩 에이전트: 코드 수정 반복
  - GitHub Actions: 독립 검증
- [ ] `law-rag`의 수집 → 정규화 → 청킹 → 임베딩 → 검색 평가 → 배포 승인 흐름을 DAG로 모델링한다.
- [ ] Orchestra 도입 전후 운영 코드, 장애 지점, 비용, 복구율을 비교한다.

## P4 — 독립 검증과 운영

- [ ] PR마다 lint, unit, integration, security, docs 검사를 실행한다.
- [ ] 에이전트가 바꿀 수 없는 보호 브랜치와 필수 체크를 설정한다.
- [ ] CI 실패를 에이전트 입력으로 변환하되, 동일 실패의 무한 반복을 제한한다.
- [ ] 실패 원인을 `provider / harness / tool / code / test / infrastructure`로 분류한다.
- [ ] 작업 완료율, 사람 개입 횟수, 재시도 횟수, 평균 복구 시간, 회귀율을 기록한다.
- [ ] 정기적인 문서·규약·중복 코드 가비지 컬렉션 작업을 만든다.

## Related implementations

| 프로젝트 | 연결 목적 | 현재 상태 |
|---|---|---|
| [yjs000/law-rag](https://github.com/yjs000/law-rag) | RAG 개발·데이터·평가 하니스 사례 | 기존 프로젝트, 본 문서의 목표 구조 구현 여부는 검증 예정 |
| Hermes 승인·Issue 브리지 | 대화형 판단과 실행 계약 분리 | TODO |
| Orchestra Agent Pipeline | 승인된 작업의 실행·관측 파일럿 | TODO |
| Codex/Hermes 비교 하니스 | 동일 조건 성능 비교 | TODO |

## 완료 증거 규약

각 TODO를 완료할 때 다음 정보를 함께 기록한다.

```yaml
task_id: P2-hermes-approval-flow
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
