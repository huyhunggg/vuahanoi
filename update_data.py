from __future__ import annotations

import json
import os
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Callable

import pandas as pd

VN_TZ = timezone(timedelta(hours=7))
VNSTOCK_API_KEY = os.getenv("VNSTOCK_API_KEY", "").strip()

if VNSTOCK_API_KEY:
    os.environ["VNSTOCK_API_KEY"] = VNSTOCK_API_KEY
    os.environ["VNSTOCK_TOKEN"] = VNSTOCK_API_KEY
    os.environ["VNSTOCK_KEY"] = VNSTOCK_API_KEY
    os.environ["VNSTOCK_INTERACTIVE"] = "0"
    os.environ["VNSTOCK_LANGUAGE"] = "2"

WATCHLIST = [
    "VCB","BID","CTG","TCB","MBB","ACB","VPB","STB","HDB","VIB",
    "SHB","LPB","MSB","EIB","OCB","TPB","SSB","NAB","BAB","BVB",

    "HPG","HSG","NKG","TLH","SMC","VGS",

    "FPT","CMG","ELC","CTR","VGI","FOX","SAM","ITD",

    "MWG","FRT","DGW","PNJ","PET","PSD","AST","SVC",

    "SSI","VND","HCM","VCI","MBS","FTS","BSI","CTS","SHS","ORS",
    "AGR","APG","VDS","BVS",

    "VHM","VIC","VRE","KDH","NLG","DXG","PDR","DIG","CEO","NVL",
    "TCH","SCR","HDC","HDG","KBC","SZC","BCM","IDC","VGC","IJC",
    "CII","NBB","NTL","SIP","TIP","LHG",

    "GAS","PVD","PVS","PLX","BSR","OIL","PVC","PVB","PVT","PVP",

    "DGC","DCM","DPM","CSV","LAS","DDV","BFC","GVR","PHR","DPR",
    "DRC","BMP","NTP","AAA","DHC","GIL","TNG","MSH","TCM",

    "VNM","MSN","MCH","SAB","KDC","QNS","DBC","BAF","PAN","TAR",
    "ANV","VHC","IDI","ASM","HAG","HNG","SBT",

    "GMD","HAH","VSC","SGP","PHP","VOS","VTO","SKG",

    "VJC","HVN","ACV","SCS","NCT","SAS","CIA",

    "REE","PC1","GEX","POW","NT2","QTP","PPC"
]

