# QUANT RESEARCH PLAYBOOK
## Quy trình kiểm soát có chủ đích — Edge thật, không edge kể chuyện

> Mục tiêu: Bạn **không** là người “sáng tạo ý tưởng đẹp”.  
> Bạn là **Research Director**: đặt ràng buộc, phê duyệt gate, ra quyết định kill/continue.  
> AI là **laborer có hiến pháp**: chỉ được làm việc trong khuôn khổ đã khóa.

---

## 0. Chẩn đoán: vì sao loop “ý tưởng hay → code → backtest” gần như luôn fail

### 0.1 Anti-pattern hiện tại

```
Model kể story hay
    → Code nhanh
    → Backtest đẹp (hoặc “gần đẹp” sau vài tweak)
    → Bạn tin
    → Live/forward fail
```

Loop này **tối ưu hóa khả năng thuyết phục**, không tối ưu hóa **edge kinh tế có thể triển khai**.

### 0.2 8 nguyên nhân gốc (xếp theo mức độ phổ biến với AI)

| # | Nguyên nhân | Dấu hiệu điển hình |
|---|-------------|-------------------|
| 1 | **Narrative fallacy** | Story “nghe có lý” nhưng không chỉ ra được *ai trả tiền* và *vì sao edge không bị arbitrage hết* |
| 2 | **Data mining / multiple testing** | Thử nhiều filter, TF, threshold; chỉ giữ cái đẹp |
| 3 | **Overfit tham số** | Equity đẹp trong 1 window; đổi 1 param là sụp |
| 4 | **Lookahead / leakage** | Dùng close của nến hiện tại, news đã biết, label tương lai lọt vào feature |
| 5 | **Chi phí ảo** | Bỏ qua spread/slippage/commission/swap; winrate 52% trên EURUSD M5 “có lãi” |
| 6 | **Non-stationarity** | Edge chỉ tồn tại 1 regime (2020–2021, COVID, 1 chu kỳ rate) |
| 7 | **Sample quá mỏng** | 40–80 trade, Sharpe “cao” nhưng không có statistical power |
| 8 | **Không có causal claim kiểm chứng được** | Chỉ có correlation + chart đẹp + jargon (mean reversion, microstructure, “smart money”) |

### 0.3 Luật vàng duy nhất

> **Không có backtest đẹp nào là bằng chứng.**  
> Backtest chỉ là **điều kiện cần yếu**.  
> Edge chỉ được coi là ứng viên khi vượt **chuỗi gate kill** bên dưới, theo thứ tự cố định.

---

## 1. Phân vai — bạn điều phối, AI lao động

### 1.1 Vai của bạn (Human Orchestrator)

Bạn **chỉ** làm 6 việc:

1. **Khóa universe & constraint** (symbol, TF, style, capital, max hold, max DD, cost model).
2. **Phê duyệt Research Card** (Gate 0–1) trước khi cho code.
3. **Khóa protocol test** (split data, metrics, kill criteria) **trước** khi xem kết quả.
4. **Ra quyết định binary** ở mỗi gate: PASS / KILL / REWORK (có giới hạn lần rework).
5. **Cấm “tweak cho đến khi đẹp”** sau khi đã thấy holdout.
6. **Ghi nhật ký quyết định** (decision log) — cái gì kill, vì sao.

Bạn **không**:

- Nhờ AI “cho vài ý tưởng hay”.
- Tự sửa param sau khi thấy OOS xấu để “cứu” strategy.
- Đánh giá bằng cảm xúc “nghe có lý / equity curve mượt”.

### 1.2 Vai của AI (Constrained Worker)

AI được phép:

- Viết hypothesis theo template bắt buộc.
- Viết code **đúng spec đã khóa**.
- Chạy test **đúng protocol đã khóa**.
- Báo cáo theo format kill-first (nêu lý do fail trước).
- Đề xuất *experiment tiếp theo* chỉ trong scope đã duyệt.

AI **bị cấm**:

- Bắt đầu từ “strategy idea” mà không có economic mechanism.
- Tối ưu param trên full sample.
- “Cải thiện” strategy sau khi đã peek holdout (trừ khi reset protocol + holdout mới).
- Dùng ngôn ngữ marketing: “robust”, “strong edge”, “highly profitable” khi chưa qua gate.
- Gộp nhiều ý tưởng thành 1 strategy để cứu performance.

