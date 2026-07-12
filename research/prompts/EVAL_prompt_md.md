# Đánh giá `../prompt.md` (legacy — “AI sáng tạo chiến lược”)

## Kết luận ngắn

| Câu hỏi | Trả lời |
|---------|---------|
| Có hợp lý không? | **Một phần** — tốt như *khuôn đặc tả kỹ thuật*, **xấu** như *cổng sáng tạo edge* |
| Dùng làm bước đầu? | **Không** — đây là anti-pattern đã làm bạn fail |
| Gate đúng | **G4** (Implementation Spec), sau G0–G3; một phần nhỏ map G1/G2 nhưng **thiếu xương sống** |
| Nên thay bằng | `G1_research_card.md` → `G2_preregister.md` → `G4_implementation_spec.md` |

---

## 1. `prompt.md` đang làm gì trong thực tế

Luồng ngầm:

```
AI đóng vai HF quant
  → kể hypothesis “học thuật”
  → chọn symbol/TF/session tự do
  → đưa parameter GRID lớn
  → full entry/exit/risk
  → đặt benchmark Sharpe/PF
  → (bạn) Python optimize → MQL5
```

Đây đúng pattern trong playbook: **tối ưu thuyết phục + degrees of freedom**, không tối ưu causal edge.

Bằng chứng trong folder: `adaptive_momentum_burst.md` (AMB-HEF) — name-drop Kaufman/Mandelbrot/de Prado/Lo, grid nhiều param (ATR, Squeeze, KER, Hurst…), rồi optimizer + EA. Đó là **output đúng template `prompt.md`**, và cũng là kiểu strategy thường chết OOS/live.

---

## 2. Điểm mạnh (giữ)

| Phần trong prompt.md | Vì sao tốt |
|----------------------|------------|
| Cấm code, chỉ pseudo | Tách design / implementation |
| Anti look-ahead, bar[1] | Bắt buộc với BT |
| “Không ghép indicator ngẫu nhiên” + tối giản | Đúng hướng anti-soup |
| Entry/exit tường minh | Cần cho G4 + EA |
| Friction filters (spread, vol) | Gần thực tế execution |
| Python vectorized → robust → MQL5 | Thứ tự *tooling* ổn **nếu** đã qua research gates |

---

## 3. Điểm yếu cấu trúc (vì sao “sáng tạo” bằng file này hay fail)

### 3.1 Sai nhiệm vụ gốc

- Prompt yêu cầu: *“thiết kế chiến lược có Statistical Edge rõ ràng”*.
- AI **không thể** “thiết kế ra edge” từ ngôn ngữ. Edge phải **kiểm chứng** sau protocol.
- Vai “Senior Quant tại HF” + list Simons/Thorp/Shaw → khuyến khích **narrative authority**, không khuyến khích **self-kill**.

### 3.2 Thiếu G0

- Symbol / TF / session do AI **đề xuất** (mục 2) thay vì human **khóa** trong `constraints.yaml`.
- Mỗi lần AI đổi universe = thêm một chiều data-mining.

### 3.3 G1 quá mỏng (mục 1)

Có “vì sao kiếm được tiền” nhưng **không bắt buộc**:

- Counterparty cụ thể (ai trả tiền?)
- Vì sao chưa bị arb hết (capacity/constraint)
- Causal chain đo được từng bước
- ≥3 falsifiers cứng
- Minimal signal tách khỏi full strategy

→ Story “Auction Market + fat tail + Hurst” vẫn pass prompt, dù chưa test được.

### 3.4 Mục 3 (Parameter Search Space) — nguy hiểm nhất

- **Mời** grid/combo optimize *trước* mechanism test.
- AI có động cơ tăng số param để “có gì mà optimize”.
- Multiple testing / overfit gần như chắc chắn nếu không có trial budget + preregister.

Trong playbook: grid chỉ xuất hiện **sau** G1–G2, và **bị cap** (`max_free_params`, `max_variants_per_family`).

### 3.5 G2 bị đảo ngược (mục 7)

