# Research Skeleton — Cách dùng

Bạn là **Research Director**. AI chỉ làm việc theo stage.  
Playbook đầy đủ: `../quant_research_playbook.md`

## Thứ tự bắt buộc

```
0. Điền constraints.yaml          (bạn khóa)
1. Dán AI_CONSTITUTION.md         (mọi session)
2. G1: prompts/G1_research_card.md → cards/YYYYMMDD-###.md
3. Bạn chấm rubric G1 → PASS/KILL
4. G2: prompts/G2_preregister.md  → prereg/YYYYMMDD-###.md
5. G3: audits/ data audit
6. G4: prompts/G4_implementation_spec.md  (CHỈ sau G1–G3 PASS)
7. G5–G7: research code / tests  → results/YYYYMMDD-###/
8. Ghi decision_log.md
9. Chỉ khi PASS research mới viết EA MQL5 ở thư mục gốc
```

## Cấm

- Dùng `../prompt.md` (legacy) làm bước đầu tiên — xem `prompts/EVAL_prompt_md.md`
- Nhảy từ ý tưởng → optimizer Python → EA
- Tối ưu param trước khi mechanism test PASS
- Sửa OOS sau khi đã mở holdout

## Cấu trúc

```
research/
  AI_CONSTITUTION.md
  constraints.yaml
  decision_log.md
  cards/          # G1
  prereg/         # G2
  audits/         # G3
  results/        # G5–G9 reports
  prompts/        # prompt theo gate
```
