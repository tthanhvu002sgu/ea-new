# DATA AUDIT — G3 — ID: YYYYMMDD-###

| Field | Value |
|-------|--------|
| Data file | |
| Symbol | |
| TF (raw → research) | |
| Status | PASS / FAIL |

## Checklist

- [ ] Timestamp timezone nhất quán với `constraints.yaml`
- [ ] Sorted, no duplicate bars
- [ ] Missing bars report gắn kèm (count / % / worst gaps)
- [ ] OHLC integrity (H≥L, H≥O,C, L≤O,C)
- [ ] No lookahead in feature pipeline (decision uses only ≤ bar[1] if close-based)
- [ ] Session filter defined in server time
- [ ] Spread model: fixed / session-varying / from data column
- [ ] Commission + swap assumptions documented
- [ ] Contract size / point / digits correct for symbol
- [ ] Weekend / holiday gaps handled
- [ ] Survivorship N/A or handled (multi-asset)
- [ ] Train/val/holdout boundaries không rò rỉ (purging/embargo nếu dùng CV)

## Leakage smoke tests

| Test | Result | Note |
|------|--------|------|
| Shift signal +1 bar → edge should drop | | |
| Future close in features? | YES=FAIL / NO | |
| Label shuffle → edge dies? | | |

## Summary

- Blockers:
- Residual risks:

**Decision:** PASS / FAIL  
**Signed:** _______________