- Benchmark Sharpe/PF/WR do AI **đặt sau khi thiết kế strategy**.
- Đúng ra: human **khóa kill floors + primary metric trước** khi thấy design/result.
- Winrate làm tiêu chí “đạt” → vanity; thiếu min trades, cost stress, permutation, top-trade concentration.

### 3.6 Nhảy cóc G5

- Không có bước **mechanism-only test** (conditional return / dose-response).
- Đi thẳng full entry+SL+TP+filter → dễ “strategy thắng trong khi hypothesis sai” (overfit stack).

### 3.7 Literature list (đầu file)

- Hướng nguồn ý tưởng: ổn **như thư viện đọc**.
- Nguy hiểm khi AI dùng citation như **tem hợp thức hóa**.
- Rule: literature ≤ 1 mục optional; không thay falsifier.

---

## 4. Map từng mục → Gate

| Mục prompt.md | Gate đúng | Ghi chú |
|---------------|-----------|---------|
| Ràng buộc tài liệu / first principles | **G0 prep / reading**, không phải gate sinh strategy | Đọc offline; không paste để AI “sáng tạo” |
| Vai HF quant + “có edge” | **Xóa / thay Constitution** | Default KILL laborer |
| (1) Alpha hypothesis | **G1** | Cần bổ sung counterparty, falsifier, minimal signal |
| (2) Market universe | **G0** (human lock) | AI không tự chọn nếu constraints LOCKED |
| (3) Parameter search space | **G2 budget + G5 limited** | Range hẹp, variants pre-listed; không “optimizer-first” |
| (4) Entry logic | **G4** | Sau card + prereg + audit |
| (5) Exit & risk | **G4** (+ risk từ G0) | |
| (6) Friction filters | **G4 / G8** | Chỉ filter đã preregister |
| (7) Robustness benchmarks | **G2 preregister** | Human khóa trước; không để AI tự set cho “dễ đạt” |
| Câu hỏi mở cho PM | Cuối **G1 hoặc G9** | Hỏi falsifier/capacity — không hỏi để nới rule |

**Tóm lại:** `prompt.md` ≈ **G4-heavy hybrid** bị nhầm thành **G1 idea engine**.

---

## 5. Nên làm gì với file `prompt.md`

### Khuyến nghị

1. **Đổi tên / đánh dấu legacy** — không xóa (để đối chiếu lịch sử), không dùng làm entrypoint.
2. Entry point mới:
   - Session research: `AI_CONSTITUTION.md` + `prompts/G1_research_card.md`
   - Sau PASS dần: G2 → G3 → **`prompts/G4_implementation_spec.md`** (thay thế functional của prompt.md)
3. Các file strategy cũ (`adaptive_momentum_burst.md`, `session_liquidity_absorption.md`, `vwap_mean_reversion.md`):  
   **backfill** Research Card + chấm rubric G1 *retroactive*.  
   - Không đủ counterparty/falsifier → đánh dấu `LEGACY_UNVALIDATED`  
   - Không optimize thêm; chỉ audit hoặc KILL archive

### Nếu vẫn muốn 1 prompt “all-in-one”

Chỉ chấp nhận khi:

1. `constraints.yaml` status=LOCKED được paste trước  
2. Stage field bắt buộc (`G1` hoặc `G4`) — AI refuse nếu stage sai  
3. Cắt hẳn mục “Parameter Search Space” khỏi stage G1  
4. Thêm self-kill criteria  
5. Cấm output full strategy ở G1  

→ Đã tách sẵn thành các file trong `research/prompts/`.

---

## 6. Checklist: bạn có đang lạm dụng prompt.md?

- [ ] AI được quyền chọn symbol/TF mỗi lần
- [ ] Có bảng grid ≥ 5–6 param trước khi có mechanism test
- [ ] Có list tên tác giả/paper dài hơn falsifier
- [ ] Chạy optimizer ngay sau khi có file .md strategy
- [ ] Viết EA trước khi có prereg + holdout sealed
- [ ] “Cải thiện” strategy khi BT xấu

Số ô tick càng nhiều → càng đúng bệnh mà playbook mô tả.

---

*Đánh giá gắn với playbook 2026-07-11. Không phải đánh giá quality của từng EA cụ thể.*