NAMES = {
    "VCB":"Vietcombank","BID":"BIDV","CTG":"VietinBank","TCB":"Techcombank","MBB":"Ngân hàng Quân đội",
    "ACB":"Ngân hàng Á Châu","VPB":"VPBank","STB":"Sacombank","HDB":"HDBank","VIB":"VIB",
    "SHB":"SHB","LPB":"LPBank","MSB":"MSB","EIB":"Eximbank","OCB":"OCB","TPB":"TPBank",
    "SSB":"SeABank","NAB":"Nam A Bank","BAB":"Bac A Bank","BVB":"VietCapital Bank",

    "HPG":"Tập đoàn Hòa Phát","HSG":"Hoa Sen Group","NKG":"Thép Nam Kim","TLH":"Thép Tiến Lên",
    "SMC":"SMC Trading","VGS":"Ống thép Việt Đức",

    "FPT":"FPT Corp","CMG":"CMC Corp","ELC":"ELCOM","CTR":"Viettel Construction","VGI":"Viettel Global",
    "FOX":"FPT Telecom","SAM":"SAM Holdings","ITD":"Công nghệ Tiên Phong",

    "MWG":"Thế Giới Di Động","FRT":"FPT Retail","DGW":"Digiworld","PNJ":"Vàng bạc Đá quý Phú Nhuận",
    "PET":"Petrosetco","PSD":"PSD","AST":"Taseco Air Services","SVC":"Savico",

    "SSI":"Chứng khoán SSI","VND":"VNDIRECT","HCM":"Chứng khoán HSC","VCI":"Vietcap",
    "MBS":"Chứng khoán MB","FTS":"Chứng khoán FPT","BSI":"Chứng khoán BIDV","CTS":"Chứng khoán VietinBank",
    "SHS":"Chứng khoán Sài Gòn Hà Nội","ORS":"Chứng khoán Tiên Phong","AGR":"Agriseco",
    "APG":"APG Securities","VDS":"Rồng Việt Securities","BVS":"Bảo Việt Securities",

    "VHM":"Vinhomes","VIC":"Vingroup","VRE":"Vincom Retail","KDH":"Khang Điền","NLG":"Nam Long",
    "DXG":"Đất Xanh","PDR":"Phát Đạt","DIG":"DIC Corp","CEO":"CEO Group","NVL":"Novaland",
    "TCH":"Hoàng Huy","SCR":"Sacomreal","HDC":"Hodeco","HDG":"Hà Đô","KBC":"Kinh Bắc",
    "SZC":"Sonadezi Châu Đức","BCM":"Becamex IDC","IDC":"IDICO","VGC":"Viglacera","IJC":"Becamex IJC",
    "CII":"CII","NBB":"577 Investment","NTL":"Lideco","SIP":"SIP Corp","TIP":"Tin Nghĩa IP","LHG":"Long Hậu",

    "GAS":"PV GAS","PVD":"PV Drilling","PVS":"PTSC","PLX":"Petrolimex","BSR":"Lọc hóa dầu Bình Sơn",
    "OIL":"PV Oil","PVC":"PVChem","PVB":"PV Coating","PVT":"PVTrans","PVP":"PVTrans Pacific",

    "DGC":"Hóa chất Đức Giang","DCM":"Đạm Cà Mau","DPM":"Đạm Phú Mỹ","CSV":"Hóa chất Cơ bản Miền Nam",
    "LAS":"Supe Lâm Thao","DDV":"DAP Vinachem","BFC":"Phân bón Bình Điền","GVR":"Tập đoàn Cao su Việt Nam",
    "PHR":"Cao su Phước Hòa","DPR":"Cao su Đồng Phú","DRC":"Cao su Đà Nẵng","BMP":"Nhựa Bình Minh",
    "NTP":"Nhựa Tiền Phong","AAA":"An Phát Bioplastics","DHC":"Đông Hải Bến Tre","GIL":"Gilimex",
    "TNG":"TNG Investment","MSH":"May Sông Hồng","TCM":"Dệt may Thành Công",

    "VNM":"Vinamilk","MSN":"Masan Group","MCH":"Masan Consumer","SAB":"Sabeco","KDC":"KIDO",
    "QNS":"Đường Quảng Ngãi","DBC":"Dabaco","BAF":"BAF Việt Nam","PAN":"PAN Group","TAR":"Trung An",
    "ANV":"Nam Việt","VHC":"Vĩnh Hoàn","IDI":"IDI Corp","ASM":"Sao Mai Group","HAG":"Hoàng Anh Gia Lai",
    "HNG":"HAGL Agrico","SBT":"Thành Thành Công Biên Hòa",

    "GMD":"Gemadept","HAH":"Hải An","VSC":"Viconship","SGP":"Cảng Sài Gòn","PHP":"Cảng Hải Phòng",
    "VOS":"Vosco","VTO":"VITACO","SKG":"Superdong",

    "VJC":"Vietjet Air","HVN":"Vietnam Airlines","ACV":"Tổng công ty Cảng HKVN","SCS":"SCSC",
    "NCT":"Nội Bài Cargo","SAS":"Dịch vụ Hàng không Tân Sơn Nhất","CIA":"Cam Ranh Airport Services",

    "REE":"REE Corp","PC1":"PC1 Group","GEX":"Gelex","POW":"PV Power","NT2":"Nhiệt điện Nhơn Trạch 2",
    "QTP":"Nhiệt điện Quảng Ninh","PPC":"Nhiệt điện Phả Lại"
}

SECTORS = {}

for s in ["VCB","BID","CTG","TCB","MBB","ACB","VPB","STB","HDB","VIB","SHB","LPB","MSB","EIB","OCB","TPB","SSB","NAB","BAB","BVB"]:
    SECTORS[s] = "Ngân hàng"

