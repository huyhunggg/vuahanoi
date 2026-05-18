# VN Stock Picker Pro Signals

Bản nâng cấp bộ lọc cổ phiếu:

- Top cơ hội
- Breakout
- Pullback MA20
- Dòng tiền mạnh
- Tích lũy đẹp
- An toàn
- Tất cả mã

## Dữ liệu

`update_data.py` tạo thêm:

```txt
subscores
signals
warnings
setupType
marketState
filters
expertSummary
```

## Cài API key

Settings → Secrets and variables → Actions → New repository secret:

```txt
Name: VNSTOCK_API_KEY
Secret: API key Vnstock của bạn
```

## Chạy cập nhật

Actions → Update stock data → Run workflow


## Bản T+

Bản này thêm tab `Lướt sóng T+`.

Tiêu chí lọc T+:
- Tổng điểm >= 72
- Money Flow >= 13
- Momentum >= 9
- Risk >= 8
- Giá trên MA20 và MA50
- Volume ratio >= 1.15
- RSI trong vùng 48-72
- Không cách MA20 quá xa
- Không tăng quá nóng 20 phiên

Mục tiêu là lọc mã có xác suất tốt hơn cho T+; không cam kết tỷ lệ thắng cố định.

## T+ Pro checklist

Bản này đã nâng bộ lọc T+ theo checklist:
- Không đánh ngược xu hướng quá sớm.
- Ưu tiên giá trên/vừa vượt MA20, MA20 cong lên.
- MACD cắt lên hoặc đang trên Signal.
- RSI đẹp nhất 52–65; trên 70 không mở vị thế lớn.
- Volume cao hơn trung bình 20 phiên; breakout cần 1.3–1.5 lần.
- Điểm mua phải gần hỗ trợ, breakout, pullback MA20/MA10 hoặc retest nền.
- Không mua đuổi nếu giá cách MA20 quá xa, đặc biệt trên 10%.
- Risk/Reward tối thiểu 1.5:1, tốt hơn 2:1.
- Stop nhanh 3–5%; sau 2–3 phiên không chạy thì giảm tỷ trọng.
- Đạt TP1 chốt 30–50%, phần còn lại kéo stop lên giá vốn/MA10.
