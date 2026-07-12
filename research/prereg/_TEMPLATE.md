# PREREGISTRATION — ID: YYYYMMDD-###

| Field | Value |
|-------|--------|
| Card ID | |
| Status | DRAFT / LOCKED |
| Locked date | |
| Locked by | (human only) |

> Khóa file này **TRƯỚC** khi chạy backtest / optimizer.  
> Sau khi xem kết quả: **cấm** sửa kill floors để cứu strategy.

---

## 1. Hypothesis under test

(1 đoạn — copy claim từ card)

## 2. Data protocol

| Split | Start | End | Allowed use |
|-------|-------|-----|-------------|
| Discovery | | | mechanism + limited IS |
| Validation | | | robustness / WF |
| Holdout final | | | **sealed** until G7 sign-off |

- Bar type / TF:
- Session filter (fixed):
- Cost model ref: `constraints.yaml` → cost_model

## 3. Primary metric (đúng 1)

- Primary:
- Direction for PASS:

## 4. Secondary metrics (chẩn đoán only — không dùng để cứu)

-

## 5. Hard kill floors (copy/adjust from constraints, then LOCK)

| Floor | Value |
|-------|--------|
| min trades (discovery) | |
| min trades (validation) | |
| min primary metric after cost | |
| max DD % | |
| max top 5% trade profit share | |
| min positive subperiods (of 3) | |
| permutation: edge must die | YES |
| cost stress | 1.5× and 2.0× |

## 6. Trial budget

| Item | Limit |
|------|--------|
| Max variants this family | |
| Max free params | |
| Allowed param names | |
| Forbidden post-hoc filters | all not listed above |

Variants planned (liệt kê trước, không thêm sau):

1.
2.
3.

## 7. Mechanism test (chạy TRƯỚC full strategy)

| Test | Spec | Pass condition |
|------|------|----------------|
| Event / conditional return | | |
| Dose-response (nếu có) | | |
| Timing (no lookahead) | | |

## 8. Robustness battery (G6) — checklist

- [ ] Param sensitivity ±20% (hoặc neighbor grid thô)
- [ ] Time subperiods (3)
- [ ] Regime split (vol high/low hoặc trend/range proxy)
- [ ] Drop top 5% winners
- [ ] Entry delay +1 bar
- [ ] Cost ×1.5 / ×2
- [ ] Permutation / label shuffle

## 9. OOS rule

- [ ] One-shot validation — no tune
- [ ] Holdout final only after G6 PASS + human sign
- [ ] Fail OOS → KILL family (new card required)

## Human lock

**I lock this protocol before seeing results.**  
Signed: _______________ Date: _______________
