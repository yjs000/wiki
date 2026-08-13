# 질문뱅크

학습계획의 큰 범위를 세션 단위 질문으로 쪼개고, 실습·검증 기록에 이미 있는 증거를 제외해 다음 질문을 고르기 위한 저비용 색인입니다.

## 파일

- `evidence-index.json`: `docs/learning-evidence/*.md`와 `docs/learning-records/**/*.md`에서 추출한 판정용 요약 색인입니다. 원문 보존용이 아니라 질문 선택용입니다.
- `question-bank.json`: 로드맵 축별 질문 후보와 상태입니다.
- `question-history.jsonl`: 실제로 뽑은 질문 기록입니다.

## 갱신

```bash
python tools/question_bank/build_question_bank.py
```

현재 MVP는 LLM을 쓰지 않고 Markdown의 frontmatter, 제목, 판정, 다음 검증 절을 기반으로 결정론적 JSON을 만듭니다. 이후 필요한 경우 바뀐 문서 조각만 LLM으로 보강합니다.

## 질문 뽑기

```bash
python tools/question_bank/pick_question.py
```

선택 규칙:

1. `status != passed` 질문만 남깁니다.
2. `blocked_by`가 없는 질문만 남깁니다.
3. 가장 앞 `stage_order` 그룹을 고릅니다.
4. 그 안에서 `weight` 기준 상위 3개를 고릅니다.
5. 상위 3개 중 랜덤으로 하나를 선택합니다.
6. `question-history.jsonl`에 기록합니다.