### 1.3 Quyền lực kill

| Ai | Quyền |
|----|--------|
| Bạn | Kill bất kỳ lúc nào, không cần giải thích dài |
| AI | **Bắt buộc self-kill** nếu vi phạm rule trong hiến pháp (mục 5) |
| Metrics | Kill tự động nếu chạm hard floor (mục 3) |

**Default = KILL.** PASS phải được *chứng minh*, không được *cảm nhận*.

---

## 2. Pipeline cố định (không được đảo thứ tự)

```
G0  Constraint Lock
G1  Causal Hypothesis Card          ← kill 70–80% idea AI ở đây
G2  Pre-registration / Test Protocol
G3  Data Integrity Audit
G4  Implementation Spec (code contract)
G5  In-Sample Discovery (limited)
G6  Robustness Battery
G7  Out-of-Sample / Walk-Forward (blind)
G8  Cost & Friction Stress
G9  Economic Plausibility Review
G10 Paper / Shadow Live
G11 Small Live Cap → Scale rules
```

**Cấm nhảy cóc.** Đặc biệt cấm: G1 → G5 (code + backtest) bỏ qua G2–G4.

---

## 3. Chi tiết từng Gate

### G0 — Constraint Lock (bạn khóa 1 lần / project)

Trước mọi ý tưởng, khóa file `constraints.yaml` (hoặc bảng cố định):

```yaml
market:            # e.g. XAUUSD, EURUSD
venue:             # MT5 broker class, futures, etc.
timeframe:         # e.g. M15, H1
session:           # London/NY/Asia or full
style:             # trend | MR | breakout | event | carry | arb
max_holding:       # bars or hours
capital_base:      # USD
max_risk_per_trade: # % 
max_daily_dd:      # %
max_total_dd:      # %
cost_model:
  spread_pips: 
  slippage_pips:     # pessimistic baseline
  commission_per_lot:
  swap: true/false
min_trades_required: # e.g. 200 for daily-ish; scale with frequency
data_range:
  discovery:         # e.g. 2018-01 → 2023-06
  validation:        # e.g. 2023-07 → 2024-12
  holdout_final:     # e.g. 2025-01 → 2026-06  (SEALED)
forbidden:
  - optimize_on_holdout
  - change_cost_after_seeing_results
  - add_filters_after_OOS
```

**Rule:** Holdout final **không được mở** cho đến G7. AI không được “nhìn lén”.

---

### G1 — Causal Hypothesis Card (KILL GATE quan trọng nhất)

Mọi ứng viên **bắt buộc** điền đủ card sau. Thiếu 1 mục = KILL.

```markdown
# RESEARCH CARD — ID: YYYYMMDD-###

## 1. Claim (1 câu, falsifiable)
"Nếu X xảy ra, thì kỳ vọng return của action A trong horizon H là dương,
sau chi phí, vì mechanism M."

## 2. Economic mechanism (ai trả tiền?)
- Nguồn edge: behavioral / structural / institutional / risk-premium / information lag / constraint
- Ai là counterparty thua? Vì sao họ chấp nhận thua (forced, uninformed, constrained, risk transfer)?
- Vì sao edge chưa bị arbitrage hết? (capacity, complexity, holding cost, mandate, latency, regulation)

## 3. Causal chain (nguyên nhân → kết quả)
Cause → measurable intermediate → price impact path → tradeable signal → PnL
Mỗi mũi tên phải chỉ ra:
  - biến đo được
  - hướng kỳ vọng
  - horizon thời gian
  - điều kiện fail (khi nào chain gãy)

## 4. Falsifiers (điều kiện bác bỏ — bắt buộc ≥ 3)
F1: ...
F2: ...
F3: ...
Nếu bất kỳ F true → strategy chết, không được “sửa cho qua”.

## 5. Non-goals (cấm scope creep)
Không làm: multi-TF stack, ML ensemble, 10 filter “cải thiện”, martingale, grid...

## 6. Minimal viable signal
Signal đơn giản nhất có thể test mechanism (không phải strategy đầy đủ).
Chỉ 1–2 rule lõi. Entry logic ≤ 5 dòng pseudo-code.

## 7. Capacity & decay expectations
- AUM ước tính trước khi edge chết
- Tần suất trade
- Kỳ vọng half-life của edge (tháng/năm) và lý do

## 8. Prior literature / known facts
Cái gì đã biết? Cái gì là giả định mới? Tránh reinvent indicator soup.
```