for s in ["HPG","HSG","NKG","TLH","SMC","VGS"]:
    SECTORS[s] = "Thép / Công nghiệp"

for s in ["FPT","CMG","ELC","CTR","VGI","FOX","SAM","ITD"]:
    SECTORS[s] = "Công nghệ / Viễn thông"

for s in ["MWG","FRT","DGW","PNJ","PET","PSD","AST","SVC"]:
    SECTORS[s] = "Bán lẻ / Phân phối"

for s in ["SSI","VND","HCM","VCI","MBS","FTS","BSI","CTS","SHS","ORS","AGR","APG","VDS","BVS"]:
    SECTORS[s] = "Chứng khoán"

for s in ["VHM","VIC","VRE","KDH","NLG","DXG","PDR","DIG","CEO","NVL","TCH","SCR","HDC","HDG","KBC","SZC","BCM","IDC","VGC","IJC","CII","NBB","NTL","SIP","TIP","LHG"]:
    SECTORS[s] = "Bất động sản / KCN"

for s in ["GAS","PVD","PVS","PLX","BSR","OIL","PVC","PVB","PVT","PVP"]:
    SECTORS[s] = "Dầu khí / Năng lượng"

for s in ["DGC","DCM","DPM","CSV","LAS","DDV","BFC","GVR","PHR","DPR","DRC","BMP","NTP","AAA","DHC","GIL","TNG","MSH","TCM"]:
    SECTORS[s] = "Hóa chất / Vật liệu / Dệt may"

for s in ["VNM","MSN","MCH","SAB","KDC","QNS","DBC","BAF","PAN","TAR","ANV","VHC","IDI","ASM","HAG","HNG","SBT"]:
    SECTORS[s] = "Tiêu dùng / Nông nghiệp / Thủy sản"

for s in ["GMD","HAH","VSC","SGP","PHP","VOS","VTO","SKG"]:
    SECTORS[s] = "Logistics / Cảng biển"

for s in ["VJC","HVN","ACV","SCS","NCT","SAS","CIA"]:
    SECTORS[s] = "Hàng không / Dịch vụ sân bay"

for s in ["REE","PC1","GEX","POW","NT2","QTP","PPC"]:
    SECTORS[s] = "Điện / Hạ tầng"

END_DATE = datetime.now(VN_TZ).strftime("%Y-%m-%d")
START_DATE = (datetime.now(VN_TZ) - timedelta(days=480)).strftime("%Y-%m-%d")


