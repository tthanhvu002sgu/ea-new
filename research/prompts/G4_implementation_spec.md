# PROMPT — G4 (Implementation Spec / đặc tả kỹ thuật)

**Điều kiện:** G1 PASS + G2 LOCKED + G3 data audit PASS.  


```text
[STAGE]: G4 only
[CARD + PREREG + AUDIT]: <paste or paths>
[CONSTRAINTS]: <paste>

Yêu cầu:
1. Tuyệt đối không viết code Python/MQL5 — chỉ công thức + pseudocode.
2. Anti look-ahead: signal chỉ dùng info available tại decision time (bar[1] close-based nếu close system).
3. Chỉ dùng free params đã liệt kê trong prereg; không mở rộng grid.
4. Simple: không thêm indicator ngoài card.
5. Gắn cost model từ constraints.

Cấu trúc output:

#### A. Signal (minimal — khớp card section 6)
#### B. Entry logic (long/short) — boolean explicit, bar index rõ
#### C. Exit & risk — SL/TP/time exit; sizing từ constraints
#### D. Friction filters — max spread, vol filter NẾU đã preregistered
#### E. Logging fields per trade (reason codes, spread, MAE/MFE)
#### F. Forbidden in code list

Cấm:
- Thêm "confluence" mới
- Đề xuất optimizer ranges rộng hơn prereg
- Đổi universe/session
- Claim "expected Sharpe > X" — metrics đã khóa ở G2

Cuối: 1–2 câu hỏi về execution reality (fill, stop level), KHÔNG hỏi để nới risk nhằm làm đẹp backtest.
```