#### Rubric chấm G1 (bạn chấm, 0–2 điểm mỗi mục; PASS ≥ 10/12 và không mục nào = 0)

| Mục | 0 | 1 | 2 |
|-----|---|---|---|
| Claim falsifiable | mơ hồ | khá rõ | đo được, có horizon |
| Ai trả tiền | không nói | nói chung chung | chỉ rõ actor + incentive |
| Vì sao chưa arb hết | im lặng | 1 lý do yếu | lý do structural/credible |
| Causal chain | correlation only | chain lỏng | chain đo được từng bước |
| Falsifiers | không có / soft | có nhưng mơ hồ | cứng, quan sát được |
| Minimal signal | strategy phức tạp | hơi gọn | cực gọn, test được mechanism |

**Heuristic kill ngay:**

- Dùng từ: “smart money”, “institutional flow”, “AI pattern”, “hidden order block” mà không map ra data cụ thể.
- Mechanism = “thị trường hay retest” / “trend tiếp diễn” mà không có *vì sao kỳ này khác random*.
- Cần ≥ 4 filter / ≥ 6 param để “ý tưởng có nghĩa”.
- Không chỉ ra được **counterparty**.

---

### G2 — Pre-registration (khóa trước khi chạy)

Trước khi AI chạy bất kỳ backtest nào, khóa:

1. **Primary metric** (chỉ 1): ví dụ deflated Sharpe, hoặc expectancy sau cost / maxDD.
2. **Secondary metrics** (chỉ để chẩn đoán, không để “cứu”): winrate, PF, avg trade, time underwater...
3. **Hard kill floors** (ví dụ — chỉnh theo style của bạn):

```text
AFTER COST:
- trades >= N_min
- avg trade (R or $) > 0 với CI không chứa 0 ở mức đã chọn (hoặc bootstrap p)
- maxDD <= limit
- performance không phụ thuộc 1 năm / 5% trade lớn nhất (top trades contribution < X%)
- param sensitivity: ±20% param chính không đảo dấu expectancy
```

4. **Số lần thử được phép** trong discovery (budget).  
   Ví dụ: tối đa 5 biến thể signal trong 1 family. Hết budget → KILL family.
5. **Cấm chỉ tiêu vanity**: equity mượt, winrate cao, “đẹp mắt”.

Ghi vào `preregistered.md`. **Sau khi xem kết quả, không được sửa floors để strategy sống.**

---

### G3 — Data Integrity Audit

Checklist bắt buộc trước code strategy:

- [ ] Timestamp timezone nhất quán
- [ ] Không lookahead (signal chỉ dùng info available at decision time)
- [ ] Xử lý gap/weekend/holiday đúng
- [ ] Spread/commission model khớp broker class
- [ ] Với FX/CFD: digs, contract size, margin không ảo
- [ ] Survivorship (nếu multi-asset): universe điểm-in-time
- [ ] Corporate actions (nếu stock)
- [ ] Duplicate bars / missing bars report
- [ ] Session filter không vô tình bias

AI phải xuất `data_audit_report.md`. Fail audit = không vào G5.

---

### G4 — Implementation Spec (code contract)

Trước khi code, AI viết spec ngắn:

```text
Inputs:
Decision time:
Signal definition (exact):
Entry rule:
Exit rule (SL/TP/time/signal flip):
Position sizing:
Costs applied when:
State variables:
What is FORBIDDEN in code:
Logging fields per trade:
```

**Rule code:**

1. Signal research tách khỏi execution (module riêng).
2. Mọi random seed cố định.
3. Không hard-code magic number không nằm trong preregistered param list.
4. Mỗi trade log: entry reason code, exit reason code, spread at entry, MAE/MFE.
5. Unit test nhỏ cho lookahead (shift test): nếu shift signal +1 bar mà PnL tương tự → nghi ngờ leakage.

---

### G5 — In-Sample Discovery (có ngân sách)

Mục tiêu G5 **không** phải “tìm strategy lãi”.  
Mục tiêu: **kiểm tra mechanism có dấu hiệu sống không**.