def try_activate_key() -> list[str]:
    logs = []

    if not VNSTOCK_API_KEY:
        logs.append("VNSTOCK_API_KEY is missing.")
        return logs

    try:
        from vnstock import register_user

        for kwargs in (
            {"api_key": VNSTOCK_API_KEY},
            {"token": VNSTOCK_API_KEY},
            {"key": VNSTOCK_API_KEY},
        ):
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
        "time": ["time", "date", "tradingdate", "trading_date"],
        "close": ["close", "closeprice", "matchprice", "price"],
        "volume": ["volume", "nmvolume", "total_volume", "matchingvolume"],
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

    # Một số nguồn trả giá dạng nghìn đồng, ví dụ 28.5 thay vì 28500.
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

    try:
        from vnstock import Quote

        for src in ["KBS", "VCI", "TCBS", "VND", "kbs", "vci", "tcbs", "vnd"]:
            attempts.append(
                (
                    f"vnstock.Quote/{src}",
                    lambda src=src: Quote(symbol=symbol, source=src).history(
                        start=START_DATE,
                        end=END_DATE,
                        interval="1D",
                    ),
                )
            )
    except Exception:
        pass

    try:
        from vnstock import Vnstock

        for src in ["KBS", "VCI", "TCBS", "kbs", "vci", "tcbs"]:
            attempts.append(
                (
                    f"vnstock.Vnstock/{src}",
                    lambda src=src: Vnstock()
                    .stock(symbol=symbol, source=src)
                    .quote.history(
                        start=START_DATE,
                        end=END_DATE,
                        interval="1D",
                    ),
                )
            )
    except Exception:
        pass

    try:
        from vnstock import stock_historical_data

        attempts.append(
            (
                "vnstock.stock_historical_data",
                lambda: stock_historical_data(
                    symbol=symbol,
                    start_date=START_DATE,
                    end_date=END_DATE,
                    resolution="1D",
                    type="stock",
                ),
            )
        )
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

    raise RuntimeError(" | ".join(errors[:8]) or "No Vnstock fetch method available")


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

    ma20 = safe_float(last.get("ma20"), 0)
    ma50 = safe_float(last.get("ma50"), 0)
    ma200 = safe_float(last.get("ma200"), 0)

    rsi14 = safe_float(last.get("rsi14"))
    macd_line = safe_float(last.get("macd"))
    macd_sig = safe_float(last.get("macd_signal"))

    v = float(last["volume"]) if pd.notna(last.get("volume")) else 0
    vol20 = float(last["vol20"]) if pd.notna(last.get("vol20")) else 0
    high20 = float(last["high20"]) if pd.notna(last.get("high20")) else c

    ret20 = round((c / prev20 - 1) * 100, 2) if prev20 else 0
    ret60 = round((c / prev60 - 1) * 100, 2) if prev60 else 0

    vol_ratio = v / vol20 if vol20 else 1

    # Scoring đã siết lại, tối đa 95 để tránh quá nhiều mã 100/100.
    score = 45

    if ma20 and c > ma20:
        score += 7
    if ma50 and c > ma50:
        score += 7
    if ma200 and c > ma200:
        score += 6

    if rsi14 is not None:
        if 48 <= rsi14 <= 62:
            score += 8
        elif 42 <= rsi14 < 48 or 62 < rsi14 <= 70:
            score += 4
        elif rsi14 > 75:
            score -= 10
        elif rsi14 < 35:
            score -= 6

    if macd_line is not None and macd_sig is not None and macd_line > macd_sig:
        score += 7

    if high20 and c >= high20 * 0.985:
        score += 5

    if vol_ratio >= 1.5:
        score += 6
    elif vol_ratio >= 1.15:
        score += 3

    if ret20 > 16:
        score -= 8
    if ret20 > 25:
        score -= 8
    if ret60 > 45:
        score -= 6

    if ma50 and c < ma50:
        score -= 10
    if ma200 and c < ma200:
        score -= 6

    score = max(0, min(95, round(score, 1)))

    if score >= 82:
        action = "MUA TỪNG PHẦN"
        allocation = "10% - 20%"
    elif score >= 74:
        action = "CANH MUA / MUA KHI XÁC NHẬN"
        allocation = "7% - 15%"
    elif score >= 65:
        action = "THEO DÕI MUA"
        allocation = "3% - 10%"
    else:
        action = "CHỜ THÊM"
        allocation = "0% - 5%"

    signals = []

    if ma20 and c > ma20:
        signals.append("giá trên MA20")
    if ma50 and c > ma50:
        signals.append("giá trên MA50")
    if ma200 and c > ma200:
        signals.append("giá trên MA200")
    if rsi14 and 48 <= rsi14 <= 62:
        signals.append("RSI đẹp")
    elif rsi14 and rsi14 > 70:
        signals.append("RSI hơi nóng")
    if macd_line and macd_sig and macd_line > macd_sig:
        signals.append("MACD tích cực")
    if vol_ratio >= 1.15:
        signals.append("thanh khoản cải thiện")

    volume_status = "Rất cao" if vol_ratio >= 1.5 else "Tốt" if vol_ratio >= 1.15 else "Trung bình"

    buy_zone = (
        f"Canh quanh MA20 ~ {int(ma20):,} hoặc nền tích lũy gần nhất.".replace(",", ".")
        if ma20
        else "Canh khi hình thành nền giá rõ."
    )

    return {
        "ticker": symbol,
        "name": NAMES.get(symbol, symbol),
        "sector": SECTORS.get(symbol, "Khác"),
        "score": score,
        "action": action,
        "risk": "Cao" if SECTORS.get(symbol, "").startswith(("Chứng khoán", "Bất động sản", "Dầu khí")) else "Trung bình",
        "close": safe_float(c, 0),
        "rsi14": rsi14,
        "ret20": ret20,
        "ret60": ret60,
        "volume_status": volume_status,
        "ma20": ma20,
        "ma50": ma50,
        "ma200": ma200,
        "macd": macd_line,
        "macd_signal": macd_sig,
        "reason": f"{symbol} đạt {score}/100 điểm: "
        + (", ".join(signals) if signals else "chưa có nhiều tín hiệu xác nhận")
        + f". Nguồn: {src}.",
        "buyZone": buy_zone,
        "stopLoss": "-7% đến -10% tùy biến động",
        "takeProfit": "+12% đến +25% hoặc dùng trailing stop",
        "allocation": allocation,
        "catalysts": [
            "Vnstock API",
            "Xu hướng kỹ thuật",
            SECTORS.get(symbol, "Dòng tiền ngành"),
        ],
        "cautions": [
            "Không mua đuổi sau phiên tăng mạnh",
            "Cắt lỗ đúng kỷ luật",
            "Kiểm tra VN-Index trước khi giải ngân",
        ],
    }


