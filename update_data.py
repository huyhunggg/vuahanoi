from __future__ import annotations

import json
import math
import os
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Callable

import pandas as pd

VN_TZ = timezone(timedelta(hours=7))
VNSTOCK_API_KEY = os.getenv("VNSTOCK_API_KEY", "").strip()

# Đặt nhiều tên biến môi trường để tăng tương thích giữa các phiên bản Vnstock.
if VNSTOCK_API_KEY:
    os.environ["VNSTOCK_API_KEY"] = VNSTOCK_API_KEY
    os.environ["VNSTOCK_TOKEN"] = VNSTOCK_API_KEY
    os.environ["VNSTOCK_KEY"] = VNSTOCK_API_KEY
    os.environ["VNSTOCK_INTERACTIVE"] = "0"
    os.environ["VNSTOCK_LANGUAGE"] = "2"

WATCHLIST = ["HPG","MWG","FPT","VCB","MBB","TCB","ACB","SSI","HCM","VND","VHM","KDH","VIC","VRE","GAS","PVD","DGC","GMD","CTR","FRT","VNM","MSN","DGW","VJC"]

SECTORS = {"HPG":"Thép / Công nghiệp","MWG":"Bán lẻ","FPT":"Công nghệ","VCB":"Ngân hàng","MBB":"Ngân hàng","TCB":"Ngân hàng","ACB":"Ngân hàng","SSI":"Chứng khoán","HCM":"Chứng khoán","VND":"Chứng khoán","VHM":"Bất động sản","KDH":"Bất động sản","VIC":"Bất động sản / Tập đoàn","VRE":"Bất động sản bán lẻ","GAS":"Dầu khí / Năng lượng","PVD":"Dầu khí","DGC":"Hóa chất","GMD":"Logistics / Cảng biển","CTR":"Hạ tầng viễn thông","FRT":"Bán lẻ","VNM":"Tiêu dùng phòng thủ","MSN":"Tiêu dùng","DGW":"Phân phối / Công nghệ","VJC":"Hàng không"}
NAMES = {"HPG":"Tập đoàn Hòa Phát","MWG":"Thế Giới Di Động","FPT":"FPT Corp","VCB":"Vietcombank","MBB":"Ngân hàng Quân đội","TCB":"Techcombank","ACB":"Ngân hàng Á Châu","SSI":"Chứng khoán SSI","HCM":"Chứng khoán HSC","VND":"Chứng khoán VNDIRECT","VHM":"Vinhomes","KDH":"Khang Điền","VIC":"Vingroup","VRE":"Vincom Retail","GAS":"PV GAS","PVD":"PV Drilling","DGC":"Hóa chất Đức Giang","GMD":"Gemadept","CTR":"Viettel Construction","FRT":"FPT Retail","VNM":"Vinamilk","MSN":"Masan Group","DGW":"Digiworld","VJC":"Vietjet Air"}

END_DATE = datetime.now(VN_TZ).strftime("%Y-%m-%d")
START_DATE = (datetime.now(VN_TZ) - timedelta(days=480)).strftime("%Y-%m-%d")

def try_activate_key() -> list[str]:
    logs = []
    if not VNSTOCK_API_KEY:
        logs.append("VNSTOCK_API_KEY is missing.")
        return logs

    # Một số phiên bản Vnstock có register_user; gọi có tham số nếu hỗ trợ.
    try:
        from vnstock import register_user
        for kwargs in ({"api_key": VNSTOCK_API_KEY}, {"token": VNSTOCK_API_KEY}, {"key": VNSTOCK_API_KEY}):
            try:
                register_user(**kwargs)
                logs.append(f"register_user success with {list(kwargs.keys())[0]}")
                return logs
            except TypeError:
                continue
            except Exception as exc:
                logs.append(f"register_user failed: {type(exc).__name__}: {exc}")
    except Exception as exc:
        logs.append(f"cannot import register_user: {type(exc).__name__}: {exc}")

    logs.append("Using VNSTOCK_API_KEY from environment only.")
    return logs