Thứ tự bắt buộc:

1. **Mechanism test trước strategy test**  
   - Ví dụ: conditional mean return sau event X có khác 0 không?  
   - Distributional shift?  
   - Có monotonicity theo strength của X không?
2. Chỉ khi mechanism test PASS mới build full entry/exit.
3. Param search **hẹp**, grid thô, budget cố định.
4. Báo cáo phải có:  
   - số hypothesis đã thử  
   - cái fail  
   - không chỉ cái đẹp nhất

**Kill nếu:**

- Mechanism test fail nhưng full strategy (nhiều filter) lại “win” → gần như chắc overfit.
- Cần stack filter mới ra lãi.
- Edge chỉ từ 1 cụm trade / 1 news regime.

---

### G6 — Robustness Battery (trước khi mở holdout)

Chạy **cùng protocol**, không cherry-pick:

| Test | Pass condition (ví dụ) |
|------|------------------------|
| Parameter sensitivity | Neighborhood không sụp |
| Time split stability | ≥ 2/3 subperiods expectancy > 0 sau cost |
| Regime split | Không phụ thuộc đúng 1 regime hiếm |
| Symbol/TF neighbor (nếu claim general) | Không yêu cầu identical, nhưng không đảo dấu hoàn toàn nếu mechanism chung |
| Trade subset | Bỏ top 5% winner → vẫn không phá sản thesis |
| Latency stress | Delay entry 1 bar: edge giảm có lý, không nổ ngược |
| Cost stress | 1.5×–2× cost model: vẫn không chết ngay (hoặc chết có giải thích capacity) |
| Bootstrap / permutation | Label shuffle → “edge” biến mất (nếu shuffle vẫn đẹp = bug/leak) |

**Permutation/shuffle test là bắt buộc** với AI-generated strategies.

---

### G7 — Blind OOS / Walk-Forward

- Mở validation theo preregister.
- **Một lần.** Không tune.
- Walk-forward: re-optimize chỉ param được phép, trên window trượt, rule cố định.
- Holdout final: chỉ mở khi G6 pass và bạn ký duyệt.

**Kill nếu OOS gãy** — kể cả IS đẹp.  
**Cấm:** thêm filter “chỉ 1 cái” sau OOS. Đó là overfit stage 2.

Nếu muốn iterate:  
→ tạo Research Card mới, holdout mới (hoặc extend data future), budget mới.  
Không được “vá” strategy cũ trên cùng holdout.

---

### G8 — Cost & Friction Reality

Map về môi trường thật (MT5 broker của bạn):

- Spread theo session (London open ≠ Asia)
- Slippage theo volatility
- Commission + swap
- Stop-level / freeze level
- Requote / partial fill assumptions (nếu relevant)
- Turn over: cost per year vs gross edge

**Rule:**  
`net_edge ≈ gross_edge - costs - adverse_selection - ops_error`  
Nếu gross edge mỏng hơn 2–3× cost baseline → KILL (không đủ margin of safety).

---

### G9 — Economic Plausibility Review (bạn chấm, qualitative)

Hỏi lại 5 câu — trả lời “không rõ” = KILL:

1. Ai trả tiền cho edge này mỗi năm?
2. Nếu 50 quỹ cùng trade, edge còn không?
3. Edge phụ thuộc data mining hay mechanism?
4. Có chỉ số trung gian (intermediate) xác nhận chain không? (không chỉ PnL)
5. Khi edge chết, bạn **biết** bằng tín hiệu nào (monitoring), không phải đợi account cháy?

---

### G10 — Paper / Shadow Live

- Chạy song song market, **không** tin paper có fill hoàn hảo.
- So sánh: signal rate, spread paid, slip, skip rate, PnL vs backtest expectation band.
- Tracking error ngoài band → dừng, điều tra (không “tối ưu live”).

Minimum shadow period: đủ để đạt ~30–50% `min_trades_required` hoặc 1–3 tháng (chọn cái dài hơn theo tần suất).

---

### G11 — Small Live → Scale

- Size nhỏ, risk cap cứng.
- Promotion rule viết trước:  
  sau N trade live, nếu expectancy CI / DD / slip trong band → tăng size 1 nấc.  
- Kill rule live viết trước:  
  DD, slip blowout, regime flag, edge monitor break.

