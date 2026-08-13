#!/usr/bin/env python3
"""Build low-cost question bank indexes for the yjs wiki.

This script intentionally avoids network and LLM calls. It reads only local
Markdown files, extracts compact evidence signals, and writes deterministic JSON.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
EVIDENCE_DIRS = [ROOT / "docs" / "learning-evidence", ROOT / "docs" / "learning-records"]
ROADMAP_PATH = ROOT / "docs" / "learning-roadmaps" / "ai-systems-study-roadmap.md"
OUT_DIR = ROOT / "docs" / "question-bank"
EVIDENCE_INDEX_PATH = OUT_DIR / "evidence-index.json"
QUESTION_BANK_PATH = OUT_DIR / "question-bank.json"

STAGES = [
    (1, "RAG 데이터 흐름", ["rag", "chunking", "embedding", "retrieval", "metadata", "citation"]),
    (2, "검색 알고리즘", ["keyword", "bm25", "vector", "hybrid", "rerank", "recall", "precision"]),
    (3, "모델 선택과 평가", ["model", "evaluation", "cost", "latency", "groundedness", "abstention"]),
    (4, "오픈소스 읽기와 축소 재구현", ["opensource", "entrypoint", "call-flow", "minimal-reimplementation"]),
    (5, "하네스 엔지니어링", ["harness", "context", "verification", "feedback-loop", "codex"]),
    (6, "단일 에이전트 런타임", ["agent-runtime", "tool-call", "state", "checkpoint", "retry"]),
    (7, "지속 실행 시스템", ["queue", "worker", "state-machine", "idempotency", "approval"]),
    (8, "멀티에이전트와 독립 설계", ["multi-agent", "orchestration", "framework-comparison", "system-design"]),
]

QUESTION_SEEDS = [
    # stage 1
    ("rag.chunking.boundary.001", 1, "chunking", "법령 검색에서 조문 단위 청킹은 고정 길이 청킹보다 어떤 질문에서 유리한가?", "comparison", ["independent_chunking_experiment"], 3),
    ("rag.embedding.vector-use.001", 1, "embedding", "질문 벡터는 어디까지 쓰이고 모델 프롬프트에는 무엇이 들어가는가?", "concept", ["independent_embedding_experiment"], 3),
    ("rag.retrieval.generation-split.001", 1, "retrieval", "검색은 성공했는데 답변이 틀리는 경우는 어떤 패턴인가?", "failure", ["retrieval_generation_separate_eval"], 2),
    ("rag.metadata.citation.001", 1, "metadata", "조문 번호와 제목 메타데이터는 계층 표현보다 어떤 검증 문제를 해결하는가?", "concept", ["metadata_for_citation"], 3),
    ("rag.context.prompt.001", 1, "context", "검색된 청크는 어떤 순서와 형식으로 프롬프트에 들어갈 때 근거가 덜 왜곡되는가?", "application", ["project_code_test_evidence"], 2),
    # stage 2
    ("search.keyword-vs-vector.001", 2, "search", "조문 번호가 포함된 질문은 BM25와 벡터 검색 중 어디서 더 잘 잡히는가?", "comparison", ["bm25_vector_same_dataset"], 3),
    ("search.semantic.001", 2, "search", "일상어 질문은 벡터 검색이 실제 근거 조문을 top-3 안에 넣는가?", "experiment", ["vector_search_eval"], 3),
    ("search.hybrid.001", 2, "hybrid-search", "하이브리드 검색은 단순 순위 결합만으로 현재 질문셋에서 좋아지는가?", "experiment", ["hybrid_search_eval"], 2),
    ("search.metric.recall.001", 2, "metrics", "recall@k가 높아졌는데 답변 품질이 그대로일 수 있는 이유는 무엇인가?", "concept", ["recall_at_k_calculation"], 2),
    ("search.reranker.need.001", 2, "reranking", "리랭커는 현재 law-rag 질문셋에서 필요한가, 아니면 과한 복잡도인가?", "decision", ["reranker_comparison"], 1),
    # stage 3
    ("model.groundedness.001", 3, "model-eval", "같은 검색 문맥을 줬을 때 모델별로 근거 밖 내용을 만드는 비율은 다른가?", "comparison", ["model_groundedness_eval"], 3),
    ("model.abstention.001", 3, "model-eval", "답이 없는 질문에서 모델은 거부를 잘하는가, 아니면 그럴듯한 답을 만드는가?", "failure", ["abstention_eval"], 3),
    ("model.cost-role.001", 3, "model-routing", "저비용 모델은 최종 답변보다 질문 분류나 요약에 더 적합한가?", "decision", ["cost_latency_quality_eval"], 2),
    ("model.korean-quality.001", 3, "model-eval", "한국어 법령 설명 품질과 근거 충실도는 같은 지표인가?", "concept", ["korean_quality_eval"], 2),
    ("model.selection.001", 3, "model-selection", "비용·지연·품질을 같이 보면 어떤 모델 조합이 현재 law-rag에 맞는가?", "decision", ["model_selection_document"], 2),
    # stage 4
    ("oss.entrypoint.001", 4, "open-source-reading", "이 저장소에서 사용자 입력은 실제로 어느 함수로 들어오는가?", "code-reading", ["entrypoint_trace"], 3),
    ("oss.readme-vs-code.001", 4, "open-source-reading", "README의 아키텍처 설명과 실제 호출 흐름은 일치하는가?", "comparison", ["readme_code_comparison"], 2),
    ("oss.state-flow.001", 4, "open-source-reading", "설정 로딩, 상태 생성, 모델 호출, 결과 파싱은 어떤 파일에서 나뉘는가?", "code-reading", ["call_flow_trace"], 3),
    ("oss.abstraction-cost.001", 4, "open-source-reading", "원본 구현이 추가한 추상화는 어떤 실패나 확장 요구를 해결하는가?", "decision", ["minimal_reimplementation"], 2),
    ("oss.minimal-rebuild.001", 4, "open-source-reading", "같은 기능을 100줄 이하로 줄이면 무엇이 사라지고 무엇이 남는가?", "experiment", ["minimal_reimplementation"], 2),
    # stage 5
    ("harness.context.001", 5, "harness", "Codex에게 보여 줄 컨텍스트를 줄이면 어떤 실패가 늘고 어떤 비용이 줄어드는가?", "experiment", ["harness_context_experiment"], 3),
    ("harness.verification.001", 5, "harness", "완료 조건을 테스트 명령으로 고정하면 부분 성공 보고가 줄어드는가?", "experiment", ["verification_loop_evidence"], 3),
    ("harness.failure-feedback.001", 5, "harness", "실패 로그를 다음 시도에 넘길 때 어떤 정보가 재시도 품질을 바꾸는가?", "failure", ["failure_feedback_loop"], 2),
    ("harness.approval.001", 5, "harness", "사람 승인이 필요한 경계는 파일 변경, 배포, 데이터 변경 중 어디에 둬야 하는가?", "decision", ["approval_boundary_evidence"], 2),
    # stage 6
    ("runtime.tool-call-loop.001", 6, "agent-runtime", "최소 에이전트 루프에서 모델의 툴 호출은 어떤 메시지 상태를 거쳐 재호출되는가?", "concept", ["minimal_tool_loop"], 3),
    ("runtime.state.001", 6, "agent-runtime", "상태를 메모리에만 두는 루프는 재시작 때 어떤 정보를 잃는가?", "failure", ["state_persistence_experiment"], 3),
    ("runtime.retry.001", 6, "agent-runtime", "재시도 가능한 실패와 중단해야 하는 실패는 최소 루프에서 어떻게 구분하는가?", "decision", ["retry_boundary_experiment"], 2),
    # stage 7
    ("durable.queue.001", 7, "durable-execution", "Discord나 GitHub 이벤트를 작업 큐에 넣을 때 중복 이벤트는 어떻게 막는가?", "concept", ["queue_idempotency_experiment"], 3),
    ("durable.worker-restart.001", 7, "durable-execution", "워커가 중단돼도 작업 상태가 사라지지 않으려면 어떤 체크포인트가 필요한가?", "experiment", ["worker_restart_experiment"], 3),
    ("durable.approval.001", 7, "durable-execution", "승인 전 외부 반영을 막으려면 상태 머신의 어느 전이가 잠겨야 하는가?", "decision", ["approval_state_machine"], 2),
    # stage 8
    ("multiagent.parallel-vs-role.001", 8, "multi-agent", "멀티에이전트 구조가 실제 병렬 실행인지 프롬프트 역할 분담인지 어떻게 구분하는가?", "comparison", ["multiagent_execution_trace"], 3),
    ("design.framework-choice.001", 8, "system-design", "요구사항 하나를 받았을 때 프레임워크 도입과 직접 구현의 경계는 어떻게 결정하는가?", "decision", ["framework_choice_comparison"], 3),
]

@dataclass
class EvidenceEntry:
    evidence_id: str
    path: str
    title: str
    stage_order: int
    stage: str
    topics: list[str]
    evidence_level: str
    passed: list[str]
    partial: list[str]
    missing: list[str]
    next_questions: list[str]
    source_hash: str


def sha256(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def parse_frontmatter(text: str) -> dict[str, Any]:
    if not text.startswith("---\n"):
        return {}
    end = text.find("\n---\n", 4)
    if end == -1:
        return {}
    raw = text[4:end]
    meta: dict[str, Any] = {}
    for line in raw.splitlines():
        if ":" not in line:
            continue
        key, val = line.split(":", 1)
        val = val.strip().strip('"')
        if val.startswith("[") and val.endswith("]"):
            meta[key.strip()] = [x.strip().strip('"\'') for x in val[1:-1].split(",") if x.strip()]
        else:
            meta[key.strip()] = val
    return meta


def slugify(value: str) -> str:
    value = value.lower()
    value = re.sub(r"[^a-z0-9가-힣]+", "-", value).strip("-")
    return value or "untitled"


def extract_section(text: str, heading: str) -> str:
    pattern = re.compile(rf"^##+\s+{re.escape(heading)}\s*$", re.MULTILINE)
    m = pattern.search(text)
    if not m:
        return ""
    start = m.end()
    next_h = re.search(r"^##\s+", text[start:], re.MULTILINE)
    end = start + next_h.start() if next_h else len(text)
    return text[start:end].strip()


def bullets_from(section: str) -> list[str]:
    values = []
    for line in section.splitlines():
        stripped = line.strip()
        if stripped.startswith("- "):
            values.append(re.sub(r"\s+", " ", stripped[2:]).strip())
    return values


def infer_stage_and_topics(meta: dict[str, Any], text: str) -> tuple[int, str, list[str]]:
    tags = [str(t).lower() for t in meta.get("tags", [])]
    hay = (" ".join(tags) + "\n" + text[:4000]).lower()
    scores: list[tuple[int, int, str, list[str]]] = []
    for order, stage, keywords in STAGES:
        score = sum(1 for kw in keywords if kw.lower() in hay)
        scores.append((score, order, stage, keywords))
    score, order, stage, keywords = sorted(scores, key=lambda x: (-x[0], x[1]))[0]
    topics = sorted({kw for kw in keywords if kw.lower() in hay} | set(tags))[:12]
    return order, stage, topics


def infer_evidence_level(text: str) -> str:
    level_line = ""
    for line in text.splitlines():
        if "**현재 증거 수준:**" in line:
            level_line = line
            break
    target = level_line or text
    if "프로젝트 적용" in target:
        return "project_application"
    if "독립 실험" in target or "실제 출력" in target or "실행 명령" in target:
        return "independent_experiment"
    return "concept_explanation"


def normalize_key(text: str) -> str:
    mapping = {
        "임베딩": "embedding_compares_question_and_chunks",
        "검색과 답변": "retrieval_generation_separate_eval",
        "검색 결과와 모델 답변": "retrieval_generation_separate_eval",
        "청킹": "chunking_purpose",
        "조문 번호": "metadata_for_citation",
        "메타데이터": "metadata_for_citation",
        "독립 실행 청킹": "independent_chunking_experiment",
        "독립 청킹": "independent_chunking_experiment",
        "독립 실행 임베딩": "independent_embedding_experiment",
        "독립 임베딩": "independent_embedding_experiment",
        "독립 실행 검색": "independent_retrieval_experiment",
        "독립 검색": "independent_retrieval_experiment",
        "프로젝트 코드": "project_code_test_evidence",
        "프로젝트 적용": "project_code_test_evidence",
    }
    for needle, key in mapping.items():
        if needle in text:
            return key
    return slugify(re.sub(r"\*\*|`", "", text))[:80]


def extract_questions(section: str) -> list[str]:
    questions: list[str] = []
    for line in section.splitlines():
        s = line.strip().lstrip("- ").strip()
        if not s:
            continue
        if "?" in s or "가?" in s or "까?" in s or s.endswith("인가") or s.endswith("하는가"):
            questions.append(s)
    return questions[:10]


def build_evidence_entry(path: Path) -> EvidenceEntry:
    text = read_text(path)
    meta = parse_frontmatter(text)
    h1 = re.search(r"^#\s+(.+)$", text, re.MULTILINE)
    title = str(meta.get("title") or (h1.group(1) if h1 else path.stem))
    stage_order, stage, topics = infer_stage_and_topics(meta, text)
    evidence_level = infer_evidence_level(text)

    context = extract_section(text, "학습 맥락")
    current = extract_section(text, "현재 판정") or extract_section(text, "판정")
    missed = extract_section(text, "놓친 부분과 정정")
    next_verification = extract_section(text, "다음 검증")

    passed: set[str] = set()
    partial: set[str] = set()
    missing: set[str] = set()

    for line in current.splitlines():
        stripped = line.strip()
        if not stripped.startswith("|") or "---" in stripped or "질문" in stripped or "판정" in stripped:
            continue
        cells = [c.strip() for c in stripped.strip("|").split("|")]
        if len(cells) < 2:
            continue
        key = normalize_key(cells[0])
        verdict = cells[1]
        if "부분" in verdict:
            partial.add(key)
        elif "이해" in verdict or "정확" in verdict or "통과" in verdict:
            passed.add(key)
        elif "미흡" in verdict or "부족" in verdict:
            missing.add(key)
    for b in bullets_from(context):
        if "아직 없는 증거" in b or "없는 증거" in b:
            for phrase in ["독립 실행 청킹", "독립 실행 임베딩", "독립 실행 검색", "프로젝트 코드", "프로젝트 적용"]:
                if phrase in b:
                    missing.add(normalize_key(phrase))
            if not missing:
                missing.add(normalize_key(b))
    for b in bullets_from(next_verification):
        missing.add(normalize_key(b))

    next_questions: list[str] = []
    for heading in ["다음 검증", "이어 생긴 질문"]:
        next_questions.extend(extract_questions(extract_section(text, heading)))
    if not next_questions:
        next_questions = extract_questions(next_verification + "\n" + missed)

    return EvidenceEntry(
        evidence_id=path.stem,
        path=str(path.relative_to(ROOT)),
        title=title,
        stage_order=stage_order,
        stage=stage,
        topics=topics,
        evidence_level=evidence_level,
        passed=sorted(passed),
        partial=sorted(partial),
        missing=sorted(missing),
        next_questions=next_questions[:10],
        source_hash=sha256(text),
    )


def build_question_bank(evidence: list[EvidenceEntry]) -> list[dict[str, Any]]:
    passed = {k for e in evidence for k in e.passed}
    partial = {k for e in evidence for k in e.partial}
    missing = {k for e in evidence for k in e.missing}
    questions: list[dict[str, Any]] = []
    for qid, stage_order, topic, question, qtype, requires, base_weight in QUESTION_SEEDS:
        covered_by = [e.evidence_id for e in evidence if any(req in e.passed for req in requires)]
        partial_by = [e.evidence_id for e in evidence if any(req in e.partial for req in requires)]
        missing_hits = [req for req in requires if req in missing or req not in passed]
        if covered_by and not partial_by:
            status = "passed"
            weight = 0
        elif partial_by or any(req in partial for req in requires):
            status = "partial"
            weight = base_weight + 1
        else:
            status = "uncovered"
            weight = base_weight + 2 if missing_hits else base_weight
        axis = next(stage for order, stage, _ in STAGES if order == stage_order)
        questions.append({
            "id": qid,
            "stage_order": stage_order,
            "axis": axis,
            "topic": topic,
            "question": question,
            "type": qtype,
            "status": status,
            "requires": requires,
            "covered_by": covered_by,
            "partial_by": partial_by,
            "blocked_by": [],
            "weight": weight,
        })
    return questions


def write_json_if_changed(path: Path, data: Any) -> bool:
    path.parent.mkdir(parents=True, exist_ok=True)
    text = json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    if path.exists() and path.read_text(encoding="utf-8") == text:
        return False
    path.write_text(text, encoding="utf-8")
    return True


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--changed-only", action="store_true", help="Reserved for future diff-scoped LLM enrichment; deterministic build still writes full compact index.")
    args = parser.parse_args()

    evidence_files = []
    for evidence_dir in EVIDENCE_DIRS:
        if evidence_dir.exists():
            evidence_files.extend(p for p in evidence_dir.rglob("*.md") if p.name != "README.md")
    evidence_files = sorted(set(evidence_files))
    evidence = [build_evidence_entry(path) for path in evidence_files]
    questions = build_question_bank(evidence)
    generated_at = "deterministic"
    evidence_payload = {
        "schema_version": 1,
        "generated_at": generated_at,
        "source": "tools/question_bank/build_question_bank.py",
        "items": [asdict(e) for e in evidence],
    }
    question_payload = {
        "schema_version": 1,
        "generated_at": generated_at,
        "selection_policy": "Sort by stage_order ascending, filter non-passed, take top 3 by weight within earliest stage, choose random.",
        "items": questions,
    }
    changed = False
    changed |= write_json_if_changed(EVIDENCE_INDEX_PATH, evidence_payload)
    changed |= write_json_if_changed(QUESTION_BANK_PATH, question_payload)
    print(json.dumps({
        "changed": changed,
        "evidence_count": len(evidence),
        "question_count": len(questions),
        "non_passed_count": sum(1 for q in questions if q["status"] != "passed"),
        "paths": [str(EVIDENCE_INDEX_PATH.relative_to(ROOT)), str(QUESTION_BANK_PATH.relative_to(ROOT))],
    }, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