def safe_float(x: Any, ndigits: int = 2) -> float | None:
    try:
        if x is None or pd.isna(x):
            return None
        return round(float(x), ndigits)
    except Exception:
        return None

def normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    lower = {str(c).lower().strip(): c for c in df.columns}
    aliases = {
        "time": ["time","date","tradingdate","trading_date"],
        "close": ["close","closeprice","matchprice","price"],
        "volume": ["volume","nmvolume","total_volume","matchingvolume"]
    }
    rename = {}
    for target, keys in aliases.items():
        for k in keys:
            if k in lower:
                rename[lower[k]] = target
                break
    df = df.rename(columns=rename)
    if "time" not in df.columns:
        df["time"] = range(len(df))
    if "close" not in df.columns:
        raise ValueError(f"Missing close column. Columns={list(df.columns)}")
    if "volume" not in df.columns:
        df["volume"] = 0
    df["close"] = pd.to_numeric(df["close"], errors="coerce")
    df["volume"] = pd.to_numeric(df["volume"], errors="coerce").fillna(0)
    df = df.dropna(subset=["close"]).reset_index(drop=True)
    if len(df) and df["close"].median() < 1000:
        df["close"] *= 1000
    return df

def rsi(series: pd.Series, period: int = 14) -> pd.Series:
    delta = series.diff()
    gain = delta.clip(lower=0).rolling(period).mean()
    loss = (-delta.clip(upper=0)).rolling(period).mean()
    rs = gain / loss.replace(0, pd.NA)
    return 100 - (100 / (1 + rs))

def macd(series: pd.Series):
    ema12 = series.ewm(span=12, adjust=False).mean()
    ema26 = series.ewm(span=26, adjust=False).mean()
    line = ema12 - ema26
    signal = line.ewm(span=9, adjust=False).mean()
    return line, signal

def fetch_history(symbol: str):
    attempts: list[tuple[str, Callable[[], pd.DataFrame]]] = []

    # API mới hơn: Quote
    try:
        from vnstock import Quote
        for src in ["KBS", "VCI", "TCBS", "VND", "kbs", "vci", "tcbs", "vnd"]:
            attempts.append((f"vnstock.Quote/{src}", lambda src=src: Quote(symbol=symbol, source=src).history(start=START_DATE, end=END_DATE, interval="1D")))
    except Exception:
        pass

    # Một số bản có class Vnstock.
    try:
        from vnstock import Vnstock
        for src in ["KBS", "VCI", "TCBS", "kbs", "vci", "tcbs"]:
            attempts.append((f"vnstock.Vnstock/{src}", lambda src=src: Vnstock().stock(symbol=symbol, source=src).quote.history(start=START_DATE, end=END_DATE, interval="1D")))
    except Exception:
        pass

    # Hàm cũ.
    try:
        from vnstock import stock_historical_data
        attempts.append(("vnstock.stock_historical_data", lambda: stock_historical_data(symbol=symbol, start_date=START_DATE, end_date=END_DATE, resolution="1D", type="stock")))
    except Exception:
        pass

    errors = []
    for name, fn in attempts:
        try:
            df = normalize_columns(fn())
            if len(df) >= 60:
                return df, name
            errors.append(f"{name}: too few rows {len(df)}")
        except Exception as exc:
            errors.append(f"{name}: {type(exc).__name__}: {exc}")

    raise RuntimeError(" | ".join(errors[:10]) or "No Vnstock fetch method available")