---

## 4. Nhận diện sớm: “ý tưởng nghe hay → sẽ fail thực tế”

### 4.1 Red-flag ngôn ngữ (AI output)

| Nghe hay | Thực chất thường là |
|----------|---------------------|
| “Kết hợp price action + volume + structure” | Indicator soup, không mechanism |
| “Dựa trên hành vi tổ chức” | Không có proxy đo được |
| “Multi-timeframe confluence” | Degrees of freedom tăng, overfit |
| “Tự tối ưu param tốt nhất” | Fit noise |
| “Winrate 70%+” | Thường RR tệ hoặc sample bias |
| “Hoạt động mọi thị trường mọi TF” | Claim quá mạnh, gần như chắc sai |
| “ML tìm pattern ẩn” | Pure data mining nếu không có feature causal |
| “Martingale/grid recovery” | Không phải edge, là phân phối ruin |
| “Backtest 10 năm profit mượt” | Có thể cost ảo + overfit + non-tradeable |

### 4.2 Red-flag số liệu

- Trades < 100–200 (tùy frequency) mà Sharpe “đẹp”
- >30% profit đến từ <5% số trade
- 1 năm đóng góp phần lớn total profit
- IS>>OOS một cách thảm họa
- Expectancy ~ 0.1 × spread
- Equity curve quá mượt so với strategy type (đặc biệt mean-reversion grid)
- Đổi session/cost nhẹ là strategy chết → fragile
- Signal rate không ổn định theo năm

### 4.3 Red-flag quy trình (bạn tự bắt mình)

- Bạn yêu cầu AI “cải thiện kết quả” sau khi xem chart
- Bạn chấp nhận thêm filter vì “logic cũng hay”
- Bạn chưa khóa cost đã nhìn profit
- Bạn so sánh 20 strategy rồi chỉ report con đẹp (selection bias)
- Bạn không ghi số lần thử

### 4.4 Test “fail-fast” 15 phút (trước khi tốn ngày code)

Cho AI / tự làm nhanh:

1. **Mechanism one-pager** — không viết được counterparty → stop.
2. **Naive baseline**: buy&hold / always-long-session / random entry same holding — strategy có thắng baseline sau cost không?
3. **Cost ×2** mental math: còn edge không?
4. **Param count**: >5 free params → nghi ngờ nặng.
5. **Tradability**: quyết định có thể execute được ở TF/venue đã chọn với latency thực không?

---

## 5. HIẾN PHÁP AI (System rules — paste vào mọi session)

Sao chép block dưới làm system prompt / project rule:

```text
You are a quantitative research laborer, not a pitch deck writer.

MISSION
- Help the human test economic hypotheses under a fixed protocol.
- Default outcome is KILL. PASS must be earned by evidence.
- Never optimize for "sounding smart" or pretty equity curves.

HARD BANS
1. Do not propose strategies without: falsifiable claim, counterparty, mechanism, falsifiers.
2. Do not code before Research Card + preregistration are approved.
3. Do not optimize on full sample or on holdout.
4. Do not add filters/params after seeing OOS results.
5. Do not use martingale, grid recovery, or unbounded risk as "edge".
6. Do not claim robustness without listing tests run AND failed.
7. Do not hide the number of trials / variants attempted.
8. Do not use marketing language (holy grail, strong edge, institutional-grade) without gate evidence.
9. Do not treat correlation, chart patterns, or indicator confluence as causation.
10. If data integrity is uncertain, stop and audit — do not backtest.

REQUIRED ORDER OF WORK
G0 constraints → G1 card → G2 preregister → G3 data audit → G4 spec →
G5 mechanism test then limited IS → G6 robustness → G7 blind OOS →
G8 costs → G9 economics → G10 shadow → G11 small live.

OUTPUT STYLE
- Lead with FAIL reasons.
- Separate: facts / assumptions / unknown.
- Quantify: sample size, costs, sensitivity, trial budget used.
- When uncertain, say what evidence would kill or save the idea.
- Prefer simplest test of the mechanism over complex strategy code.

IF HUMAN ASKS TO "MAKE IT PROFITABLE"
- Refuse parameter hacking.
- Offer: new Research Card, new trial budget, or explicit kill.
```

