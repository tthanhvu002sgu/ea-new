> **LEGACY — KHÔNG dùng làm bước đầu / "AI sáng tạo edge".**  
> Đánh giá gate: `research/prompts/EVAL_prompt_md.md`  
> Entry point mới: `research/AI_CONSTITUTION.md` + `research/prompts/G1_research_card.md`  
> Phần entry/exit/friction chỉ hợp lệ ở **G4** (sau G0–G3 PASS) → `research/prompts/G4_implementation_spec.md`

---

# PROMPT THIẾT KẾ CHIẾN LƯỢC GIAO DỊCH ĐỊNH LƯỢNG (QUANTITATIVE RESEARCH PROMPT)

**Đóng vai trò là một Chuyên gia Nghiên cứu Định lượng (Senior Quantitative Researcher) và Nhà thiết kế Thuật toán Giao dịch tại một Quỹ phòng hộ (Hedge Fund). Tôi cần bạn thiết kế một chiến lược giao dịch tự động có lợi thế cạnh tranh thống kê (Statistical Edge) rõ ràng.**

**Ràng buộc về tài liệu / phạm vị lấy ý tưởng**: 
* Trích xuất ý tưởng từ các nền tảng học thuật hoặc các tác giả có tầm ảnh hưởng trong ngành tài chính định lượng (chẳng hạn như các nghiên cứu của Ernie Chan, Edward Thorp, hoặc Perry Kaufman), arXiv (Quantitative Finance), SSRN (Social Science Research Network), Quantpedia (The Encyclopedia of Algorithmic Trading Strategies), Portfolio Management Research (PMR), QuantConnect (LEAN Engine), QuantStart / QuantInsti
* Dựa trên các Nguyên lý Cơ học Thị trường (First Principles): lý thuyết đấu giá, order flow  imbalance
* Các trader nên tham khảo: Jim Simons, Edward Thorp (Ed Thorp), David Shaw (D. E. Shaw), Cliff Asnes, Marcos López de Prado, Perry Kaufman, 


**Quy trình nghiên cứu của chúng tôi:** Chiến lược này sẽ được **mô hình hóa và tối ưu hóa tham số tổ hợp trên Python trước** (sử dụng Vectorized Backtesting), sau đó kiểm định tính bền vững (Robustness Testing) trước khi đưa sang lập trình bằng C++/MQL5 trên MetaTrader 5.

### Yêu cầu nghiêm ngặt:
1. **Tuyệt đối không viết mã nguồn (code Python hay MQL5)** trong câu trả lời này. Chỉ cung cấp cấu trúc logic toán học, công thức tường minh và mã giả (pseudocode).
2. **Chống Look-ahead Bias:** Định nghĩa rõ thời điểm lấy tín hiệu (ví dụ: *ngay khi đóng nến [1]*), tuyệt đối không sử dụng giá Close của nến đang chạy để ra quyết định.
3. **Chống Overfitting:** Các chỉ báo sử dụng phải có mối liên hệ logic cơ bản (Fundamental/Microstructure Rationale), không ghép nối các chỉ báo ngẫu nhiên.
4. **Không giải thích lý thuyết tài chính cơ bản.** Đi thẳng vào đặc tả kỹ thuật.
5. **Không phụ thuộc quá nhiều chỉ báo / thông số**: áp dụng triết lý simple make perfect. Khai thác sự tối giản một cách hiệu quả thay vì biến chiến lược thành một mớ lộn xộn gồm nhiều chỉ báo và thông số.

---

### Vui lòng cung cấp chi tiết chiến lược theo đúng cấu trúc 7 phần sau:

#### 1. Giả thuyết Định lượng & Lợi thế Thị trường (Alpha Hypothesis & Edge)
* **Ý tưởng cốt lõi:** Chiến lược khai thác sự bất hiệu quả nào của thị trường? (Ví dụ: sự kiệt sức của xu hướng - Mean Reversion, bùng nổ động lượng - Momentum Burst, hay dòng tiền cấu trúc vi mô quanh VWAP...).
* **Tại sao chiến lược này tồn tại và kiếm được tiền?** Giải thích ngắn gọn động lực hành vi/cung cầu phía sau tín hiệu.

