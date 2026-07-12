# RESEARCH CARD — ID: YYYYMMDD-###

| Field | Value |
|-------|--------|
| Status | DRAFT / SUBMITTED / PASS / KILL |
| Author | AI / Human hybrid |
| Date | |
| Constraints file | `research/constraints.yaml` (must be LOCKED) |
| Style | momentum / MR / breakout / session / event |
| Symbols | (must ⊆ constraints) |
| Timeframe | (must ⊆ constraints) |

---

## 1. Claim (1 câu, falsifiable)

> Nếu **X** xảy ra, thì kỳ vọng return của action **A** trong horizon **H** là dương **sau chi phí**, vì mechanism **M**.

Claim:

## 2. Economic mechanism — ai trả tiền?

| Câu hỏi | Trả lời |
|---------|---------|
| Nguồn edge | behavioral / structural / institutional / risk-premium / info-lag / constraint |
| Counterparty thua là ai? | |
| Vì sao họ chấp nhận thua? | forced / uninformed / constrained / risk transfer |
| Vì sao edge chưa bị arb hết? | capacity / complexity / holding cost / mandate / latency / regulation |
| Capacity ước tính trước khi decay | |

**KILL nếu** không chỉ ra được counterparty + lý do chưa arb.

## 3. Causal chain (mỗi mũi tên phải đo được)

```
Cause → Intermediate → Price impact path → Tradeable signal → PnL
```

| Bước | Biến đo | Hướng kỳ vọng | Horizon | Khi nào gãy |
|------|---------|---------------|---------|-------------|
| 1 | | | | |
| 2 | | | | |
| 3 | | | | |

## 4. Falsifiers (≥ 3 — true thì chết, không vá)

- F1:
- F2:
- F3:

## 5. Non-goals (cấm scope creep)

Không làm:

## 6. Minimal viable signal (1–2 rule lõi)

Pseudo-code ≤ 5 dòng:

```
// signal only — chưa phải full EA
```

Free params (≤ max_free_params trong constraints):

| Param | Role | Range thô (không grid lớn) |
|-------|------|----------------------------|
| | | |

## 7. Decay & monitoring

- Kỳ vọng half-life edge:
- Live kill signal (không phải chờ account cháy):

## 8. Prior / literature (optional, không thay mechanism)

- Đã biết:
- Giả định mới:
- **Cấm** list tên tác giả thay cho test

## 9. Human rubric (bạn chấm 0–2; PASS ≥ 10/12 và không mục = 0)

| Mục | Score 0–2 | Note |
|-----|-----------|------|
| Claim falsifiable | | |
| Ai trả tiền | | |
| Vì sao chưa arb | | |
| Causal chain | | |
| Falsifiers | | |
| Minimal signal | | |
| **Total** | /12 | |

**Decision:** PASS / KILL / REWORK  
**Signed:** _______________ **Date:** _______________