### 5.1 Prompt templates (bạn dùng khi điều phối)

#### A) Mở session nghiên cứu

```text
[CONSTRAINTS]: <paste constraints>
[STAGE]: G1 only
Nhiệm vụ: Không đưa strategy hoàn chỉnh. Chỉ viết Research Card theo template.
Nếu không có mechanism + counterparty đủ mạnh → self-kill và giải thích.
```

#### B) Sau khi bạn PASS card

```text
[CARD APPROVED]: <id>
[STAGE]: G2–G4
Viết preregistration + data audit checklist + code contract.
Chưa được backtest. Chưa được tối ưu param.
```

#### C) Khi vào test

```text
[STAGE]: G5
Chỉ chạy mechanism test đã preregister.
Budget: tối đa K variants.
Báo cáo tất cả variants (kể cả fail).
Cấm đề xuất filter mới ngoài card.
```

#### D) Khi AI muốn “cải thiện”

```text
Dừng. Đây là request tối ưu sau khi có kết quả — bị cấm.
Chỉ được: (1) KILL, (2) REWORK với card mới + budget mới, (3) audit bug/leakage.
```

---

## 6. Decision Log (bạn bắt buộc ghi)

File `decision_log.md`:

```markdown
| Date | ID | Gate | Decision | Why | Trials used | Next |
|------|----|------|----------|-----|-------------|------|
| 2026-07-11 | 001 | G1 | KILL | no counterparty | 0 | - |
| 2026-07-11 | 002 | G6 | KILL | fails cost×2 + 1 regime only | 4 | new card |
```

Mục đích: chống tự lừa, đo tỷ lệ kill, học pattern fail của AI.

**KPI quy trình (không phải KPI profit):**

- % kill ở G1 (càng cao càng tốt lúc đầu — filter rác)
- % pass G1 mà fail G6/G7 (bắt overfit)
- Số lần vi phạm protocol (mục tiêu → 0)
- Không KPI: số strategy “đẹp”, winrate cảm tính

---

## 7. Map vào workflow hiện tại của bạn (MT5 + strategy_analyzer)

Bạn đang có vòng: backtest MT5 → `strategy_analyzer.py`.  
Đó mới là **phần đuôi** (sau G5–G8). Thiếu phần đầu nên “hầu hết đều fail”.

### 7.1 Tách 2 repo tư duy

| Tầng | Công cụ | Câu hỏi |
|------|---------|---------|
| Research | Python/notebook, event study, simple bars | Mechanism có tồn tại không? |
| Execution BT | MT5 Strategy Tester | Implement được không, cost/fill ra sao? |
| Diagnostics | `strategy_analyzer` | Phân bố trade, MC, weak points? |

**Cấm:** nhảy thẳng viết EA MQL5 cho mọi ý tưởng AI.  
Chỉ viết EA khi G1–G6 (research-level) đã PASS.

### 7.2 Dùng strategy_analyzer đúng vai

Analyzer trả lời: “kết quả backtest này có đặc điểm gì / rủi ro thống kê nào?”  
Analyzer **không** trả lời: “strategy có edge thật không?”

Bổ sung checklist khi đọc analyzer:

- [ ] Đã trừ cost pessimistic?
- [ ] Top trades dependency?
- [ ] Stability theo năm?
- [ ] Sample size đủ?
- [ ] Có log reason code không?
- [ ] Đã qua permutation/leakage test ở tầng research chưa?

### 7.3 Promotion criteria (từ analyzer → shadow)

Chỉ shadow live khi:

1. Card + preregister tồn tại  
2. Research robustness pass  
3. MT5 BT với cost model khớp broker  
4. Analyzer không flag: single-regime, tiny sample, top-trade concentration  
5. Bạn ký G9  

---

## 8. Nguyên tắc “nguyên nhân – kết quả” (operational)

### 8.1 Causal claim phải có 3 lớp bằng chứng

1. **Theoretical/economic**: incentive + constraint  
2. **Statistical predictive**: X → future return (đúng horizon, đúng timing)  
3. **Intermediate confirmation**: X → microstructure/vol/positioning proxy → return  

Chỉ có (2) = correlation trading → dễ chết.  
Có (1)+(2)+(3) = ứng viên edge.

### 8.2 Phân biệt 3 loại “edge” giả

