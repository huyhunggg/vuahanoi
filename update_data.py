def fallback_data(errors: dict[str, str], activation_logs: list[str]):
    stocks = [
        {
                "ticker": "VCB",
                "name": "Vietcombank",
                "sector": "Ngân hàng",
                "score": 48.0,
                "subscores": {
                        "trend": 10, "momentum": 7.0, "moneyFlow": 8.0,
                        "setup": 5.0, "risk": 12.0, "relativeStrength": 6.0
                },
                "setupType": "Pullback MA20",
                "marketState": "Trung tính",
                "action": "TRÁNH MUA MỚI",
                "risk": "Trung bình",
                "close": 20000, "rsi14": 42.0, "ret20": -8.0, "ret60": -12.0,
                "volume_status": "Mẫu", "volumeRatio": 0.8,
                "ma20": 19500, "ma50": 19000, "ma200": 18000,
                "macd": None, "macd_signal": None, "distanceToMA20": -3.5, "atr14": None,
                "signals": ["Dữ liệu mẫu trước khi chạy Vnstock API"],
                "warnings": ["Không dùng dữ liệu mẫu để giao dịch thật"],
                "filters": {
                        "topOpportunity": False, "breakout": False, "pullbackMA20": True,
                        "moneyFlow": False, "accumulation": False, "safe": False
                },
                "reason": "Dữ liệu mẫu cho VCB.",
                "expertSummary": "VCB đang ở trạng thái mẫu.",
                "buyZone": "Canh quanh MA20.", "stopLoss": "-7%", "takeProfit": "+12%", "allocation": "5%"
        }
    ]
    return {
        "meta": {
            "updated_at": datetime.now(VN_TZ).strftime("%Y-%m-%d %H:%M:%S VN"),
            "source": "fallback sample pro signals",
            "has_api_key": bool(VNSTOCK_API_KEY),
            "success": 0,
            "universe": len(WATCHLIST),
            "note": "Vnstock API lỗi nên dùng dữ liệu mẫu.",
            "activation_logs": activation_logs,
            "errors": errors,
        },
        "stocks": stocks,
    }
