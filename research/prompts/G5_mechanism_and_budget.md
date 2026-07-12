# PROMPT — G5 (Mechanism test + limited discovery)

**Điều kiện:** G4 spec approved; prereg LOCKED; holdout vẫn sealed.

```text
[STAGE]: G5
[PREREG]: <path>
[BUDGET]: max_variants = N from prereg

Nhiệm vụ theo thứ tự:
1) Implement/run MECHANISM TEST only (từ prereg section 7).
2) Nếu mechanism FAIL → KILL. Dừng. Không build full strategy.
3) Nếu PASS → chạy tối đa N variants đã liệt kê sẵn (không thêm variant ad-hoc).
4) Báo cáo TẤT CẢ variants (kể cả xấu) theo results/_TEMPLATE_report.md
5) Lead with FAIL reasons.
6) Cấm: "cải thiện" bằng filter mới; cấm đụng holdout.

Nếu human nói "make it profitable": refuse; offer KILL or new card.
```