| Loại | Mô tả | Kết cục |
|------|-------|---------|
| Statistical mirage | Fit noise, p-hacking | OOS chết |
| Transfer of luck | Bắt 1 regime lịch sử | Regime đổi là chết |
| Untradeable premium | Có trên paper, không qua cost/capacity | Live chết |

### 8.3 Câu hỏi nhân-quả bắt buộc mỗi strategy

1. **Intervention**: Nếu tôi *không* trade khi X, tôi mất edge không? (counterfactual)
2. **Timing**: X có *trước* price move đủ để vào lệnh không?
3. **Dose-response**: X mạnh hơn → edge lớn hơn chứ không random?
4. **Disable condition**: Điều kiện nào tắt mechanism?
5. **Competing explanation**: Random + selection có giải thích kết quả không?

---

## 9. Ngân sách nghiên cứu (để không nghiên cứu đến chết)

### 9.1 Time box

| Phase | Time box gợi ý |
|-------|----------------|
| G1 card | 30–60 phút |
| G2–G4 | 1–3 giờ |
| G5 mechanism | 0.5–2 ngày |
| G6–G7 | 1–3 ngày |
| EA + MT5 | chỉ sau pass trên |

Nếu G1 không PASS trong 60 phút → KILL, không “cố nhào nặn story”.

### 9.2 Trial budget

- Mỗi family hypothesis: tối đa **5** variants  
- Mỗi tháng: tối đa **N** family (ví dụ 4)  
- Hết budget: dừng, review decision log, không xin AI thêm ý tưởng

### 9.3 Portfolio of bets

Bạn không cần 1 holy grail.  
Bạn cần **quy trình có positive expected research value**:  
nhiều kill rẻ + ít bet đắt đã qua gate.

---

## 10. Checklist 1 trang (in ra / để cạnh màn hình)

**Trước code**

- [ ] Constraints khóa  
- [ ] Research Card đủ 8 mục  
- [ ] Có counterparty + lý do chưa arb  
- [ ] ≥3 falsifiers  
- [ ] Preregister metrics + kill floors  
- [ ] Holdout sealed  
- [ ] Trial budget set  

**Trước khi tin backtest**

- [ ] Data audit pass  
- [ ] Mechanism test pass (không chỉ full strategy)  
- [ ] Costs pessimistic  
- [ ] Sensitivity / regime / permutation  
- [ ] Trial count disclosed  
- [ ] OOS chưa bị tune  

**Kill ngay nếu**

- [ ] “Nghe hay” nhưng không đo được  
- [ ] Thêm filter sau khi xấu  
- [ ] OOS fail mà vẫn vá  
- [ ] Edge < 2–3× cost  
- [ ] Phụ thuộc top trades / 1 năm  
- [ ] AI dùng ngôn ngữ marketing thay evidence  

---

## 11. Mẫu file làm việc (cấu trúc thư mục gợi ý)

```text
research/
  constraints.yaml
  decision_log.md
  cards/
    20260711-001.md
  prereg/
    20260711-001.md
  audits/
    data_audit_....md
  results/
    20260711-001/
      is_summary.md
      robustness.md
      oos_summary.md
      KILL_or_PASS.md
execution/
  ea/                 # chỉ strategy PASS research
  mt5_reports/
analyzer/             # strategy_analyzer.py
```

Mỗi strategy 1 folder. Nhánh chết vẫn giữ — để chống lặp lại sai lầm.

---

## 12. Tóm tắt điều hành (đọc 30 giây)

1. **Bạn là người khóa cửa**, không phải người xin ý tưởng.  
2. **70%+ ý tưởng AI phải chết ở G1** — đó là dấu hiệu quy trình khỏe.  
3. **Cấm** idea → code → backtest.  
4. **Bắt buộc** mechanism + counterparty + falsifier + preregister.  
5. **Backtest đẹp không phải evidence**; robustness + blind OOS + cost + live track mới là.  
6. **Sau khi peek holdout: không được tune.**  
7. **AI hiến pháp**: default KILL, cấm marketing, cấm param hack, bắt buộc báo trial count.  
8. **MT5 analyzer** = chẩn đoán phần đuôi, không thay research khoa học phần đầu.

---

*Version: 2026-07-11 — Playbook quy trình, không chứa strategy idea.*
```