def score_stock(symbol: str, df: pd.DataFrame, src: str) -> dict[str, Any]:
    close = df["close"]
    volume = df["volume"]
    df["ma20"] = close.rolling(20).mean()
    df["ma50"] = close.rolling(50).mean()
    df["ma200"] = close.rolling(200).mean()
    df["rsi14"] = rsi(close)
    df["macd"], df["macd_signal"] = macd(close)
    df["vol20"] = volume.rolling(20).mean()
    df["high20"] = close.rolling(20).max()

    last = df.iloc[-1]
    c = float(last["close"])
    prev20 = float(df.iloc[-21]["close"]) if len(df) > 21 else float(df.iloc[0]["close"])
    prev60 = float(df.iloc[-61]["close"]) if len(df) > 61 else float(df.iloc[0]["close"])
    ma20, ma50, ma200 = safe_float(last.get("ma20"),0), safe_float(last.get("ma50"),0), safe_float(last.get("ma200"),0)
    rsi14, macd_line, macd_sig = safe_float(last.get("rsi14")), safe_float(last.get("macd")), safe_float(last.get("macd_signal"))
    v = float(last["volume"]) if pd.notna(last.get("volume")) else 0
    vol20 = float(last["vol20"]) if pd.notna(last.get("vol20")) else 0
    high20 = float(last["high20"]) if pd.notna(last.get("high20")) else c
    ret20 = round((c / prev20 - 1) * 100, 2) if prev20 else 0
    ret60 = round((c / prev60 - 1) * 100, 2) if prev60 else 0
    vol_ratio = v / vol20 if vol20 else 1

    score = 50
    if ma20 and c > ma20: score += 8
    if ma50 and c > ma50: score += 8
    if ma200 and c > ma200: score += 8
    if rsi14 is not None:
        if 45 <= rsi14 <= 68: score += 10
        elif 68 < rsi14 <= 75: score += 4
        elif rsi14 > 78: score -= 8
        elif rsi14 < 35: score -= 5
    if macd_line is not None and macd_sig is not None and macd_line > macd_sig: score += 8
    if high20 and c >= high20 * 0.97: score += 8
    if vol_ratio >= 1.5: score += 7
    elif vol_ratio >= 1.1: score += 4
    if ret20 > 18: score -= 8
    if ma50 and c < ma50: score -= 10
    score = max(0, min(100, round(score, 1)))

    if score >= 82:
        action, allocation = "MUA TỪNG PHẦN", "15% - 25%"
    elif score >= 74:
        action, allocation = "CANH MUA / MUA KHI XÁC NHẬN", "10% - 15%"
    elif score >= 65:
        action, allocation = "THEO DÕI MUA", "5% - 10%"
    else:
        action, allocation = "CHỜ THÊM", "0% - 5%"

    signals = []
    if ma20 and c > ma20: signals.append("giá trên MA20")
    if ma50 and c > ma50: signals.append("giá trên MA50")
    if ma200 and c > ma200: signals.append("giá trên MA200")
    if rsi14 and 45 <= rsi14 <= 68: signals.append("RSI hợp lý")
    if macd_line and macd_sig and macd_line > macd_sig: signals.append("MACD tích cực")
    if vol_ratio >= 1.1: signals.append("thanh khoản cải thiện")
    volume_status = "Rất cao" if vol_ratio >= 1.5 else "Tốt" if vol_ratio >= 1.1 else "Trung bình"

    return {
        "ticker": symbol, "name": NAMES.get(symbol, symbol), "sector": SECTORS.get(symbol, "Khác"),
        "score": score, "action": action,
        "risk": "Cao" if symbol in {"SSI","HCM","VND","PVD","VHM","KDH","VJC"} else "Trung bình",
        "close": safe_float(c,0), "rsi14": rsi14, "ret20": ret20, "ret60": ret60,
        "volume_status": volume_status, "ma20": ma20, "ma50": ma50, "ma200": ma200,
        "macd": macd_line, "macd_signal": macd_sig,
        "reason": f"{symbol} đạt {score}/100 điểm: " + (", ".join(signals) if signals else "chưa có nhiều tín hiệu xác nhận") + f". Nguồn: {src}.",
        "buyZone": f"Canh quanh MA20 ~ {int(ma20):,} hoặc nền tích lũy gần nhất.".replace(",", ".") if ma20 else "Canh khi hình thành nền giá rõ.",
        "stopLoss": "-7% đến -10% tùy biến động",
        "takeProfit": "+12% đến +25% hoặc dùng trailing stop",
        "allocation": allocation,
        "catalysts": ["Vnstock API", "Xu hướng kỹ thuật", SECTORS.get(symbol, "Dòng tiền ngành")],
        "cautions": ["Không mua đuổi sau phiên tăng mạnh", "Cắt lỗ đúng kỷ luật", "Kiểm tra VN-Index trước khi giải ngân"],
    }

