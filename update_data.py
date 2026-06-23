def fallback_data(errors: dict[str, str], activation_logs: list[str]):
    stocks = [
        {
                "ticker": "VCB",
                "name": "Vietcombank",
                "sector": "Ngân hàng",
                "score": 48.0,
                "subscores": {
                        "trend": 10,
                        "momentum": 7.0,
                        "moneyFlow": 8.0,
                        "setup": 5.0,
                        "risk": 12.0,
                        "relativeStrength": 6.0
                },
                "setupType": "Pullback MA20",
                "marketState": "Trung tính",
                "action": "TRÁNH MUA MỚI",
                "risk": "Trung bình",
                "close": 20000,
                "rsi14": 42.0,
                "ret20": -8.0,
                "ret60": -12.0,
                "volume_status": "Mẫu",
                "volumeRatio": 0.8,
                "ma20": 19500,
                "ma50": 19000,
                "ma200": 18000,
                "macd": None,
                "macd_signal": None,
                "distanceToMA20": -3.5,
                "atr14": None,
                "signals": [
                        "Dữ liệu mẫu trước khi chạy Vnstock API",
                        "Có cấu trúc phân tích nâng cấp",
                        "Chạy workflow để cập nhật dữ liệu thật"
                ],
                "warnings": [
                        "Không dùng dữ liệu mẫu để giao dịch thật",
                        "Kiểm tra data.json sau khi chạy Actions"
                ],
                "filters": {
                        "topOpportunity": False,
                        "breakout": False,
                        "pullbackMA20": True,
                        "moneyFlow": False,
                        "accumulation": False,
                        "safe": False
                },
                "reason": "Dữ liệu mẫu cho VCB. Chạy GitHub Actions sau khi thêm VNSTOCK_API_KEY để cập nhật tín hiệu thật.",
                "expertSummary": "VCB đang ở trạng thái mẫu. Hệ thống sẽ cập nhật xu hướng, động lượng, dòng tiền, setup và rủi ro sau khi chạy Vnstock API.",
                "buyZone": "Canh quanh MA20 hoặc nền tích lũy gần nhất, không mua đuổi.",
                "stopLoss": "-7% đến -10%",
                "takeProfit": "+12% đến +25%",
                "allocation": "5% - 20%",
                "catalysts": [
                        "Vnstock API",
                        "Ngân hàng"
                ],
                "cautions": [
                        "Đây là dữ liệu mẫu trước khi chạy API",
                        "Không dùng để giao dịch thật",
                        "Chạy workflow để cập nhật"
                ]
        },
        {
                "ticker": "BID",
                "name": "BIDV",
                "sector": "Ngân hàng",
                "score": 54.5,
                "subscores": {
                        "trend": 12,
                        "momentum": 8.4,
                        "moneyFlow": 9.5,
                        "setup": 6.7,
                        "risk": 10.8,
                        "relativeStrength": 7.1
                },
                "setupType": "Breakout 20 phiên",
                "marketState": "Tích cực",
                "action": "TRÁNH MUA MỚI",
                "risk": "Trung bình",
                "close": 20800,
                "rsi14": 43.7,
                "ret20": -7.1,
                "ret60": -10.8,
                "volume_status": "Mẫu",
                "volumeRatio": 0.95,
                "ma20": 20290,
                "ma50": 19780,
                "ma200": 18760,
                "macd": None,
                "macd_signal": None,
                "distanceToMA20": -2.5,
                "atr14": None,
                "signals": [
                        "Dữ liệu mẫu trước khi chạy Vnstock API",
                        "Có cấu trúc phân tích nâng cấp",
                        "Chạy workflow để cập nhật dữ liệu thật"
                ],
                "warnings": [
                        "Không dùng dữ liệu mẫu để giao dịch thật",
                        "Kiểm tra data.json sau khi chạy Actions"
                ],
                "filters": {
                        "topOpportunity": False,
                        "breakout": True,
                        "pullbackMA20": False,
                        "moneyFlow": False,
                        "accumulation": False,
                        "safe": False
                },
                "reason": "Dữ liệu mẫu cho BID. Chạy GitHub Actions sau khi thêm VNSTOCK_API_KEY để cập nhật tín hiệu thật.",
                "expertSummary": "BID đang ở trạng thái mẫu. Hệ thống sẽ cập nhật xu hướng, động lượng, dòng tiền, setup và rủi ro sau khi chạy Vnstock API.",
                "buyZone": "Canh quanh MA20 hoặc nền tích lũy gần nhất, không mua đuổi.",
                "stopLoss": "-7% đến -10%",
                "takeProfit": "+12% đến +25%",
                "allocation": "5% - 20%",
                "catalysts": [
                        "Vnstock API",
                        "Ngân hàng"
                ],
                "cautions": [
                        "Đây là dữ liệu mẫu trước khi chạy API",
                        "Không dùng để giao dịch thật",
                        "Chạy workflow để cập nhật"
                ]
        },
        {
                "ticker": "CTG",
                "name": "VietinBank",
                "sector": "Ngân hàng",
                "score": 61.0,
                "subscores": {
                        "trend": 14,
                        "momentum": 9.8,
                        "moneyFlow": 11.0,
                        "setup": 8.4,
                        "risk": 9.6,
                        "relativeStrength": 8.2
                },
                "setupType": "Tích lũy biên hẹp",
                "marketState": "Tích cực",
                "action": "CHỜ THÊM",
                "risk": "Trung bình",
                "close": 21600,
                "rsi14": 45.4,
                "ret20": -6.2,
                "ret60": -9.6,
                "volume_status": "Mẫu",
                "volumeRatio": 1.1,
                "ma20": 21080,
                "ma50": 20560,
                "ma200": 19520,
                "macd": None,
                "macd_signal": None,
                "distanceToMA20": -1.5,
                "atr14": None,
                "signals": [
                        "Dữ liệu mẫu trước khi chạy Vnstock API",
                        "Có cấu trúc phân tích nâng cấp",
                        "Chạy workflow để cập nhật dữ liệu thật"
                ],
                "warnings": [
                        "Không dùng dữ liệu mẫu để giao dịch thật",
                        "Kiểm tra data.json sau khi chạy Actions"
                ],
                "filters": {
                        "topOpportunity": False,
                        "breakout": False,
                        "pullbackMA20": False,
                        "moneyFlow": False,
                        "accumulation": True,
                        "safe": False
                },
                "reason": "Dữ liệu mẫu cho CTG. Chạy GitHub Actions sau khi thêm VNSTOCK_API_KEY để cập nhật tín hiệu thật.",
                "expertSummary": "CTG đang ở trạng thái mẫu. Hệ thống sẽ cập nhật xu hướng, động lượng, dòng tiền, setup và rủi ro sau khi chạy Vnstock API.",
                "buyZone": "Canh quanh MA20 hoặc nền tích lũy gần nhất, không mua đuổi.",
                "stopLoss": "-7% đến -10%",
                "takeProfit": "+12% đến +25%",
                "allocation": "5% - 20%",
                "catalysts": [
                        "Vnstock API",
                        "Ngân hàng"
                ],
                "cautions": [
                        "Đây là dữ liệu mẫu trước khi chạy API",
                        "Không dùng để giao dịch thật",
                        "Chạy workflow để cập nhật"
                ]
        },
        {
                "ticker": "TCB",
                "name": "Techcombank",
                "sector": "Ngân hàng",
                "score": 67.5,
                "subscores": {
                        "trend": 16,
                        "momentum": 11.2,
                        "moneyFlow": 12.5,
                        "setup": 10.1,
                        "risk": 8.4,
                        "relativeStrength": 9.3
                },
                "setupType": "Retest nền",
                "marketState": "Uptrend",
                "action": "THEO DÕI MUA",
                "risk": "Trung bình",
                "close": 22400,
                "rsi14": 47.1,
                "ret20": -5.3,
                "ret60": -8.4,
                "volume_status": "Mẫu",
                "volumeRatio": 1.25,
                "ma20": 21870,
                "ma50": 21340,
                "ma200": 20280,
                "macd": None,
                "macd_signal": None,
                "distanceToMA20": -0.5,
                "atr14": None,
                "signals": [
                        "Dữ liệu mẫu trước khi chạy Vnstock API",
                        "Có cấu trúc phân tích nâng cấp",
                        "Chạy workflow để cập nhật dữ liệu thật"
                ],
                "warnings": [
                        "Không dùng dữ liệu mẫu để giao dịch thật",
                        "Kiểm tra data.json sau khi chạy Actions"
                ],
                "filters": {
                        "topOpportunity": False,
                        "breakout": False,
                        "pullbackMA20": False,
                        "moneyFlow": False,
                        "accumulation": False,
                        "safe": False
                },
                "reason": "Dữ liệu mẫu cho TCB. Chạy GitHub Actions sau khi thêm VNSTOCK_API_KEY để cập nhật tín hiệu thật.",
                "expertSummary": "TCB đang ở trạng thái mẫu. Hệ thống sẽ cập nhật xu hướng, động lượng, dòng tiền, setup và rủi ro sau khi chạy Vnstock API.",
                "buyZone": "Canh quanh MA20 hoặc nền tích lũy gần nhất, không mua đuổi.",
                "stopLoss": "-7% đến -10%",
                "takeProfit": "+12% đến +25%",
                "allocation": "5% - 20%",
                "catalysts": [
                        "Vnstock API",
                        "Ngân hàng"
                ],
                "cautions": [
                        "Đây là dữ liệu mẫu trước khi chạy API",
                        "Không dùng để giao dịch thật",
                        "Chạy workflow để cập nhật"
                ]
        },
        {
                "ticker": "MBB",
                "name": "Ngân hàng Quân đội",
                "sector": "Ngân hàng",
                "score": 74.0,
                "subscores": {
                        "trend": 18,
                        "momentum": 12.6,
                        "moneyFlow": 14.0,
                        "setup": 11.8,
                        "risk": 7.2,
                        "relativeStrength": 10.4
                },
                "setupType": "Vượt lại MA50",
                "marketState": "Uptrend",
                "action": "CANH MUA / MUA KHI XÁC NHẬN",
                "risk": "Trung bình",
                "close": 23200,
                "rsi14": 48.8,
                "ret20": -4.4,
                "ret60": -7.2,
                "volume_status": "Mẫu",
                "volumeRatio": 1.4,
                "ma20": 22660,
                "ma50": 22120,
                "ma200": 21040,
                "macd": None,
                "macd_signal": None,
                "distanceToMA20": 0.5,
                "atr14": None,
                "signals": [
                        "Dữ liệu mẫu trước khi chạy Vnstock API",
                        "Có cấu trúc phân tích nâng cấp",
                        "Chạy workflow để cập nhật dữ liệu thật"
                ],
                "warnings": [
                        "Không dùng dữ liệu mẫu để giao dịch thật",
                        "Kiểm tra data.json sau khi chạy Actions"
                ],
                "filters": {
                        "topOpportunity": False,
                        "breakout": False,
                        "pullbackMA20": False,
                        "moneyFlow": False,
                        "accumulation": False,
                        "safe": False
                },
                "reason": "Dữ liệu mẫu cho MBB. Chạy GitHub Actions sau khi thêm VNSTOCK_API_KEY để cập nhật tín hiệu thật.",
                "expertSummary": "MBB đang ở trạng thái mẫu. Hệ thống sẽ cập nhật xu hướng, động lượng, dòng tiền, setup và rủi ro sau khi chạy Vnstock API.",
                "buyZone": "Canh quanh MA20 hoặc nền tích lũy gần nhất, không mua đuổi.",
                "stopLoss": "-7% đến -10%",
                "takeProfit": "+12% đến +25%",
                "allocation": "5% - 20%",
                "catalysts": [
                        "Vnstock API",
                        "Ngân hàng"
                ],
                "cautions": [
                        "Đây là dữ liệu mẫu trước khi chạy API",
                        "Không dùng để giao dịch thật",
                        "Chạy workflow để cập nhật"
                ]
        },
        {
                "ticker": "ACB",
                "name": "Ngân hàng Á Châu",
                "sector": "Ngân hàng",
                "score": 79.5,
                "subscores": {
                        "trend": 20,
                        "momentum": 7.0,
                        "moneyFlow": 15.5,
                        "setup": 13.5,
                        "risk": 12.0,
                        "relativeStrength": 11.5
                },
                "setupType": "Chưa có setup rõ",
                "marketState": "Uptrend",
                "action": "CANH MUA / MUA KHI XÁC NHẬN",
                "risk": "Trung bình",
                "close": 24000,
                "rsi14": 50.5,
                "ret20": -3.5,
                "ret60": -6.0,
                "volume_status": "Mẫu",
                "volumeRatio": 1.55,
                "ma20": 23450,
                "ma50": 22900,
                "ma200": 21800,
                "macd": None,
                "macd_signal": None,
                "distanceToMA20": 1.5,
                "atr14": None,
                "signals": [
                        "Dữ liệu mẫu trước khi chạy Vnstock API",
                        "Có cấu trúc phân tích nâng cấp",
                        "Chạy workflow để cập nhật dữ liệu thật"
                ],
                "warnings": [
                        "Không dùng dữ liệu mẫu để giao dịch thật",
                        "Kiểm tra data.json sau khi chạy Actions"
                ],
                "filters": {
                        "topOpportunity": True,
                        "breakout": False,
                        "pullbackMA20": False,
                        "moneyFlow": True,
                        "accumulation": False,
                        "safe": True
                },
                "reason": "Dữ liệu mẫu cho ACB. Chạy GitHub Actions sau khi thêm VNSTOCK_API_KEY để cập nhật tín hiệu thật.",
                "expertSummary": "ACB đang ở trạng thái mẫu. Hệ thống sẽ cập nhật xu hướng, động lượng, dòng tiền, setup và rủi ro sau khi chạy Vnstock API.",
                "buyZone": "Canh quanh MA20 hoặc nền tích lũy gần nhất, không mua đuổi.",
                "stopLoss": "-7% đến -10%",
                "takeProfit": "+12% đến +25%",
                "allocation": "5% - 20%",
                "catalysts": [
                        "Vnstock API",
                        "Ngân hàng"
                ],
                "cautions": [
                        "Đây là dữ liệu mẫu trước khi chạy API",
                        "Không dùng để giao dịch thật",
                        "Chạy workflow để cập nhật"
                ]
        },
        {
                "ticker": "VPB",
                "name": "VPBank",
                "sector": "Ngân hàng",
                "score": 63.8,
                "subscores": {
                        "trend": 10,
                        "momentum": 8.4,
                        "moneyFlow": 17.0,
                        "setup": 5.0,
                        "risk": 10.8,
                        "relativeStrength": 12.6
                },
                "setupType": "Pullback MA20",
                "marketState": "Trung tính",
                "action": "CHỜ THÊM",
                "risk": "Trung bình",
                "close": 24800,
                "rsi14": 52.2,
                "ret20": -2.6,
                "ret60": -4.8,
                "volume_status": "Mẫu",
                "volumeRatio": 1.7,
                "ma20": 24240,
                "ma50": 23680,
                "ma200": 22560,
                "macd": None,
                "macd_signal": None,
                "distanceToMA20": 2.5,
                "atr14": None,
                "signals": [
                        "Dữ liệu mẫu trước khi chạy Vnstock API",
                        "Có cấu trúc phân tích nâng cấp",
                        "Chạy workflow để cập nhật dữ liệu thật"
                ],
                "warnings": [
                        "Không dùng dữ liệu mẫu để giao dịch thật",
                        "Kiểm tra data.json sau khi chạy Actions"
                ],
                "filters": {
                        "topOpportunity": False,
                        "breakout": False,
                        "pullbackMA20": True,
                        "moneyFlow": True,
                        "accumulation": False,
                        "safe": False
                },
                "reason": "Dữ liệu mẫu cho VPB. Chạy GitHub Actions sau khi thêm VNSTOCK_API_KEY để cập nhật tín hiệu thật.",
                "expertSummary": "VPB đang ở trạng thái mẫu. Hệ thống sẽ cập nhật xu hướng, động lượng, dòng tiền, setup và rủi ro sau khi chạy Vnstock API.",
                "buyZone": "Canh quanh MA20 hoặc nền tích lũy gần nhất, không mua đuổi.",
                "stopLoss": "-7% đến -10%",
                "takeProfit": "+12% đến +25%",
                "allocation": "5% - 20%",
                "catalysts": [
                        "Vnstock API",
                        "Ngân hàng"
                ],
                "cautions": [
                        "Đây là dữ liệu mẫu trước khi chạy API",
                        "Không dùng để giao dịch thật",
                        "Chạy workflow để cập nhật"
                ]
        },
        {
                "ticker": "STB",
                "name": "Sacombank",
                "sector": "Ngân hàng",
                "score": 59.8,
                "subscores": {
                        "trend": 12,
                        "momentum": 9.8,
                        "moneyFlow": 8.0,
                        "setup": 6.7,
                        "risk": 9.6,
                        "relativeStrength": 13.7
                },
                "setupType": "Breakout 20 phiên",
                "marketState": "Tích cực",
                "action": "CHỜ THÊM",
                "risk": "Trung bình",
                "close": 25600,
                "rsi14": 53.9,
                "ret20": -1.7,
                "ret60": -3.6,
                "volume_status": "Mẫu",
                "volumeRatio": 1.85,
                "ma20": 25030,
                "ma50": 24460,
                "ma200": 23320,
                "macd": None,
                "macd_signal": None,
                "distanceToMA20": 3.5,
                "atr14": None,
                "signals": [
                        "Dữ liệu mẫu trước khi chạy Vnstock API",
                        "Có cấu trúc phân tích nâng cấp",
                        "Chạy workflow để cập nhật dữ liệu thật"
                ],
                "warnings": [
                        "Không dùng dữ liệu mẫu để giao dịch thật",
                        "Kiểm tra data.json sau khi chạy Actions"
                ],
                "filters": {
                        "topOpportunity": False,
                        "breakout": True,
                        "pullbackMA20": False,
                        "moneyFlow": False,
                        "accumulation": False,
                        "safe": False
                },
                "reason": "Dữ liệu mẫu cho STB. Chạy GitHub Actions sau khi thêm VNSTOCK_API_KEY để cập nhật tín hiệu thật.",
                "expertSummary": "STB đang ở trạng thái mẫu. Hệ thống sẽ cập nhật xu hướng, động lượng, dòng tiền, setup và rủi ro sau khi chạy Vnstock API.",
                "buyZone": "Canh quanh MA20 hoặc nền tích lũy gần nhất, không mua đuổi.",
                "stopLoss": "-7% đến -10%",
                "takeProfit": "+12% đến +25%",
                "allocation": "5% - 20%",
                "catalysts": [
                        "Vnstock API",
                        "Ngân hàng"
                ],
                "cautions": [
                        "Đây là dữ liệu mẫu trước khi chạy API",
                        "Không dùng để giao dịch thật",
                        "Chạy workflow để cập nhật"
                ]
        },
        {
                "ticker": "HDB",
                "name": "HDBank",
                "sector": "Ngân hàng",
                "score": 57.5,
                "subscores": {
                        "trend": 14,
                        "momentum": 11.2,
                        "moneyFlow": 9.5,
                        "setup": 8.4,
                        "risk": 8.4,
                        "relativeStrength": 6.0
                },
                "setupType": "Tích lũy biên hẹp",
                "marketState": "Tích cực",
                "action": "CHỜ THÊM",
                "risk": "Trung bình",
                "close": 26400,
                "rsi14": 55.6,
                "ret20": -0.8,
                "ret60": -2.4,
                "volume_status": "Mẫu",
                "volumeRatio": 0.8,
                "ma20": 25820,
                "ma50": 25240,
                "ma200": 24080,
                "macd": None,
                "macd_signal": None,
                "distanceToMA20": 4.5,
                "atr14": None,
                "signals": [
                        "Dữ liệu mẫu trước khi chạy Vnstock API",
                        "Có cấu trúc phân tích nâng cấp",
                        "Chạy workflow để cập nhật dữ liệu thật"
                ],
                "warnings": [
                        "Không dùng dữ liệu mẫu để giao dịch thật",
                        "Kiểm tra data.json sau khi chạy Actions"
                ],
                "filters": {
                        "topOpportunity": False,
                        "breakout": false,
                        "pullbackMA20": false,
                        "moneyFlow": False,
                        "accumulation": True,
                        "safe": False
                },
                "reason": "Dữ liệu mẫu cho HDB. Chạy GitHub Actions sau khi thêm VNSTOCK_API_KEY để cập nhật tín hiệu thật.",
                "expertSummary": "HDB đang ở trạng thái mẫu. Hệ thống sẽ cập nhật xu hướng, động lượng, dòng tiền, setup và rủi ro sau khi chạy Vnstock API.",
                "buyZone": "Canh quanh MA20 hoặc nền tích lũy gần nhất, không mua đuổi.",
                "stopLoss": "-7% đến -10%",
                "takeProfit": "+12% đến +25%",
                "allocation": "5% - 20%",
                "catalysts": [
                        "Vnstock API",
                        "Ngân hàng"
                ],
                "cautions": [
                        "Đây là dữ liệu mẫu trước khi chạy API",
                        "Không dùng để giao dịch thật",
                        "Chạy workflow để cập nhật"
                ]
        },
        {
                "ticker": "VIB",
                "name": "VIB",
                "sector": "Ngân hàng",
                "score": 64.0,
                "subscores": {
                        "trend": 16,
                        "momentum": 12.6,
                        "moneyFlow": 11.0,
                        "setup": 10.1,
                        "risk": 7.2,
                        "relativeStrength": 7.1
                },
                "setupType": "Retest nền",
                "marketState": "Uptrend",
                "action": "CHỜ THÊM",
                "risk": "Trung bình",
                "close": 27200,
                "rsi14": 57.3,
                "ret20": 0.1,
                "ret60": -1.2,
                "volume_status": "Mẫu",
                "volumeRatio": 0.95,
                "ma20": 26610,
                "ma50": 26020,
                "ma200": 24840,
                "macd": None,
                "macd_signal": None,
                "distanceToMA20": 5.5,
                "atr14": None,
                "signals": [
                        "Dữ liệu mẫu trước khi chạy Vnstock API",
                        "Có cấu trúc phân tích nâng cấp",
                        "Chạy workflow để cập nhật dữ liệu thật"
                ],
                "warnings": [
                        "Không dùng dữ liệu mẫu để giao dịch thật",
                        "Kiểm tra data.json sau khi chạy Actions"
                ],
                "filters": {
                        "topOpportunity": False,
                        "breakout": False,
                        "pullbackMA20": false,
                        "moneyFlow": false,
                        "accumulation": false,
                        "safe": False
                },
                "reason": "Dữ liệu mẫu cho VIB. Chạy GitHub Actions sau khi thêm VNSTOCK_API_KEY để cập nhật tín hiệu thật.",
                "expertSummary": "VIB đang ở trạng thái mẫu. Hệ thống sẽ cập nhật xu hướng, động lượng, dòng tiền, setup và rủi ro sau khi chạy Vnstock API.",
                "buyZone": "Canh quanh MA20 hoặc nền tích lũy gần nhất, không mua đuổi.",
                "stopLoss": "-7% đến -10%",
                "takeProfit": "+12% đến +25%",
                "allocation": "5% - 20%",
                "catalysts": [
                        "Vnstock API",
                        "Ngân hàng"
                ],
                "cautions": [
                        "Đây là dữ liệu mẫu trước khi chạy API",
                        "Không dùng để giao dịch thật",
                        "Chạy workflow để cập nhật"
                ]
        }
    ]
    
    # Đoạn code ghi file JSON ở cuối hàm Sếp giữ nguyên nhé:
    output = {"meta": {"updated_at": datetime.now(VN_TZ).strftime("%Y-%m-%d %H:%M:%S"), "source": "Fallback Data", "success": False}, "stocks": stocks}
    with open("data.json", "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=8)
    print("Wrote data.json with fallback data due to errors.")