def fallback_data(errors: dict[str, str], activation_logs: list[str]):
    stocks = []

    for i, symbol in enumerate(WATCHLIST):
        score = round(max(35, min(86, 78 - (i % 17) * 1.1 + (i % 5) * 1.8)), 1)

        if score >= 82:
            action = "MUA TỪNG PHẦN"
        elif score >= 74:
            action = "CANH MUA / MUA KHI XÁC NHẬN"
        elif score >= 65:
            action = "THEO DÕI MUA"
        else:
            action = "CHỜ THÊM"

        stocks.append(
            {
                "ticker": symbol,
                "name": NAMES.get(symbol, symbol),
                "sector": SECTORS.get(symbol, "Khác"),
                "score": score,
                "action": action,
                "risk": "Cao" if SECTORS.get(symbol, "").startswith(("Chứng khoán", "Bất động sản", "Dầu khí")) else "Trung bình",
                "close": 20000 + i * 800,
                "rsi14": round(42 + (i % 18) * 1.7, 2),
                "ret20": round(-8 + (i % 21) * 0.9, 2),
                "ret60": round(-12 + (i % 25) * 1.2, 2),
                "volume_status": "Mẫu",
                "ma20": 19500 + i * 790,
                "ma50": 19000 + i * 780,
                "ma200": 18000 + i * 760,
                "macd": None,
                "macd_signal": None,
                "reason": f"Dữ liệu mẫu cho {symbol}. Vnstock API chưa lấy được dữ liệu trên GitHub Actions.",
                "buyZone": "Kiểm tra log GitHub Actions hoặc meta.errors.",
                "stopLoss": "-7% đến -10%",
                "takeProfit": "+12% đến +25%",
                "allocation": "5% - 20%",
                "catalysts": [
                    "Fallback sample",
                    SECTORS.get(symbol, "Ngành"),
                ],
                "cautions": [
                    "Đây là dữ liệu mẫu",
                    "Không dùng để giao dịch thật",
                    "Kiểm tra workflow log",
                ],
            }
        )

    return {
        "meta": {
            "updated_at": datetime.now(VN_TZ).strftime("%Y-%m-%d %H:%M:%S VN"),
            "source": "fallback sample top 150",
            "has_api_key": bool(VNSTOCK_API_KEY),
            "success": 0,
            "universe": len(WATCHLIST),
            "note": "Vnstock API lỗi nên dùng dữ liệu mẫu đủ top 150. Xem errors để sửa.",
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
                "source": "Vnstock API top 150",
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

    Path("data.json").write_text(
        json.dumps(data, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    print(f"Wrote data.json: {len(data['stocks'])} stocks. Source={data['meta']['source']}")


if __name__ == "__main__":
    main()