def fallback_data(errors: dict[str, str], activation_logs: list[str]):
    stocks = []
    for i, symbol in enumerate(WATCHLIST):
        score = round(max(45, min(90, 86 - i*1.2 + (i%4)*1.7)), 1)
        action = "MUA TỪNG PHẦN" if score >= 82 else "CANH MUA / MUA KHI XÁC NHẬN" if score >= 74 else "THEO DÕI MUA" if score >= 65 else "CHỜ THÊM"
        stocks.append({
            "ticker": symbol, "name": NAMES.get(symbol, symbol), "sector": SECTORS.get(symbol, "Khác"),
            "score": score, "action": action, "risk": "Cao" if symbol in {"SSI","HCM","VND","PVD","VHM","KDH","VJC"} else "Trung bình",
            "close": 20000+i*2500, "rsi14": round(48+(i%8)*3,2), "ret20": round(-3+(i%10)*1.4,2), "ret60": round(-5+(i%12)*1.8,2),
            "volume_status": "Mẫu", "ma20": 19500+i*2450, "ma50": 19000+i*2400, "ma200": 18000+i*2300,
            "macd": None, "macd_signal": None,
            "reason": f"Dữ liệu mẫu cho {symbol}. Vnstock API chưa lấy được dữ liệu trên GitHub Actions.",
            "buyZone": "Kiểm tra log GitHub Actions hoặc meta.errors.", "stopLoss": "-7% đến -10%", "takeProfit": "+12% đến +25%",
            "allocation": "5% - 20%", "catalysts": ["Fallback sample", SECTORS.get(symbol,"Ngành")],
            "cautions": ["Đây là dữ liệu mẫu", "Không dùng để giao dịch thật", "Kiểm tra workflow log"]
        })
    return {
        "meta": {
            "updated_at": datetime.now(VN_TZ).strftime("%Y-%m-%d %H:%M:%S VN"),
            "source": "fallback sample",
            "has_api_key": bool(VNSTOCK_API_KEY),
            "note": "Vnstock API lỗi nên dùng dữ liệu mẫu đủ WATCHLIST. Xem errors để sửa.",
            "activation_logs": activation_logs,
            "errors": errors,
        },
        "stocks": stocks,
    }

def main():
    activation_logs = try_activate_key()
    print("Activation logs:", activation_logs)

    results = []
    errors = {}
    for symbol in WATCHLIST:
        try:
            df, src = fetch_history(symbol)
            item = score_stock(symbol, df, src)
            results.append(item)
            print(f"OK {symbol}: {item['score']} via {src}")
        except Exception as exc:
            errors[symbol] = str(exc)
            print(f"ERROR {symbol}: {exc}")

    if results:
        results = sorted(results, key=lambda x: x.get("score", 0), reverse=True)
        data = {
            "meta": {
                "updated_at": datetime.now(VN_TZ).strftime("%Y-%m-%d %H:%M:%S VN"),
                "source": "Vnstock API",
                "has_api_key": bool(VNSTOCK_API_KEY),
                "success": len(results),
                "universe": len(WATCHLIST),
                "note": "Dữ liệu lấy qua Vnstock với VNSTOCK_API_KEY trong GitHub Secrets.",
                "activation_logs": activation_logs,
                "errors": errors,
            },
            "stocks": results,
        }
    else:
        data = fallback_data(errors, activation_logs)

    Path("data.json").write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Wrote data.json: {len(data['stocks'])} stocks. Source={data['meta']['source']}")

if __name__ == "__main__":
    main()