#### 2. Đặc tả Tài sản & Môi trường (Market Universe)
* **Tài sản phù hợp:** Đề xuất cặp tiền (Forex), Hàng hóa (Vàng/Dầu) hoặc Chỉ số cụ thể.
* **Khung thời gian (Timeframe):** Khung thời gian biểu đồ chính.
* **Khung giờ giao dịch tối ưu:** Các phiên thị trường nên hoạt động (ví dụ: London + New York session) và các giờ cần tránh.

#### 3. Không gian Tham số Tối ưu (Parameter Search Space - Dành cho Python Optimizer)
* Liệt kê toàn bộ chỉ báo và biến số của hệ thống.
* Thay vì đưa ra 1 con số cố định dễ overfitting, **hãy xác định miền giá trị (Range/Grid) hợp lý để chúng tôi chạy tối ưu tổ hợp trên Python**.
  * *Ví dụ:* `ATR_Period`: [10, 14, 20], `RSI_Period`: [7, 14, 21], `RSI_Oversold`: [25, 30, 35].

#### 4. Logic Mở lệnh Tường minh (Explicit Entry Logic)
* **Tín hiệu Mua (Long Entry):** Viết công thức bằng các mệnh đề logic toán học (`AND`, `OR`, `>`, `<`, `cắt lên`, `cắt xuống`). Chỉ rõ chỉ số nến cụ thể (Nến `[1]` là nến vừa đóng, Nến `[0]` là nến hiện tại).
* **Tín hiệu Bán (Short Entry):** Tương tự tín hiệu Mua.
* **Điều kiện Kích hoạt:** Xác định rõ tín hiệu được đánh giá tại *giá đóng cửa nến `[1]`* hay *giá chạm ngưỡng tức thời*.

#### 5. Logic Thoát lệnh & Quản lý rủi ro (Exit & Risk Management)
* **Dừng lỗ ban đầu (Initial Stop Loss):** Công thức tính SL động (ví dụ: dựa trên `ATR` hoặc cấu trúc Đỉnh/Đáy gần nhất).
* **Chốt lời (Take Profit):** Công thức tính TP hoặc tỷ lệ Risk:Reward động.
* **Thoát lệnh theo Thời gian (Time-based Exit):** Nếu sau `X` nến kể từ khi vào lệnh mà giá không đi đúng hướng hoặc chưa chạm SL/TP, công thức đóng lệnh sớm là gì?
* **Quản lý lệnh động:** Thuật toán Trailing Stop hoặc Breakeven (nếu phù hợp với bản chất chiến lược).

#### 6. Bộ lọc Ma sát Thị trường (Market Friction Filters)
* **Max Spread:** Ngưỡng giãn chênh lệch tối đa cho phép mở lệnh.
* **Bộ lọc biến động (Volatility Filter):** Tránh vào lệnh khi thị trường quá "chết" (vùng sideway hẹp) hoặc biến động hỗn loạn mất kiểm soát do tin tức lớn (News Blackout).

#### 7. Tiêu chí Đánh giá Tính bền vững mong đợi (Robustness Benchmarks)
* Khi chúng tôi backtest trên Python (Out-of-Sample 3 năm gần nhất), chiến lược này cần đạt các chỉ số tối thiểu nào để được coi là "Đạt yêu cầu":
  * *Sharpe Ratio tối thiểu:* (ví dụ: > 1.3)
  * *Profit Factor tối thiểu:* (ví dụ: > 1.4)
  * *Win Rate kỳ vọng:* (%)
  * *Max Drawdown tối đa:* (%)

---
*Lưu ý cho AI: Sau khi hoàn thành đặc tả, hãy đặt ra 1 - 2 câu hỏi mở quan trọng cho Quản lý Quỹ (người dùng) liên quan đến định hướng phân bổ vốn hoặc khẩu vị rủi ro của chiến lược này.*
