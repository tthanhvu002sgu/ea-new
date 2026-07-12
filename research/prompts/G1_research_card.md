# PROMPT — G1 ONLY (Research Card)

**Dán kèm:** `AI_CONSTITUTION.md` + nội dung `constraints.yaml` (status LOCKED).

```text
[STAGE]: G1 only
[CONSTRAINTS]: <paste constraints.yaml>
[OUTPUT FILE FORMAT]: research/cards/_TEMPLATE.md

Nhiệm vụ:
- KHÔNG thiết kế full strategy (không entry/exit/SL/TP chi tiết, không parameter grid, không robustness benchmark số).
- KHÔNG viết code.
- CHỈ điền Research Card theo template.
- Nếu không có: falsifiable claim + counterparty + lý do chưa arb + ≥3 falsifiers + minimal signal
  → SELF-KILL, giải thích ngắn, đề xuất family khác CHỈ nếu còn budget.

Cấm:
- Name-drop (Ernie Chan, Lo, de Prado, Kaufman...) thay cho mechanism đo được
- Multi-indicator confluence làm "ý tưởng"
- Đề xuất symbol/TF ngoài constraints
- Grid search space
- Martingale / grid

Sau card: đặt đúng 2 câu hỏi cho human về (1) falsifier nào human chấp nhận (2) capacity kỳ vọng.
```
