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
    "VCB",
    "BID",
    "CTG",
    "TCB",
    "MBB",
    "ACB",
    "VPB",
    "STB",
    "HDB",
    "VIB",
    "SHB",
    "LPB",
    "MSB",
    "EIB",
    "OCB",
    "TPB",
    "SSB",
    "NAB",
    "BAB",
    "BVB",
    "HPG",
    "HSG",
    "NKG",
    "TLH",
    "SMC",
    "VGS",
    "FPT",
    "CMG",
    "ELC",
    "CTR",
    "VGI",
    "FOX",
    "SAM",
    "ITD",
    "MWG",
    "FRT",
    "DGW",
    "PNJ",
    "PET",
    "PSD",
    "AST",
    "SVC",
    "SSI",
    "VND",
    "HCM",
    "VCI",
    "MBS",
    "FTS",
    "BSI",
    "CTS",
    "SHS",
    "ORS",
    "AGR",
    "APG",
    "VDS",
    "BVS",
    "VHM",
    "VIC",
    "VRE",
    "KDH",
    "NLG",
    "DXG",
    "PDR",
    "DIG",
    "CEO",
    "NVL",
    "TCH",
    "SCR",
    "HDC",
    "HDG",
    "KBC",
    "SZC",
    "BCM",
    "IDC",
    "VGC",
    "IJC",
    "CII",
    "NBB",
    "NTL",
    "SIP",
    "TIP",
    "LHG",
    "GAS",
    "PVD",
    "PVS",
    "PLX",
    "BSR",
    "OIL",
    "PVC",
    "PVB",
    "PVT",
    "PVP",
    "DGC",
    "DCM",
    "DPM",
    "CSV",
    "LAS",
    "DDV",
    "BFC",
    "GVR",
    "PHR",
    "DPR",
    "DRC",
    "BMP",
    "NTP",
    "AAA",
    "DHC",
    "GIL",
    "TNG",
    "MSH",
    "TCM",
    "VNM",
    "MSN",
    "MCH",
    "SAB",
    "KDC",
    "QNS",
    "DBC",
    "BAF",
    "PAN",
    "TAR",
    "ANV",
    "VHC",
    "IDI",
    "ASM",
    "HAG",
    "HNG",
    "SBT",
    "GMD",
    "HAH",
    "VSC",
    "SGP",
    "PHP",
    "VOS",
    "VTO",
    "SKG",
    "VJC",
    "HVN",
    "ACV",
    "SCS",
    "NCT",
    "SAS",
    "CIA",
    "REE",
    "PC1",
    "GEX",
    "POW",
    "NT2",
    "QTP",
    "PPC"
]
NAMES = {
    "VCB": "Vietcombank",
    "BID": "BIDV",
    "CTG": "VietinBank",
    "TCB": "Techcombank",
    "MBB": "Ngân hàng Quân đội",
    "ACB": "Ngân hàng Á Châu",
    "VPB": "VPBank",
    "STB": "Sacombank",
    "HDB": "HDBank",
    "VIB": "VIB",
    "SHB": "SHB",
    "LPB": "LPBank",
    "MSB": "MSB",
    "EIB": "Eximbank",
    "OCB": "OCB",
    "TPB": "TPBank",
    "SSB": "SeABank",
    "NAB": "Nam A Bank",
    "BAB": "Bac A Bank",
    "BVB": "VietCapital Bank",
    "HPG": "Tập đoàn Hòa Phát",
    "HSG": "Hoa Sen Group",
    "NKG": "Thép Nam Kim",
    "TLH": "Thép Tiến Lên",
    "SMC": "SMC Trading",
    "VGS": "Ống thép Việt Đức",
    "FPT": "FPT Corp",
    "CMG": "CMC Corp",
    "ELC": "ELCOM",
    "CTR": "Viettel Construction",
    "VGI": "Viettel Global",
    "FOX": "FPT Telecom",
    "SAM": "SAM Holdings",
    "ITD": "Công nghệ Tiên Phong",
    "MWG": "Thế Giới Di Động",
    "FRT": "FPT Retail",
    "DGW": "Digiworld",
    "PNJ": "Vàng bạc Đá quý Phú Nhuận",
    "PET": "Petrosetco",
    "PSD": "PSD",
    "AST": "Taseco Air Services",
    "SVC": "Savico",
    "SSI": "Chứng khoán SSI",
    "VND": "VNDIRECT",
    "HCM": "Chứng khoán HSC",
    "VCI": "Vietcap",
    "MBS": "Chứng khoán MB",
    "FTS": "Chứng khoán FPT",
    "BSI": "Chứng khoán BIDV",
    "CTS": "Chứng khoán VietinBank",
    "SHS": "Chứng khoán Sài Gòn Hà Nội",
    "ORS": "Chứng khoán Tiên Phong",
    "AGR": "Agriseco",
    "APG": "APG Securities",
    "VDS": "Rồng Việt Securities",
    "BVS": "Bảo Việt Securities",
    "VHM": "Vinhomes",
    "VIC": "Vingroup",
    "VRE": "Vincom Retail",
    "KDH": "Khang Điền",
    "NLG": "Nam Long",
    "DXG": "Đất Xanh",
    "PDR": "Phát Đạt",
    "DIG": "DIC Corp",
    "CEO": "CEO Group",
    "NVL": "Novaland",
    "TCH": "Hoàng Huy",
    "SCR": "Sacomreal",
    "HDC": "Hodeco",
    "HDG": "Hà Đô",
    "KBC": "Kinh Bắc",
    "SZC": "Sonadezi Châu Đức",
    "BCM": "Becamex IDC",
    "IDC": "IDICO",
    "VGC": "Viglacera",
    "IJC": "Becamex IJC",
    "CII": "CII",
    "NBB": "577 Investment",
    "NTL": "Lideco",
    "SIP": "SIP Corp",
    "TIP": "Tin Nghĩa IP",
    "LHG": "Long Hậu",
    "GAS": "PV GAS",
    "PVD": "PV Drilling",
    "PVS": "PTSC",
    "PLX": "Petrolimex",
    "BSR": "Lọc hóa dầu Bình Sơn",
    "OIL": "PV Oil",
    "PVC": "PVChem",
    "PVB": "PV Coating",
    "PVT": "PVTrans",
    "PVP": "PVTrans Pacific",
    "DGC": "Hóa chất Đức Giang",
    "DCM": "Đạm Cà Mau",
    "DPM": "Đạm Phú Mỹ",
    "CSV": "Hóa chất Cơ bản Miền Nam",
    "LAS": "Supe Lâm Thao",
    "DDV": "DAP Vinachem",
    "BFC": "Phân bón Bình Điền",
    "GVR": "Tập đoàn Cao su Việt Nam",
    "PHR": "Cao su Phước Hòa",
    "DPR": "Cao su Đồng Phú",
    "DRC": "Cao su Đà Nẵng",
    "BMP": "Nhựa Bình Minh",
    "NTP": "Nhựa Tiền Phong",
    "AAA": "An Phát Bioplastics",
    "DHC": "Đông Hải Bến Tre",
    "GIL": "Gilimex",
    "TNG": "TNG Investment",
    "MSH": "May Sông Hồng",
    "TCM": "Dệt may Thành Công",
    "VNM": "Vinamilk",
    "MSN": "Masan Group",
    "MCH": "Masan Consumer",
    "SAB": "Sabeco",
    "KDC": "KIDO",
    "QNS": "Đường Quảng Ngãi",
    "DBC": "Dabaco",
    "BAF": "BAF Việt Nam",
    "PAN": "PAN Group",
    "TAR": "Trung An",
    "ANV": "Nam Việt",
    "VHC": "Vĩnh Hoàn",
    "IDI": "IDI Corp",
    "ASM": "Sao Mai Group",
    "HAG": "Hoàng Anh Gia Lai",
    "HNG": "HAGL Agrico",
    "SBT": "Thành Thành Công Biên Hòa",
    "GMD": "Gemadept",
    "HAH": "Hải An",
    "VSC": "Viconship",
    "SGP": "Cảng Sài Gòn",
    "PHP": "Cảng Hải Phòng",
    "VOS": "Vosco",
    "VTO": "VITACO",
    "SKG": "Superdong",
    "VJC": "Vietjet Air",
    "HVN": "Vietnam Airlines",
    "ACV": "Tổng công ty Cảng HKVN",
    "SCS": "SCSC",
    "NCT": "Nội Bài Cargo",
    "SAS": "Dịch vụ Hàng không Tân Sơn Nhất",
    "CIA": "Cam Ranh Airport Services",
    "REE": "REE Corp",
    "PC1": "PC1 Group",
    "GEX": "Gelex",
    "POW": "PV Power",
    "NT2": "Nhiệt điện Nhơn Trạch 2",
    "QTP": "Nhiệt điện Quảng Ninh",
    "PPC": "Nhiệt điện Phả Lại"
}
SECTORS = {
    "VCB": "Ngân hàng",
    "BID": "Ngân hàng",
    "CTG": "Ngân hàng",
    "TCB": "Ngân hàng",
    "MBB": "Ngân hàng",
    "ACB": "Ngân hàng",
    "VPB": "Ngân hàng",
    "STB": "Ngân hàng",
    "HDB": "Ngân hàng",
    "VIB": "Ngân hàng",
    "SHB": "Ngân hàng",
    "LPB": "Ngân hàng",
    "MSB": "Ngân hàng",
    "EIB": "Ngân hàng",
    "OCB": "Ngân hàng",
    "TPB": "Ngân hàng",
    "SSB": "Ngân hàng",
    "NAB": "Ngân hàng",
    "BAB": "Ngân hàng",
    "BVB": "Ngân hàng",
    "HPG": "Thép / Công nghiệp",
    "HSG": "Thép / Công nghiệp",
    "NKG": "Thép / Công nghiệp",
    "TLH": "Thép / Công nghiệp",
    "SMC": "Thép / Công nghiệp",
    "VGS": "Thép / Công nghiệp",
    "FPT": "Công nghệ / Viễn thông",
    "CMG": "Công nghệ / Viễn thông",
    "ELC": "Công nghệ / Viễn thông",
    "CTR": "Công nghệ / Viễn thông",
    "VGI": "Công nghệ / Viễn thông",
    "FOX": "Công nghệ / Viễn thông",
    "SAM": "Công nghệ / Viễn thông",
    "ITD": "Công nghệ / Viễn thông",
    "MWG": "Bán lẻ / Phân phối",
    "FRT": "Bán lẻ / Phân phối",
    "DGW": "Bán lẻ / Phân phối",
    "PNJ": "Bán lẻ / Phân phối",
    "PET": "Bán lẻ / Phân phối",
    "PSD": "Bán lẻ / Phân phối",
    "AST": "Bán lẻ / Phân phối",
    "SVC": "Bán lẻ / Phân phối",
    "SSI": "Chứng khoán",
    "VND": "Chứng khoán",
    "HCM": "Chứng khoán",
    "VCI": "Chứng khoán",
    "MBS": "Chứng khoán",
    "FTS": "Chứng khoán",
    "BSI": "Chứng khoán",
    "CTS": "Chứng khoán",
    "SHS": "Chứng khoán",
    "ORS": "Chứng khoán",
    "AGR": "Chứng khoán",
    "APG": "Chứng khoán",
    "VDS": "Chứng khoán",
    "BVS": "Chứng khoán",
    "VHM": "Bất động sản / KCN",
    "VIC": "Bất động sản / KCN",
    "VRE": "Bất động sản / KCN",
    "KDH": "Bất động sản / KCN",
    "NLG": "Bất động sản / KCN",
    "DXG": "Bất động sản / KCN",
    "PDR": "Bất động sản / KCN",
    "DIG": "Bất động sản / KCN",
    "CEO": "Bất động sản / KCN",
    "NVL": "Bất động sản / KCN",
    "TCH": "Bất động sản / KCN",
    "SCR": "Bất động sản / KCN",
    "HDC": "Bất động sản / KCN",
    "HDG": "Bất động sản / KCN",
    "KBC": "Bất động sản / KCN",
    "SZC": "Bất động sản / KCN",
    "BCM": "Bất động sản / KCN",
    "IDC": "Bất động sản / KCN",
    "VGC": "Bất động sản / KCN",
    "IJC": "Bất động sản / KCN",
    "CII": "Bất động sản / KCN",
    "NBB": "Bất động sản / KCN",
    "NTL": "Bất động sản / KCN",
    "SIP": "Bất động sản / KCN",
    "TIP": "Bất động sản / KCN",
    "LHG": "Bất động sản / KCN",
    "GAS": "Dầu khí / Năng lượng",
    "PVD": "Dầu khí / Năng lượng",
    "PVS": "Dầu khí / Năng lượng",
    "PLX": "Dầu khí / Năng lượng",
    "BSR": "Dầu khí / Năng lượng",
    "OIL": "Dầu khí / Năng lượng",
    "PVC": "Dầu khí / Năng lượng",
    "PVB": "Dầu khí / Năng lượng",
    "PVT": "Dầu khí / Năng lượng",
    "PVP": "Dầu khí / Năng lượng",
    "DGC": "Hóa chất / Vật liệu / Dệt may",
    "DCM": "Hóa chất / Vật liệu / Dệt may",
    "DPM": "Hóa chất / Vật liệu / Dệt may",
    "CSV": "Hóa chất / Vật liệu / Dệt may",
    "LAS": "Hóa chất / Vật liệu / Dệt may",
    "DDV": "Hóa chất / Vật liệu / Dệt may",
    "BFC": "Hóa chất / Vật liệu / Dệt may",
    "GVR": "Hóa chất / Vật liệu / Dệt may",
    "PHR": "Hóa chất / Vật liệu / Dệt may",
    "DPR": "Hóa chất / Vật liệu / Dệt may",
    "DRC": "Hóa chất / Vật liệu / Dệt may",
    "BMP": "Hóa chất / Vật liệu / Dệt may",
    "NTP": "Hóa chất / Vật liệu / Dệt may",
    "AAA": "Hóa chất / Vật liệu / Dệt may",
    "DHC": "Hóa chất / Vật liệu / Dệt may",
    "GIL": "Hóa chất / Vật liệu / Dệt may",
    "TNG": "Hóa chất / Vật liệu / Dệt may",
    "MSH": "Hóa chất / Vật liệu / Dệt may",
    "TCM": "Hóa chất / Vật liệu / Dệt may",
    "VNM": "Tiêu dùng / Nông nghiệp / Thủy sản",
    "MSN": "Tiêu dùng / Nông nghiệp / Thủy sản",
    "MCH": "Tiêu dùng / Nông nghiệp / Thủy sản",
    "SAB": "Tiêu dùng / Nông nghiệp / Thủy sản",
    "KDC": "Tiêu dùng / Nông nghiệp / Thủy sản",
    "QNS": "Tiêu dùng / Nông nghiệp / Thủy sản",
    "DBC": "Tiêu dùng / Nông nghiệp / Thủy sản",
    "BAF": "Tiêu dùng / Nông nghiệp / Thủy sản",
    "PAN": "Tiêu dùng / Nông nghiệp / Thủy sản",
    "TAR": "Tiêu dùng / Nông nghiệp / Thủy sản",
    "ANV": "Tiêu dùng / Nông nghiệp / Thủy sản",
    "VHC": "Tiêu dùng / Nông nghiệp / Thủy sản",
    "IDI": "Tiêu dùng / Nông nghiệp / Thủy sản",
    "ASM": "Tiêu dùng / Nông nghiệp / Thủy sản",
    "HAG": "Tiêu dùng / Nông nghiệp / Thủy sản",
    "HNG": "Tiêu dùng / Nông nghiệp / Thủy sản",
    "SBT": "Tiêu dùng / Nông nghiệp / Thủy sản",
    "GMD": "Logistics / Cảng biển",
    "HAH": "Logistics / Cảng biển",
    "VSC": "Logistics / Cảng biển",
    "SGP": "Logistics / Cảng biển",
    "PHP": "Logistics / Cảng biển",
    "VOS": "Logistics / Cảng biển",
    "VTO": "Logistics / Cảng biển",
    "SKG": "Logistics / Cảng biển",
    "VJC": "Hàng không / Dịch vụ sân bay",
    "HVN": "Hàng không / Dịch vụ sân bay",
    "ACV": "Hàng không / Dịch vụ sân bay",
    "SCS": "Hàng không / Dịch vụ sân bay",
    "NCT": "Hàng không / Dịch vụ sân bay",
    "SAS": "Hàng không / Dịch vụ sân bay",
    "CIA": "Hàng không / Dịch vụ sân bay",
    "REE": "Điện / Hạ tầng",
    "PC1": "Điện / Hạ tầng",
    "GEX": "Điện / Hạ tầng",
    "POW": "Điện / Hạ tầng",
    "NT2": "Điện / Hạ tầng",
    "QTP": "Điện / Hạ tầng",
    "PPC": "Điện / Hạ tầng"
}

END_DATE = datetime.now(VN_TZ).strftime("%Y-%m-%d")
START_DATE = (datetime.now(VN_TZ) - timedelta(days=520)).strftime("%Y-%m-%d")

def try_activate_key() -> list[str]:
    logs = []
    if not VNSTOCK_API_KEY:
        logs.append("VNSTOCK_API_KEY is missing.")
        return logs
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
        "time": ["time", "date", "tradingdate", "trading_date"],
        "open": ["open", "openprice"],
        "high": ["high", "highestprice"],
        "low": ["low", "lowestprice"],
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
    for col in ["open", "high", "low"]:
        if col not in df.columns:
            df[col] = df["close"]
    if "volume" not in df.columns:
        df["volume"] = 0
    for col in ["open", "high", "low", "close", "volume"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    df["volume"] = df["volume"].fillna(0)
    df = df.dropna(subset=["close"]).reset_index(drop=True)
    if len(df) and df["close"].median() < 1000:
        for col in ["open", "high", "low", "close"]:
            df[col] *= 1000
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

def atr(df: pd.DataFrame, period: int = 14) -> pd.Series:
    high_low = df["high"] - df["low"]
    high_close = (df["high"] - df["close"].shift()).abs()
    low_close = (df["low"] - df["close"].shift()).abs()
    tr = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
    return tr.rolling(period).mean()

def fetch_history(symbol: str):
    attempts: list[tuple[str, Callable[[], pd.DataFrame]]] = []
    try:
        from vnstock import Quote
        for src in ["KBS", "VCI", "TCBS", "VND", "kbs", "vci", "tcbs", "vnd"]:
            attempts.append((f"vnstock.Quote/{src}", lambda src=src: Quote(symbol=symbol, source=src).history(start=START_DATE, end=END_DATE, interval="1D")))
    except Exception:
        pass
    try:
        from vnstock import Vnstock
        for src in ["KBS", "VCI", "TCBS", "kbs", "vci", "tcbs"]:
            attempts.append((f"vnstock.Vnstock/{src}", lambda src=src: Vnstock().stock(symbol=symbol, source=src).quote.history(start=START_DATE, end=END_DATE, interval="1D")))
    except Exception:
        pass
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
    raise RuntimeError(" | ".join(errors[:8]) or "No Vnstock fetch method available")

def clamp(v, lo, hi):
    return max(lo, min(hi, v))



def build_cycle_plan(
    symbol: str,
    c: float,
    ma20: float | None,
    ma50: float | None,
    ma100: float | None,
    ma200: float | None,
    rsi14: float | None,
    macd_line: float | None,
    macd_sig: float | None,
    vol_ratio: float,
    distance_ma20: float | None,
    ret20: float,
    ret60: float,
    high20: float,
    low20: float,
    range20: float | None,
    close_pos: float,
    trend: float,
    momentum: float,
    money: float,
    risk_score: float,
    value_traded: float,
    df: pd.DataFrame,
):
    """Lọc mô hình chu kỳ tăng mới kiểu VIC: giảm/tích lũy dài, tạo đáy, vượt MA, MACD/RSI phục hồi, dòng tiền quay lại."""
    checklist = []

    # 1. Giảm sâu hoặc tích lũy kéo dài 3-6 tháng
    lookback_120 = df.tail(120).copy()
    lookback_180 = df.tail(180).copy()
    high_120 = float(lookback_120["close"].max()) if len(lookback_120) else c
    low_120 = float(lookback_120["close"].min()) if len(lookback_120) else c
    drawdown_120 = round((c / high_120 - 1) * 100, 2) if high_120 else 0
    recovery_from_low_120 = round((c / low_120 - 1) * 100, 2) if low_120 else 0
    range_120 = round((high_120 / low_120 - 1) * 100, 2) if low_120 else 0

    long_base = bool((range_120 <= 35 and len(lookback_120) >= 90) or drawdown_120 <= -25 or (recovery_from_low_120 >= 10 and drawdown_120 <= -10))
    checklist.append({"label": "Đã giảm sâu hoặc tích lũy 3–6 tháng", "ok": long_base})

    # 2. Đáy sau cao hơn đáy trước, đỉnh sau cao hơn đỉnh trước
    lows = df["close"].rolling(10).min()
    highs = df["close"].rolling(10).max()
    higher_low = bool(len(lows.dropna()) > 40 and lows.iloc[-1] > lows.iloc[-25])
    higher_high = bool(len(highs.dropna()) > 40 and highs.iloc[-1] >= highs.iloc[-25])
    structure_up = higher_low and higher_high
    checklist.append({"label": "Cấu trúc đáy sau/đỉnh sau cải thiện", "ok": structure_up})

    # 3. Vượt lại MA20/50, tiến tới MA100/200
    reclaim_ma = bool(ma20 and ma50 and c > ma20 and c > ma50)
    near_long_ma = bool((ma100 and c > ma100 * 0.97) or (ma200 and c > ma200 * 0.94))
    checklist.append({"label": "Giá vượt MA20/MA50 và tiếp cận MA100/MA200", "ok": reclaim_ma and near_long_ma})

    # 4. MA20 cong lên/cắt lên MA50
    ma20_series = df["ma20"] if "ma20" in df.columns else df["close"].rolling(20).mean()
    ma50_series = df["ma50"] if "ma50" in df.columns else df["close"].rolling(50).mean()
    ma20_up = bool(len(ma20_series.dropna()) > 10 and ma20_series.iloc[-1] > ma20_series.iloc[-5])
    ma20_crossing = bool(ma20 and ma50 and (ma20 >= ma50 * 0.98))
    checklist.append({"label": "MA20 bắt đầu cong lên/gần cắt MA50", "ok": ma20_up and ma20_crossing})

    # 5-6. MACD cắt lên/Histogram từ âm sang dương
    macd_positive = bool(macd_line is not None and macd_sig is not None and macd_line >= macd_sig)
    macd_from_weak = bool(macd_line is not None and macd_sig is not None and macd_line < 0 and macd_line >= macd_sig)
    checklist.append({"label": "MACD cải thiện từ vùng yếu hoặc cắt lên Signal", "ok": macd_positive or macd_from_weak})

    # 7. RSI phục hồi > 50, lý tưởng 50-65
    rsi_recover = bool(rsi14 is not None and 50 <= rsi14 <= 65)
    rsi_ok = bool(rsi14 is not None and 48 <= rsi14 <= 70)
    checklist.append({"label": "RSI phục hồi trên 50, lý tưởng 50–65", "ok": rsi_recover})

    # 8-9. Volume breakout tăng, pullback volume thấp
    vol_breakout = bool(vol_ratio >= 1.3 and c >= high20 * 0.97)
    recent = df.tail(20).copy()
    recent["chg"] = recent["close"].pct_change()
    down_low_vol = False
    if "volume" in recent.columns:
        avg_vol = float(recent["volume"].mean()) if len(recent) else 0
        down_days = recent[recent["chg"] < 0]
        if len(down_days) > 0 and avg_vol > 0:
            down_low_vol = bool(down_days["volume"].median() <= avg_vol * 1.05)
    checklist.append({"label": "Volume tăng khi breakout, điều chỉnh volume thấp", "ok": vol_breakout or down_low_vol})

    # 10. Ichimoku proxy: giá trên vùng trung bình 26/52 hoặc test lại thành công
    tenkan = (df["high"].rolling(9).max() + df["low"].rolling(9).min()) / 2
    kijun = (df["high"].rolling(26).max() + df["low"].rolling(26).min()) / 2
    senkou_b = (df["high"].rolling(52).max() + df["low"].rolling(52).min()) / 2
    ichi_ok = False
    try:
        ichi_ok = bool(c > float(kijun.iloc[-1]) and c > min(float(kijun.iloc[-1]), float(senkou_b.iloc[-1])) and close_pos >= 0.45)
    except Exception:
        ichi_ok = bool(c > ma50) if ma50 else False
    checklist.append({"label": "Thoát vùng Ichimoku proxy hoặc test Kijun thành công", "ok": ichi_ok})

    # 11-12. Fundamental/catalyst proxy: không có dữ liệu cơ bản sâu -> chỉ dùng thanh khoản/ngành và flag cần bổ sung
    liquidity_ok = bool(value_traded >= 10_000_000_000)
    not_hot = bool(ret20 <= 20 and (distance_ma20 is None or distance_ma20 <= 15) and (rsi14 is None or rsi14 <= 70))
    checklist.append({"label": "Không tăng nóng, thanh khoản đủ để theo chu kỳ", "ok": liquidity_ok and not_hot})

    yes_count = sum(1 for x in checklist if x["ok"])
    cycle_score = round(yes_count / len(checklist) * 100, 1)

    early_stage = bool(
        yes_count >= 7
        and reclaim_ma
        and (macd_positive or macd_from_weak)
        and rsi_ok
        and liquidity_ok
        and not_hot
        and (long_base or structure_up)
    )

    if early_stage and c > ma50 and (not ma200 or c < ma200 * 1.15):
        stage = "Giai đoạn đầu xu hướng tăng mới"
    elif long_base and reclaim_ma:
        stage = "Đang xác nhận đảo chiều sau tích lũy"
    elif long_base:
        stage = "Đang tích lũy, chưa xác nhận"
    elif not_hot and trend >= 13:
        stage = "Xu hướng tăng nhưng cần kiểm tra đã qua giai đoạn đầu chưa"
    else:
        stage = "Chưa đạt mẫu chu kỳ tăng mới"

    probe = f"Thăm dò quanh MA20/MA50 nếu giữ nền; ưu tiên vùng gần MA20 ~ {int(ma20):,}".replace(",", ".") if ma20 else "Chỉ thăm dò khi hình thành hỗ trợ rõ"
    retest_buy = "Gia tăng khi retest MA20/MA50 hoặc nền breakout thành công, volume giảm trong nhịp chỉnh"
    breakout_buy = f"Mua xác nhận khi vượt vùng {int(high20):,} kèm volume >= 1.3–1.5 lần trung bình".replace(",", ".")
    protection = "Cắt lỗ nếu thủng MA50/nền tích lũy hoặc MACD quay đầu xấu; bảo vệ lợi nhuận bằng MA20 khi đã có lãi"

    # Target ước lượng theo biên độ nền/range
    base_height_pct = min(40, max(12, range_120 * 0.5 if range_120 else 15))
    targets = f"Target 1 +15%; Target 2 +25–35%; Target 3 nếu thành chu kỳ mạnh: +{round(base_height_pct + 35,0)}% hoặc trailing theo MA20/MA50"

    thesis = (
        "Mã có dấu hiệu thoát khỏi giai đoạn giảm/tích lũy, cấu trúc giá cải thiện và dòng tiền bắt đầu quay lại."
        if early_stage else
        "Mã chưa đủ xác nhận chu kỳ tăng mới; cần thêm tín hiệu về cấu trúc giá, dòng tiền hoặc MA dài hạn."
    )

    plan = {
        "score": cycle_score,
        "yesCount": yes_count,
        "totalChecks": len(checklist),
        "stage": stage,
        "thesis": thesis,
        "confirmation": "Cần duy trì trên MA20/MA50, MACD không quay đầu, RSI giữ trên 50 và volume xác nhận trong phiên breakout/retest",
        "probeBuy": probe,
        "retestBuy": retest_buy,
        "breakoutBuy": breakout_buy,
        "targets": targets,
        "protection": protection,
        "capitalPlan": "Mua thăm dò 20–30%, gia tăng 30–40% khi retest thành công, phần còn lại khi breakout xác nhận; không mua đuổi nếu cách MA20 > 12–15%",
        "fundamentalNote": "Cần bổ sung dữ liệu cơ bản/catalyst: doanh thu, lợi nhuận, ROE/ROA, nợ vay, dòng tiền kinh doanh, P/E, P/B, câu chuyện ngành/tái cấu trúc/dự án mới.",
        "checklist": checklist,
    }

    return early_stage, cycle_score, plan


def build_tplus_plan(symbol, c, ma20, ma50, rsi14, macd_line, macd_sig, vol_ratio, close_pos, distance_ma20, ret20, setupType, breakout, pullback, retest, accumulation, trend, momentum, money, risk_score, value_traded):
    checklist = []

    cond_market_proxy = trend >= 12
    checklist.append({"label": "VN-Index/xu hướng không quá yếu", "ok": bool(cond_market_proxy)})

    cond_ma = bool(ma20 and ma50 and c >= ma20 and c >= ma50)
    checklist.append({"label": "Giá nằm trên MA20 và MA50", "ok": cond_ma})

    cond_macd = bool(macd_line is not None and macd_sig is not None and macd_line >= macd_sig)
    checklist.append({"label": "MACD cắt lên/đang trên Signal", "ok": cond_macd})

    cond_rsi_best = bool(rsi14 is not None and 52 <= rsi14 <= 65)
    cond_rsi_ok = bool(rsi14 is not None and 48 <= rsi14 <= 70)
    checklist.append({"label": "RSI nằm vùng đẹp 52–65", "ok": cond_rsi_best})

    cond_volume = bool(vol_ratio >= 1.2)
    checklist.append({"label": "Volume cao hơn trung bình 20 phiên", "ok": cond_volume})

    cond_setup = bool(breakout or pullback or retest or accumulation)
    checklist.append({"label": "Có điểm mua: breakout/pullback/retest/tích lũy", "ok": cond_setup})

    cond_not_chase = bool((distance_ma20 is None or distance_ma20 <= 10) and ret20 <= 20)
    checklist.append({"label": "Không mua đuổi: giá không cách MA20 quá xa", "ok": cond_not_chase})

    cond_liquidity = bool(value_traded >= 5_000_000_000)
    checklist.append({"label": "Thanh khoản đủ để đánh T+", "ok": cond_liquidity})

    if ma20:
        stop_price = min(c * 0.965, ma20 * 0.985)
    else:
        stop_price = c * 0.965

    risk_pct = max(1.0, round((c / stop_price - 1) * 100, 2))
    target_pct = 7.0 if breakout else 6.0 if (pullback or retest) else 5.5
    rr = round(target_pct / risk_pct, 2) if risk_pct else 0
    cond_rr = rr >= 1.5 and risk_pct <= 5.0
    checklist.append({"label": "Risk/Reward >= 1.5 và stop dưới 5%", "ok": cond_rr})

    yes_count = sum(1 for x in checklist if x["ok"])
    checklist_score = round(yes_count / len(checklist) * 100, 1)

    tplus_ok = (
        yes_count >= 7
        and cond_ma
        and cond_macd
        and cond_rsi_ok
        and cond_volume
        and cond_setup
        and cond_not_chase
        and cond_rr
        and risk_score >= 8
        and money >= 13
        and momentum >= 8
    )

    if breakout:
        strategy = "Breakout T+ có volume xác nhận"
        entry = "Mua khi giữ trên vùng breakout, close gần cao nhất phiên và volume >= 1.3 lần trung bình"
    elif pullback:
        strategy = "Pullback MA20 trong xu hướng tăng"
        entry = "Mua khi giá bật lại quanh MA20/MA10, volume tăng trở lại sau nhịp giảm volume thấp"
    elif retest:
        strategy = "Retest nền/MA20 thành công"
        entry = "Mua khi retest không thủng nền, nến đóng trên hỗ trợ và lực bán yếu"
    elif accumulation:
        strategy = "Tích lũy biên hẹp chờ nổ volume"
        entry = "Chỉ mua khi vượt biên trên nền tích lũy kèm volume xác nhận"
    else:
        strategy = "Chưa đủ setup T+ xác suất cao"
        entry = "Chờ thêm tín hiệu MACD/volume/setup, không mua vì thấy xanh mạnh"

    plan = {
        "score": checklist_score,
        "yesCount": yes_count,
        "totalChecks": len(checklist),
        "strategy": strategy,
        "entry": entry,
        "quickStop": f"Cắt nhanh quanh {int(stop_price):,} hoặc khi mất MA20/vùng breakout; risk khoảng {risk_pct}%".replace(",", "."),
        "quickTakeProfit": f"TP1 +{round(target_pct*0.65,1)}% đến +{target_pct}%; đạt TP1 chốt 30–50%, phần còn lại kéo stop lên giá vốn/MA10",
        "riskReward": f"{rr}:1, risk ~{risk_pct}%, target ~{target_pct}%",
        "positionSizing": "Lệnh thăm dò 20–30%, lệnh xác nhận 50–70%, lệnh rất đẹp tối đa 100% vị thế dự kiến" if tplus_ok else "Chỉ theo dõi hoặc thăm dò rất nhỏ; chưa đủ điều kiện T+ xác suất cao",
        "holdingPeriod": "T+3 đến T+10; sau 2–3 phiên không chạy thì giảm tỷ trọng",
        "invalidCondition": "MACD quay đầu xấu, RSI > 70 khi chưa có nền, volume cao nhưng râu trên dài, giá thủng MA20/MA50, hoặc VN-Index gãy hỗ trợ",
        "checklist": checklist,
    }
    return tplus_ok, checklist_score, plan


def score_stock(symbol: str, df: pd.DataFrame, src: str, market_ret20: float | None, market_ret60: float | None, sector_ret20: float | None) -> dict[str, Any]:
    close = df["close"]
    volume = df["volume"]

    df["ma20"] = close.rolling(20).mean()
    df["ma50"] = close.rolling(50).mean()
    df["ma100"] = close.rolling(100).mean()
    df["ma200"] = close.rolling(200).mean()
    df["rsi14"] = rsi(close)
    df["macd"], df["macd_signal"] = macd(close)
    df["atr14"] = atr(df)
    df["vol20"] = volume.rolling(20).mean()
    df["high20"] = close.rolling(20).max()
    df["low20"] = close.rolling(20).min()
    df["range20"] = (df["high"].rolling(20).max() - df["low"].rolling(20).min()) / close * 100

    last = df.iloc[-1]
    prev = df.iloc[-2] if len(df) > 1 else last
    c = float(last["close"])
    prev_close = float(prev["close"])
    prev20 = float(df.iloc[-21]["close"]) if len(df) > 21 else float(df.iloc[0]["close"])
    prev60 = float(df.iloc[-61]["close"]) if len(df) > 61 else float(df.iloc[0]["close"])

    ma20, ma50, ma100, ma200 = [safe_float(last.get(k),0) for k in ["ma20","ma50","ma100","ma200"]]
    rsi14, macd_line, macd_sig, atr14 = [safe_float(last.get(k)) for k in ["rsi14","macd","macd_signal","atr14"]]
    v = float(last["volume"]) if pd.notna(last.get("volume")) else 0
    vol20 = float(last["vol20"]) if pd.notna(last.get("vol20")) else 0
    high20 = float(last["high20"]) if pd.notna(last.get("high20")) else c
    low20 = float(last["low20"]) if pd.notna(last.get("low20")) else c
    range20 = safe_float(last.get("range20"))
    ret20 = round((c / prev20 - 1) * 100, 2) if prev20 else 0
    ret60 = round((c / prev60 - 1) * 100, 2) if prev60 else 0
    day_change = round((c / prev_close - 1) * 100, 2) if prev_close else 0
    vol_ratio = round(v / vol20, 2) if vol20 else 1
    distance_ma20 = round((c / ma20 - 1) * 100, 2) if ma20 else None
    distance_ma50 = round((c / ma50 - 1) * 100, 2) if ma50 else None
    close_pos = round((float(last["close"]) - float(last["low"])) / max(1, float(last["high"]) - float(last["low"])), 2)

    # Trend 20
    trend = 0
    if ma20 and c > ma20: trend += 4
    if ma50 and c > ma50: trend += 4
    if ma100 and c > ma100: trend += 3
    if ma200 and c > ma200: trend += 4
    if ma20 and ma50 and ma20 > ma50: trend += 3
    if ma50 and ma200 and ma50 > ma200: trend += 2

    # Momentum 15
    momentum = 0
    if rsi14 is not None:
        if 50 <= rsi14 <= 65: momentum += 5
        elif 45 <= rsi14 < 50 or 65 < rsi14 <= 70: momentum += 3
        elif rsi14 > 75: momentum -= 5
    if macd_line is not None and macd_sig is not None and macd_line > macd_sig: momentum += 4
    if 3 <= ret20 <= 15: momentum += 2
    if high20 and c >= high20 * 0.985 and (rsi14 is None or rsi14 < 75): momentum += 2
    if ret20 > 20: momentum -= 5
    if ret60 > 40: momentum -= 5
    if distance_ma20 is not None and distance_ma20 > 15: momentum -= 4
    momentum = clamp(momentum, 0, 15)

    # Money Flow 20
    money = 0
    if vol_ratio >= 1.5: money += 6
    elif vol_ratio >= 1.2: money += 4
    if day_change > 0 and vol_ratio >= 1.15: money += 5
    if close_pos >= 0.65: money += 3
    up_big = 0
    down_big = 0
    recent = df.tail(20).copy()
    recent["chg"] = recent["close"].pct_change()
    recent["vol_avg"] = recent["volume"].rolling(10).mean()
    up_big = int(((recent["chg"] > 0) & (recent["volume"] > recent["vol_avg"])).sum())
    down_big = int(((recent["chg"] < 0) & (recent["volume"] > recent["vol_avg"])).sum())
    if up_big > down_big: money += 4
    value_traded = c * v
    if value_traded >= 20_000_000_000: money += 2
    if vol_ratio >= 1.8 and day_change <= 0.5: money -= 5
    if day_change < -3 and vol_ratio >= 1.3: money -= 6
    money = clamp(money, 0, 20)

    # Setup 15
    setup = 0
    setupType = "Chưa có setup rõ"
    breakout = bool(high20 and c >= high20 * 0.995 and vol_ratio >= 1.3 and (rsi14 is None or rsi14 < 75))
    pullback = bool(ma20 and ma50 and c > ma50 and ma20 > ma50 and distance_ma20 is not None and -2 <= distance_ma20 <= 5 and (rsi14 is None or 45 <= rsi14 <= 68))
    retest = bool(ma20 and ma50 and c > ma50 and distance_ma20 is not None and 0 <= distance_ma20 <= 3 and close_pos >= 0.55)
    reclaim_ma50 = bool(ma50 and c > ma50 and float(prev["close"]) <= ma50 and vol_ratio >= 1.1)
    accumulation = bool(range20 is not None and range20 <= 10 and ma50 and c >= ma50 and ret20 < 12)

    if breakout:
        setup, setupType = 14, "Breakout 20 phiên"
    elif pullback:
        setup, setupType = 12, "Pullback MA20"
    elif retest:
        setup, setupType = 11, "Retest nền / MA20"
    elif reclaim_ma50:
        setup, setupType = 9, "Vượt lại MA50"
    elif accumulation:
        setup, setupType = 9, "Tích lũy biên hẹp"
    else:
        setup = 5 if trend >= 12 else 2

    # Risk 15, càng cao càng an toàn
    risk_score = 0
    if distance_ma20 is not None and distance_ma20 < 7: risk_score += 3
    if rsi14 is None or rsi14 < 70: risk_score += 3
    if ret20 < 15: risk_score += 3
    if ma50 and c > ma50: risk_score += 3
    if value_traded >= 10_000_000_000: risk_score += 2
    if atr14 and c and (atr14 / c * 100) < 5: risk_score += 1
    if distance_ma20 is not None and distance_ma20 > 15: risk_score -= 5
    if rsi14 and rsi14 > 75: risk_score -= 5
    if ma50 and c < ma50: risk_score -= 5
    if ma200 and c < ma200: risk_score -= 5
    if value_traded < 3_000_000_000: risk_score -= 4
    risk_score = clamp(risk_score, 0, 15)

    # Relative strength 15
    rs = 0
    if market_ret20 is not None and ret20 > market_ret20: rs += 4
    if market_ret60 is not None and ret60 > market_ret60: rs += 4
    if sector_ret20 is not None and ret20 > sector_ret20: rs += 4
    if ret20 >= 8 or ret60 >= 15: rs += 3
    rs = clamp(rs, 0, 15)

    total = clamp(round(trend + momentum + money + setup + risk_score + rs, 1), 0, 95)

    tplus_ok, tplus_score, tplus_plan = build_tplus_plan(
        symbol, c, ma20, ma50, rsi14, macd_line, macd_sig, vol_ratio, close_pos, distance_ma20, ret20,
        setupType, breakout, pullback, retest, accumulation, trend, momentum, money, risk_score, value_traded
    )

    cycle_ok, cycle_score, cycle_plan = build_cycle_plan(
        symbol=symbol,
        c=c,
        ma20=ma20,
        ma50=ma50,
        ma100=safe_float(last.get("ma100"),0),
        ma200=ma200,
        rsi14=rsi14,
        macd_line=macd_line,
        macd_sig=macd_sig,
        vol_ratio=vol_ratio,
        distance_ma20=distance_ma20,
        ret20=ret20,
        ret60=ret60,
        high20=high20,
        low20=low20,
        range20=range20,
        close_pos=close_pos,
        trend=trend,
        momentum=momentum,
        money=money,
        risk_score=risk_score,
        value_traded=value_traded,
        df=df,
    )

    filters = {
        "topOpportunity": total >= 78 and trend >= 14 and money >= 12 and risk_score >= 9,
        "cycleTurnaround": cycle_ok,
        "tplus": tplus_ok,
        "breakout": breakout,
        "pullbackMA20": pullback,
        "moneyFlow": money >= 14,
        "accumulation": accumulation,
        "safe": risk_score >= 12 and total >= 65,
    }

    if total >= 82 and trend >= 16 and money >= 14 and risk_score >= 10 and not (distance_ma20 and distance_ma20 > 12):
        action, allocation = "MUA TỪNG PHẦN", "10% - 20%"
    elif total >= 74:
        action, allocation = "CANH MUA / MUA KHI XÁC NHẬN", "7% - 15%"
    elif total >= 65:
        action, allocation = "THEO DÕI MUA", "3% - 10%"
    elif total >= 55:
        action, allocation = "CHỜ THÊM", "0% - 5%"
    else:
        action, allocation = "TRÁNH MUA MỚI", "0%"

    signals, warnings = [], []
    if trend >= 16: signals.append("Xu hướng tích cực, giá duy trì trên các đường MA quan trọng")
    if ma20 and ma50 and ma20 > ma50: signals.append("MA20 nằm trên MA50, cấu trúc ngắn hạn tốt")
    if macd_line and macd_sig and macd_line > macd_sig: signals.append("MACD đang trên đường tín hiệu")
    if money >= 14: signals.append("Dòng tiền cải thiện so với trung bình")
    if breakout: signals.append("Có tín hiệu breakout vùng 20 phiên")
    if pullback: signals.append("Có setup pullback MA20 trong xu hướng tăng")
    if accumulation: signals.append("Biên độ 20 phiên thu hẹp, có dấu hiệu tích lũy")
    if filters.get("cycleTurnaround"):
        signals.append(f"Đạt bộ lọc Chu kỳ tăng mới: {cycle_plan.get('yesCount',0)}/{cycle_plan.get('totalChecks',0)} tiêu chí")
    elif cycle_plan.get("yesCount",0) >= 6:
        warnings.append(f"Gần đạt mẫu Chu kỳ tăng mới: {cycle_plan.get('yesCount',0)}/{cycle_plan.get('totalChecks',0)} tiêu chí, cần thêm xác nhận")
    if filters.get("tplus"):
        signals.append(f"Đạt bộ lọc T+ Pro: {tplus_plan.get('yesCount',0)}/{tplus_plan.get('totalChecks',0)} tiêu chí")
    elif total >= 72 and money >= 13:
        warnings.append(f"Có dòng tiền nhưng chưa đủ T+ Pro: {tplus_plan.get('yesCount',0)}/{tplus_plan.get('totalChecks',0)} tiêu chí")

    if rsi14 and rsi14 > 70: warnings.append("RSI cao, hạn chế mua đuổi")
    if distance_ma20 and distance_ma20 > 12: warnings.append(f"Giá cách MA20 {distance_ma20}%, nên chờ điều chỉnh")
    if ret20 > 20: warnings.append(f"Giá đã tăng {ret20}% trong 20 phiên, rủi ro hưng phấn")
    if ma50 and c < ma50: warnings.append("Giá dưới MA50, chưa đủ điều kiện mua mới")
    if value_traded < 3_000_000_000: warnings.append("Thanh khoản thấp, cần hạn chế tỷ trọng")
    if not signals: signals.append("Chưa có nhiều tín hiệu xác nhận rõ ràng")

    marketState = "Uptrend mạnh" if trend >= 17 else "Tích cực" if trend >= 13 else "Trung tính" if trend >= 8 else "Yếu"

    buyZone = f"Canh quanh MA20 ~ {int(ma20):,} hoặc nền tích lũy gần nhất.".replace(",", ".") if ma20 else "Chờ hình thành nền giá rõ."
    expertSummary = f"{symbol} đạt {total}/100 điểm, setup {setupType}. Xu hướng {marketState.lower()}, dòng tiền {money}/20, rủi ro {risk_score}/15. Hành động phù hợp: {action.lower()}."

    return {
        "ticker": symbol, "name": NAMES.get(symbol, symbol), "sector": SECTORS.get(symbol, "Khác"),
        "score": total,
        "subscores": {
            "trend": trend, "momentum": momentum, "moneyFlow": money,
            "setup": setup, "risk": risk_score, "relativeStrength": rs
        },
        "setupType": setupType,
        "marketState": marketState,
        "action": action,
        "risk": "Cao" if SECTORS.get(symbol,"").startswith(("Chứng khoán","Bất động sản","Dầu khí")) else "Trung bình",
        "close": safe_float(c,0), "rsi14": rsi14, "ret20": ret20, "ret60": ret60,
        "volume_status": "Rất cao" if vol_ratio >= 1.5 else "Tốt" if vol_ratio >= 1.15 else "Trung bình",
        "volumeRatio": vol_ratio, "ma20": ma20, "ma50": ma50, "ma100": safe_float(last.get("ma100"),0), "ma200": ma200,
        "macd": macd_line, "macd_signal": macd_sig, "atr14": atr14,
        "distanceToMA20": distance_ma20, "distanceToMA50": distance_ma50,
        "signals": signals, "warnings": warnings, "filters": filters, "tplusScore": tplus_score, "cycleScore": cycle_score,
        "reason": expertSummary,
        "expertSummary": expertSummary,
        "buyZone": buyZone,
        "stopLoss": "-7% đến -10% hoặc khi thủng MA50/nền hỗ trợ",
        "takeProfit": "+12% đến +25% hoặc dùng trailing stop theo MA20",
        "allocation": allocation,
        "tplusPlan": tplus_plan,
        "cyclePlan": cycle_plan,
        "catalysts": ["Vnstock API", "Tín hiệu kỹ thuật", SECTORS.get(symbol, "Dòng tiền ngành")],
        "cautions": warnings or ["Không mua đuổi; cần tuân thủ cắt lỗ"],
    }

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
                "macd": null,
                "macd_signal": null,
                "distanceToMA20": -3.5,
                "atr14": null,
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
                        "topOpportunity": false,
                        "breakout": false,
                        "pullbackMA20": true,
                        "moneyFlow": false,
                        "accumulation": false,
                        "safe": false
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
                "macd": null,
                "macd_signal": null,
                "distanceToMA20": -2.5,
                "atr14": null,
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
                        "topOpportunity": false,
                        "breakout": true,
                        "pullbackMA20": false,
                        "moneyFlow": false,
                        "accumulation": false,
                        "safe": false
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
                "macd": null,
                "macd_signal": null,
                "distanceToMA20": -1.5,
                "atr14": null,
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
                        "topOpportunity": false,
                        "breakout": false,
                        "pullbackMA20": false,
                        "moneyFlow": false,
                        "accumulation": true,
                        "safe": false
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
                "macd": null,
                "macd_signal": null,
                "distanceToMA20": -0.5,
                "atr14": null,
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
                        "topOpportunity": false,
                        "breakout": false,
                        "pullbackMA20": false,
                        "moneyFlow": false,
                        "accumulation": false,
                        "safe": false
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
                "macd": null,
                "macd_signal": null,
                "distanceToMA20": 0.5,
                "atr14": null,
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
                        "topOpportunity": false,
                        "breakout": false,
                        "pullbackMA20": false,
                        "moneyFlow": false,
                        "accumulation": false,
                        "safe": false
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
                "macd": null,
                "macd_signal": null,
                "distanceToMA20": 1.5,
                "atr14": null,
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
                        "topOpportunity": true,
                        "breakout": false,
                        "pullbackMA20": false,
                        "moneyFlow": true,
                        "accumulation": false,
                        "safe": true
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
                "macd": null,
                "macd_signal": null,
                "distanceToMA20": 2.5,
                "atr14": null,
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
                        "topOpportunity": false,
                        "breakout": false,
                        "pullbackMA20": true,
                        "moneyFlow": true,
                        "accumulation": false,
                        "safe": false
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
                "macd": null,
                "macd_signal": null,
                "distanceToMA20": 3.5,
                "atr14": null,
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
                        "topOpportunity": false,
                        "breakout": true,
                        "pullbackMA20": false,
                        "moneyFlow": false,
                        "accumulation": false,
                        "safe": false
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
                "macd": null,
                "macd_signal": null,
                "distanceToMA20": 4.5,
                "atr14": null,
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
                        "topOpportunity": false,
                        "breakout": false,
                        "pullbackMA20": false,
                        "moneyFlow": false,
                        "accumulation": true,
                        "safe": false
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
                "macd": null,
                "macd_signal": null,
                "distanceToMA20": 5.5,
                "atr14": null,
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
                        "topOpportunity": false,
                        "breakout": false,
                        "pullbackMA20": false,
                        "moneyFlow": false,
                        "accumulation": false,
                        "safe": false
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
        },
        {
                "ticker": "SHB",
                "name": "SHB",
                "sector": "Ngân hàng",
                "score": 69.5,
                "subscores": {
                        "trend": 18,
                        "momentum": 7.0,
                        "moneyFlow": 12.5,
                        "setup": 11.8,
                        "risk": 12.0,
                        "relativeStrength": 8.2
                },
                "setupType": "Vượt lại MA50",
                "marketState": "Uptrend",
                "action": "THEO DÕI MUA",
                "risk": "Trung bình",
                "close": 28000,
                "rsi14": 59.0,
                "ret20": 1.0,
                "ret60": 0.0,
                "volume_status": "Mẫu",
                "volumeRatio": 1.1,
                "ma20": 27400,
                "ma50": 26800,
                "ma200": 25600,
                "macd": null,
                "macd_signal": null,
                "distanceToMA20": 6.5,
                "atr14": null,
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
                        "topOpportunity": false,
                        "breakout": false,
                        "pullbackMA20": false,
                        "moneyFlow": false,
                        "accumulation": false,
                        "safe": true
                },
                "reason": "Dữ liệu mẫu cho SHB. Chạy GitHub Actions sau khi thêm VNSTOCK_API_KEY để cập nhật tín hiệu thật.",
                "expertSummary": "SHB đang ở trạng thái mẫu. Hệ thống sẽ cập nhật xu hướng, động lượng, dòng tiền, setup và rủi ro sau khi chạy Vnstock API.",
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
                "ticker": "LPB",
                "name": "LPBank",
                "sector": "Ngân hàng",
                "score": 76.0,
                "subscores": {
                        "trend": 20,
                        "momentum": 8.4,
                        "moneyFlow": 14.0,
                        "setup": 13.5,
                        "risk": 10.8,
                        "relativeStrength": 9.3
                },
                "setupType": "Chưa có setup rõ",
                "marketState": "Uptrend",
                "action": "CANH MUA / MUA KHI XÁC NHẬN",
                "risk": "Trung bình",
                "close": 28800,
                "rsi14": 60.7,
                "ret20": 1.9,
                "ret60": 1.2,
                "volume_status": "Mẫu",
                "volumeRatio": 1.25,
                "ma20": 28190,
                "ma50": 27580,
                "ma200": 26360,
                "macd": null,
                "macd_signal": null,
                "distanceToMA20": 7.5,
                "atr14": null,
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
                        "topOpportunity": false,
                        "breakout": false,
                        "pullbackMA20": false,
                        "moneyFlow": false,
                        "accumulation": false,
                        "safe": false
                },
                "reason": "Dữ liệu mẫu cho LPB. Chạy GitHub Actions sau khi thêm VNSTOCK_API_KEY để cập nhật tín hiệu thật.",
                "expertSummary": "LPB đang ở trạng thái mẫu. Hệ thống sẽ cập nhật xu hướng, động lượng, dòng tiền, setup và rủi ro sau khi chạy Vnstock API.",
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
                "ticker": "MSB",
                "name": "MSB",
                "sector": "Ngân hàng",
                "score": 60.3,
                "subscores": {
                        "trend": 10,
                        "momentum": 9.8,
                        "moneyFlow": 15.5,
                        "setup": 5.0,
                        "risk": 9.6,
                        "relativeStrength": 10.4
                },
                "setupType": "Pullback MA20",
                "marketState": "Trung tính",
                "action": "CHỜ THÊM",
                "risk": "Trung bình",
                "close": 29600,
                "rsi14": 62.4,
                "ret20": 2.8,
                "ret60": 2.4,
                "volume_status": "Mẫu",
                "volumeRatio": 1.4,
                "ma20": 28980,
                "ma50": 28360,
                "ma200": 27120,
                "macd": null,
                "macd_signal": null,
                "distanceToMA20": -3.5,
                "atr14": null,
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
                        "topOpportunity": false,
                        "breakout": false,
                        "pullbackMA20": true,
                        "moneyFlow": true,
                        "accumulation": false,
                        "safe": false
                },
                "reason": "Dữ liệu mẫu cho MSB. Chạy GitHub Actions sau khi thêm VNSTOCK_API_KEY để cập nhật tín hiệu thật.",
                "expertSummary": "MSB đang ở trạng thái mẫu. Hệ thống sẽ cập nhật xu hướng, động lượng, dòng tiền, setup và rủi ro sau khi chạy Vnstock API.",
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
                "ticker": "EIB",
                "name": "Eximbank",
                "sector": "Ngân hàng",
                "score": 66.8,
                "subscores": {
                        "trend": 12,
                        "momentum": 11.2,
                        "moneyFlow": 17.0,
                        "setup": 6.7,
                        "risk": 8.4,
                        "relativeStrength": 11.5
                },
                "setupType": "Breakout 20 phiên",
                "marketState": "Tích cực",
                "action": "THEO DÕI MUA",
                "risk": "Trung bình",
                "close": 30400,
                "rsi14": 64.1,
                "ret20": 3.7,
                "ret60": 3.6,
                "volume_status": "Mẫu",
                "volumeRatio": 1.55,
                "ma20": 29770,
                "ma50": 29140,
                "ma200": 27880,
                "macd": null,
                "macd_signal": null,
                "distanceToMA20": -2.5,
                "atr14": null,
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
                        "topOpportunity": false,
                        "breakout": true,
                        "pullbackMA20": false,
                        "moneyFlow": true,
                        "accumulation": false,
                        "safe": false
                },
                "reason": "Dữ liệu mẫu cho EIB. Chạy GitHub Actions sau khi thêm VNSTOCK_API_KEY để cập nhật tín hiệu thật.",
                "expertSummary": "EIB đang ở trạng thái mẫu. Hệ thống sẽ cập nhật xu hướng, động lượng, dòng tiền, setup và rủi ro sau khi chạy Vnstock API.",
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
                "ticker": "OCB",
                "name": "OCB",
                "sector": "Ngân hàng",
                "score": 62.8,
                "subscores": {
                        "trend": 14,
                        "momentum": 12.6,
                        "moneyFlow": 8.0,
                        "setup": 8.4,
                        "risk": 7.2,
                        "relativeStrength": 12.6
                },
                "setupType": "Tích lũy biên hẹp",
                "marketState": "Tích cực",
                "action": "CHỜ THÊM",
                "risk": "Trung bình",
                "close": 31200,
                "rsi14": 65.8,
                "ret20": 4.6,
                "ret60": 4.8,
                "volume_status": "Mẫu",
                "volumeRatio": 1.7,
                "ma20": 30560,
                "ma50": 29920,
                "ma200": 28640,
                "macd": null,
                "macd_signal": null,
                "distanceToMA20": -1.5,
                "atr14": null,
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
                        "topOpportunity": false,
                        "breakout": false,
                        "pullbackMA20": false,
                        "moneyFlow": false,
                        "accumulation": true,
                        "safe": false
                },
                "reason": "Dữ liệu mẫu cho OCB. Chạy GitHub Actions sau khi thêm VNSTOCK_API_KEY để cập nhật tín hiệu thật.",
                "expertSummary": "OCB đang ở trạng thái mẫu. Hệ thống sẽ cập nhật xu hướng, động lượng, dòng tiền, setup và rủi ro sau khi chạy Vnstock API.",
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
                "ticker": "TPB",
                "name": "TPBank",
                "sector": "Ngân hàng",
                "score": 68.3,
                "subscores": {
                        "trend": 16,
                        "momentum": 7.0,
                        "moneyFlow": 9.5,
                        "setup": 10.1,
                        "risk": 12.0,
                        "relativeStrength": 13.7
                },
                "setupType": "Retest nền",
                "marketState": "Uptrend",
                "action": "THEO DÕI MUA",
                "risk": "Trung bình",
                "close": 32000,
                "rsi14": 67.5,
                "ret20": 5.5,
                "ret60": 6.0,
                "volume_status": "Mẫu",
                "volumeRatio": 1.85,
                "ma20": 31350,
                "ma50": 30700,
                "ma200": 29400,
                "macd": null,
                "macd_signal": null,
                "distanceToMA20": -0.5,
                "atr14": null,
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
                        "topOpportunity": false,
                        "breakout": false,
                        "pullbackMA20": false,
                        "moneyFlow": false,
                        "accumulation": false,
                        "safe": true
                },
                "reason": "Dữ liệu mẫu cho TPB. Chạy GitHub Actions sau khi thêm VNSTOCK_API_KEY để cập nhật tín hiệu thật.",
                "expertSummary": "TPB đang ở trạng thái mẫu. Hệ thống sẽ cập nhật xu hướng, động lượng, dòng tiền, setup và rủi ro sau khi chạy Vnstock API.",
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
                "ticker": "SSB",
                "name": "SeABank",
                "sector": "Ngân hàng",
                "score": 66.0,
                "subscores": {
                        "trend": 18,
                        "momentum": 8.4,
                        "moneyFlow": 11.0,
                        "setup": 11.8,
                        "risk": 10.8,
                        "relativeStrength": 6.0
                },
                "setupType": "Vượt lại MA50",
                "marketState": "Uptrend",
                "action": "THEO DÕI MUA",
                "risk": "Trung bình",
                "close": 32800,
                "rsi14": 69.2,
                "ret20": 6.4,
                "ret60": 7.2,
                "volume_status": "Mẫu",
                "volumeRatio": 0.8,
                "ma20": 32140,
                "ma50": 31480,
                "ma200": 30160,
                "macd": null,
                "macd_signal": null,
                "distanceToMA20": 0.5,
                "atr14": null,
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
                        "topOpportunity": false,
                        "breakout": false,
                        "pullbackMA20": false,
                        "moneyFlow": false,
                        "accumulation": false,
                        "safe": false
                },
                "reason": "Dữ liệu mẫu cho SSB. Chạy GitHub Actions sau khi thêm VNSTOCK_API_KEY để cập nhật tín hiệu thật.",
                "expertSummary": "SSB đang ở trạng thái mẫu. Hệ thống sẽ cập nhật xu hướng, động lượng, dòng tiền, setup và rủi ro sau khi chạy Vnstock API.",
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
                "ticker": "NAB",
                "name": "Nam A Bank",
                "sector": "Ngân hàng",
                "score": 72.5,
                "subscores": {
                        "trend": 20,
                        "momentum": 9.8,
                        "moneyFlow": 12.5,
                        "setup": 13.5,
                        "risk": 9.6,
                        "relativeStrength": 7.1
                },
                "setupType": "Chưa có setup rõ",
                "marketState": "Uptrend",
                "action": "THEO DÕI MUA",
                "risk": "Trung bình",
                "close": 33600,
                "rsi14": 70.9,
                "ret20": 7.3,
                "ret60": 8.4,
                "volume_status": "Mẫu",
                "volumeRatio": 0.95,
                "ma20": 32930,
                "ma50": 32260,
                "ma200": 30920,
                "macd": null,
                "macd_signal": null,
                "distanceToMA20": 1.5,
                "atr14": null,
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
                        "topOpportunity": false,
                        "breakout": false,
                        "pullbackMA20": false,
                        "moneyFlow": false,
                        "accumulation": false,
                        "safe": false
                },
                "reason": "Dữ liệu mẫu cho NAB. Chạy GitHub Actions sau khi thêm VNSTOCK_API_KEY để cập nhật tín hiệu thật.",
                "expertSummary": "NAB đang ở trạng thái mẫu. Hệ thống sẽ cập nhật xu hướng, động lượng, dòng tiền, setup và rủi ro sau khi chạy Vnstock API.",
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
                "ticker": "BAB",
                "name": "Bac A Bank",
                "sector": "Ngân hàng",
                "score": 56.8,
                "subscores": {
                        "trend": 10,
                        "momentum": 11.2,
                        "moneyFlow": 14.0,
                        "setup": 5.0,
                        "risk": 8.4,
                        "relativeStrength": 8.2
                },
                "setupType": "Pullback MA20",
                "marketState": "Trung tính",
                "action": "CHỜ THÊM",
                "risk": "Trung bình",
                "close": 34400,
                "rsi14": 42.0,
                "ret20": 8.2,
                "ret60": 9.6,
                "volume_status": "Mẫu",
                "volumeRatio": 1.1,
                "ma20": 33720,
                "ma50": 33040,
                "ma200": 31680,
                "macd": null,
                "macd_signal": null,
                "distanceToMA20": 2.5,
                "atr14": null,
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
                        "topOpportunity": false,
                        "breakout": false,
                        "pullbackMA20": true,
                        "moneyFlow": false,
                        "accumulation": false,
                        "safe": false
                },
                "reason": "Dữ liệu mẫu cho BAB. Chạy GitHub Actions sau khi thêm VNSTOCK_API_KEY để cập nhật tín hiệu thật.",
                "expertSummary": "BAB đang ở trạng thái mẫu. Hệ thống sẽ cập nhật xu hướng, động lượng, dòng tiền, setup và rủi ro sau khi chạy Vnstock API.",
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
                "ticker": "BVB",
                "name": "VietCapital Bank",
                "sector": "Ngân hàng",
                "score": 63.3,
                "subscores": {
                        "trend": 12,
                        "momentum": 12.6,
                        "moneyFlow": 15.5,
                        "setup": 6.7,
                        "risk": 7.2,
                        "relativeStrength": 9.3
                },
                "setupType": "Breakout 20 phiên",
                "marketState": "Tích cực",
                "action": "CHỜ THÊM",
                "risk": "Trung bình",
                "close": 35200,
                "rsi14": 43.7,
                "ret20": 9.1,
                "ret60": 10.8,
                "volume_status": "Mẫu",
                "volumeRatio": 1.25,
                "ma20": 34510,
                "ma50": 33820,
                "ma200": 32440,
                "macd": null,
                "macd_signal": null,
                "distanceToMA20": 3.5,
                "atr14": null,
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
                        "topOpportunity": false,
                        "breakout": true,
                        "pullbackMA20": false,
                        "moneyFlow": true,
                        "accumulation": false,
                        "safe": false
                },
                "reason": "Dữ liệu mẫu cho BVB. Chạy GitHub Actions sau khi thêm VNSTOCK_API_KEY để cập nhật tín hiệu thật.",
                "expertSummary": "BVB đang ở trạng thái mẫu. Hệ thống sẽ cập nhật xu hướng, động lượng, dòng tiền, setup và rủi ro sau khi chạy Vnstock API.",
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
                "ticker": "HPG",
                "name": "Tập đoàn Hòa Phát",
                "sector": "Thép / Công nghiệp",
                "score": 68.8,
                "subscores": {
                        "trend": 14,
                        "momentum": 7.0,
                        "moneyFlow": 17.0,
                        "setup": 8.4,
                        "risk": 12.0,
                        "relativeStrength": 10.4
                },
                "setupType": "Tích lũy biên hẹp",
                "marketState": "Tích cực",
                "action": "THEO DÕI MUA",
                "risk": "Trung bình",
                "close": 36000,
                "rsi14": 45.4,
                "ret20": 10.0,
                "ret60": 12.0,
                "volume_status": "Mẫu",
                "volumeRatio": 1.4,
                "ma20": 35300,
                "ma50": 34600,
                "ma200": 33200,
                "macd": null,
                "macd_signal": null,
                "distanceToMA20": 4.5,
                "atr14": null,
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
                        "topOpportunity": false,
                        "breakout": false,
                        "pullbackMA20": false,
                        "moneyFlow": true,
                        "accumulation": true,
                        "safe": true
                },
                "reason": "Dữ liệu mẫu cho HPG. Chạy GitHub Actions sau khi thêm VNSTOCK_API_KEY để cập nhật tín hiệu thật.",
                "expertSummary": "HPG đang ở trạng thái mẫu. Hệ thống sẽ cập nhật xu hướng, động lượng, dòng tiền, setup và rủi ro sau khi chạy Vnstock API.",
                "buyZone": "Canh quanh MA20 hoặc nền tích lũy gần nhất, không mua đuổi.",
                "stopLoss": "-7% đến -10%",
                "takeProfit": "+12% đến +25%",
                "allocation": "5% - 20%",
                "catalysts": [
                        "Vnstock API",
                        "Thép / Công nghiệp"
                ],
                "cautions": [
                        "Đây là dữ liệu mẫu trước khi chạy API",
                        "Không dùng để giao dịch thật",
                        "Chạy workflow để cập nhật"
                ]
        },
        {
                "ticker": "HSG",
                "name": "Hoa Sen Group",
                "sector": "Thép / Công nghiệp",
                "score": 64.8,
                "subscores": {
                        "trend": 16,
                        "momentum": 8.4,
                        "moneyFlow": 8.0,
                        "setup": 10.1,
                        "risk": 10.8,
                        "relativeStrength": 11.5
                },
                "setupType": "Retest nền",
                "marketState": "Uptrend",
                "action": "CHỜ THÊM",
                "risk": "Trung bình",
                "close": 36800,
                "rsi14": 47.1,
                "ret20": -8.0,
                "ret60": 13.2,
                "volume_status": "Mẫu",
                "volumeRatio": 1.55,
                "ma20": 36090,
                "ma50": 35380,
                "ma200": 33960,
                "macd": null,
                "macd_signal": null,
                "distanceToMA20": 5.5,
                "atr14": null,
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
                        "topOpportunity": false,
                        "breakout": false,
                        "pullbackMA20": false,
                        "moneyFlow": false,
                        "accumulation": false,
                        "safe": false
                },
                "reason": "Dữ liệu mẫu cho HSG. Chạy GitHub Actions sau khi thêm VNSTOCK_API_KEY để cập nhật tín hiệu thật.",
                "expertSummary": "HSG đang ở trạng thái mẫu. Hệ thống sẽ cập nhật xu hướng, động lượng, dòng tiền, setup và rủi ro sau khi chạy Vnstock API.",
                "buyZone": "Canh quanh MA20 hoặc nền tích lũy gần nhất, không mua đuổi.",
                "stopLoss": "-7% đến -10%",
                "takeProfit": "+12% đến +25%",
                "allocation": "5% - 20%",
                "catalysts": [
                        "Vnstock API",
                        "Thép / Công nghiệp"
                ],
                "cautions": [
                        "Đây là dữ liệu mẫu trước khi chạy API",
                        "Không dùng để giao dịch thật",
                        "Chạy workflow để cập nhật"
                ]
        },
        {
                "ticker": "NKG",
                "name": "Thép Nam Kim",
                "sector": "Thép / Công nghiệp",
                "score": 71.3,
                "subscores": {
                        "trend": 18,
                        "momentum": 9.8,
                        "moneyFlow": 9.5,
                        "setup": 11.8,
                        "risk": 9.6,
                        "relativeStrength": 12.6
                },
                "setupType": "Vượt lại MA50",
                "marketState": "Uptrend",
                "action": "THEO DÕI MUA",
                "risk": "Trung bình",
                "close": 37600,
                "rsi14": 48.8,
                "ret20": -7.1,
                "ret60": 14.4,
                "volume_status": "Mẫu",
                "volumeRatio": 1.7,
                "ma20": 36880,
                "ma50": 36160,
                "ma200": 34720,
                "macd": null,
                "macd_signal": null,
                "distanceToMA20": 6.5,
                "atr14": null,
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
                        "topOpportunity": false,
                        "breakout": false,
                        "pullbackMA20": false,
                        "moneyFlow": false,
                        "accumulation": false,
                        "safe": false
                },
                "reason": "Dữ liệu mẫu cho NKG. Chạy GitHub Actions sau khi thêm VNSTOCK_API_KEY để cập nhật tín hiệu thật.",
                "expertSummary": "NKG đang ở trạng thái mẫu. Hệ thống sẽ cập nhật xu hướng, động lượng, dòng tiền, setup và rủi ro sau khi chạy Vnstock API.",
                "buyZone": "Canh quanh MA20 hoặc nền tích lũy gần nhất, không mua đuổi.",
                "stopLoss": "-7% đến -10%",
                "takeProfit": "+12% đến +25%",
                "allocation": "5% - 20%",
                "catalysts": [
                        "Vnstock API",
                        "Thép / Công nghiệp"
                ],
                "cautions": [
                        "Đây là dữ liệu mẫu trước khi chạy API",
                        "Không dùng để giao dịch thật",
                        "Chạy workflow để cập nhật"
                ]
        },
        {
                "ticker": "TLH",
                "name": "Thép Tiến Lên",
                "sector": "Thép / Công nghiệp",
                "score": 77.8,
                "subscores": {
                        "trend": 20,
                        "momentum": 11.2,
                        "moneyFlow": 11.0,
                        "setup": 13.5,
                        "risk": 8.4,
                        "relativeStrength": 13.7
                },
                "setupType": "Chưa có setup rõ",
                "marketState": "Uptrend",
                "action": "CANH MUA / MUA KHI XÁC NHẬN",
                "risk": "Trung bình",
                "close": 38400,
                "rsi14": 50.5,
                "ret20": -6.2,
                "ret60": 15.6,
                "volume_status": "Mẫu",
                "volumeRatio": 1.85,
                "ma20": 37670,
                "ma50": 36940,
                "ma200": 35480,
                "macd": null,
                "macd_signal": null,
                "distanceToMA20": 7.5,
                "atr14": null,
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
                        "topOpportunity": false,
                        "breakout": false,
                        "pullbackMA20": false,
                        "moneyFlow": false,
                        "accumulation": false,
                        "safe": false
                },
                "reason": "Dữ liệu mẫu cho TLH. Chạy GitHub Actions sau khi thêm VNSTOCK_API_KEY để cập nhật tín hiệu thật.",
                "expertSummary": "TLH đang ở trạng thái mẫu. Hệ thống sẽ cập nhật xu hướng, động lượng, dòng tiền, setup và rủi ro sau khi chạy Vnstock API.",
                "buyZone": "Canh quanh MA20 hoặc nền tích lũy gần nhất, không mua đuổi.",
                "stopLoss": "-7% đến -10%",
                "takeProfit": "+12% đến +25%",
                "allocation": "5% - 20%",
                "catalysts": [
                        "Vnstock API",
                        "Thép / Công nghiệp"
                ],
                "cautions": [
                        "Đây là dữ liệu mẫu trước khi chạy API",
                        "Không dùng để giao dịch thật",
                        "Chạy workflow để cập nhật"
                ]
        },
        {
                "ticker": "SMC",
                "name": "SMC Trading",
                "sector": "Thép / Công nghiệp",
                "score": 53.3,
                "subscores": {
                        "trend": 10,
                        "momentum": 12.6,
                        "moneyFlow": 12.5,
                        "setup": 5.0,
                        "risk": 7.2,
                        "relativeStrength": 6.0
                },
                "setupType": "Pullback MA20",
                "marketState": "Trung tính",
                "action": "TRÁNH MUA MỚI",
                "risk": "Trung bình",
                "close": 39200,
                "rsi14": 52.2,
                "ret20": -5.3,
                "ret60": 16.8,
                "volume_status": "Mẫu",
                "volumeRatio": 0.8,
                "ma20": 38460,
                "ma50": 37720,
                "ma200": 36240,
                "macd": null,
                "macd_signal": null,
                "distanceToMA20": -3.5,
                "atr14": null,
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
                        "topOpportunity": false,
                        "breakout": false,
                        "pullbackMA20": true,
                        "moneyFlow": false,
                        "accumulation": false,
                        "safe": false
                },
                "reason": "Dữ liệu mẫu cho SMC. Chạy GitHub Actions sau khi thêm VNSTOCK_API_KEY để cập nhật tín hiệu thật.",
                "expertSummary": "SMC đang ở trạng thái mẫu. Hệ thống sẽ cập nhật xu hướng, động lượng, dòng tiền, setup và rủi ro sau khi chạy Vnstock API.",
                "buyZone": "Canh quanh MA20 hoặc nền tích lũy gần nhất, không mua đuổi.",
                "stopLoss": "-7% đến -10%",
                "takeProfit": "+12% đến +25%",
                "allocation": "5% - 20%",
                "catalysts": [
                        "Vnstock API",
                        "Thép / Công nghiệp"
                ],
                "cautions": [
                        "Đây là dữ liệu mẫu trước khi chạy API",
                        "Không dùng để giao dịch thật",
                        "Chạy workflow để cập nhật"
                ]
        },
        {
                "ticker": "VGS",
                "name": "Ống thép Việt Đức",
                "sector": "Thép / Công nghiệp",
                "score": 58.8,
                "subscores": {
                        "trend": 12,
                        "momentum": 7.0,
                        "moneyFlow": 14.0,
                        "setup": 6.7,
                        "risk": 12.0,
                        "relativeStrength": 7.1
                },
                "setupType": "Breakout 20 phiên",
                "marketState": "Tích cực",
                "action": "CHỜ THÊM",
                "risk": "Trung bình",
                "close": 40000,
                "rsi14": 53.9,
                "ret20": -4.4,
                "ret60": -12.0,
                "volume_status": "Mẫu",
                "volumeRatio": 0.95,
                "ma20": 39250,
                "ma50": 38500,
                "ma200": 37000,
                "macd": null,
                "macd_signal": null,
                "distanceToMA20": -2.5,
                "atr14": null,
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
                        "topOpportunity": false,
                        "breakout": true,
                        "pullbackMA20": false,
                        "moneyFlow": false,
                        "accumulation": false,
                        "safe": false
                },
                "reason": "Dữ liệu mẫu cho VGS. Chạy GitHub Actions sau khi thêm VNSTOCK_API_KEY để cập nhật tín hiệu thật.",
                "expertSummary": "VGS đang ở trạng thái mẫu. Hệ thống sẽ cập nhật xu hướng, động lượng, dòng tiền, setup và rủi ro sau khi chạy Vnstock API.",
                "buyZone": "Canh quanh MA20 hoặc nền tích lũy gần nhất, không mua đuổi.",
                "stopLoss": "-7% đến -10%",
                "takeProfit": "+12% đến +25%",
                "allocation": "5% - 20%",
                "catalysts": [
                        "Vnstock API",
                        "Thép / Công nghiệp"
                ],
                "cautions": [
                        "Đây là dữ liệu mẫu trước khi chạy API",
                        "Không dùng để giao dịch thật",
                        "Chạy workflow để cập nhật"
                ]
        },
        {
                "ticker": "FPT",
                "name": "FPT Corp",
                "sector": "Công nghệ / Viễn thông",
                "score": 65.3,
                "subscores": {
                        "trend": 14,
                        "momentum": 8.4,
                        "moneyFlow": 15.5,
                        "setup": 8.4,
                        "risk": 10.8,
                        "relativeStrength": 8.2
                },
                "setupType": "Tích lũy biên hẹp",
                "marketState": "Tích cực",
                "action": "THEO DÕI MUA",
                "risk": "Trung bình",
                "close": 40800,
                "rsi14": 55.6,
                "ret20": -3.5,
                "ret60": -10.8,
                "volume_status": "Mẫu",
                "volumeRatio": 1.1,
                "ma20": 40040,
                "ma50": 39280,
                "ma200": 37760,
                "macd": null,
                "macd_signal": null,
                "distanceToMA20": -1.5,
                "atr14": null,
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
                        "topOpportunity": false,
                        "breakout": false,
                        "pullbackMA20": false,
                        "moneyFlow": true,
                        "accumulation": true,
                        "safe": false
                },
                "reason": "Dữ liệu mẫu cho FPT. Chạy GitHub Actions sau khi thêm VNSTOCK_API_KEY để cập nhật tín hiệu thật.",
                "expertSummary": "FPT đang ở trạng thái mẫu. Hệ thống sẽ cập nhật xu hướng, động lượng, dòng tiền, setup và rủi ro sau khi chạy Vnstock API.",
                "buyZone": "Canh quanh MA20 hoặc nền tích lũy gần nhất, không mua đuổi.",
                "stopLoss": "-7% đến -10%",
                "takeProfit": "+12% đến +25%",
                "allocation": "5% - 20%",
                "catalysts": [
                        "Vnstock API",
                        "Công nghệ / Viễn thông"
                ],
                "cautions": [
                        "Đây là dữ liệu mẫu trước khi chạy API",
                        "Không dùng để giao dịch thật",
                        "Chạy workflow để cập nhật"
                ]
        },
        {
                "ticker": "CMG",
                "name": "CMC Corp",
                "sector": "Công nghệ / Viễn thông",
                "score": 71.8,
                "subscores": {
                        "trend": 16,
                        "momentum": 9.8,
                        "moneyFlow": 17.0,
                        "setup": 10.1,
                        "risk": 9.6,
                        "relativeStrength": 9.3
                },
                "setupType": "Retest nền",
                "marketState": "Uptrend",
                "action": "THEO DÕI MUA",
                "risk": "Trung bình",
                "close": 41600,
                "rsi14": 57.3,
                "ret20": -2.6,
                "ret60": -9.6,
                "volume_status": "Mẫu",
                "volumeRatio": 1.25,
                "ma20": 40830,
                "ma50": 40060,
                "ma200": 38520,
                "macd": null,
                "macd_signal": null,
                "distanceToMA20": -0.5,
                "atr14": null,
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
                        "topOpportunity": false,
                        "breakout": false,
                        "pullbackMA20": false,
                        "moneyFlow": true,
                        "accumulation": false,
                        "safe": false
                },
                "reason": "Dữ liệu mẫu cho CMG. Chạy GitHub Actions sau khi thêm VNSTOCK_API_KEY để cập nhật tín hiệu thật.",
                "expertSummary": "CMG đang ở trạng thái mẫu. Hệ thống sẽ cập nhật xu hướng, động lượng, dòng tiền, setup và rủi ro sau khi chạy Vnstock API.",
                "buyZone": "Canh quanh MA20 hoặc nền tích lũy gần nhất, không mua đuổi.",
                "stopLoss": "-7% đến -10%",
                "takeProfit": "+12% đến +25%",
                "allocation": "5% - 20%",
                "catalysts": [
                        "Vnstock API",
                        "Công nghệ / Viễn thông"
                ],
                "cautions": [
                        "Đây là dữ liệu mẫu trước khi chạy API",
                        "Không dùng để giao dịch thật",
                        "Chạy workflow để cập nhật"
                ]
        },
        {
                "ticker": "ELC",
                "name": "ELCOM",
                "sector": "Công nghệ / Viễn thông",
                "score": 67.8,
                "subscores": {
                        "trend": 18,
                        "momentum": 11.2,
                        "moneyFlow": 8.0,
                        "setup": 11.8,
                        "risk": 8.4,
                        "relativeStrength": 10.4
                },
                "setupType": "Vượt lại MA50",
                "marketState": "Uptrend",
                "action": "THEO DÕI MUA",
                "risk": "Trung bình",
                "close": 42400,
                "rsi14": 59.0,
                "ret20": -1.7,
                "ret60": -8.4,
                "volume_status": "Mẫu",
                "volumeRatio": 1.4,
                "ma20": 41620,
                "ma50": 40840,
                "ma200": 39280,
                "macd": null,
                "macd_signal": null,
                "distanceToMA20": 0.5,
                "atr14": null,
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
                        "topOpportunity": false,
                        "breakout": false,
                        "pullbackMA20": false,
                        "moneyFlow": false,
                        "accumulation": false,
                        "safe": false
                },
                "reason": "Dữ liệu mẫu cho ELC. Chạy GitHub Actions sau khi thêm VNSTOCK_API_KEY để cập nhật tín hiệu thật.",
                "expertSummary": "ELC đang ở trạng thái mẫu. Hệ thống sẽ cập nhật xu hướng, động lượng, dòng tiền, setup và rủi ro sau khi chạy Vnstock API.",
                "buyZone": "Canh quanh MA20 hoặc nền tích lũy gần nhất, không mua đuổi.",
                "stopLoss": "-7% đến -10%",
                "takeProfit": "+12% đến +25%",
                "allocation": "5% - 20%",
                "catalysts": [
                        "Vnstock API",
                        "Công nghệ / Viễn thông"
                ],
                "cautions": [
                        "Đây là dữ liệu mẫu trước khi chạy API",
                        "Không dùng để giao dịch thật",
                        "Chạy workflow để cập nhật"
                ]
        },
        {
                "ticker": "CTR",
                "name": "Viettel Construction",
                "sector": "Công nghệ / Viễn thông",
                "score": 74.3,
                "subscores": {
                        "trend": 20,
                        "momentum": 12.6,
                        "moneyFlow": 9.5,
                        "setup": 13.5,
                        "risk": 7.2,
                        "relativeStrength": 11.5
                },
                "setupType": "Chưa có setup rõ",
                "marketState": "Uptrend",
                "action": "CANH MUA / MUA KHI XÁC NHẬN",
                "risk": "Trung bình",
                "close": 43200,
                "rsi14": 60.7,
                "ret20": -0.8,
                "ret60": -7.2,
                "volume_status": "Mẫu",
                "volumeRatio": 1.55,
                "ma20": 42410,
                "ma50": 41620,
                "ma200": 40040,
                "macd": null,
                "macd_signal": null,
                "distanceToMA20": 1.5,
                "atr14": null,
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
                        "topOpportunity": false,
                        "breakout": false,
                        "pullbackMA20": false,
                        "moneyFlow": false,
                        "accumulation": false,
                        "safe": false
                },
                "reason": "Dữ liệu mẫu cho CTR. Chạy GitHub Actions sau khi thêm VNSTOCK_API_KEY để cập nhật tín hiệu thật.",
                "expertSummary": "CTR đang ở trạng thái mẫu. Hệ thống sẽ cập nhật xu hướng, động lượng, dòng tiền, setup và rủi ro sau khi chạy Vnstock API.",
                "buyZone": "Canh quanh MA20 hoặc nền tích lũy gần nhất, không mua đuổi.",
                "stopLoss": "-7% đến -10%",
                "takeProfit": "+12% đến +25%",
                "allocation": "5% - 20%",
                "catalysts": [
                        "Vnstock API",
                        "Công nghệ / Viễn thông"
                ],
                "cautions": [
                        "Đây là dữ liệu mẫu trước khi chạy API",
                        "Không dùng để giao dịch thật",
                        "Chạy workflow để cập nhật"
                ]
        },
        {
                "ticker": "VGI",
                "name": "Viettel Global",
                "sector": "Công nghệ / Viễn thông",
                "score": 57.6,
                "subscores": {
                        "trend": 10,
                        "momentum": 7.0,
                        "moneyFlow": 11.0,
                        "setup": 5.0,
                        "risk": 12.0,
                        "relativeStrength": 12.6
                },
                "setupType": "Pullback MA20",
                "marketState": "Trung tính",
                "action": "CHỜ THÊM",
                "risk": "Trung bình",
                "close": 44000,
                "rsi14": 62.4,
                "ret20": 0.1,
                "ret60": -6.0,
                "volume_status": "Mẫu",
                "volumeRatio": 1.7,
                "ma20": 43200,
                "ma50": 42400,
                "ma200": 40800,
                "macd": null,
                "macd_signal": null,
                "distanceToMA20": 2.5,
                "atr14": null,
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
                        "topOpportunity": false,
                        "breakout": false,
                        "pullbackMA20": true,
                        "moneyFlow": false,
                        "accumulation": false,
                        "safe": false
                },
                "reason": "Dữ liệu mẫu cho VGI. Chạy GitHub Actions sau khi thêm VNSTOCK_API_KEY để cập nhật tín hiệu thật.",
                "expertSummary": "VGI đang ở trạng thái mẫu. Hệ thống sẽ cập nhật xu hướng, động lượng, dòng tiền, setup và rủi ro sau khi chạy Vnstock API.",
                "buyZone": "Canh quanh MA20 hoặc nền tích lũy gần nhất, không mua đuổi.",
                "stopLoss": "-7% đến -10%",
                "takeProfit": "+12% đến +25%",
                "allocation": "5% - 20%",
                "catalysts": [
                        "Vnstock API",
                        "Công nghệ / Viễn thông"
                ],
                "cautions": [
                        "Đây là dữ liệu mẫu trước khi chạy API",
                        "Không dùng để giao dịch thật",
                        "Chạy workflow để cập nhật"
                ]
        },
        {
                "ticker": "FOX",
                "name": "FPT Telecom",
                "sector": "Công nghệ / Viễn thông",
                "score": 64.1,
                "subscores": {
                        "trend": 12,
                        "momentum": 8.4,
                        "moneyFlow": 12.5,
                        "setup": 6.7,
                        "risk": 10.8,
                        "relativeStrength": 13.7
                },
                "setupType": "Breakout 20 phiên",
                "marketState": "Tích cực",
                "action": "CHỜ THÊM",
                "risk": "Trung bình",
                "close": 44800,
                "rsi14": 64.1,
                "ret20": 1.0,
                "ret60": -4.8,
                "volume_status": "Mẫu",
                "volumeRatio": 1.85,
                "ma20": 43990,
                "ma50": 43180,
                "ma200": 41560,
                "macd": null,
                "macd_signal": null,
                "distanceToMA20": 3.5,
                "atr14": null,
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
                        "topOpportunity": false,
                        "breakout": true,
                        "pullbackMA20": false,
                        "moneyFlow": false,
                        "accumulation": false,
                        "safe": false
                },
                "reason": "Dữ liệu mẫu cho FOX. Chạy GitHub Actions sau khi thêm VNSTOCK_API_KEY để cập nhật tín hiệu thật.",
                "expertSummary": "FOX đang ở trạng thái mẫu. Hệ thống sẽ cập nhật xu hướng, động lượng, dòng tiền, setup và rủi ro sau khi chạy Vnstock API.",
                "buyZone": "Canh quanh MA20 hoặc nền tích lũy gần nhất, không mua đuổi.",
                "stopLoss": "-7% đến -10%",
                "takeProfit": "+12% đến +25%",
                "allocation": "5% - 20%",
                "catalysts": [
                        "Vnstock API",
                        "Công nghệ / Viễn thông"
                ],
                "cautions": [
                        "Đây là dữ liệu mẫu trước khi chạy API",
                        "Không dùng để giao dịch thật",
                        "Chạy workflow để cập nhật"
                ]
        },
        {
                "ticker": "SAM",
                "name": "SAM Holdings",
                "sector": "Công nghệ / Viễn thông",
                "score": 61.8,
                "subscores": {
                        "trend": 14,
                        "momentum": 9.8,
                        "moneyFlow": 14.0,
                        "setup": 8.4,
                        "risk": 9.6,
                        "relativeStrength": 6.0
                },
                "setupType": "Tích lũy biên hẹp",
                "marketState": "Tích cực",
                "action": "CHỜ THÊM",
                "risk": "Trung bình",
                "close": 45600,
                "rsi14": 65.8,
                "ret20": 1.9,
                "ret60": -3.6,
                "volume_status": "Mẫu",
                "volumeRatio": 0.8,
                "ma20": 44780,
                "ma50": 43960,
                "ma200": 42320,
                "macd": null,
                "macd_signal": null,
                "distanceToMA20": 4.5,
                "atr14": null,
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
                        "topOpportunity": false,
                        "breakout": false,
                        "pullbackMA20": false,
                        "moneyFlow": false,
                        "accumulation": true,
                        "safe": false
                },
                "reason": "Dữ liệu mẫu cho SAM. Chạy GitHub Actions sau khi thêm VNSTOCK_API_KEY để cập nhật tín hiệu thật.",
                "expertSummary": "SAM đang ở trạng thái mẫu. Hệ thống sẽ cập nhật xu hướng, động lượng, dòng tiền, setup và rủi ro sau khi chạy Vnstock API.",
                "buyZone": "Canh quanh MA20 hoặc nền tích lũy gần nhất, không mua đuổi.",
                "stopLoss": "-7% đến -10%",
                "takeProfit": "+12% đến +25%",
                "allocation": "5% - 20%",
                "catalysts": [
                        "Vnstock API",
                        "Công nghệ / Viễn thông"
                ],
                "cautions": [
                        "Đây là dữ liệu mẫu trước khi chạy API",
                        "Không dùng để giao dịch thật",
                        "Chạy workflow để cập nhật"
                ]
        },
        {
                "ticker": "ITD",
                "name": "Công nghệ Tiên Phong",
                "sector": "Công nghệ / Viễn thông",
                "score": 68.3,
                "subscores": {
                        "trend": 16,
                        "momentum": 11.2,
                        "moneyFlow": 15.5,
                        "setup": 10.1,
                        "risk": 8.4,
                        "relativeStrength": 7.1
                },
                "setupType": "Retest nền",
                "marketState": "Uptrend",
                "action": "THEO DÕI MUA",
                "risk": "Trung bình",
                "close": 46400,
                "rsi14": 67.5,
                "ret20": 2.8,
                "ret60": -2.4,
                "volume_status": "Mẫu",
                "volumeRatio": 0.95,
                "ma20": 45570,
                "ma50": 44740,
                "ma200": 43080,
                "macd": null,
                "macd_signal": null,
                "distanceToMA20": 5.5,
                "atr14": null,
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
                        "topOpportunity": false,
                        "breakout": false,
                        "pullbackMA20": false,
                        "moneyFlow": true,
                        "accumulation": false,
                        "safe": false
                },
                "reason": "Dữ liệu mẫu cho ITD. Chạy GitHub Actions sau khi thêm VNSTOCK_API_KEY để cập nhật tín hiệu thật.",
                "expertSummary": "ITD đang ở trạng thái mẫu. Hệ thống sẽ cập nhật xu hướng, động lượng, dòng tiền, setup và rủi ro sau khi chạy Vnstock API.",
                "buyZone": "Canh quanh MA20 hoặc nền tích lũy gần nhất, không mua đuổi.",
                "stopLoss": "-7% đến -10%",
                "takeProfit": "+12% đến +25%",
                "allocation": "5% - 20%",
                "catalysts": [
                        "Vnstock API",
                        "Công nghệ / Viễn thông"
                ],
                "cautions": [
                        "Đây là dữ liệu mẫu trước khi chạy API",
                        "Không dùng để giao dịch thật",
                        "Chạy workflow để cập nhật"
                ]
        },
        {
                "ticker": "MWG",
                "name": "Thế Giới Di Động",
                "sector": "Bán lẻ / Phân phối",
                "score": 74.8,
                "subscores": {
                        "trend": 18,
                        "momentum": 12.6,
                        "moneyFlow": 17.0,
                        "setup": 11.8,
                        "risk": 7.2,
                        "relativeStrength": 8.2
                },
                "setupType": "Vượt lại MA50",
                "marketState": "Uptrend",
                "action": "CANH MUA / MUA KHI XÁC NHẬN",
                "risk": "Trung bình",
                "close": 47200,
                "rsi14": 69.2,
                "ret20": 3.7,
                "ret60": -1.2,
                "volume_status": "Mẫu",
                "volumeRatio": 1.1,
                "ma20": 46360,
                "ma50": 45520,
                "ma200": 43840,
                "macd": null,
                "macd_signal": null,
                "distanceToMA20": 6.5,
                "atr14": null,
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
                        "topOpportunity": false,
                        "breakout": false,
                        "pullbackMA20": false,
                        "moneyFlow": true,
                        "accumulation": false,
                        "safe": false
                },
                "reason": "Dữ liệu mẫu cho MWG. Chạy GitHub Actions sau khi thêm VNSTOCK_API_KEY để cập nhật tín hiệu thật.",
                "expertSummary": "MWG đang ở trạng thái mẫu. Hệ thống sẽ cập nhật xu hướng, động lượng, dòng tiền, setup và rủi ro sau khi chạy Vnstock API.",
                "buyZone": "Canh quanh MA20 hoặc nền tích lũy gần nhất, không mua đuổi.",
                "stopLoss": "-7% đến -10%",
                "takeProfit": "+12% đến +25%",
                "allocation": "5% - 20%",
                "catalysts": [
                        "Vnstock API",
                        "Bán lẻ / Phân phối"
                ],
                "cautions": [
                        "Đây là dữ liệu mẫu trước khi chạy API",
                        "Không dùng để giao dịch thật",
                        "Chạy workflow để cập nhật"
                ]
        },
        {
                "ticker": "FRT",
                "name": "FPT Retail",
                "sector": "Bán lẻ / Phân phối",
                "score": 69.8,
                "subscores": {
                        "trend": 20,
                        "momentum": 7.0,
                        "moneyFlow": 8.0,
                        "setup": 13.5,
                        "risk": 12.0,
                        "relativeStrength": 9.3
                },
                "setupType": "Chưa có setup rõ",
                "marketState": "Uptrend",
                "action": "THEO DÕI MUA",
                "risk": "Trung bình",
                "close": 48000,
                "rsi14": 70.9,
                "ret20": 4.6,
                "ret60": 0.0,
                "volume_status": "Mẫu",
                "volumeRatio": 1.25,
                "ma20": 47150,
                "ma50": 46300,
                "ma200": 44600,
                "macd": null,
                "macd_signal": null,
                "distanceToMA20": 7.5,
                "atr14": null,
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
                        "topOpportunity": false,
                        "breakout": false,
                        "pullbackMA20": false,
                        "moneyFlow": false,
                        "accumulation": false,
                        "safe": true
                },
                "reason": "Dữ liệu mẫu cho FRT. Chạy GitHub Actions sau khi thêm VNSTOCK_API_KEY để cập nhật tín hiệu thật.",
                "expertSummary": "FRT đang ở trạng thái mẫu. Hệ thống sẽ cập nhật xu hướng, động lượng, dòng tiền, setup và rủi ro sau khi chạy Vnstock API.",
                "buyZone": "Canh quanh MA20 hoặc nền tích lũy gần nhất, không mua đuổi.",
                "stopLoss": "-7% đến -10%",
                "takeProfit": "+12% đến +25%",
                "allocation": "5% - 20%",
                "catalysts": [
                        "Vnstock API",
                        "Bán lẻ / Phân phối"
                ],
                "cautions": [
                        "Đây là dữ liệu mẫu trước khi chạy API",
                        "Không dùng để giao dịch thật",
                        "Chạy workflow để cập nhật"
                ]
        },
        {
                "ticker": "DGW",
                "name": "Digiworld",
                "sector": "Bán lẻ / Phân phối",
                "score": 54.1,
                "subscores": {
                        "trend": 10,
                        "momentum": 8.4,
                        "moneyFlow": 9.5,
                        "setup": 5.0,
                        "risk": 10.8,
                        "relativeStrength": 10.4
                },
                "setupType": "Pullback MA20",
                "marketState": "Trung tính",
                "action": "TRÁNH MUA MỚI",
                "risk": "Trung bình",
                "close": 48800,
                "rsi14": 42.0,
                "ret20": 5.5,
                "ret60": 1.2,
                "volume_status": "Mẫu",
                "volumeRatio": 1.4,
                "ma20": 47940,
                "ma50": 47080,
                "ma200": 45360,
                "macd": null,
                "macd_signal": null,
                "distanceToMA20": -3.5,
                "atr14": null,
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
                        "topOpportunity": false,
                        "breakout": false,
                        "pullbackMA20": true,
                        "moneyFlow": false,
                        "accumulation": false,
                        "safe": false
                },
                "reason": "Dữ liệu mẫu cho DGW. Chạy GitHub Actions sau khi thêm VNSTOCK_API_KEY để cập nhật tín hiệu thật.",
                "expertSummary": "DGW đang ở trạng thái mẫu. Hệ thống sẽ cập nhật xu hướng, động lượng, dòng tiền, setup và rủi ro sau khi chạy Vnstock API.",
                "buyZone": "Canh quanh MA20 hoặc nền tích lũy gần nhất, không mua đuổi.",
                "stopLoss": "-7% đến -10%",
                "takeProfit": "+12% đến +25%",
                "allocation": "5% - 20%",
                "catalysts": [
                        "Vnstock API",
                        "Bán lẻ / Phân phối"
                ],
                "cautions": [
                        "Đây là dữ liệu mẫu trước khi chạy API",
                        "Không dùng để giao dịch thật",
                        "Chạy workflow để cập nhật"
                ]
        },
        {
                "ticker": "PNJ",
                "name": "Vàng bạc Đá quý Phú Nhuận",
                "sector": "Bán lẻ / Phân phối",
                "score": 60.6,
                "subscores": {
                        "trend": 12,
                        "momentum": 9.8,
                        "moneyFlow": 11.0,
                        "setup": 6.7,
                        "risk": 9.6,
                        "relativeStrength": 11.5
                },
                "setupType": "Breakout 20 phiên",
                "marketState": "Tích cực",
                "action": "CHỜ THÊM",
                "risk": "Trung bình",
                "close": 49600,
                "rsi14": 43.7,
                "ret20": 6.4,
                "ret60": 2.4,
                "volume_status": "Mẫu",
                "volumeRatio": 1.55,
                "ma20": 48730,
                "ma50": 47860,
                "ma200": 46120,
                "macd": null,
                "macd_signal": null,
                "distanceToMA20": -2.5,
                "atr14": null,
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
                        "topOpportunity": false,
                        "breakout": true,
                        "pullbackMA20": false,
                        "moneyFlow": false,
                        "accumulation": false,
                        "safe": false
                },
                "reason": "Dữ liệu mẫu cho PNJ. Chạy GitHub Actions sau khi thêm VNSTOCK_API_KEY để cập nhật tín hiệu thật.",
                "expertSummary": "PNJ đang ở trạng thái mẫu. Hệ thống sẽ cập nhật xu hướng, động lượng, dòng tiền, setup và rủi ro sau khi chạy Vnstock API.",
                "buyZone": "Canh quanh MA20 hoặc nền tích lũy gần nhất, không mua đuổi.",
                "stopLoss": "-7% đến -10%",
                "takeProfit": "+12% đến +25%",
                "allocation": "5% - 20%",
                "catalysts": [
                        "Vnstock API",
                        "Bán lẻ / Phân phối"
                ],
                "cautions": [
                        "Đây là dữ liệu mẫu trước khi chạy API",
                        "Không dùng để giao dịch thật",
                        "Chạy workflow để cập nhật"
                ]
        },
        {
                "ticker": "PET",
                "name": "Petrosetco",
                "sector": "Bán lẻ / Phân phối",
                "score": 67.1,
                "subscores": {
                        "trend": 14,
                        "momentum": 11.2,
                        "moneyFlow": 12.5,
                        "setup": 8.4,
                        "risk": 8.4,
                        "relativeStrength": 12.6
                },
                "setupType": "Tích lũy biên hẹp",
                "marketState": "Tích cực",
                "action": "THEO DÕI MUA",
                "risk": "Trung bình",
                "close": 50400,
                "rsi14": 45.4,
                "ret20": 7.3,
                "ret60": 3.6,
                "volume_status": "Mẫu",
                "volumeRatio": 1.7,
                "ma20": 49520,
                "ma50": 48640,
                "ma200": 46880,
                "macd": null,
                "macd_signal": null,
                "distanceToMA20": -1.5,
                "atr14": null,
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
                        "topOpportunity": false,
                        "breakout": false,
                        "pullbackMA20": false,
                        "moneyFlow": false,
                        "accumulation": true,
                        "safe": false
                },
                "reason": "Dữ liệu mẫu cho PET. Chạy GitHub Actions sau khi thêm VNSTOCK_API_KEY để cập nhật tín hiệu thật.",
                "expertSummary": "PET đang ở trạng thái mẫu. Hệ thống sẽ cập nhật xu hướng, động lượng, dòng tiền, setup và rủi ro sau khi chạy Vnstock API.",
                "buyZone": "Canh quanh MA20 hoặc nền tích lũy gần nhất, không mua đuổi.",
                "stopLoss": "-7% đến -10%",
                "takeProfit": "+12% đến +25%",
                "allocation": "5% - 20%",
                "catalysts": [
                        "Vnstock API",
                        "Bán lẻ / Phân phối"
                ],
                "cautions": [
                        "Đây là dữ liệu mẫu trước khi chạy API",
                        "Không dùng để giao dịch thật",
                        "Chạy workflow để cập nhật"
                ]
        },
        {
                "ticker": "PSD",
                "name": "PSD",
                "sector": "Bán lẻ / Phân phối",
                "score": 73.6,
                "subscores": {
                        "trend": 16,
                        "momentum": 12.6,
                        "moneyFlow": 14.0,
                        "setup": 10.1,
                        "risk": 7.2,
                        "relativeStrength": 13.7
                },
                "setupType": "Retest nền",
                "marketState": "Uptrend",
                "action": "THEO DÕI MUA",
                "risk": "Trung bình",
                "close": 51200,
                "rsi14": 47.1,
                "ret20": 8.2,
                "ret60": 4.8,
                "volume_status": "Mẫu",
                "volumeRatio": 1.85,
                "ma20": 50310,
                "ma50": 49420,
                "ma200": 47640,
                "macd": null,
                "macd_signal": null,
                "distanceToMA20": -0.5,
                "atr14": null,
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
                        "topOpportunity": false,
                        "breakout": false,
                        "pullbackMA20": false,
                        "moneyFlow": false,
                        "accumulation": false,
                        "safe": false
                },
                "reason": "Dữ liệu mẫu cho PSD. Chạy GitHub Actions sau khi thêm VNSTOCK_API_KEY để cập nhật tín hiệu thật.",
                "expertSummary": "PSD đang ở trạng thái mẫu. Hệ thống sẽ cập nhật xu hướng, động lượng, dòng tiền, setup và rủi ro sau khi chạy Vnstock API.",
                "buyZone": "Canh quanh MA20 hoặc nền tích lũy gần nhất, không mua đuổi.",
                "stopLoss": "-7% đến -10%",
                "takeProfit": "+12% đến +25%",
                "allocation": "5% - 20%",
                "catalysts": [
                        "Vnstock API",
                        "Bán lẻ / Phân phối"
                ],
                "cautions": [
                        "Đây là dữ liệu mẫu trước khi chạy API",
                        "Không dùng để giao dịch thật",
                        "Chạy workflow để cập nhật"
                ]
        },
        {
                "ticker": "AST",
                "name": "Taseco Air Services",
                "sector": "Bán lẻ / Phân phối",
                "score": 70.3,
                "subscores": {
                        "trend": 18,
                        "momentum": 7.0,
                        "moneyFlow": 15.5,
                        "setup": 11.8,
                        "risk": 12.0,
                        "relativeStrength": 6.0
                },
                "setupType": "Vượt lại MA50",
                "marketState": "Uptrend",
                "action": "THEO DÕI MUA",
                "risk": "Trung bình",
                "close": 52000,
                "rsi14": 48.8,
                "ret20": 9.1,
                "ret60": 6.0,
                "volume_status": "Mẫu",
                "volumeRatio": 0.8,
                "ma20": 51100,
                "ma50": 50200,
                "ma200": 48400,
                "macd": null,
                "macd_signal": null,
                "distanceToMA20": 0.5,
                "atr14": null,
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
                        "topOpportunity": false,
                        "breakout": false,
                        "pullbackMA20": false,
                        "moneyFlow": true,
                        "accumulation": false,
                        "safe": true
                },
                "reason": "Dữ liệu mẫu cho AST. Chạy GitHub Actions sau khi thêm VNSTOCK_API_KEY để cập nhật tín hiệu thật.",
                "expertSummary": "AST đang ở trạng thái mẫu. Hệ thống sẽ cập nhật xu hướng, động lượng, dòng tiền, setup và rủi ro sau khi chạy Vnstock API.",
                "buyZone": "Canh quanh MA20 hoặc nền tích lũy gần nhất, không mua đuổi.",
                "stopLoss": "-7% đến -10%",
                "takeProfit": "+12% đến +25%",
                "allocation": "5% - 20%",
                "catalysts": [
                        "Vnstock API",
                        "Bán lẻ / Phân phối"
                ],
                "cautions": [
                        "Đây là dữ liệu mẫu trước khi chạy API",
                        "Không dùng để giao dịch thật",
                        "Chạy workflow để cập nhật"
                ]
        },
        {
                "ticker": "SVC",
                "name": "Savico",
                "sector": "Bán lẻ / Phân phối",
                "score": 76.8,
                "subscores": {
                        "trend": 20,
                        "momentum": 8.4,
                        "moneyFlow": 17.0,
                        "setup": 13.5,
                        "risk": 10.8,
                        "relativeStrength": 7.1
                },
                "setupType": "Chưa có setup rõ",
                "marketState": "Uptrend",
                "action": "CANH MUA / MUA KHI XÁC NHẬN",
                "risk": "Trung bình",
                "close": 52800,
                "rsi14": 50.5,
                "ret20": 10.0,
                "ret60": 7.2,
                "volume_status": "Mẫu",
                "volumeRatio": 0.95,
                "ma20": 51890,
                "ma50": 50980,
                "ma200": 49160,
                "macd": null,
                "macd_signal": null,
                "distanceToMA20": 1.5,
                "atr14": null,
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
                        "topOpportunity": false,
                        "breakout": false,
                        "pullbackMA20": false,
                        "moneyFlow": true,
                        "accumulation": false,
                        "safe": false
                },
                "reason": "Dữ liệu mẫu cho SVC. Chạy GitHub Actions sau khi thêm VNSTOCK_API_KEY để cập nhật tín hiệu thật.",
                "expertSummary": "SVC đang ở trạng thái mẫu. Hệ thống sẽ cập nhật xu hướng, động lượng, dòng tiền, setup và rủi ro sau khi chạy Vnstock API.",
                "buyZone": "Canh quanh MA20 hoặc nền tích lũy gần nhất, không mua đuổi.",
                "stopLoss": "-7% đến -10%",
                "takeProfit": "+12% đến +25%",
                "allocation": "5% - 20%",
                "catalysts": [
                        "Vnstock API",
                        "Bán lẻ / Phân phối"
                ],
                "cautions": [
                        "Đây là dữ liệu mẫu trước khi chạy API",
                        "Không dùng để giao dịch thật",
                        "Chạy workflow để cập nhật"
                ]
        },
        {
                "ticker": "SSI",
                "name": "Chứng khoán SSI",
                "sector": "Chứng khoán",
                "score": 50.6,
                "subscores": {
                        "trend": 10,
                        "momentum": 9.8,
                        "moneyFlow": 8.0,
                        "setup": 5.0,
                        "risk": 9.6,
                        "relativeStrength": 8.2
                },
                "setupType": "Pullback MA20",
                "marketState": "Trung tính",
                "action": "TRÁNH MUA MỚI",
                "risk": "Cao",
                "close": 53600,
                "rsi14": 52.2,
                "ret20": -8.0,
                "ret60": 8.4,
                "volume_status": "Mẫu",
                "volumeRatio": 1.1,
                "ma20": 52680,
                "ma50": 51760,
                "ma200": 49920,
                "macd": null,
                "macd_signal": null,
                "distanceToMA20": 2.5,
                "atr14": null,
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
                        "topOpportunity": false,
                        "breakout": false,
                        "pullbackMA20": true,
                        "moneyFlow": false,
                        "accumulation": false,
                        "safe": false
                },
                "reason": "Dữ liệu mẫu cho SSI. Chạy GitHub Actions sau khi thêm VNSTOCK_API_KEY để cập nhật tín hiệu thật.",
                "expertSummary": "SSI đang ở trạng thái mẫu. Hệ thống sẽ cập nhật xu hướng, động lượng, dòng tiền, setup và rủi ro sau khi chạy Vnstock API.",
                "buyZone": "Canh quanh MA20 hoặc nền tích lũy gần nhất, không mua đuổi.",
                "stopLoss": "-7% đến -10%",
                "takeProfit": "+12% đến +25%",
                "allocation": "5% - 20%",
                "catalysts": [
                        "Vnstock API",
                        "Chứng khoán"
                ],
                "cautions": [
                        "Đây là dữ liệu mẫu trước khi chạy API",
                        "Không dùng để giao dịch thật",
                        "Chạy workflow để cập nhật"
                ]
        },
        {
                "ticker": "VND",
                "name": "VNDIRECT",
                "sector": "Chứng khoán",
                "score": 57.1,
                "subscores": {
                        "trend": 12,
                        "momentum": 11.2,
                        "moneyFlow": 9.5,
                        "setup": 6.7,
                        "risk": 8.4,
                        "relativeStrength": 9.3
                },
                "setupType": "Breakout 20 phiên",
                "marketState": "Tích cực",
                "action": "CHỜ THÊM",
                "risk": "Cao",
                "close": 54400,
                "rsi14": 53.9,
                "ret20": -7.1,
                "ret60": 9.6,
                "volume_status": "Mẫu",
                "volumeRatio": 1.25,
                "ma20": 53470,
                "ma50": 52540,
                "ma200": 50680,
                "macd": null,
                "macd_signal": null,
                "distanceToMA20": 3.5,
                "atr14": null,
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
                        "topOpportunity": false,
                        "breakout": true,
                        "pullbackMA20": false,
                        "moneyFlow": false,
                        "accumulation": false,
                        "safe": false
                },
                "reason": "Dữ liệu mẫu cho VND. Chạy GitHub Actions sau khi thêm VNSTOCK_API_KEY để cập nhật tín hiệu thật.",
                "expertSummary": "VND đang ở trạng thái mẫu. Hệ thống sẽ cập nhật xu hướng, động lượng, dòng tiền, setup và rủi ro sau khi chạy Vnstock API.",
                "buyZone": "Canh quanh MA20 hoặc nền tích lũy gần nhất, không mua đuổi.",
                "stopLoss": "-7% đến -10%",
                "takeProfit": "+12% đến +25%",
                "allocation": "5% - 20%",
                "catalysts": [
                        "Vnstock API",
                        "Chứng khoán"
                ],
                "cautions": [
                        "Đây là dữ liệu mẫu trước khi chạy API",
                        "Không dùng để giao dịch thật",
                        "Chạy workflow để cập nhật"
                ]
        },
        {
                "ticker": "HCM",
                "name": "Chứng khoán HSC",
                "sector": "Chứng khoán",
                "score": 63.6,
                "subscores": {
                        "trend": 14,
                        "momentum": 12.6,
                        "moneyFlow": 11.0,
                        "setup": 8.4,
                        "risk": 7.2,
                        "relativeStrength": 10.4
                },
                "setupType": "Tích lũy biên hẹp",
                "marketState": "Tích cực",
                "action": "CHỜ THÊM",
                "risk": "Cao",
                "close": 55200,
                "rsi14": 55.6,
                "ret20": -6.2,
                "ret60": 10.8,
                "volume_status": "Mẫu",
                "volumeRatio": 1.4,
                "ma20": 54260,
                "ma50": 53320,
                "ma200": 51440,
                "macd": null,
                "macd_signal": null,
                "distanceToMA20": 4.5,
                "atr14": null,
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
                        "topOpportunity": false,
                        "breakout": false,
                        "pullbackMA20": false,
                        "moneyFlow": false,
                        "accumulation": true,
                        "safe": false
                },
                "reason": "Dữ liệu mẫu cho HCM. Chạy GitHub Actions sau khi thêm VNSTOCK_API_KEY để cập nhật tín hiệu thật.",
                "expertSummary": "HCM đang ở trạng thái mẫu. Hệ thống sẽ cập nhật xu hướng, động lượng, dòng tiền, setup và rủi ro sau khi chạy Vnstock API.",
                "buyZone": "Canh quanh MA20 hoặc nền tích lũy gần nhất, không mua đuổi.",
                "stopLoss": "-7% đến -10%",
                "takeProfit": "+12% đến +25%",
                "allocation": "5% - 20%",
                "catalysts": [
                        "Vnstock API",
                        "Chứng khoán"
                ],
                "cautions": [
                        "Đây là dữ liệu mẫu trước khi chạy API",
                        "Không dùng để giao dịch thật",
                        "Chạy workflow để cập nhật"
                ]
        },
        {
                "ticker": "VCI",
                "name": "Vietcap",
                "sector": "Chứng khoán",
                "score": 69.1,
                "subscores": {
                        "trend": 16,
                        "momentum": 7.0,
                        "moneyFlow": 12.5,
                        "setup": 10.1,
                        "risk": 12.0,
                        "relativeStrength": 11.5
                },
                "setupType": "Retest nền",
                "marketState": "Uptrend",
                "action": "THEO DÕI MUA",
                "risk": "Cao",
                "close": 56000,
                "rsi14": 57.3,
                "ret20": -5.3,
                "ret60": 12.0,
                "volume_status": "Mẫu",
                "volumeRatio": 1.55,
                "ma20": 55050,
                "ma50": 54100,
                "ma200": 52200,
                "macd": null,
                "macd_signal": null,
                "distanceToMA20": 5.5,
                "atr14": null,
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
                        "topOpportunity": false,
                        "breakout": false,
                        "pullbackMA20": false,
                        "moneyFlow": false,
                        "accumulation": false,
                        "safe": true
                },
                "reason": "Dữ liệu mẫu cho VCI. Chạy GitHub Actions sau khi thêm VNSTOCK_API_KEY để cập nhật tín hiệu thật.",
                "expertSummary": "VCI đang ở trạng thái mẫu. Hệ thống sẽ cập nhật xu hướng, động lượng, dòng tiền, setup và rủi ro sau khi chạy Vnstock API.",
                "buyZone": "Canh quanh MA20 hoặc nền tích lũy gần nhất, không mua đuổi.",
                "stopLoss": "-7% đến -10%",
                "takeProfit": "+12% đến +25%",
                "allocation": "5% - 20%",
                "catalysts": [
                        "Vnstock API",
                        "Chứng khoán"
                ],
                "cautions": [
                        "Đây là dữ liệu mẫu trước khi chạy API",
                        "Không dùng để giao dịch thật",
                        "Chạy workflow để cập nhật"
                ]
        },
        {
                "ticker": "MBS",
                "name": "Chứng khoán MB",
                "sector": "Chứng khoán",
                "score": 75.6,
                "subscores": {
                        "trend": 18,
                        "momentum": 8.4,
                        "moneyFlow": 14.0,
                        "setup": 11.8,
                        "risk": 10.8,
                        "relativeStrength": 12.6
                },
                "setupType": "Vượt lại MA50",
                "marketState": "Uptrend",
                "action": "CANH MUA / MUA KHI XÁC NHẬN",
                "risk": "Cao",
                "close": 56800,
                "rsi14": 59.0,
                "ret20": -4.4,
                "ret60": 13.2,
                "volume_status": "Mẫu",
                "volumeRatio": 1.7,
                "ma20": 55840,
                "ma50": 54880,
                "ma200": 52960,
                "macd": null,
                "macd_signal": null,
                "distanceToMA20": 6.5,
                "atr14": null,
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
                        "topOpportunity": false,
                        "breakout": false,
                        "pullbackMA20": false,
                        "moneyFlow": false,
                        "accumulation": false,
                        "safe": false
                },
                "reason": "Dữ liệu mẫu cho MBS. Chạy GitHub Actions sau khi thêm VNSTOCK_API_KEY để cập nhật tín hiệu thật.",
                "expertSummary": "MBS đang ở trạng thái mẫu. Hệ thống sẽ cập nhật xu hướng, động lượng, dòng tiền, setup và rủi ro sau khi chạy Vnstock API.",
                "buyZone": "Canh quanh MA20 hoặc nền tích lũy gần nhất, không mua đuổi.",
                "stopLoss": "-7% đến -10%",
                "takeProfit": "+12% đến +25%",
                "allocation": "5% - 20%",
                "catalysts": [
                        "Vnstock API",
                        "Chứng khoán"
                ],
                "cautions": [
                        "Đây là dữ liệu mẫu trước khi chạy API",
                        "Không dùng để giao dịch thật",
                        "Chạy workflow để cập nhật"
                ]
        },
        {
                "ticker": "FTS",
                "name": "Chứng khoán FPT",
                "sector": "Chứng khoán",
                "score": 82.1,
                "subscores": {
                        "trend": 20,
                        "momentum": 9.8,
                        "moneyFlow": 15.5,
                        "setup": 13.5,
                        "risk": 9.6,
                        "relativeStrength": 13.7
                },
                "setupType": "Chưa có setup rõ",
                "marketState": "Uptrend",
                "action": "CANH MUA / MUA KHI XÁC NHẬN",
                "risk": "Cao",
                "close": 57600,
                "rsi14": 60.7,
                "ret20": -3.5,
                "ret60": 14.4,
                "volume_status": "Mẫu",
                "volumeRatio": 1.85,
                "ma20": 56630,
                "ma50": 55660,
                "ma200": 53720,
                "macd": null,
                "macd_signal": null,
                "distanceToMA20": 7.5,
                "atr14": null,
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
                        "topOpportunity": true,
                        "breakout": false,
                        "pullbackMA20": false,
                        "moneyFlow": true,
                        "accumulation": false,
                        "safe": false
                },
                "reason": "Dữ liệu mẫu cho FTS. Chạy GitHub Actions sau khi thêm VNSTOCK_API_KEY để cập nhật tín hiệu thật.",
                "expertSummary": "FTS đang ở trạng thái mẫu. Hệ thống sẽ cập nhật xu hướng, động lượng, dòng tiền, setup và rủi ro sau khi chạy Vnstock API.",
                "buyZone": "Canh quanh MA20 hoặc nền tích lũy gần nhất, không mua đuổi.",
                "stopLoss": "-7% đến -10%",
                "takeProfit": "+12% đến +25%",
                "allocation": "5% - 20%",
                "catalysts": [
                        "Vnstock API",
                        "Chứng khoán"
                ],
                "cautions": [
                        "Đây là dữ liệu mẫu trước khi chạy API",
                        "Không dùng để giao dịch thật",
                        "Chạy workflow để cập nhật"
                ]
        },
        {
                "ticker": "BSI",
                "name": "Chứng khoán BIDV",
                "sector": "Chứng khoán",
                "score": 57.6,
                "subscores": {
                        "trend": 10,
                        "momentum": 11.2,
                        "moneyFlow": 17.0,
                        "setup": 5.0,
                        "risk": 8.4,
                        "relativeStrength": 6.0
                },
                "setupType": "Pullback MA20",
                "marketState": "Trung tính",
                "action": "CHỜ THÊM",
                "risk": "Cao",
                "close": 58400,
                "rsi14": 62.4,
                "ret20": -2.6,
                "ret60": 15.6,
                "volume_status": "Mẫu",
                "volumeRatio": 0.8,
                "ma20": 57420,
                "ma50": 56440,
                "ma200": 54480,
                "macd": null,
                "macd_signal": null,
                "distanceToMA20": -3.5,
                "atr14": null,
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
                        "topOpportunity": false,
                        "breakout": false,
                        "pullbackMA20": true,
                        "moneyFlow": true,
                        "accumulation": false,
                        "safe": false
                },
                "reason": "Dữ liệu mẫu cho BSI. Chạy GitHub Actions sau khi thêm VNSTOCK_API_KEY để cập nhật tín hiệu thật.",
                "expertSummary": "BSI đang ở trạng thái mẫu. Hệ thống sẽ cập nhật xu hướng, động lượng, dòng tiền, setup và rủi ro sau khi chạy Vnstock API.",
                "buyZone": "Canh quanh MA20 hoặc nền tích lũy gần nhất, không mua đuổi.",
                "stopLoss": "-7% đến -10%",
                "takeProfit": "+12% đến +25%",
                "allocation": "5% - 20%",
                "catalysts": [
                        "Vnstock API",
                        "Chứng khoán"
                ],
                "cautions": [
                        "Đây là dữ liệu mẫu trước khi chạy API",
                        "Không dùng để giao dịch thật",
                        "Chạy workflow để cập nhật"
                ]
        },
        {
                "ticker": "CTS",
                "name": "Chứng khoán VietinBank",
                "sector": "Chứng khoán",
                "score": 53.6,
                "subscores": {
                        "trend": 12,
                        "momentum": 12.6,
                        "moneyFlow": 8.0,
                        "setup": 6.7,
                        "risk": 7.2,
                        "relativeStrength": 7.1
                },
                "setupType": "Breakout 20 phiên",
                "marketState": "Tích cực",
                "action": "TRÁNH MUA MỚI",
                "risk": "Cao",
                "close": 59200,
                "rsi14": 64.1,
                "ret20": -1.7,
                "ret60": 16.8,
                "volume_status": "Mẫu",
                "volumeRatio": 0.95,
                "ma20": 58210,
                "ma50": 57220,
                "ma200": 55240,
                "macd": null,
                "macd_signal": null,
                "distanceToMA20": -2.5,
                "atr14": null,
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
                        "topOpportunity": false,
                        "breakout": true,
                        "pullbackMA20": false,
                        "moneyFlow": false,
                        "accumulation": false,
                        "safe": false
                },
                "reason": "Dữ liệu mẫu cho CTS. Chạy GitHub Actions sau khi thêm VNSTOCK_API_KEY để cập nhật tín hiệu thật.",
                "expertSummary": "CTS đang ở trạng thái mẫu. Hệ thống sẽ cập nhật xu hướng, động lượng, dòng tiền, setup và rủi ro sau khi chạy Vnstock API.",
                "buyZone": "Canh quanh MA20 hoặc nền tích lũy gần nhất, không mua đuổi.",
                "stopLoss": "-7% đến -10%",
                "takeProfit": "+12% đến +25%",
                "allocation": "5% - 20%",
                "catalysts": [
                        "Vnstock API",
                        "Chứng khoán"
                ],
                "cautions": [
                        "Đây là dữ liệu mẫu trước khi chạy API",
                        "Không dùng để giao dịch thật",
                        "Chạy workflow để cập nhật"
                ]
        },
        {
                "ticker": "SHS",
                "name": "Chứng khoán Sài Gòn Hà Nội",
                "sector": "Chứng khoán",
                "score": 59.1,
                "subscores": {
                        "trend": 14,
                        "momentum": 7.0,
                        "moneyFlow": 9.5,
                        "setup": 8.4,
                        "risk": 12.0,
                        "relativeStrength": 8.2
                },
                "setupType": "Tích lũy biên hẹp",
                "marketState": "Tích cực",
                "action": "CHỜ THÊM",
                "risk": "Cao",
                "close": 60000,
                "rsi14": 65.8,
                "ret20": -0.8,
                "ret60": -12.0,
                "volume_status": "Mẫu",
                "volumeRatio": 1.1,
                "ma20": 59000,
                "ma50": 58000,
                "ma200": 56000,
                "macd": null,
                "macd_signal": null,
                "distanceToMA20": -1.5,
                "atr14": null,
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
                        "topOpportunity": false,
                        "breakout": false,
                        "pullbackMA20": false,
                        "moneyFlow": false,
                        "accumulation": true,
                        "safe": false
                },
                "reason": "Dữ liệu mẫu cho SHS. Chạy GitHub Actions sau khi thêm VNSTOCK_API_KEY để cập nhật tín hiệu thật.",
                "expertSummary": "SHS đang ở trạng thái mẫu. Hệ thống sẽ cập nhật xu hướng, động lượng, dòng tiền, setup và rủi ro sau khi chạy Vnstock API.",
                "buyZone": "Canh quanh MA20 hoặc nền tích lũy gần nhất, không mua đuổi.",
                "stopLoss": "-7% đến -10%",
                "takeProfit": "+12% đến +25%",
                "allocation": "5% - 20%",
                "catalysts": [
                        "Vnstock API",
                        "Chứng khoán"
                ],
                "cautions": [
                        "Đây là dữ liệu mẫu trước khi chạy API",
                        "Không dùng để giao dịch thật",
                        "Chạy workflow để cập nhật"
                ]
        },
        {
                "ticker": "ORS",
                "name": "Chứng khoán Tiên Phong",
                "sector": "Chứng khoán",
                "score": 65.6,
                "subscores": {
                        "trend": 16,
                        "momentum": 8.4,
                        "moneyFlow": 11.0,
                        "setup": 10.1,
                        "risk": 10.8,
                        "relativeStrength": 9.3
                },
                "setupType": "Retest nền",
                "marketState": "Uptrend",
                "action": "THEO DÕI MUA",
                "risk": "Cao",
                "close": 60800,
                "rsi14": 67.5,
                "ret20": 0.1,
                "ret60": -10.8,
                "volume_status": "Mẫu",
                "volumeRatio": 1.25,
                "ma20": 59790,
                "ma50": 58780,
                "ma200": 56760,
                "macd": null,
                "macd_signal": null,
                "distanceToMA20": -0.5,
                "atr14": null,
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
                        "topOpportunity": false,
                        "breakout": false,
                        "pullbackMA20": false,
                        "moneyFlow": false,
                        "accumulation": false,
                        "safe": false
                },
                "reason": "Dữ liệu mẫu cho ORS. Chạy GitHub Actions sau khi thêm VNSTOCK_API_KEY để cập nhật tín hiệu thật.",
                "expertSummary": "ORS đang ở trạng thái mẫu. Hệ thống sẽ cập nhật xu hướng, động lượng, dòng tiền, setup và rủi ro sau khi chạy Vnstock API.",
                "buyZone": "Canh quanh MA20 hoặc nền tích lũy gần nhất, không mua đuổi.",
                "stopLoss": "-7% đến -10%",
                "takeProfit": "+12% đến +25%",
                "allocation": "5% - 20%",
                "catalysts": [
                        "Vnstock API",
                        "Chứng khoán"
                ],
                "cautions": [
                        "Đây là dữ liệu mẫu trước khi chạy API",
                        "Không dùng để giao dịch thật",
                        "Chạy workflow để cập nhật"
                ]
        },
        {
                "ticker": "AGR",
                "name": "Agriseco",
                "sector": "Chứng khoán",
                "score": 72.1,
                "subscores": {
                        "trend": 18,
                        "momentum": 9.8,
                        "moneyFlow": 12.5,
                        "setup": 11.8,
                        "risk": 9.6,
                        "relativeStrength": 10.4
                },
                "setupType": "Vượt lại MA50",
                "marketState": "Uptrend",
                "action": "THEO DÕI MUA",
                "risk": "Cao",
                "close": 61600,
                "rsi14": 69.2,
                "ret20": 1.0,
                "ret60": -9.6,
                "volume_status": "Mẫu",
                "volumeRatio": 1.4,
                "ma20": 60580,
                "ma50": 59560,
                "ma200": 57520,
                "macd": null,
                "macd_signal": null,
                "distanceToMA20": 0.5,
                "atr14": null,
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
                        "topOpportunity": false,
                        "breakout": false,
                        "pullbackMA20": false,
                        "moneyFlow": false,
                        "accumulation": false,
                        "safe": false
                },
                "reason": "Dữ liệu mẫu cho AGR. Chạy GitHub Actions sau khi thêm VNSTOCK_API_KEY để cập nhật tín hiệu thật.",
                "expertSummary": "AGR đang ở trạng thái mẫu. Hệ thống sẽ cập nhật xu hướng, động lượng, dòng tiền, setup và rủi ro sau khi chạy Vnstock API.",
                "buyZone": "Canh quanh MA20 hoặc nền tích lũy gần nhất, không mua đuổi.",
                "stopLoss": "-7% đến -10%",
                "takeProfit": "+12% đến +25%",
                "allocation": "5% - 20%",
                "catalysts": [
                        "Vnstock API",
                        "Chứng khoán"
                ],
                "cautions": [
                        "Đây là dữ liệu mẫu trước khi chạy API",
                        "Không dùng để giao dịch thật",
                        "Chạy workflow để cập nhật"
                ]
        },
        {
                "ticker": "APG",
                "name": "APG Securities",
                "sector": "Chứng khoán",
                "score": 78.6,
                "subscores": {
                        "trend": 20,
                        "momentum": 11.2,
                        "moneyFlow": 14.0,
                        "setup": 13.5,
                        "risk": 8.4,
                        "relativeStrength": 11.5
                },
                "setupType": "Chưa có setup rõ",
                "marketState": "Uptrend",
                "action": "CANH MUA / MUA KHI XÁC NHẬN",
                "risk": "Cao",
                "close": 62400,
                "rsi14": 70.9,
                "ret20": 1.9,
                "ret60": -8.4,
                "volume_status": "Mẫu",
                "volumeRatio": 1.55,
                "ma20": 61370,
                "ma50": 60340,
                "ma200": 58280,
                "macd": null,
                "macd_signal": null,
                "distanceToMA20": 1.5,
                "atr14": null,
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
                        "topOpportunity": false,
                        "breakout": false,
                        "pullbackMA20": false,
                        "moneyFlow": false,
                        "accumulation": false,
                        "safe": false
                },
                "reason": "Dữ liệu mẫu cho APG. Chạy GitHub Actions sau khi thêm VNSTOCK_API_KEY để cập nhật tín hiệu thật.",
                "expertSummary": "APG đang ở trạng thái mẫu. Hệ thống sẽ cập nhật xu hướng, động lượng, dòng tiền, setup và rủi ro sau khi chạy Vnstock API.",
                "buyZone": "Canh quanh MA20 hoặc nền tích lũy gần nhất, không mua đuổi.",
                "stopLoss": "-7% đến -10%",
                "takeProfit": "+12% đến +25%",
                "allocation": "5% - 20%",
                "catalysts": [
                        "Vnstock API",
                        "Chứng khoán"
                ],
                "cautions": [
                        "Đây là dữ liệu mẫu trước khi chạy API",
                        "Không dùng để giao dịch thật",
                        "Chạy workflow để cập nhật"
                ]
        },
        {
                "ticker": "VDS",
                "name": "Rồng Việt Securities",
                "sector": "Chứng khoán",
                "score": 62.9,
                "subscores": {
                        "trend": 10,
                        "momentum": 12.6,
                        "moneyFlow": 15.5,
                        "setup": 5.0,
                        "risk": 7.2,
                        "relativeStrength": 12.6
                },
                "setupType": "Pullback MA20",
                "marketState": "Trung tính",
                "action": "CHỜ THÊM",
                "risk": "Cao",
                "close": 63200,
                "rsi14": 42.0,
                "ret20": 2.8,
                "ret60": -7.2,
                "volume_status": "Mẫu",
                "volumeRatio": 1.7,
                "ma20": 62160,
                "ma50": 61120,
                "ma200": 59040,
                "macd": null,
                "macd_signal": null,
                "distanceToMA20": 2.5,
                "atr14": null,
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
                        "topOpportunity": false,
                        "breakout": false,
                        "pullbackMA20": true,
                        "moneyFlow": true,
                        "accumulation": false,
                        "safe": false
                },
                "reason": "Dữ liệu mẫu cho VDS. Chạy GitHub Actions sau khi thêm VNSTOCK_API_KEY để cập nhật tín hiệu thật.",
                "expertSummary": "VDS đang ở trạng thái mẫu. Hệ thống sẽ cập nhật xu hướng, động lượng, dòng tiền, setup và rủi ro sau khi chạy Vnstock API.",
                "buyZone": "Canh quanh MA20 hoặc nền tích lũy gần nhất, không mua đuổi.",
                "stopLoss": "-7% đến -10%",
                "takeProfit": "+12% đến +25%",
                "allocation": "5% - 20%",
                "catalysts": [
                        "Vnstock API",
                        "Chứng khoán"
                ],
                "cautions": [
                        "Đây là dữ liệu mẫu trước khi chạy API",
                        "Không dùng để giao dịch thật",
                        "Chạy workflow để cập nhật"
                ]
        },
        {
                "ticker": "BVS",
                "name": "Bảo Việt Securities",
                "sector": "Chứng khoán",
                "score": 68.4,
                "subscores": {
                        "trend": 12,
                        "momentum": 7.0,
                        "moneyFlow": 17.0,
                        "setup": 6.7,
                        "risk": 12.0,
                        "relativeStrength": 13.7
                },
                "setupType": "Breakout 20 phiên",
                "marketState": "Tích cực",
                "action": "THEO DÕI MUA",
                "risk": "Cao",
                "close": 64000,
                "rsi14": 43.7,
                "ret20": 3.7,
                "ret60": -6.0,
                "volume_status": "Mẫu",
                "volumeRatio": 1.85,
                "ma20": 62950,
                "ma50": 61900,
                "ma200": 59800,
                "macd": null,
                "macd_signal": null,
                "distanceToMA20": 3.5,
                "atr14": null,
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
                        "topOpportunity": false,
                        "breakout": true,
                        "pullbackMA20": false,
                        "moneyFlow": true,
                        "accumulation": false,
                        "safe": true
                },
                "reason": "Dữ liệu mẫu cho BVS. Chạy GitHub Actions sau khi thêm VNSTOCK_API_KEY để cập nhật tín hiệu thật.",
                "expertSummary": "BVS đang ở trạng thái mẫu. Hệ thống sẽ cập nhật xu hướng, động lượng, dòng tiền, setup và rủi ro sau khi chạy Vnstock API.",
                "buyZone": "Canh quanh MA20 hoặc nền tích lũy gần nhất, không mua đuổi.",
                "stopLoss": "-7% đến -10%",
                "takeProfit": "+12% đến +25%",
                "allocation": "5% - 20%",
                "catalysts": [
                        "Vnstock API",
                        "Chứng khoán"
                ],
                "cautions": [
                        "Đây là dữ liệu mẫu trước khi chạy API",
                        "Không dùng để giao dịch thật",
                        "Chạy workflow để cập nhật"
                ]
        },
        {
                "ticker": "VHM",
                "name": "Vinhomes",
                "sector": "Bất động sản / KCN",
                "score": 55.6,
                "subscores": {
                        "trend": 14,
                        "momentum": 8.4,
                        "moneyFlow": 8.0,
                        "setup": 8.4,
                        "risk": 10.8,
                        "relativeStrength": 6.0
                },
                "setupType": "Tích lũy biên hẹp",
                "marketState": "Tích cực",
                "action": "CHỜ THÊM",
                "risk": "Cao",
                "close": 64800,
                "rsi14": 45.4,
                "ret20": 4.6,
                "ret60": -4.8,
                "volume_status": "Mẫu",
                "volumeRatio": 0.8,
                "ma20": 63740,
                "ma50": 62680,
                "ma200": 60560,
                "macd": null,
                "macd_signal": null,
                "distanceToMA20": 4.5,
                "atr14": null,
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
                        "topOpportunity": false,
                        "breakout": false,
                        "pullbackMA20": false,
                        "moneyFlow": false,
                        "accumulation": true,
                        "safe": false
                },
                "reason": "Dữ liệu mẫu cho VHM. Chạy GitHub Actions sau khi thêm VNSTOCK_API_KEY để cập nhật tín hiệu thật.",
                "expertSummary": "VHM đang ở trạng thái mẫu. Hệ thống sẽ cập nhật xu hướng, động lượng, dòng tiền, setup và rủi ro sau khi chạy Vnstock API.",
                "buyZone": "Canh quanh MA20 hoặc nền tích lũy gần nhất, không mua đuổi.",
                "stopLoss": "-7% đến -10%",
                "takeProfit": "+12% đến +25%",
                "allocation": "5% - 20%",
                "catalysts": [
                        "Vnstock API",
                        "Bất động sản / KCN"
                ],
                "cautions": [
                        "Đây là dữ liệu mẫu trước khi chạy API",
                        "Không dùng để giao dịch thật",
                        "Chạy workflow để cập nhật"
                ]
        },
        {
                "ticker": "VIC",
                "name": "Vingroup",
                "sector": "Bất động sản / KCN",
                "score": 62.1,
                "subscores": {
                        "trend": 16,
                        "momentum": 9.8,
                        "moneyFlow": 9.5,
                        "setup": 10.1,
                        "risk": 9.6,
                        "relativeStrength": 7.1
                },
                "setupType": "Retest nền",
                "marketState": "Uptrend",
                "action": "CHỜ THÊM",
                "risk": "Cao",
                "close": 65600,
                "rsi14": 47.1,
                "ret20": 5.5,
                "ret60": -3.6,
                "volume_status": "Mẫu",
                "volumeRatio": 0.95,
                "ma20": 64530,
                "ma50": 63460,
                "ma200": 61320,
                "macd": null,
                "macd_signal": null,
                "distanceToMA20": 5.5,
                "atr14": null,
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
                        "topOpportunity": false,
                        "breakout": false,
                        "pullbackMA20": false,
                        "moneyFlow": false,
                        "accumulation": false,
                        "safe": false
                },
                "reason": "Dữ liệu mẫu cho VIC. Chạy GitHub Actions sau khi thêm VNSTOCK_API_KEY để cập nhật tín hiệu thật.",
                "expertSummary": "VIC đang ở trạng thái mẫu. Hệ thống sẽ cập nhật xu hướng, động lượng, dòng tiền, setup và rủi ro sau khi chạy Vnstock API.",
                "buyZone": "Canh quanh MA20 hoặc nền tích lũy gần nhất, không mua đuổi.",
                "stopLoss": "-7% đến -10%",
                "takeProfit": "+12% đến +25%",
                "allocation": "5% - 20%",
                "catalysts": [
                        "Vnstock API",
                        "Bất động sản / KCN"
                ],
                "cautions": [
                        "Đây là dữ liệu mẫu trước khi chạy API",
                        "Không dùng để giao dịch thật",
                        "Chạy workflow để cập nhật"
                ]
        },
        {
                "ticker": "VRE",
                "name": "Vincom Retail",
                "sector": "Bất động sản / KCN",
                "score": 68.6,
                "subscores": {
                        "trend": 18,
                        "momentum": 11.2,
                        "moneyFlow": 11.0,
                        "setup": 11.8,
                        "risk": 8.4,
                        "relativeStrength": 8.2
                },
                "setupType": "Vượt lại MA50",
                "marketState": "Uptrend",
                "action": "THEO DÕI MUA",
                "risk": "Cao",
                "close": 66400,
                "rsi14": 48.8,
                "ret20": 6.4,
                "ret60": -2.4,
                "volume_status": "Mẫu",
                "volumeRatio": 1.1,
                "ma20": 65320,
                "ma50": 64240,
                "ma200": 62080,
                "macd": null,
                "macd_signal": null,
                "distanceToMA20": 6.5,
                "atr14": null,
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
                        "topOpportunity": false,
                        "breakout": false,
                        "pullbackMA20": false,
                        "moneyFlow": false,
                        "accumulation": false,
                        "safe": false
                },
                "reason": "Dữ liệu mẫu cho VRE. Chạy GitHub Actions sau khi thêm VNSTOCK_API_KEY để cập nhật tín hiệu thật.",
                "expertSummary": "VRE đang ở trạng thái mẫu. Hệ thống sẽ cập nhật xu hướng, động lượng, dòng tiền, setup và rủi ro sau khi chạy Vnstock API.",
                "buyZone": "Canh quanh MA20 hoặc nền tích lũy gần nhất, không mua đuổi.",
                "stopLoss": "-7% đến -10%",
                "takeProfit": "+12% đến +25%",
                "allocation": "5% - 20%",
                "catalysts": [
                        "Vnstock API",
                        "Bất động sản / KCN"
                ],
                "cautions": [
                        "Đây là dữ liệu mẫu trước khi chạy API",
                        "Không dùng để giao dịch thật",
                        "Chạy workflow để cập nhật"
                ]
        },
        {
                "ticker": "KDH",
                "name": "Khang Điền",
                "sector": "Bất động sản / KCN",
                "score": 75.1,
                "subscores": {
                        "trend": 20,
                        "momentum": 12.6,
                        "moneyFlow": 12.5,
                        "setup": 13.5,
                        "risk": 7.2,
                        "relativeStrength": 9.3
                },
                "setupType": "Chưa có setup rõ",
                "marketState": "Uptrend",
                "action": "CANH MUA / MUA KHI XÁC NHẬN",
                "risk": "Cao",
                "close": 67200,
                "rsi14": 50.5,
                "ret20": 7.3,
                "ret60": -1.2,
                "volume_status": "Mẫu",
                "volumeRatio": 1.25,
                "ma20": 66110,
                "ma50": 65020,
                "ma200": 62840,
                "macd": null,
                "macd_signal": null,
                "distanceToMA20": 7.5,
                "atr14": null,
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
                        "topOpportunity": false,
                        "breakout": false,
                        "pullbackMA20": false,
                        "moneyFlow": false,
                        "accumulation": false,
                        "safe": false
                },
                "reason": "Dữ liệu mẫu cho KDH. Chạy GitHub Actions sau khi thêm VNSTOCK_API_KEY để cập nhật tín hiệu thật.",
                "expertSummary": "KDH đang ở trạng thái mẫu. Hệ thống sẽ cập nhật xu hướng, động lượng, dòng tiền, setup và rủi ro sau khi chạy Vnstock API.",
                "buyZone": "Canh quanh MA20 hoặc nền tích lũy gần nhất, không mua đuổi.",
                "stopLoss": "-7% đến -10%",
                "takeProfit": "+12% đến +25%",
                "allocation": "5% - 20%",
                "catalysts": [
                        "Vnstock API",
                        "Bất động sản / KCN"
                ],
                "cautions": [
                        "Đây là dữ liệu mẫu trước khi chạy API",
                        "Không dùng để giao dịch thật",
                        "Chạy workflow để cập nhật"
                ]
        },
        {
                "ticker": "NLG",
                "name": "Nam Long",
                "sector": "Bất động sản / KCN",
                "score": 58.4,
                "subscores": {
                        "trend": 10,
                        "momentum": 7.0,
                        "moneyFlow": 14.0,
                        "setup": 5.0,
                        "risk": 12.0,
                        "relativeStrength": 10.4
                },
                "setupType": "Pullback MA20",
                "marketState": "Trung tính",
                "action": "CHỜ THÊM",
                "risk": "Cao",
                "close": 68000,
                "rsi14": 52.2,
                "ret20": 8.2,
                "ret60": 0.0,
                "volume_status": "Mẫu",
                "volumeRatio": 1.4,
                "ma20": 66900,
                "ma50": 65800,
                "ma200": 63600,
                "macd": null,
                "macd_signal": null,
                "distanceToMA20": -3.5,
                "atr14": null,
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
                        "topOpportunity": false,
                        "breakout": false,
                        "pullbackMA20": true,
                        "moneyFlow": false,
                        "accumulation": false,
                        "safe": false
                },
                "reason": "Dữ liệu mẫu cho NLG. Chạy GitHub Actions sau khi thêm VNSTOCK_API_KEY để cập nhật tín hiệu thật.",
                "expertSummary": "NLG đang ở trạng thái mẫu. Hệ thống sẽ cập nhật xu hướng, động lượng, dòng tiền, setup và rủi ro sau khi chạy Vnstock API.",
                "buyZone": "Canh quanh MA20 hoặc nền tích lũy gần nhất, không mua đuổi.",
                "stopLoss": "-7% đến -10%",
                "takeProfit": "+12% đến +25%",
                "allocation": "5% - 20%",
                "catalysts": [
                        "Vnstock API",
                        "Bất động sản / KCN"
                ],
                "cautions": [
                        "Đây là dữ liệu mẫu trước khi chạy API",
                        "Không dùng để giao dịch thật",
                        "Chạy workflow để cập nhật"
                ]
        },
        {
                "ticker": "DXG",
                "name": "Đất Xanh",
                "sector": "Bất động sản / KCN",
                "score": 64.9,
                "subscores": {
                        "trend": 12,
                        "momentum": 8.4,
                        "moneyFlow": 15.5,
                        "setup": 6.7,
                        "risk": 10.8,
                        "relativeStrength": 11.5
                },
                "setupType": "Breakout 20 phiên",
                "marketState": "Tích cực",
                "action": "CHỜ THÊM",
                "risk": "Cao",
                "close": 68800,
                "rsi14": 53.9,
                "ret20": 9.1,
                "ret60": 1.2,
                "volume_status": "Mẫu",
                "volumeRatio": 1.55,
                "ma20": 67690,
                "ma50": 66580,
                "ma200": 64360,
                "macd": null,
                "macd_signal": null,
                "distanceToMA20": -2.5,
                "atr14": null,
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
                        "topOpportunity": false,
                        "breakout": true,
                        "pullbackMA20": false,
                        "moneyFlow": true,
                        "accumulation": false,
                        "safe": false
                },
                "reason": "Dữ liệu mẫu cho DXG. Chạy GitHub Actions sau khi thêm VNSTOCK_API_KEY để cập nhật tín hiệu thật.",
                "expertSummary": "DXG đang ở trạng thái mẫu. Hệ thống sẽ cập nhật xu hướng, động lượng, dòng tiền, setup và rủi ro sau khi chạy Vnstock API.",
                "buyZone": "Canh quanh MA20 hoặc nền tích lũy gần nhất, không mua đuổi.",
                "stopLoss": "-7% đến -10%",
                "takeProfit": "+12% đến +25%",
                "allocation": "5% - 20%",
                "catalysts": [
                        "Vnstock API",
                        "Bất động sản / KCN"
                ],
                "cautions": [
                        "Đây là dữ liệu mẫu trước khi chạy API",
                        "Không dùng để giao dịch thật",
                        "Chạy workflow để cập nhật"
                ]
        },
        {
                "ticker": "PDR",
                "name": "Phát Đạt",
                "sector": "Bất động sản / KCN",
                "score": 71.4,
                "subscores": {
                        "trend": 14,
                        "momentum": 9.8,
                        "moneyFlow": 17.0,
                        "setup": 8.4,
                        "risk": 9.6,
                        "relativeStrength": 12.6
                },
                "setupType": "Tích lũy biên hẹp",
                "marketState": "Tích cực",
                "action": "THEO DÕI MUA",
                "risk": "Cao",
                "close": 69600,
                "rsi14": 55.6,
                "ret20": 10.0,
                "ret60": 2.4,
                "volume_status": "Mẫu",
                "volumeRatio": 1.7,
                "ma20": 68480,
                "ma50": 67360,
                "ma200": 65120,
                "macd": null,
                "macd_signal": null,
                "distanceToMA20": -1.5,
                "atr14": null,
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
                        "topOpportunity": false,
                        "breakout": false,
                        "pullbackMA20": false,
                        "moneyFlow": true,
                        "accumulation": true,
                        "safe": false
                },
                "reason": "Dữ liệu mẫu cho PDR. Chạy GitHub Actions sau khi thêm VNSTOCK_API_KEY để cập nhật tín hiệu thật.",
                "expertSummary": "PDR đang ở trạng thái mẫu. Hệ thống sẽ cập nhật xu hướng, động lượng, dòng tiền, setup và rủi ro sau khi chạy Vnstock API.",
                "buyZone": "Canh quanh MA20 hoặc nền tích lũy gần nhất, không mua đuổi.",
                "stopLoss": "-7% đến -10%",
                "takeProfit": "+12% đến +25%",
                "allocation": "5% - 20%",
                "catalysts": [
                        "Vnstock API",
                        "Bất động sản / KCN"
                ],
                "cautions": [
                        "Đây là dữ liệu mẫu trước khi chạy API",
                        "Không dùng để giao dịch thật",
                        "Chạy workflow để cập nhật"
                ]
        },
        {
                "ticker": "DIG",
                "name": "DIC Corp",
                "sector": "Bất động sản / KCN",
                "score": 67.4,
                "subscores": {
                        "trend": 16,
                        "momentum": 11.2,
                        "moneyFlow": 8.0,
                        "setup": 10.1,
                        "risk": 8.4,
                        "relativeStrength": 13.7
                },
                "setupType": "Retest nền",
                "marketState": "Uptrend",
                "action": "THEO DÕI MUA",
                "risk": "Cao",
                "close": 70400,
                "rsi14": 57.3,
                "ret20": -8.0,
                "ret60": 3.6,
                "volume_status": "Mẫu",
                "volumeRatio": 1.85,
                "ma20": 69270,
                "ma50": 68140,
                "ma200": 65880,
                "macd": null,
                "macd_signal": null,
                "distanceToMA20": -0.5,
                "atr14": null,
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
                        "topOpportunity": false,
                        "breakout": false,
                        "pullbackMA20": false,
                        "moneyFlow": false,
                        "accumulation": false,
                        "safe": false
                },
                "reason": "Dữ liệu mẫu cho DIG. Chạy GitHub Actions sau khi thêm VNSTOCK_API_KEY để cập nhật tín hiệu thật.",
                "expertSummary": "DIG đang ở trạng thái mẫu. Hệ thống sẽ cập nhật xu hướng, động lượng, dòng tiền, setup và rủi ro sau khi chạy Vnstock API.",
                "buyZone": "Canh quanh MA20 hoặc nền tích lũy gần nhất, không mua đuổi.",
                "stopLoss": "-7% đến -10%",
                "takeProfit": "+12% đến +25%",
                "allocation": "5% - 20%",
                "catalysts": [
                        "Vnstock API",
                        "Bất động sản / KCN"
                ],
                "cautions": [
                        "Đây là dữ liệu mẫu trước khi chạy API",
                        "Không dùng để giao dịch thật",
                        "Chạy workflow để cập nhật"
                ]
        },
        {
                "ticker": "CEO",
                "name": "CEO Group",
                "sector": "Bất động sản / KCN",
                "score": 65.1,
                "subscores": {
                        "trend": 18,
                        "momentum": 12.6,
                        "moneyFlow": 9.5,
                        "setup": 11.8,
                        "risk": 7.2,
                        "relativeStrength": 6.0
                },
                "setupType": "Vượt lại MA50",
                "marketState": "Uptrend",
                "action": "THEO DÕI MUA",
                "risk": "Cao",
                "close": 71200,
                "rsi14": 59.0,
                "ret20": -7.1,
                "ret60": 4.8,
                "volume_status": "Mẫu",
                "volumeRatio": 0.8,
                "ma20": 70060,
                "ma50": 68920,
                "ma200": 66640,
                "macd": null,
                "macd_signal": null,
                "distanceToMA20": 0.5,
                "atr14": null,
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
                        "topOpportunity": false,
                        "breakout": false,
                        "pullbackMA20": false,
                        "moneyFlow": false,
                        "accumulation": false,
                        "safe": false
                },
                "reason": "Dữ liệu mẫu cho CEO. Chạy GitHub Actions sau khi thêm VNSTOCK_API_KEY để cập nhật tín hiệu thật.",
                "expertSummary": "CEO đang ở trạng thái mẫu. Hệ thống sẽ cập nhật xu hướng, động lượng, dòng tiền, setup và rủi ro sau khi chạy Vnstock API.",
                "buyZone": "Canh quanh MA20 hoặc nền tích lũy gần nhất, không mua đuổi.",
                "stopLoss": "-7% đến -10%",
                "takeProfit": "+12% đến +25%",
                "allocation": "5% - 20%",
                "catalysts": [
                        "Vnstock API",
                        "Bất động sản / KCN"
                ],
                "cautions": [
                        "Đây là dữ liệu mẫu trước khi chạy API",
                        "Không dùng để giao dịch thật",
                        "Chạy workflow để cập nhật"
                ]
        },
        {
                "ticker": "NVL",
                "name": "Novaland",
                "sector": "Bất động sản / KCN",
                "score": 70.6,
                "subscores": {
                        "trend": 20,
                        "momentum": 7.0,
                        "moneyFlow": 11.0,
                        "setup": 13.5,
                        "risk": 12.0,
                        "relativeStrength": 7.1
                },
                "setupType": "Chưa có setup rõ",
                "marketState": "Uptrend",
                "action": "THEO DÕI MUA",
                "risk": "Cao",
                "close": 72000,
                "rsi14": 60.7,
                "ret20": -6.2,
                "ret60": 6.0,
                "volume_status": "Mẫu",
                "volumeRatio": 0.95,
                "ma20": 70850,
                "ma50": 69700,
                "ma200": 67400,
                "macd": null,
                "macd_signal": null,
                "distanceToMA20": 1.5,
                "atr14": null,
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
                        "topOpportunity": false,
                        "breakout": false,
                        "pullbackMA20": false,
                        "moneyFlow": false,
                        "accumulation": false,
                        "safe": true
                },
                "reason": "Dữ liệu mẫu cho NVL. Chạy GitHub Actions sau khi thêm VNSTOCK_API_KEY để cập nhật tín hiệu thật.",
                "expertSummary": "NVL đang ở trạng thái mẫu. Hệ thống sẽ cập nhật xu hướng, động lượng, dòng tiền, setup và rủi ro sau khi chạy Vnstock API.",
                "buyZone": "Canh quanh MA20 hoặc nền tích lũy gần nhất, không mua đuổi.",
                "stopLoss": "-7% đến -10%",
                "takeProfit": "+12% đến +25%",
                "allocation": "5% - 20%",
                "catalysts": [
                        "Vnstock API",
                        "Bất động sản / KCN"
                ],
                "cautions": [
                        "Đây là dữ liệu mẫu trước khi chạy API",
                        "Không dùng để giao dịch thật",
                        "Chạy workflow để cập nhật"
                ]
        },
        {
                "ticker": "TCH",
                "name": "Hoàng Huy",
                "sector": "Bất động sản / KCN",
                "score": 54.9,
                "subscores": {
                        "trend": 10,
                        "momentum": 8.4,
                        "moneyFlow": 12.5,
                        "setup": 5.0,
                        "risk": 10.8,
                        "relativeStrength": 8.2
                },
                "setupType": "Pullback MA20",
                "marketState": "Trung tính",
                "action": "TRÁNH MUA MỚI",
                "risk": "Cao",
                "close": 72800,
                "rsi14": 62.4,
                "ret20": -5.3,
                "ret60": 7.2,
                "volume_status": "Mẫu",
                "volumeRatio": 1.1,
                "ma20": 71640,
                "ma50": 70480,
                "ma200": 68160,
                "macd": null,
                "macd_signal": null,
                "distanceToMA20": 2.5,
                "atr14": null,
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
                        "topOpportunity": false,
                        "breakout": false,
                        "pullbackMA20": true,
                        "moneyFlow": false,
                        "accumulation": false,
                        "safe": false
                },
                "reason": "Dữ liệu mẫu cho TCH. Chạy GitHub Actions sau khi thêm VNSTOCK_API_KEY để cập nhật tín hiệu thật.",
                "expertSummary": "TCH đang ở trạng thái mẫu. Hệ thống sẽ cập nhật xu hướng, động lượng, dòng tiền, setup và rủi ro sau khi chạy Vnstock API.",
                "buyZone": "Canh quanh MA20 hoặc nền tích lũy gần nhất, không mua đuổi.",
                "stopLoss": "-7% đến -10%",
                "takeProfit": "+12% đến +25%",
                "allocation": "5% - 20%",
                "catalysts": [
                        "Vnstock API",
                        "Bất động sản / KCN"
                ],
                "cautions": [
                        "Đây là dữ liệu mẫu trước khi chạy API",
                        "Không dùng để giao dịch thật",
                        "Chạy workflow để cập nhật"
                ]
        },
        {
                "ticker": "SCR",
                "name": "Sacomreal",
                "sector": "Bất động sản / KCN",
                "score": 61.4,
                "subscores": {
                        "trend": 12,
                        "momentum": 9.8,
                        "moneyFlow": 14.0,
                        "setup": 6.7,
                        "risk": 9.6,
                        "relativeStrength": 9.3
                },
                "setupType": "Breakout 20 phiên",
                "marketState": "Tích cực",
                "action": "CHỜ THÊM",
                "risk": "Cao",
                "close": 73600,
                "rsi14": 64.1,
                "ret20": -4.4,
                "ret60": 8.4,
                "volume_status": "Mẫu",
                "volumeRatio": 1.25,
                "ma20": 72430,
                "ma50": 71260,
                "ma200": 68920,
                "macd": null,
                "macd_signal": null,
                "distanceToMA20": 3.5,
                "atr14": null,
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
                        "topOpportunity": false,
                        "breakout": true,
                        "pullbackMA20": false,
                        "moneyFlow": false,
                        "accumulation": false,
                        "safe": false
                },
                "reason": "Dữ liệu mẫu cho SCR. Chạy GitHub Actions sau khi thêm VNSTOCK_API_KEY để cập nhật tín hiệu thật.",
                "expertSummary": "SCR đang ở trạng thái mẫu. Hệ thống sẽ cập nhật xu hướng, động lượng, dòng tiền, setup và rủi ro sau khi chạy Vnstock API.",
                "buyZone": "Canh quanh MA20 hoặc nền tích lũy gần nhất, không mua đuổi.",
                "stopLoss": "-7% đến -10%",
                "takeProfit": "+12% đến +25%",
                "allocation": "5% - 20%",
                "catalysts": [
                        "Vnstock API",
                        "Bất động sản / KCN"
                ],
                "cautions": [
                        "Đây là dữ liệu mẫu trước khi chạy API",
                        "Không dùng để giao dịch thật",
                        "Chạy workflow để cập nhật"
                ]
        },
        {
                "ticker": "HDC",
                "name": "Hodeco",
                "sector": "Bất động sản / KCN",
                "score": 67.9,
                "subscores": {
                        "trend": 14,
                        "momentum": 11.2,
                        "moneyFlow": 15.5,
                        "setup": 8.4,
                        "risk": 8.4,
                        "relativeStrength": 10.4
                },
                "setupType": "Tích lũy biên hẹp",
                "marketState": "Tích cực",
                "action": "THEO DÕI MUA",
                "risk": "Cao",
                "close": 74400,
                "rsi14": 65.8,
                "ret20": -3.5,
                "ret60": 9.6,
                "volume_status": "Mẫu",
                "volumeRatio": 1.4,
                "ma20": 73220,
                "ma50": 72040,
                "ma200": 69680,
                "macd": null,
                "macd_signal": null,
                "distanceToMA20": 4.5,
                "atr14": null,
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
                        "topOpportunity": false,
                        "breakout": false,
                        "pullbackMA20": false,
                        "moneyFlow": true,
                        "accumulation": true,
                        "safe": false
                },
                "reason": "Dữ liệu mẫu cho HDC. Chạy GitHub Actions sau khi thêm VNSTOCK_API_KEY để cập nhật tín hiệu thật.",
                "expertSummary": "HDC đang ở trạng thái mẫu. Hệ thống sẽ cập nhật xu hướng, động lượng, dòng tiền, setup và rủi ro sau khi chạy Vnstock API.",
                "buyZone": "Canh quanh MA20 hoặc nền tích lũy gần nhất, không mua đuổi.",
                "stopLoss": "-7% đến -10%",
                "takeProfit": "+12% đến +25%",
                "allocation": "5% - 20%",
                "catalysts": [
                        "Vnstock API",
                        "Bất động sản / KCN"
                ],
                "cautions": [
                        "Đây là dữ liệu mẫu trước khi chạy API",
                        "Không dùng để giao dịch thật",
                        "Chạy workflow để cập nhật"
                ]
        },
        {
                "ticker": "HDG",
                "name": "Hà Đô",
                "sector": "Bất động sản / KCN",
                "score": 74.4,
                "subscores": {
                        "trend": 16,
                        "momentum": 12.6,
                        "moneyFlow": 17.0,
                        "setup": 10.1,
                        "risk": 7.2,
                        "relativeStrength": 11.5
                },
                "setupType": "Retest nền",
                "marketState": "Uptrend",
                "action": "CANH MUA / MUA KHI XÁC NHẬN",
                "risk": "Cao",
                "close": 75200,
                "rsi14": 67.5,
                "ret20": -2.6,
                "ret60": 10.8,
                "volume_status": "Mẫu",
                "volumeRatio": 1.55,
                "ma20": 74010,
                "ma50": 72820,
                "ma200": 70440,
                "macd": null,
                "macd_signal": null,
                "distanceToMA20": 5.5,
                "atr14": null,
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
                        "topOpportunity": false,
                        "breakout": false,
                        "pullbackMA20": false,
                        "moneyFlow": true,
                        "accumulation": false,
                        "safe": false
                },
                "reason": "Dữ liệu mẫu cho HDG. Chạy GitHub Actions sau khi thêm VNSTOCK_API_KEY để cập nhật tín hiệu thật.",
                "expertSummary": "HDG đang ở trạng thái mẫu. Hệ thống sẽ cập nhật xu hướng, động lượng, dòng tiền, setup và rủi ro sau khi chạy Vnstock API.",
                "buyZone": "Canh quanh MA20 hoặc nền tích lũy gần nhất, không mua đuổi.",
                "stopLoss": "-7% đến -10%",
                "takeProfit": "+12% đến +25%",
                "allocation": "5% - 20%",
                "catalysts": [
                        "Vnstock API",
                        "Bất động sản / KCN"
                ],
                "cautions": [
                        "Đây là dữ liệu mẫu trước khi chạy API",
                        "Không dùng để giao dịch thật",
                        "Chạy workflow để cập nhật"
                ]
        },
        {
                "ticker": "KBC",
                "name": "Kinh Bắc",
                "sector": "Bất động sản / KCN",
                "score": 69.4,
                "subscores": {
                        "trend": 18,
                        "momentum": 7.0,
                        "moneyFlow": 8.0,
                        "setup": 11.8,
                        "risk": 12.0,
                        "relativeStrength": 12.6
                },
                "setupType": "Vượt lại MA50",
                "marketState": "Uptrend",
                "action": "THEO DÕI MUA",
                "risk": "Cao",
                "close": 76000,
                "rsi14": 69.2,
                "ret20": -1.7,
                "ret60": 12.0,
                "volume_status": "Mẫu",
                "volumeRatio": 1.7,
                "ma20": 74800,
                "ma50": 73600,
                "ma200": 71200,
                "macd": null,
                "macd_signal": null,
                "distanceToMA20": 6.5,
                "atr14": null,
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
                        "topOpportunity": false,
                        "breakout": false,
                        "pullbackMA20": false,
                        "moneyFlow": false,
                        "accumulation": false,
                        "safe": true
                },
                "reason": "Dữ liệu mẫu cho KBC. Chạy GitHub Actions sau khi thêm VNSTOCK_API_KEY để cập nhật tín hiệu thật.",
                "expertSummary": "KBC đang ở trạng thái mẫu. Hệ thống sẽ cập nhật xu hướng, động lượng, dòng tiền, setup và rủi ro sau khi chạy Vnstock API.",
                "buyZone": "Canh quanh MA20 hoặc nền tích lũy gần nhất, không mua đuổi.",
                "stopLoss": "-7% đến -10%",
                "takeProfit": "+12% đến +25%",
                "allocation": "5% - 20%",
                "catalysts": [
                        "Vnstock API",
                        "Bất động sản / KCN"
                ],
                "cautions": [
                        "Đây là dữ liệu mẫu trước khi chạy API",
                        "Không dùng để giao dịch thật",
                        "Chạy workflow để cập nhật"
                ]
        },
        {
                "ticker": "SZC",
                "name": "Sonadezi Châu Đức",
                "sector": "Bất động sản / KCN",
                "score": 75.9,
                "subscores": {
                        "trend": 20,
                        "momentum": 8.4,
                        "moneyFlow": 9.5,
                        "setup": 13.5,
                        "risk": 10.8,
                        "relativeStrength": 13.7
                },
                "setupType": "Chưa có setup rõ",
                "marketState": "Uptrend",
                "action": "CANH MUA / MUA KHI XÁC NHẬN",
                "risk": "Cao",
                "close": 76800,
                "rsi14": 70.9,
                "ret20": -0.8,
                "ret60": 13.2,
                "volume_status": "Mẫu",
                "volumeRatio": 1.85,
                "ma20": 75590,
                "ma50": 74380,
                "ma200": 71960,
                "macd": null,
                "macd_signal": null,
                "distanceToMA20": 7.5,
                "atr14": null,
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
                        "topOpportunity": false,
                        "breakout": false,
                        "pullbackMA20": false,
                        "moneyFlow": false,
                        "accumulation": false,
                        "safe": false
                },
                "reason": "Dữ liệu mẫu cho SZC. Chạy GitHub Actions sau khi thêm VNSTOCK_API_KEY để cập nhật tín hiệu thật.",
                "expertSummary": "SZC đang ở trạng thái mẫu. Hệ thống sẽ cập nhật xu hướng, động lượng, dòng tiền, setup và rủi ro sau khi chạy Vnstock API.",
                "buyZone": "Canh quanh MA20 hoặc nền tích lũy gần nhất, không mua đuổi.",
                "stopLoss": "-7% đến -10%",
                "takeProfit": "+12% đến +25%",
                "allocation": "5% - 20%",
                "catalysts": [
                        "Vnstock API",
                        "Bất động sản / KCN"
                ],
                "cautions": [
                        "Đây là dữ liệu mẫu trước khi chạy API",
                        "Không dùng để giao dịch thật",
                        "Chạy workflow để cập nhật"
                ]
        },
        {
                "ticker": "BCM",
                "name": "Becamex IDC",
                "sector": "Bất động sản / KCN",
                "score": 51.4,
                "subscores": {
                        "trend": 10,
                        "momentum": 9.8,
                        "moneyFlow": 11.0,
                        "setup": 5.0,
                        "risk": 9.6,
                        "relativeStrength": 6.0
                },
                "setupType": "Pullback MA20",
                "marketState": "Trung tính",
                "action": "TRÁNH MUA MỚI",
                "risk": "Cao",
                "close": 77600,
                "rsi14": 42.0,
                "ret20": 0.1,
                "ret60": 14.4,
                "volume_status": "Mẫu",
                "volumeRatio": 0.8,
                "ma20": 76380,
                "ma50": 75160,
                "ma200": 72720,
                "macd": null,
                "macd_signal": null,
                "distanceToMA20": -3.5,
                "atr14": null,
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
                        "topOpportunity": false,
                        "breakout": false,
                        "pullbackMA20": true,
                        "moneyFlow": false,
                        "accumulation": false,
                        "safe": false
                },
                "reason": "Dữ liệu mẫu cho BCM. Chạy GitHub Actions sau khi thêm VNSTOCK_API_KEY để cập nhật tín hiệu thật.",
                "expertSummary": "BCM đang ở trạng thái mẫu. Hệ thống sẽ cập nhật xu hướng, động lượng, dòng tiền, setup và rủi ro sau khi chạy Vnstock API.",
                "buyZone": "Canh quanh MA20 hoặc nền tích lũy gần nhất, không mua đuổi.",
                "stopLoss": "-7% đến -10%",
                "takeProfit": "+12% đến +25%",
                "allocation": "5% - 20%",
                "catalysts": [
                        "Vnstock API",
                        "Bất động sản / KCN"
                ],
                "cautions": [
                        "Đây là dữ liệu mẫu trước khi chạy API",
                        "Không dùng để giao dịch thật",
                        "Chạy workflow để cập nhật"
                ]
        },
        {
                "ticker": "IDC",
                "name": "IDICO",
                "sector": "Bất động sản / KCN",
                "score": 57.9,
                "subscores": {
                        "trend": 12,
                        "momentum": 11.2,
                        "moneyFlow": 12.5,
                        "setup": 6.7,
                        "risk": 8.4,
                        "relativeStrength": 7.1
                },
                "setupType": "Breakout 20 phiên",
                "marketState": "Tích cực",
                "action": "CHỜ THÊM",
                "risk": "Cao",
                "close": 78400,
                "rsi14": 43.7,
                "ret20": 1.0,
                "ret60": 15.6,
                "volume_status": "Mẫu",
                "volumeRatio": 0.95,
                "ma20": 77170,
                "ma50": 75940,
                "ma200": 73480,
                "macd": null,
                "macd_signal": null,
                "distanceToMA20": -2.5,
                "atr14": null,
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
                        "topOpportunity": false,
                        "breakout": true,
                        "pullbackMA20": false,
                        "moneyFlow": false,
                        "accumulation": false,
                        "safe": false
                },
                "reason": "Dữ liệu mẫu cho IDC. Chạy GitHub Actions sau khi thêm VNSTOCK_API_KEY để cập nhật tín hiệu thật.",
                "expertSummary": "IDC đang ở trạng thái mẫu. Hệ thống sẽ cập nhật xu hướng, động lượng, dòng tiền, setup và rủi ro sau khi chạy Vnstock API.",
                "buyZone": "Canh quanh MA20 hoặc nền tích lũy gần nhất, không mua đuổi.",
                "stopLoss": "-7% đến -10%",
                "takeProfit": "+12% đến +25%",
                "allocation": "5% - 20%",
                "catalysts": [
                        "Vnstock API",
                        "Bất động sản / KCN"
                ],
                "cautions": [
                        "Đây là dữ liệu mẫu trước khi chạy API",
                        "Không dùng để giao dịch thật",
                        "Chạy workflow để cập nhật"
                ]
        },
        {
                "ticker": "VGC",
                "name": "Viglacera",
                "sector": "Bất động sản / KCN",
                "score": 64.4,
                "subscores": {
                        "trend": 14,
                        "momentum": 12.6,
                        "moneyFlow": 14.0,
                        "setup": 8.4,
                        "risk": 7.2,
                        "relativeStrength": 8.2
                },
                "setupType": "Tích lũy biên hẹp",
                "marketState": "Tích cực",
                "action": "CHỜ THÊM",
                "risk": "Cao",
                "close": 79200,
                "rsi14": 45.4,
                "ret20": 1.9,
                "ret60": 16.8,
                "volume_status": "Mẫu",
                "volumeRatio": 1.1,
                "ma20": 77960,
                "ma50": 76720,
                "ma200": 74240,
                "macd": null,
                "macd_signal": null,
                "distanceToMA20": -1.5,
                "atr14": null,
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
                        "topOpportunity": false,
                        "breakout": false,
                        "pullbackMA20": false,
                        "moneyFlow": false,
                        "accumulation": true,
                        "safe": false
                },
                "reason": "Dữ liệu mẫu cho VGC. Chạy GitHub Actions sau khi thêm VNSTOCK_API_KEY để cập nhật tín hiệu thật.",
                "expertSummary": "VGC đang ở trạng thái mẫu. Hệ thống sẽ cập nhật xu hướng, động lượng, dòng tiền, setup và rủi ro sau khi chạy Vnstock API.",
                "buyZone": "Canh quanh MA20 hoặc nền tích lũy gần nhất, không mua đuổi.",
                "stopLoss": "-7% đến -10%",
                "takeProfit": "+12% đến +25%",
                "allocation": "5% - 20%",
                "catalysts": [
                        "Vnstock API",
                        "Bất động sản / KCN"
                ],
                "cautions": [
                        "Đây là dữ liệu mẫu trước khi chạy API",
                        "Không dùng để giao dịch thật",
                        "Chạy workflow để cập nhật"
                ]
        },
        {
                "ticker": "IJC",
                "name": "Becamex IJC",
                "sector": "Bất động sản / KCN",
                "score": 69.9,
                "subscores": {
                        "trend": 16,
                        "momentum": 7.0,
                        "moneyFlow": 15.5,
                        "setup": 10.1,
                        "risk": 12.0,
                        "relativeStrength": 9.3
                },
                "setupType": "Retest nền",
                "marketState": "Uptrend",
                "action": "THEO DÕI MUA",
                "risk": "Cao",
                "close": 80000,
                "rsi14": 47.1,
                "ret20": 2.8,
                "ret60": -12.0,
                "volume_status": "Mẫu",
                "volumeRatio": 1.25,
                "ma20": 78750,
                "ma50": 77500,
                "ma200": 75000,
                "macd": null,
                "macd_signal": null,
                "distanceToMA20": -0.5,
                "atr14": null,
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
                        "topOpportunity": false,
                        "breakout": false,
                        "pullbackMA20": false,
                        "moneyFlow": true,
                        "accumulation": false,
                        "safe": true
                },
                "reason": "Dữ liệu mẫu cho IJC. Chạy GitHub Actions sau khi thêm VNSTOCK_API_KEY để cập nhật tín hiệu thật.",
                "expertSummary": "IJC đang ở trạng thái mẫu. Hệ thống sẽ cập nhật xu hướng, động lượng, dòng tiền, setup và rủi ro sau khi chạy Vnstock API.",
                "buyZone": "Canh quanh MA20 hoặc nền tích lũy gần nhất, không mua đuổi.",
                "stopLoss": "-7% đến -10%",
                "takeProfit": "+12% đến +25%",
                "allocation": "5% - 20%",
                "catalysts": [
                        "Vnstock API",
                        "Bất động sản / KCN"
                ],
                "cautions": [
                        "Đây là dữ liệu mẫu trước khi chạy API",
                        "Không dùng để giao dịch thật",
                        "Chạy workflow để cập nhật"
                ]
        },
        {
                "ticker": "CII",
                "name": "CII",
                "sector": "Bất động sản / KCN",
                "score": 76.4,
                "subscores": {
                        "trend": 18,
                        "momentum": 8.4,
                        "moneyFlow": 17.0,
                        "setup": 11.8,
                        "risk": 10.8,
                        "relativeStrength": 10.4
                },
                "setupType": "Vượt lại MA50",
                "marketState": "Uptrend",
                "action": "CANH MUA / MUA KHI XÁC NHẬN",
                "risk": "Cao",
                "close": 80800,
                "rsi14": 48.8,
                "ret20": 3.7,
                "ret60": -10.8,
                "volume_status": "Mẫu",
                "volumeRatio": 1.4,
                "ma20": 79540,
                "ma50": 78280,
                "ma200": 75760,
                "macd": null,
                "macd_signal": null,
                "distanceToMA20": 0.5,
                "atr14": null,
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
                        "topOpportunity": false,
                        "breakout": false,
                        "pullbackMA20": false,
                        "moneyFlow": true,
                        "accumulation": false,
                        "safe": false
                },
                "reason": "Dữ liệu mẫu cho CII. Chạy GitHub Actions sau khi thêm VNSTOCK_API_KEY để cập nhật tín hiệu thật.",
                "expertSummary": "CII đang ở trạng thái mẫu. Hệ thống sẽ cập nhật xu hướng, động lượng, dòng tiền, setup và rủi ro sau khi chạy Vnstock API.",
                "buyZone": "Canh quanh MA20 hoặc nền tích lũy gần nhất, không mua đuổi.",
                "stopLoss": "-7% đến -10%",
                "takeProfit": "+12% đến +25%",
                "allocation": "5% - 20%",
                "catalysts": [
                        "Vnstock API",
                        "Bất động sản / KCN"
                ],
                "cautions": [
                        "Đây là dữ liệu mẫu trước khi chạy API",
                        "Không dùng để giao dịch thật",
                        "Chạy workflow để cập nhật"
                ]
        },
        {
                "ticker": "NBB",
                "name": "577 Investment",
                "sector": "Bất động sản / KCN",
                "score": 72.4,
                "subscores": {
                        "trend": 20,
                        "momentum": 9.8,
                        "moneyFlow": 8.0,
                        "setup": 13.5,
                        "risk": 9.6,
                        "relativeStrength": 11.5
                },
                "setupType": "Chưa có setup rõ",
                "marketState": "Uptrend",
                "action": "THEO DÕI MUA",
                "risk": "Cao",
                "close": 81600,
                "rsi14": 50.5,
                "ret20": 4.6,
                "ret60": -9.6,
                "volume_status": "Mẫu",
                "volumeRatio": 1.55,
                "ma20": 80330,
                "ma50": 79060,
                "ma200": 76520,
                "macd": null,
                "macd_signal": null,
                "distanceToMA20": 1.5,
                "atr14": null,
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
                        "topOpportunity": false,
                        "breakout": false,
                        "pullbackMA20": false,
                        "moneyFlow": false,
                        "accumulation": false,
                        "safe": false
                },
                "reason": "Dữ liệu mẫu cho NBB. Chạy GitHub Actions sau khi thêm VNSTOCK_API_KEY để cập nhật tín hiệu thật.",
                "expertSummary": "NBB đang ở trạng thái mẫu. Hệ thống sẽ cập nhật xu hướng, động lượng, dòng tiền, setup và rủi ro sau khi chạy Vnstock API.",
                "buyZone": "Canh quanh MA20 hoặc nền tích lũy gần nhất, không mua đuổi.",
                "stopLoss": "-7% đến -10%",
                "takeProfit": "+12% đến +25%",
                "allocation": "5% - 20%",
                "catalysts": [
                        "Vnstock API",
                        "Bất động sản / KCN"
                ],
                "cautions": [
                        "Đây là dữ liệu mẫu trước khi chạy API",
                        "Không dùng để giao dịch thật",
                        "Chạy workflow để cập nhật"
                ]
        },
        {
                "ticker": "NTL",
                "name": "Lideco",
                "sector": "Bất động sản / KCN",
                "score": 56.7,
                "subscores": {
                        "trend": 10,
                        "momentum": 11.2,
                        "moneyFlow": 9.5,
                        "setup": 5.0,
                        "risk": 8.4,
                        "relativeStrength": 12.6
                },
                "setupType": "Pullback MA20",
                "marketState": "Trung tính",
                "action": "CHỜ THÊM",
                "risk": "Cao",
                "close": 82400,
                "rsi14": 52.2,
                "ret20": 5.5,
                "ret60": -8.4,
                "volume_status": "Mẫu",
                "volumeRatio": 1.7,
                "ma20": 81120,
                "ma50": 79840,
                "ma200": 77280,
                "macd": null,
                "macd_signal": null,
                "distanceToMA20": 2.5,
                "atr14": null,
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
                        "topOpportunity": false,
                        "breakout": false,
                        "pullbackMA20": true,
                        "moneyFlow": false,
                        "accumulation": false,
                        "safe": false
                },
                "reason": "Dữ liệu mẫu cho NTL. Chạy GitHub Actions sau khi thêm VNSTOCK_API_KEY để cập nhật tín hiệu thật.",
                "expertSummary": "NTL đang ở trạng thái mẫu. Hệ thống sẽ cập nhật xu hướng, động lượng, dòng tiền, setup và rủi ro sau khi chạy Vnstock API.",
                "buyZone": "Canh quanh MA20 hoặc nền tích lũy gần nhất, không mua đuổi.",
                "stopLoss": "-7% đến -10%",
                "takeProfit": "+12% đến +25%",
                "allocation": "5% - 20%",
                "catalysts": [
                        "Vnstock API",
                        "Bất động sản / KCN"
                ],
                "cautions": [
                        "Đây là dữ liệu mẫu trước khi chạy API",
                        "Không dùng để giao dịch thật",
                        "Chạy workflow để cập nhật"
                ]
        },
        {
                "ticker": "SIP",
                "name": "SIP Corp",
                "sector": "Bất động sản / KCN",
                "score": 63.2,
                "subscores": {
                        "trend": 12,
                        "momentum": 12.6,
                        "moneyFlow": 11.0,
                        "setup": 6.7,
                        "risk": 7.2,
                        "relativeStrength": 13.7
                },
                "setupType": "Breakout 20 phiên",
                "marketState": "Tích cực",
                "action": "CHỜ THÊM",
                "risk": "Cao",
                "close": 83200,
                "rsi14": 53.9,
                "ret20": 6.4,
                "ret60": -7.2,
                "volume_status": "Mẫu",
                "volumeRatio": 1.85,
                "ma20": 81910,
                "ma50": 80620,
                "ma200": 78040,
                "macd": null,
                "macd_signal": null,
                "distanceToMA20": 3.5,
                "atr14": null,
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
                        "topOpportunity": false,
                        "breakout": true,
                        "pullbackMA20": false,
                        "moneyFlow": false,
                        "accumulation": false,
                        "safe": false
                },
                "reason": "Dữ liệu mẫu cho SIP. Chạy GitHub Actions sau khi thêm VNSTOCK_API_KEY để cập nhật tín hiệu thật.",
                "expertSummary": "SIP đang ở trạng thái mẫu. Hệ thống sẽ cập nhật xu hướng, động lượng, dòng tiền, setup và rủi ro sau khi chạy Vnstock API.",
                "buyZone": "Canh quanh MA20 hoặc nền tích lũy gần nhất, không mua đuổi.",
                "stopLoss": "-7% đến -10%",
                "takeProfit": "+12% đến +25%",
                "allocation": "5% - 20%",
                "catalysts": [
                        "Vnstock API",
                        "Bất động sản / KCN"
                ],
                "cautions": [
                        "Đây là dữ liệu mẫu trước khi chạy API",
                        "Không dùng để giao dịch thật",
                        "Chạy workflow để cập nhật"
                ]
        },
        {
                "ticker": "TIP",
                "name": "Tin Nghĩa IP",
                "sector": "Bất động sản / KCN",
                "score": 59.9,
                "subscores": {
                        "trend": 14,
                        "momentum": 7.0,
                        "moneyFlow": 12.5,
                        "setup": 8.4,
                        "risk": 12.0,
                        "relativeStrength": 6.0
                },
                "setupType": "Tích lũy biên hẹp",
                "marketState": "Tích cực",
                "action": "CHỜ THÊM",
                "risk": "Cao",
                "close": 84000,
                "rsi14": 55.6,
                "ret20": 7.3,
                "ret60": -6.0,
                "volume_status": "Mẫu",
                "volumeRatio": 0.8,
                "ma20": 82700,
                "ma50": 81400,
                "ma200": 78800,
                "macd": null,
                "macd_signal": null,
                "distanceToMA20": 4.5,
                "atr14": null,
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
                        "topOpportunity": false,
                        "breakout": false,
                        "pullbackMA20": false,
                        "moneyFlow": false,
                        "accumulation": true,
                        "safe": false
                },
                "reason": "Dữ liệu mẫu cho TIP. Chạy GitHub Actions sau khi thêm VNSTOCK_API_KEY để cập nhật tín hiệu thật.",
                "expertSummary": "TIP đang ở trạng thái mẫu. Hệ thống sẽ cập nhật xu hướng, động lượng, dòng tiền, setup và rủi ro sau khi chạy Vnstock API.",
                "buyZone": "Canh quanh MA20 hoặc nền tích lũy gần nhất, không mua đuổi.",
                "stopLoss": "-7% đến -10%",
                "takeProfit": "+12% đến +25%",
                "allocation": "5% - 20%",
                "catalysts": [
                        "Vnstock API",
                        "Bất động sản / KCN"
                ],
                "cautions": [
                        "Đây là dữ liệu mẫu trước khi chạy API",
                        "Không dùng để giao dịch thật",
                        "Chạy workflow để cập nhật"
                ]
        },
        {
                "ticker": "LHG",
                "name": "Long Hậu",
                "sector": "Bất động sản / KCN",
                "score": 66.4,
                "subscores": {
                        "trend": 16,
                        "momentum": 8.4,
                        "moneyFlow": 14.0,
                        "setup": 10.1,
                        "risk": 10.8,
                        "relativeStrength": 7.1
                },
                "setupType": "Retest nền",
                "marketState": "Uptrend",
                "action": "THEO DÕI MUA",
                "risk": "Cao",
                "close": 84800,
                "rsi14": 57.3,
                "ret20": 8.2,
                "ret60": -4.8,
                "volume_status": "Mẫu",
                "volumeRatio": 0.95,
                "ma20": 83490,
                "ma50": 82180,
                "ma200": 79560,
                "macd": null,
                "macd_signal": null,
                "distanceToMA20": 5.5,
                "atr14": null,
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
                        "topOpportunity": false,
                        "breakout": false,
                        "pullbackMA20": false,
                        "moneyFlow": false,
                        "accumulation": false,
                        "safe": false
                },
                "reason": "Dữ liệu mẫu cho LHG. Chạy GitHub Actions sau khi thêm VNSTOCK_API_KEY để cập nhật tín hiệu thật.",
                "expertSummary": "LHG đang ở trạng thái mẫu. Hệ thống sẽ cập nhật xu hướng, động lượng, dòng tiền, setup và rủi ro sau khi chạy Vnstock API.",
                "buyZone": "Canh quanh MA20 hoặc nền tích lũy gần nhất, không mua đuổi.",
                "stopLoss": "-7% đến -10%",
                "takeProfit": "+12% đến +25%",
                "allocation": "5% - 20%",
                "catalysts": [
                        "Vnstock API",
                        "Bất động sản / KCN"
                ],
                "cautions": [
                        "Đây là dữ liệu mẫu trước khi chạy API",
                        "Không dùng để giao dịch thật",
                        "Chạy workflow để cập nhật"
                ]
        },
        {
                "ticker": "GAS",
                "name": "PV GAS",
                "sector": "Dầu khí / Năng lượng",
                "score": 72.9,
                "subscores": {
                        "trend": 18,
                        "momentum": 9.8,
                        "moneyFlow": 15.5,
                        "setup": 11.8,
                        "risk": 9.6,
                        "relativeStrength": 8.2
                },
                "setupType": "Vượt lại MA50",
                "marketState": "Uptrend",
                "action": "THEO DÕI MUA",
                "risk": "Cao",
                "close": 85600,
                "rsi14": 59.0,
                "ret20": 9.1,
                "ret60": -3.6,
                "volume_status": "Mẫu",
                "volumeRatio": 1.1,
                "ma20": 84280,
                "ma50": 82960,
                "ma200": 80320,
                "macd": null,
                "macd_signal": null,
                "distanceToMA20": 6.5,
                "atr14": null,
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
                        "topOpportunity": false,
                        "breakout": false,
                        "pullbackMA20": false,
                        "moneyFlow": true,
                        "accumulation": false,
                        "safe": false
                },
                "reason": "Dữ liệu mẫu cho GAS. Chạy GitHub Actions sau khi thêm VNSTOCK_API_KEY để cập nhật tín hiệu thật.",
                "expertSummary": "GAS đang ở trạng thái mẫu. Hệ thống sẽ cập nhật xu hướng, động lượng, dòng tiền, setup và rủi ro sau khi chạy Vnstock API.",
                "buyZone": "Canh quanh MA20 hoặc nền tích lũy gần nhất, không mua đuổi.",
                "stopLoss": "-7% đến -10%",
                "takeProfit": "+12% đến +25%",
                "allocation": "5% - 20%",
                "catalysts": [
                        "Vnstock API",
                        "Dầu khí / Năng lượng"
                ],
                "cautions": [
                        "Đây là dữ liệu mẫu trước khi chạy API",
                        "Không dùng để giao dịch thật",
                        "Chạy workflow để cập nhật"
                ]
        },
        {
                "ticker": "PVD",
                "name": "PV Drilling",
                "sector": "Dầu khí / Năng lượng",
                "score": 79.4,
                "subscores": {
                        "trend": 20,
                        "momentum": 11.2,
                        "moneyFlow": 17.0,
                        "setup": 13.5,
                        "risk": 8.4,
                        "relativeStrength": 9.3
                },
                "setupType": "Chưa có setup rõ",
                "marketState": "Uptrend",
                "action": "CANH MUA / MUA KHI XÁC NHẬN",
                "risk": "Cao",
                "close": 86400,
                "rsi14": 60.7,
                "ret20": 10.0,
                "ret60": -2.4,
                "volume_status": "Mẫu",
                "volumeRatio": 1.25,
                "ma20": 85070,
                "ma50": 83740,
                "ma200": 81080,
                "macd": null,
                "macd_signal": null,
                "distanceToMA20": 7.5,
                "atr14": null,
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
                        "topOpportunity": false,
                        "breakout": false,
                        "pullbackMA20": false,
                        "moneyFlow": true,
                        "accumulation": false,
                        "safe": false
                },
                "reason": "Dữ liệu mẫu cho PVD. Chạy GitHub Actions sau khi thêm VNSTOCK_API_KEY để cập nhật tín hiệu thật.",
                "expertSummary": "PVD đang ở trạng thái mẫu. Hệ thống sẽ cập nhật xu hướng, động lượng, dòng tiền, setup và rủi ro sau khi chạy Vnstock API.",
                "buyZone": "Canh quanh MA20 hoặc nền tích lũy gần nhất, không mua đuổi.",
                "stopLoss": "-7% đến -10%",
                "takeProfit": "+12% đến +25%",
                "allocation": "5% - 20%",
                "catalysts": [
                        "Vnstock API",
                        "Dầu khí / Năng lượng"
                ],
                "cautions": [
                        "Đây là dữ liệu mẫu trước khi chạy API",
                        "Không dùng để giao dịch thật",
                        "Chạy workflow để cập nhật"
                ]
        },
        {
                "ticker": "PVS",
                "name": "PTSC",
                "sector": "Dầu khí / Năng lượng",
                "score": 53.2,
                "subscores": {
                        "trend": 10,
                        "momentum": 12.6,
                        "moneyFlow": 8.0,
                        "setup": 5.0,
                        "risk": 7.2,
                        "relativeStrength": 10.4
                },
                "setupType": "Pullback MA20",
                "marketState": "Trung tính",
                "action": "TRÁNH MUA MỚI",
                "risk": "Cao",
                "close": 87200,
                "rsi14": 62.4,
                "ret20": -8.0,
                "ret60": -1.2,
                "volume_status": "Mẫu",
                "volumeRatio": 1.4,
                "ma20": 85860,
                "ma50": 84520,
                "ma200": 81840,
                "macd": null,
                "macd_signal": null,
                "distanceToMA20": -3.5,
                "atr14": null,
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
                        "topOpportunity": false,
                        "breakout": false,
                        "pullbackMA20": true,
                        "moneyFlow": false,
                        "accumulation": false,
                        "safe": false
                },
                "reason": "Dữ liệu mẫu cho PVS. Chạy GitHub Actions sau khi thêm VNSTOCK_API_KEY để cập nhật tín hiệu thật.",
                "expertSummary": "PVS đang ở trạng thái mẫu. Hệ thống sẽ cập nhật xu hướng, động lượng, dòng tiền, setup và rủi ro sau khi chạy Vnstock API.",
                "buyZone": "Canh quanh MA20 hoặc nền tích lũy gần nhất, không mua đuổi.",
                "stopLoss": "-7% đến -10%",
                "takeProfit": "+12% đến +25%",
                "allocation": "5% - 20%",
                "catalysts": [
                        "Vnstock API",
                        "Dầu khí / Năng lượng"
                ],
                "cautions": [
                        "Đây là dữ liệu mẫu trước khi chạy API",
                        "Không dùng để giao dịch thật",
                        "Chạy workflow để cập nhật"
                ]
        },
        {
                "ticker": "PLX",
                "name": "Petrolimex",
                "sector": "Dầu khí / Năng lượng",
                "score": 58.7,
                "subscores": {
                        "trend": 12,
                        "momentum": 7.0,
                        "moneyFlow": 9.5,
                        "setup": 6.7,
                        "risk": 12.0,
                        "relativeStrength": 11.5
                },
                "setupType": "Breakout 20 phiên",
                "marketState": "Tích cực",
                "action": "CHỜ THÊM",
                "risk": "Cao",
                "close": 88000,
                "rsi14": 64.1,
                "ret20": -7.1,
                "ret60": 0.0,
                "volume_status": "Mẫu",
                "volumeRatio": 1.55,
                "ma20": 86650,
                "ma50": 85300,
                "ma200": 82600,
                "macd": null,
                "macd_signal": null,
                "distanceToMA20": -2.5,
                "atr14": null,
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
                        "topOpportunity": false,
                        "breakout": true,
                        "pullbackMA20": false,
                        "moneyFlow": false,
                        "accumulation": false,
                        "safe": false
                },
                "reason": "Dữ liệu mẫu cho PLX. Chạy GitHub Actions sau khi thêm VNSTOCK_API_KEY để cập nhật tín hiệu thật.",
                "expertSummary": "PLX đang ở trạng thái mẫu. Hệ thống sẽ cập nhật xu hướng, động lượng, dòng tiền, setup và rủi ro sau khi chạy Vnstock API.",
                "buyZone": "Canh quanh MA20 hoặc nền tích lũy gần nhất, không mua đuổi.",
                "stopLoss": "-7% đến -10%",
                "takeProfit": "+12% đến +25%",
                "allocation": "5% - 20%",
                "catalysts": [
                        "Vnstock API",
                        "Dầu khí / Năng lượng"
                ],
                "cautions": [
                        "Đây là dữ liệu mẫu trước khi chạy API",
                        "Không dùng để giao dịch thật",
                        "Chạy workflow để cập nhật"
                ]
        },
        {
                "ticker": "BSR",
                "name": "Lọc hóa dầu Bình Sơn",
                "sector": "Dầu khí / Năng lượng",
                "score": 65.2,
                "subscores": {
                        "trend": 14,
                        "momentum": 8.4,
                        "moneyFlow": 11.0,
                        "setup": 8.4,
                        "risk": 10.8,
                        "relativeStrength": 12.6
                },
                "setupType": "Tích lũy biên hẹp",
                "marketState": "Tích cực",
                "action": "THEO DÕI MUA",
                "risk": "Cao",
                "close": 88800,
                "rsi14": 65.8,
                "ret20": -6.2,
                "ret60": 1.2,
                "volume_status": "Mẫu",
                "volumeRatio": 1.7,
                "ma20": 87440,
                "ma50": 86080,
                "ma200": 83360,
                "macd": null,
                "macd_signal": null,
                "distanceToMA20": -1.5,
                "atr14": null,
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
                        "topOpportunity": false,
                        "breakout": false,
                        "pullbackMA20": false,
                        "moneyFlow": false,
                        "accumulation": true,
                        "safe": false
                },
                "reason": "Dữ liệu mẫu cho BSR. Chạy GitHub Actions sau khi thêm VNSTOCK_API_KEY để cập nhật tín hiệu thật.",
                "expertSummary": "BSR đang ở trạng thái mẫu. Hệ thống sẽ cập nhật xu hướng, động lượng, dòng tiền, setup và rủi ro sau khi chạy Vnstock API.",
                "buyZone": "Canh quanh MA20 hoặc nền tích lũy gần nhất, không mua đuổi.",
                "stopLoss": "-7% đến -10%",
                "takeProfit": "+12% đến +25%",
                "allocation": "5% - 20%",
                "catalysts": [
                        "Vnstock API",
                        "Dầu khí / Năng lượng"
                ],
                "cautions": [
                        "Đây là dữ liệu mẫu trước khi chạy API",
                        "Không dùng để giao dịch thật",
                        "Chạy workflow để cập nhật"
                ]
        },
        {
                "ticker": "OIL",
                "name": "PV Oil",
                "sector": "Dầu khí / Năng lượng",
                "score": 71.7,
                "subscores": {
                        "trend": 16,
                        "momentum": 9.8,
                        "moneyFlow": 12.5,
                        "setup": 10.1,
                        "risk": 9.6,
                        "relativeStrength": 13.7
                },
                "setupType": "Retest nền",
                "marketState": "Uptrend",
                "action": "THEO DÕI MUA",
                "risk": "Cao",
                "close": 89600,
                "rsi14": 67.5,
                "ret20": -5.3,
                "ret60": 2.4,
                "volume_status": "Mẫu",
                "volumeRatio": 1.85,
                "ma20": 88230,
                "ma50": 86860,
                "ma200": 84120,
                "macd": null,
                "macd_signal": null,
                "distanceToMA20": -0.5,
                "atr14": null,
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
                        "topOpportunity": false,
                        "breakout": false,
                        "pullbackMA20": false,
                        "moneyFlow": false,
                        "accumulation": false,
                        "safe": false
                },
                "reason": "Dữ liệu mẫu cho OIL. Chạy GitHub Actions sau khi thêm VNSTOCK_API_KEY để cập nhật tín hiệu thật.",
                "expertSummary": "OIL đang ở trạng thái mẫu. Hệ thống sẽ cập nhật xu hướng, động lượng, dòng tiền, setup và rủi ro sau khi chạy Vnstock API.",
                "buyZone": "Canh quanh MA20 hoặc nền tích lũy gần nhất, không mua đuổi.",
                "stopLoss": "-7% đến -10%",
                "takeProfit": "+12% đến +25%",
                "allocation": "5% - 20%",
                "catalysts": [
                        "Vnstock API",
                        "Dầu khí / Năng lượng"
                ],
                "cautions": [
                        "Đây là dữ liệu mẫu trước khi chạy API",
                        "Không dùng để giao dịch thật",
                        "Chạy workflow để cập nhật"
                ]
        },
        {
                "ticker": "PVC",
                "name": "PVChem",
                "sector": "Dầu khí / Năng lượng",
                "score": 69.4,
                "subscores": {
                        "trend": 18,
                        "momentum": 11.2,
                        "moneyFlow": 14.0,
                        "setup": 11.8,
                        "risk": 8.4,
                        "relativeStrength": 6.0
                },
                "setupType": "Vượt lại MA50",
                "marketState": "Uptrend",
                "action": "THEO DÕI MUA",
                "risk": "Cao",
                "close": 90400,
                "rsi14": 69.2,
                "ret20": -4.4,
                "ret60": 3.6,
                "volume_status": "Mẫu",
                "volumeRatio": 0.8,
                "ma20": 89020,
                "ma50": 87640,
                "ma200": 84880,
                "macd": null,
                "macd_signal": null,
                "distanceToMA20": 0.5,
                "atr14": null,
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
                        "topOpportunity": false,
                        "breakout": false,
                        "pullbackMA20": false,
                        "moneyFlow": false,
                        "accumulation": false,
                        "safe": false
                },
                "reason": "Dữ liệu mẫu cho PVC. Chạy GitHub Actions sau khi thêm VNSTOCK_API_KEY để cập nhật tín hiệu thật.",
                "expertSummary": "PVC đang ở trạng thái mẫu. Hệ thống sẽ cập nhật xu hướng, động lượng, dòng tiền, setup và rủi ro sau khi chạy Vnstock API.",
                "buyZone": "Canh quanh MA20 hoặc nền tích lũy gần nhất, không mua đuổi.",
                "stopLoss": "-7% đến -10%",
                "takeProfit": "+12% đến +25%",
                "allocation": "5% - 20%",
                "catalysts": [
                        "Vnstock API",
                        "Dầu khí / Năng lượng"
                ],
                "cautions": [
                        "Đây là dữ liệu mẫu trước khi chạy API",
                        "Không dùng để giao dịch thật",
                        "Chạy workflow để cập nhật"
                ]
        },
        {
                "ticker": "PVB",
                "name": "PV Coating",
                "sector": "Dầu khí / Năng lượng",
                "score": 75.9,
                "subscores": {
                        "trend": 20,
                        "momentum": 12.6,
                        "moneyFlow": 15.5,
                        "setup": 13.5,
                        "risk": 7.2,
                        "relativeStrength": 7.1
                },
                "setupType": "Chưa có setup rõ",
                "marketState": "Uptrend",
                "action": "CANH MUA / MUA KHI XÁC NHẬN",
                "risk": "Cao",
                "close": 91200,
                "rsi14": 70.9,
                "ret20": -3.5,
                "ret60": 4.8,
                "volume_status": "Mẫu",
                "volumeRatio": 0.95,
                "ma20": 89810,
                "ma50": 88420,
                "ma200": 85640,
                "macd": null,
                "macd_signal": null,
                "distanceToMA20": 1.5,
                "atr14": null,
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
                        "topOpportunity": false,
                        "breakout": false,
                        "pullbackMA20": false,
                        "moneyFlow": true,
                        "accumulation": false,
                        "safe": false
                },
                "reason": "Dữ liệu mẫu cho PVB. Chạy GitHub Actions sau khi thêm VNSTOCK_API_KEY để cập nhật tín hiệu thật.",
                "expertSummary": "PVB đang ở trạng thái mẫu. Hệ thống sẽ cập nhật xu hướng, động lượng, dòng tiền, setup và rủi ro sau khi chạy Vnstock API.",
                "buyZone": "Canh quanh MA20 hoặc nền tích lũy gần nhất, không mua đuổi.",
                "stopLoss": "-7% đến -10%",
                "takeProfit": "+12% đến +25%",
                "allocation": "5% - 20%",
                "catalysts": [
                        "Vnstock API",
                        "Dầu khí / Năng lượng"
                ],
                "cautions": [
                        "Đây là dữ liệu mẫu trước khi chạy API",
                        "Không dùng để giao dịch thật",
                        "Chạy workflow để cập nhật"
                ]
        },
        {
                "ticker": "PVT",
                "name": "PVTrans",
                "sector": "Dầu khí / Năng lượng",
                "score": 59.2,
                "subscores": {
                        "trend": 10,
                        "momentum": 7.0,
                        "moneyFlow": 17.0,
                        "setup": 5.0,
                        "risk": 12.0,
                        "relativeStrength": 8.2
                },
                "setupType": "Pullback MA20",
                "marketState": "Trung tính",
                "action": "CHỜ THÊM",
                "risk": "Cao",
                "close": 92000,
                "rsi14": 42.0,
                "ret20": -2.6,
                "ret60": 6.0,
                "volume_status": "Mẫu",
                "volumeRatio": 1.1,
                "ma20": 90600,
                "ma50": 89200,
                "ma200": 86400,
                "macd": null,
                "macd_signal": null,
                "distanceToMA20": 2.5,
                "atr14": null,
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
                        "topOpportunity": false,
                        "breakout": false,
                        "pullbackMA20": true,
                        "moneyFlow": true,
                        "accumulation": false,
                        "safe": false
                },
                "reason": "Dữ liệu mẫu cho PVT. Chạy GitHub Actions sau khi thêm VNSTOCK_API_KEY để cập nhật tín hiệu thật.",
                "expertSummary": "PVT đang ở trạng thái mẫu. Hệ thống sẽ cập nhật xu hướng, động lượng, dòng tiền, setup và rủi ro sau khi chạy Vnstock API.",
                "buyZone": "Canh quanh MA20 hoặc nền tích lũy gần nhất, không mua đuổi.",
                "stopLoss": "-7% đến -10%",
                "takeProfit": "+12% đến +25%",
                "allocation": "5% - 20%",
                "catalysts": [
                        "Vnstock API",
                        "Dầu khí / Năng lượng"
                ],
                "cautions": [
                        "Đây là dữ liệu mẫu trước khi chạy API",
                        "Không dùng để giao dịch thật",
                        "Chạy workflow để cập nhật"
                ]
        },
        {
                "ticker": "PVP",
                "name": "PVTrans Pacific",
                "sector": "Dầu khí / Năng lượng",
                "score": 55.2,
                "subscores": {
                        "trend": 12,
                        "momentum": 8.4,
                        "moneyFlow": 8.0,
                        "setup": 6.7,
                        "risk": 10.8,
                        "relativeStrength": 9.3
                },
                "setupType": "Breakout 20 phiên",
                "marketState": "Tích cực",
                "action": "CHỜ THÊM",
                "risk": "Cao",
                "close": 92800,
                "rsi14": 43.7,
                "ret20": -1.7,
                "ret60": 7.2,
                "volume_status": "Mẫu",
                "volumeRatio": 1.25,
                "ma20": 91390,
                "ma50": 89980,
                "ma200": 87160,
                "macd": null,
                "macd_signal": null,
                "distanceToMA20": 3.5,
                "atr14": null,
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
                        "topOpportunity": false,
                        "breakout": true,
                        "pullbackMA20": false,
                        "moneyFlow": false,
                        "accumulation": false,
                        "safe": false
                },
                "reason": "Dữ liệu mẫu cho PVP. Chạy GitHub Actions sau khi thêm VNSTOCK_API_KEY để cập nhật tín hiệu thật.",
                "expertSummary": "PVP đang ở trạng thái mẫu. Hệ thống sẽ cập nhật xu hướng, động lượng, dòng tiền, setup và rủi ro sau khi chạy Vnstock API.",
                "buyZone": "Canh quanh MA20 hoặc nền tích lũy gần nhất, không mua đuổi.",
                "stopLoss": "-7% đến -10%",
                "takeProfit": "+12% đến +25%",
                "allocation": "5% - 20%",
                "catalysts": [
                        "Vnstock API",
                        "Dầu khí / Năng lượng"
                ],
                "cautions": [
                        "Đây là dữ liệu mẫu trước khi chạy API",
                        "Không dùng để giao dịch thật",
                        "Chạy workflow để cập nhật"
                ]
        },
        {
                "ticker": "DGC",
                "name": "Hóa chất Đức Giang",
                "sector": "Hóa chất / Vật liệu / Dệt may",
                "score": 61.7,
                "subscores": {
                        "trend": 14,
                        "momentum": 9.8,
                        "moneyFlow": 9.5,
                        "setup": 8.4,
                        "risk": 9.6,
                        "relativeStrength": 10.4
                },
                "setupType": "Tích lũy biên hẹp",
                "marketState": "Tích cực",
                "action": "CHỜ THÊM",
                "risk": "Trung bình",
                "close": 93600,
                "rsi14": 45.4,
                "ret20": -0.8,
                "ret60": 8.4,
                "volume_status": "Mẫu",
                "volumeRatio": 1.4,
                "ma20": 92180,
                "ma50": 90760,
                "ma200": 87920,
                "macd": null,
                "macd_signal": null,
                "distanceToMA20": 4.5,
                "atr14": null,
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
                        "topOpportunity": false,
                        "breakout": false,
                        "pullbackMA20": false,
                        "moneyFlow": false,
                        "accumulation": true,
                        "safe": false
                },
                "reason": "Dữ liệu mẫu cho DGC. Chạy GitHub Actions sau khi thêm VNSTOCK_API_KEY để cập nhật tín hiệu thật.",
                "expertSummary": "DGC đang ở trạng thái mẫu. Hệ thống sẽ cập nhật xu hướng, động lượng, dòng tiền, setup và rủi ro sau khi chạy Vnstock API.",
                "buyZone": "Canh quanh MA20 hoặc nền tích lũy gần nhất, không mua đuổi.",
                "stopLoss": "-7% đến -10%",
                "takeProfit": "+12% đến +25%",
                "allocation": "5% - 20%",
                "catalysts": [
                        "Vnstock API",
                        "Hóa chất / Vật liệu / Dệt may"
                ],
                "cautions": [
                        "Đây là dữ liệu mẫu trước khi chạy API",
                        "Không dùng để giao dịch thật",
                        "Chạy workflow để cập nhật"
                ]
        },
        {
                "ticker": "DCM",
                "name": "Đạm Cà Mau",
                "sector": "Hóa chất / Vật liệu / Dệt may",
                "score": 68.2,
                "subscores": {
                        "trend": 16,
                        "momentum": 11.2,
                        "moneyFlow": 11.0,
                        "setup": 10.1,
                        "risk": 8.4,
                        "relativeStrength": 11.5
                },
                "setupType": "Retest nền",
                "marketState": "Uptrend",
                "action": "THEO DÕI MUA",
                "risk": "Trung bình",
                "close": 94400,
                "rsi14": 47.1,
                "ret20": 0.1,
                "ret60": 9.6,
                "volume_status": "Mẫu",
                "volumeRatio": 1.55,
                "ma20": 92970,
                "ma50": 91540,
                "ma200": 88680,
                "macd": null,
                "macd_signal": null,
                "distanceToMA20": 5.5,
                "atr14": null,
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
                        "topOpportunity": false,
                        "breakout": false,
                        "pullbackMA20": false,
                        "moneyFlow": false,
                        "accumulation": false,
                        "safe": false
                },
                "reason": "Dữ liệu mẫu cho DCM. Chạy GitHub Actions sau khi thêm VNSTOCK_API_KEY để cập nhật tín hiệu thật.",
                "expertSummary": "DCM đang ở trạng thái mẫu. Hệ thống sẽ cập nhật xu hướng, động lượng, dòng tiền, setup và rủi ro sau khi chạy Vnstock API.",
                "buyZone": "Canh quanh MA20 hoặc nền tích lũy gần nhất, không mua đuổi.",
                "stopLoss": "-7% đến -10%",
                "takeProfit": "+12% đến +25%",
                "allocation": "5% - 20%",
                "catalysts": [
                        "Vnstock API",
                        "Hóa chất / Vật liệu / Dệt may"
                ],
                "cautions": [
                        "Đây là dữ liệu mẫu trước khi chạy API",
                        "Không dùng để giao dịch thật",
                        "Chạy workflow để cập nhật"
                ]
        },
        {
                "ticker": "DPM",
                "name": "Đạm Phú Mỹ",
                "sector": "Hóa chất / Vật liệu / Dệt may",
                "score": 74.7,
                "subscores": {
                        "trend": 18,
                        "momentum": 12.6,
                        "moneyFlow": 12.5,
                        "setup": 11.8,
                        "risk": 7.2,
                        "relativeStrength": 12.6
                },
                "setupType": "Vượt lại MA50",
                "marketState": "Uptrend",
                "action": "CANH MUA / MUA KHI XÁC NHẬN",
                "risk": "Trung bình",
                "close": 95200,
                "rsi14": 48.8,
                "ret20": 1.0,
                "ret60": 10.8,
                "volume_status": "Mẫu",
                "volumeRatio": 1.7,
                "ma20": 93760,
                "ma50": 92320,
                "ma200": 89440,
                "macd": null,
                "macd_signal": null,
                "distanceToMA20": 6.5,
                "atr14": null,
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
                        "topOpportunity": false,
                        "breakout": false,
                        "pullbackMA20": false,
                        "moneyFlow": false,
                        "accumulation": false,
                        "safe": false
                },
                "reason": "Dữ liệu mẫu cho DPM. Chạy GitHub Actions sau khi thêm VNSTOCK_API_KEY để cập nhật tín hiệu thật.",
                "expertSummary": "DPM đang ở trạng thái mẫu. Hệ thống sẽ cập nhật xu hướng, động lượng, dòng tiền, setup và rủi ro sau khi chạy Vnstock API.",
                "buyZone": "Canh quanh MA20 hoặc nền tích lũy gần nhất, không mua đuổi.",
                "stopLoss": "-7% đến -10%",
                "takeProfit": "+12% đến +25%",
                "allocation": "5% - 20%",
                "catalysts": [
                        "Vnstock API",
                        "Hóa chất / Vật liệu / Dệt may"
                ],
                "cautions": [
                        "Đây là dữ liệu mẫu trước khi chạy API",
                        "Không dùng để giao dịch thật",
                        "Chạy workflow để cập nhật"
                ]
        },
        {
                "ticker": "CSV",
                "name": "Hóa chất Cơ bản Miền Nam",
                "sector": "Hóa chất / Vật liệu / Dệt may",
                "score": 80.2,
                "subscores": {
                        "trend": 20,
                        "momentum": 7.0,
                        "moneyFlow": 14.0,
                        "setup": 13.5,
                        "risk": 12.0,
                        "relativeStrength": 13.7
                },
                "setupType": "Chưa có setup rõ",
                "marketState": "Uptrend",
                "action": "CANH MUA / MUA KHI XÁC NHẬN",
                "risk": "Trung bình",
                "close": 96000,
                "rsi14": 50.5,
                "ret20": 1.9,
                "ret60": 12.0,
                "volume_status": "Mẫu",
                "volumeRatio": 1.85,
                "ma20": 94550,
                "ma50": 93100,
                "ma200": 90200,
                "macd": null,
                "macd_signal": null,
                "distanceToMA20": 7.5,
                "atr14": null,
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
                        "topOpportunity": true,
                        "breakout": false,
                        "pullbackMA20": false,
                        "moneyFlow": false,
                        "accumulation": false,
                        "safe": true
                },
                "reason": "Dữ liệu mẫu cho CSV. Chạy GitHub Actions sau khi thêm VNSTOCK_API_KEY để cập nhật tín hiệu thật.",
                "expertSummary": "CSV đang ở trạng thái mẫu. Hệ thống sẽ cập nhật xu hướng, động lượng, dòng tiền, setup và rủi ro sau khi chạy Vnstock API.",
                "buyZone": "Canh quanh MA20 hoặc nền tích lũy gần nhất, không mua đuổi.",
                "stopLoss": "-7% đến -10%",
                "takeProfit": "+12% đến +25%",
                "allocation": "5% - 20%",
                "catalysts": [
                        "Vnstock API",
                        "Hóa chất / Vật liệu / Dệt may"
                ],
                "cautions": [
                        "Đây là dữ liệu mẫu trước khi chạy API",
                        "Không dùng để giao dịch thật",
                        "Chạy workflow để cập nhật"
                ]
        },
        {
                "ticker": "LAS",
                "name": "Supe Lâm Thao",
                "sector": "Hóa chất / Vật liệu / Dệt may",
                "score": 55.7,
                "subscores": {
                        "trend": 10,
                        "momentum": 8.4,
                        "moneyFlow": 15.5,
                        "setup": 5.0,
                        "risk": 10.8,
                        "relativeStrength": 6.0
                },
                "setupType": "Pullback MA20",
                "marketState": "Trung tính",
                "action": "CHỜ THÊM",
                "risk": "Trung bình",
                "close": 96800,
                "rsi14": 52.2,
                "ret20": 2.8,
                "ret60": 13.2,
                "volume_status": "Mẫu",
                "volumeRatio": 0.8,
                "ma20": 95340,
                "ma50": 93880,
                "ma200": 90960,
                "macd": null,
                "macd_signal": null,
                "distanceToMA20": -3.5,
                "atr14": null,
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
                        "topOpportunity": false,
                        "breakout": false,
                        "pullbackMA20": true,
                        "moneyFlow": true,
                        "accumulation": false,
                        "safe": false
                },
                "reason": "Dữ liệu mẫu cho LAS. Chạy GitHub Actions sau khi thêm VNSTOCK_API_KEY để cập nhật tín hiệu thật.",
                "expertSummary": "LAS đang ở trạng thái mẫu. Hệ thống sẽ cập nhật xu hướng, động lượng, dòng tiền, setup và rủi ro sau khi chạy Vnstock API.",
                "buyZone": "Canh quanh MA20 hoặc nền tích lũy gần nhất, không mua đuổi.",
                "stopLoss": "-7% đến -10%",
                "takeProfit": "+12% đến +25%",
                "allocation": "5% - 20%",
                "catalysts": [
                        "Vnstock API",
                        "Hóa chất / Vật liệu / Dệt may"
                ],
                "cautions": [
                        "Đây là dữ liệu mẫu trước khi chạy API",
                        "Không dùng để giao dịch thật",
                        "Chạy workflow để cập nhật"
                ]
        },
        {
                "ticker": "DDV",
                "name": "DAP Vinachem",
                "sector": "Hóa chất / Vật liệu / Dệt may",
                "score": 62.2,
                "subscores": {
                        "trend": 12,
                        "momentum": 9.8,
                        "moneyFlow": 17.0,
                        "setup": 6.7,
                        "risk": 9.6,
                        "relativeStrength": 7.1
                },
                "setupType": "Breakout 20 phiên",
                "marketState": "Tích cực",
                "action": "CHỜ THÊM",
                "risk": "Trung bình",
                "close": 97600,
                "rsi14": 53.9,
                "ret20": 3.7,
                "ret60": 14.4,
                "volume_status": "Mẫu",
                "volumeRatio": 0.95,
                "ma20": 96130,
                "ma50": 94660,
                "ma200": 91720,
                "macd": null,
                "macd_signal": null,
                "distanceToMA20": -2.5,
                "atr14": null,
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
                        "topOpportunity": false,
                        "breakout": true,
                        "pullbackMA20": false,
                        "moneyFlow": true,
                        "accumulation": false,
                        "safe": false
                },
                "reason": "Dữ liệu mẫu cho DDV. Chạy GitHub Actions sau khi thêm VNSTOCK_API_KEY để cập nhật tín hiệu thật.",
                "expertSummary": "DDV đang ở trạng thái mẫu. Hệ thống sẽ cập nhật xu hướng, động lượng, dòng tiền, setup và rủi ro sau khi chạy Vnstock API.",
                "buyZone": "Canh quanh MA20 hoặc nền tích lũy gần nhất, không mua đuổi.",
                "stopLoss": "-7% đến -10%",
                "takeProfit": "+12% đến +25%",
                "allocation": "5% - 20%",
                "catalysts": [
                        "Vnstock API",
                        "Hóa chất / Vật liệu / Dệt may"
                ],
                "cautions": [
                        "Đây là dữ liệu mẫu trước khi chạy API",
                        "Không dùng để giao dịch thật",
                        "Chạy workflow để cập nhật"
                ]
        },
        {
                "ticker": "BFC",
                "name": "Phân bón Bình Điền",
                "sector": "Hóa chất / Vật liệu / Dệt may",
                "score": 58.2,
                "subscores": {
                        "trend": 14,
                        "momentum": 11.2,
                        "moneyFlow": 8.0,
                        "setup": 8.4,
                        "risk": 8.4,
                        "relativeStrength": 8.2
                },
                "setupType": "Tích lũy biên hẹp",
                "marketState": "Tích cực",
                "action": "CHỜ THÊM",
                "risk": "Trung bình",
                "close": 98400,
                "rsi14": 55.6,
                "ret20": 4.6,
                "ret60": 15.6,
                "volume_status": "Mẫu",
                "volumeRatio": 1.1,
                "ma20": 96920,
                "ma50": 95440,
                "ma200": 92480,
                "macd": null,
                "macd_signal": null,
                "distanceToMA20": -1.5,
                "atr14": null,
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
                        "topOpportunity": false,
                        "breakout": false,
                        "pullbackMA20": false,
                        "moneyFlow": false,
                        "accumulation": true,
                        "safe": false
                },
                "reason": "Dữ liệu mẫu cho BFC. Chạy GitHub Actions sau khi thêm VNSTOCK_API_KEY để cập nhật tín hiệu thật.",
                "expertSummary": "BFC đang ở trạng thái mẫu. Hệ thống sẽ cập nhật xu hướng, động lượng, dòng tiền, setup và rủi ro sau khi chạy Vnstock API.",
                "buyZone": "Canh quanh MA20 hoặc nền tích lũy gần nhất, không mua đuổi.",
                "stopLoss": "-7% đến -10%",
                "takeProfit": "+12% đến +25%",
                "allocation": "5% - 20%",
                "catalysts": [
                        "Vnstock API",
                        "Hóa chất / Vật liệu / Dệt may"
                ],
                "cautions": [
                        "Đây là dữ liệu mẫu trước khi chạy API",
                        "Không dùng để giao dịch thật",
                        "Chạy workflow để cập nhật"
                ]
        },
        {
                "ticker": "GVR",
                "name": "Tập đoàn Cao su Việt Nam",
                "sector": "Hóa chất / Vật liệu / Dệt may",
                "score": 64.7,
                "subscores": {
                        "trend": 16,
                        "momentum": 12.6,
                        "moneyFlow": 9.5,
                        "setup": 10.1,
                        "risk": 7.2,
                        "relativeStrength": 9.3
                },
                "setupType": "Retest nền",
                "marketState": "Uptrend",
                "action": "CHỜ THÊM",
                "risk": "Trung bình",
                "close": 99200,
                "rsi14": 57.3,
                "ret20": 5.5,
                "ret60": 16.8,
                "volume_status": "Mẫu",
                "volumeRatio": 1.25,
                "ma20": 97710,
                "ma50": 96220,
                "ma200": 93240,
                "macd": null,
                "macd_signal": null,
                "distanceToMA20": -0.5,
                "atr14": null,
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
                        "topOpportunity": false,
                        "breakout": false,
                        "pullbackMA20": false,
                        "moneyFlow": false,
                        "accumulation": false,
                        "safe": false
                },
                "reason": "Dữ liệu mẫu cho GVR. Chạy GitHub Actions sau khi thêm VNSTOCK_API_KEY để cập nhật tín hiệu thật.",
                "expertSummary": "GVR đang ở trạng thái mẫu. Hệ thống sẽ cập nhật xu hướng, động lượng, dòng tiền, setup và rủi ro sau khi chạy Vnstock API.",
                "buyZone": "Canh quanh MA20 hoặc nền tích lũy gần nhất, không mua đuổi.",
                "stopLoss": "-7% đến -10%",
                "takeProfit": "+12% đến +25%",
                "allocation": "5% - 20%",
                "catalysts": [
                        "Vnstock API",
                        "Hóa chất / Vật liệu / Dệt may"
                ],
                "cautions": [
                        "Đây là dữ liệu mẫu trước khi chạy API",
                        "Không dùng để giao dịch thật",
                        "Chạy workflow để cập nhật"
                ]
        },
        {
                "ticker": "PHR",
                "name": "Cao su Phước Hòa",
                "sector": "Hóa chất / Vật liệu / Dệt may",
                "score": 70.2,
                "subscores": {
                        "trend": 18,
                        "momentum": 7.0,
                        "moneyFlow": 11.0,
                        "setup": 11.8,
                        "risk": 12.0,
                        "relativeStrength": 10.4
                },
                "setupType": "Vượt lại MA50",
                "marketState": "Uptrend",
                "action": "THEO DÕI MUA",
                "risk": "Trung bình",
                "close": 100000,
                "rsi14": 59.0,
                "ret20": 6.4,
                "ret60": -12.0,
                "volume_status": "Mẫu",
                "volumeRatio": 1.4,
                "ma20": 98500,
                "ma50": 97000,
                "ma200": 94000,
                "macd": null,
                "macd_signal": null,
                "distanceToMA20": 0.5,
                "atr14": null,
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
                        "topOpportunity": false,
                        "breakout": false,
                        "pullbackMA20": false,
                        "moneyFlow": false,
                        "accumulation": false,
                        "safe": true
                },
                "reason": "Dữ liệu mẫu cho PHR. Chạy GitHub Actions sau khi thêm VNSTOCK_API_KEY để cập nhật tín hiệu thật.",
                "expertSummary": "PHR đang ở trạng thái mẫu. Hệ thống sẽ cập nhật xu hướng, động lượng, dòng tiền, setup và rủi ro sau khi chạy Vnstock API.",
                "buyZone": "Canh quanh MA20 hoặc nền tích lũy gần nhất, không mua đuổi.",
                "stopLoss": "-7% đến -10%",
                "takeProfit": "+12% đến +25%",
                "allocation": "5% - 20%",
                "catalysts": [
                        "Vnstock API",
                        "Hóa chất / Vật liệu / Dệt may"
                ],
                "cautions": [
                        "Đây là dữ liệu mẫu trước khi chạy API",
                        "Không dùng để giao dịch thật",
                        "Chạy workflow để cập nhật"
                ]
        },
        {
                "ticker": "DPR",
                "name": "Cao su Đồng Phú",
                "sector": "Hóa chất / Vật liệu / Dệt may",
                "score": 76.7,
                "subscores": {
                        "trend": 20,
                        "momentum": 8.4,
                        "moneyFlow": 12.5,
                        "setup": 13.5,
                        "risk": 10.8,
                        "relativeStrength": 11.5
                },
                "setupType": "Chưa có setup rõ",
                "marketState": "Uptrend",
                "action": "CANH MUA / MUA KHI XÁC NHẬN",
                "risk": "Trung bình",
                "close": 100800,
                "rsi14": 60.7,
                "ret20": 7.3,
                "ret60": -10.8,
                "volume_status": "Mẫu",
                "volumeRatio": 1.55,
                "ma20": 99290,
                "ma50": 97780,
                "ma200": 94760,
                "macd": null,
                "macd_signal": null,
                "distanceToMA20": 1.5,
                "atr14": null,
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
                        "topOpportunity": false,
                        "breakout": false,
                        "pullbackMA20": false,
                        "moneyFlow": false,
                        "accumulation": false,
                        "safe": false
                },
                "reason": "Dữ liệu mẫu cho DPR. Chạy GitHub Actions sau khi thêm VNSTOCK_API_KEY để cập nhật tín hiệu thật.",
                "expertSummary": "DPR đang ở trạng thái mẫu. Hệ thống sẽ cập nhật xu hướng, động lượng, dòng tiền, setup và rủi ro sau khi chạy Vnstock API.",
                "buyZone": "Canh quanh MA20 hoặc nền tích lũy gần nhất, không mua đuổi.",
                "stopLoss": "-7% đến -10%",
                "takeProfit": "+12% đến +25%",
                "allocation": "5% - 20%",
                "catalysts": [
                        "Vnstock API",
                        "Hóa chất / Vật liệu / Dệt may"
                ],
                "cautions": [
                        "Đây là dữ liệu mẫu trước khi chạy API",
                        "Không dùng để giao dịch thật",
                        "Chạy workflow để cập nhật"
                ]
        },
        {
                "ticker": "DRC",
                "name": "Cao su Đà Nẵng",
                "sector": "Hóa chất / Vật liệu / Dệt may",
                "score": 61.0,
                "subscores": {
                        "trend": 10,
                        "momentum": 9.8,
                        "moneyFlow": 14.0,
                        "setup": 5.0,
                        "risk": 9.6,
                        "relativeStrength": 12.6
                },
                "setupType": "Pullback MA20",
                "marketState": "Trung tính",
                "action": "CHỜ THÊM",
                "risk": "Trung bình",
                "close": 101600,
                "rsi14": 62.4,
                "ret20": 8.2,
                "ret60": -9.6,
                "volume_status": "Mẫu",
                "volumeRatio": 1.7,
                "ma20": 100080,
                "ma50": 98560,
                "ma200": 95520,
                "macd": null,
                "macd_signal": null,
                "distanceToMA20": 2.5,
                "atr14": null,
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
                        "topOpportunity": false,
                        "breakout": false,
                        "pullbackMA20": true,
                        "moneyFlow": false,
                        "accumulation": false,
                        "safe": false
                },
                "reason": "Dữ liệu mẫu cho DRC. Chạy GitHub Actions sau khi thêm VNSTOCK_API_KEY để cập nhật tín hiệu thật.",
                "expertSummary": "DRC đang ở trạng thái mẫu. Hệ thống sẽ cập nhật xu hướng, động lượng, dòng tiền, setup và rủi ro sau khi chạy Vnstock API.",
                "buyZone": "Canh quanh MA20 hoặc nền tích lũy gần nhất, không mua đuổi.",
                "stopLoss": "-7% đến -10%",
                "takeProfit": "+12% đến +25%",
                "allocation": "5% - 20%",
                "catalysts": [
                        "Vnstock API",
                        "Hóa chất / Vật liệu / Dệt may"
                ],
                "cautions": [
                        "Đây là dữ liệu mẫu trước khi chạy API",
                        "Không dùng để giao dịch thật",
                        "Chạy workflow để cập nhật"
                ]
        },
        {
                "ticker": "BMP",
                "name": "Nhựa Bình Minh",
                "sector": "Hóa chất / Vật liệu / Dệt may",
                "score": 67.5,
                "subscores": {
                        "trend": 12,
                        "momentum": 11.2,
                        "moneyFlow": 15.5,
                        "setup": 6.7,
                        "risk": 8.4,
                        "relativeStrength": 13.7
                },
                "setupType": "Breakout 20 phiên",
                "marketState": "Tích cực",
                "action": "THEO DÕI MUA",
                "risk": "Trung bình",
                "close": 102400,
                "rsi14": 64.1,
                "ret20": 9.1,
                "ret60": -8.4,
                "volume_status": "Mẫu",
                "volumeRatio": 1.85,
                "ma20": 100870,
                "ma50": 99340,
                "ma200": 96280,
                "macd": null,
                "macd_signal": null,
                "distanceToMA20": 3.5,
                "atr14": null,
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
                        "topOpportunity": false,
                        "breakout": true,
                        "pullbackMA20": false,
                        "moneyFlow": true,
                        "accumulation": false,
                        "safe": false
                },
                "reason": "Dữ liệu mẫu cho BMP. Chạy GitHub Actions sau khi thêm VNSTOCK_API_KEY để cập nhật tín hiệu thật.",
                "expertSummary": "BMP đang ở trạng thái mẫu. Hệ thống sẽ cập nhật xu hướng, động lượng, dòng tiền, setup và rủi ro sau khi chạy Vnstock API.",
                "buyZone": "Canh quanh MA20 hoặc nền tích lũy gần nhất, không mua đuổi.",
                "stopLoss": "-7% đến -10%",
                "takeProfit": "+12% đến +25%",
                "allocation": "5% - 20%",
                "catalysts": [
                        "Vnstock API",
                        "Hóa chất / Vật liệu / Dệt may"
                ],
                "cautions": [
                        "Đây là dữ liệu mẫu trước khi chạy API",
                        "Không dùng để giao dịch thật",
                        "Chạy workflow để cập nhật"
                ]
        },
        {
                "ticker": "NTP",
                "name": "Nhựa Tiền Phong",
                "sector": "Hóa chất / Vật liệu / Dệt may",
                "score": 65.2,
                "subscores": {
                        "trend": 14,
                        "momentum": 12.6,
                        "moneyFlow": 17.0,
                        "setup": 8.4,
                        "risk": 7.2,
                        "relativeStrength": 6.0
                },
                "setupType": "Tích lũy biên hẹp",
                "marketState": "Tích cực",
                "action": "THEO DÕI MUA",
                "risk": "Trung bình",
                "close": 103200,
                "rsi14": 65.8,
                "ret20": 10.0,
                "ret60": -7.2,
                "volume_status": "Mẫu",
                "volumeRatio": 0.8,
                "ma20": 101660,
                "ma50": 100120,
                "ma200": 97040,
                "macd": null,
                "macd_signal": null,
                "distanceToMA20": 4.5,
                "atr14": null,
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
                        "topOpportunity": false,
                        "breakout": false,
                        "pullbackMA20": false,
                        "moneyFlow": true,
                        "accumulation": true,
                        "safe": false
                },
                "reason": "Dữ liệu mẫu cho NTP. Chạy GitHub Actions sau khi thêm VNSTOCK_API_KEY để cập nhật tín hiệu thật.",
                "expertSummary": "NTP đang ở trạng thái mẫu. Hệ thống sẽ cập nhật xu hướng, động lượng, dòng tiền, setup và rủi ro sau khi chạy Vnstock API.",
                "buyZone": "Canh quanh MA20 hoặc nền tích lũy gần nhất, không mua đuổi.",
                "stopLoss": "-7% đến -10%",
                "takeProfit": "+12% đến +25%",
                "allocation": "5% - 20%",
                "catalysts": [
                        "Vnstock API",
                        "Hóa chất / Vật liệu / Dệt may"
                ],
                "cautions": [
                        "Đây là dữ liệu mẫu trước khi chạy API",
                        "Không dùng để giao dịch thật",
                        "Chạy workflow để cập nhật"
                ]
        },
        {
                "ticker": "AAA",
                "name": "An Phát Bioplastics",
                "sector": "Hóa chất / Vật liệu / Dệt may",
                "score": 60.2,
                "subscores": {
                        "trend": 16,
                        "momentum": 7.0,
                        "moneyFlow": 8.0,
                        "setup": 10.1,
                        "risk": 12.0,
                        "relativeStrength": 7.1
                },
                "setupType": "Retest nền",
                "marketState": "Uptrend",
                "action": "CHỜ THÊM",
                "risk": "Trung bình",
                "close": 104000,
                "rsi14": 67.5,
                "ret20": -8.0,
                "ret60": -6.0,
                "volume_status": "Mẫu",
                "volumeRatio": 0.95,
                "ma20": 102450,
                "ma50": 100900,
                "ma200": 97800,
                "macd": null,
                "macd_signal": null,
                "distanceToMA20": 5.5,
                "atr14": null,
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
                        "topOpportunity": false,
                        "breakout": false,
                        "pullbackMA20": false,
                        "moneyFlow": false,
                        "accumulation": false,
                        "safe": false
                },
                "reason": "Dữ liệu mẫu cho AAA. Chạy GitHub Actions sau khi thêm VNSTOCK_API_KEY để cập nhật tín hiệu thật.",
                "expertSummary": "AAA đang ở trạng thái mẫu. Hệ thống sẽ cập nhật xu hướng, động lượng, dòng tiền, setup và rủi ro sau khi chạy Vnstock API.",
                "buyZone": "Canh quanh MA20 hoặc nền tích lũy gần nhất, không mua đuổi.",
                "stopLoss": "-7% đến -10%",
                "takeProfit": "+12% đến +25%",
                "allocation": "5% - 20%",
                "catalysts": [
                        "Vnstock API",
                        "Hóa chất / Vật liệu / Dệt may"
                ],
                "cautions": [
                        "Đây là dữ liệu mẫu trước khi chạy API",
                        "Không dùng để giao dịch thật",
                        "Chạy workflow để cập nhật"
                ]
        },
        {
                "ticker": "DHC",
                "name": "Đông Hải Bến Tre",
                "sector": "Hóa chất / Vật liệu / Dệt may",
                "score": 66.7,
                "subscores": {
                        "trend": 18,
                        "momentum": 8.4,
                        "moneyFlow": 9.5,
                        "setup": 11.8,
                        "risk": 10.8,
                        "relativeStrength": 8.2
                },
                "setupType": "Vượt lại MA50",
                "marketState": "Uptrend",
                "action": "THEO DÕI MUA",
                "risk": "Trung bình",
                "close": 104800,
                "rsi14": 69.2,
                "ret20": -7.1,
                "ret60": -4.8,
                "volume_status": "Mẫu",
                "volumeRatio": 1.1,
                "ma20": 103240,
                "ma50": 101680,
                "ma200": 98560,
                "macd": null,
                "macd_signal": null,
                "distanceToMA20": 6.5,
                "atr14": null,
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
                        "topOpportunity": false,
                        "breakout": false,
                        "pullbackMA20": false,
                        "moneyFlow": false,
                        "accumulation": false,
                        "safe": false
                },
                "reason": "Dữ liệu mẫu cho DHC. Chạy GitHub Actions sau khi thêm VNSTOCK_API_KEY để cập nhật tín hiệu thật.",
                "expertSummary": "DHC đang ở trạng thái mẫu. Hệ thống sẽ cập nhật xu hướng, động lượng, dòng tiền, setup và rủi ro sau khi chạy Vnstock API.",
                "buyZone": "Canh quanh MA20 hoặc nền tích lũy gần nhất, không mua đuổi.",
                "stopLoss": "-7% đến -10%",
                "takeProfit": "+12% đến +25%",
                "allocation": "5% - 20%",
                "catalysts": [
                        "Vnstock API",
                        "Hóa chất / Vật liệu / Dệt may"
                ],
                "cautions": [
                        "Đây là dữ liệu mẫu trước khi chạy API",
                        "Không dùng để giao dịch thật",
                        "Chạy workflow để cập nhật"
                ]
        },
        {
                "ticker": "GIL",
                "name": "Gilimex",
                "sector": "Hóa chất / Vật liệu / Dệt may",
                "score": 73.2,
                "subscores": {
                        "trend": 20,
                        "momentum": 9.8,
                        "moneyFlow": 11.0,
                        "setup": 13.5,
                        "risk": 9.6,
                        "relativeStrength": 9.3
                },
                "setupType": "Chưa có setup rõ",
                "marketState": "Uptrend",
                "action": "THEO DÕI MUA",
                "risk": "Trung bình",
                "close": 105600,
                "rsi14": 70.9,
                "ret20": -6.2,
                "ret60": -3.6,
                "volume_status": "Mẫu",
                "volumeRatio": 1.25,
                "ma20": 104030,
                "ma50": 102460,
                "ma200": 99320,
                "macd": null,
                "macd_signal": null,
                "distanceToMA20": 7.5,
                "atr14": null,
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
                        "topOpportunity": false,
                        "breakout": false,
                        "pullbackMA20": false,
                        "moneyFlow": false,
                        "accumulation": false,
                        "safe": false
                },
                "reason": "Dữ liệu mẫu cho GIL. Chạy GitHub Actions sau khi thêm VNSTOCK_API_KEY để cập nhật tín hiệu thật.",
                "expertSummary": "GIL đang ở trạng thái mẫu. Hệ thống sẽ cập nhật xu hướng, động lượng, dòng tiền, setup và rủi ro sau khi chạy Vnstock API.",
                "buyZone": "Canh quanh MA20 hoặc nền tích lũy gần nhất, không mua đuổi.",
                "stopLoss": "-7% đến -10%",
                "takeProfit": "+12% đến +25%",
                "allocation": "5% - 20%",
                "catalysts": [
                        "Vnstock API",
                        "Hóa chất / Vật liệu / Dệt may"
                ],
                "cautions": [
                        "Đây là dữ liệu mẫu trước khi chạy API",
                        "Không dùng để giao dịch thật",
                        "Chạy workflow để cập nhật"
                ]
        },
        {
                "ticker": "TNG",
                "name": "TNG Investment",
                "sector": "Hóa chất / Vật liệu / Dệt may",
                "score": 57.5,
                "subscores": {
                        "trend": 10,
                        "momentum": 11.2,
                        "moneyFlow": 12.5,
                        "setup": 5.0,
                        "risk": 8.4,
                        "relativeStrength": 10.4
                },
                "setupType": "Pullback MA20",
                "marketState": "Trung tính",
                "action": "CHỜ THÊM",
                "risk": "Trung bình",
                "close": 106400,
                "rsi14": 42.0,
                "ret20": -5.3,
                "ret60": -2.4,
                "volume_status": "Mẫu",
                "volumeRatio": 1.4,
                "ma20": 104820,
                "ma50": 103240,
                "ma200": 100080,
                "macd": null,
                "macd_signal": null,
                "distanceToMA20": -3.5,
                "atr14": null,
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
                        "topOpportunity": false,
                        "breakout": false,
                        "pullbackMA20": true,
                        "moneyFlow": false,
                        "accumulation": false,
                        "safe": false
                },
                "reason": "Dữ liệu mẫu cho TNG. Chạy GitHub Actions sau khi thêm VNSTOCK_API_KEY để cập nhật tín hiệu thật.",
                "expertSummary": "TNG đang ở trạng thái mẫu. Hệ thống sẽ cập nhật xu hướng, động lượng, dòng tiền, setup và rủi ro sau khi chạy Vnstock API.",
                "buyZone": "Canh quanh MA20 hoặc nền tích lũy gần nhất, không mua đuổi.",
                "stopLoss": "-7% đến -10%",
                "takeProfit": "+12% đến +25%",
                "allocation": "5% - 20%",
                "catalysts": [
                        "Vnstock API",
                        "Hóa chất / Vật liệu / Dệt may"
                ],
                "cautions": [
                        "Đây là dữ liệu mẫu trước khi chạy API",
                        "Không dùng để giao dịch thật",
                        "Chạy workflow để cập nhật"
                ]
        },
        {
                "ticker": "MSH",
                "name": "May Sông Hồng",
                "sector": "Hóa chất / Vật liệu / Dệt may",
                "score": 64.0,
                "subscores": {
                        "trend": 12,
                        "momentum": 12.6,
                        "moneyFlow": 14.0,
                        "setup": 6.7,
                        "risk": 7.2,
                        "relativeStrength": 11.5
                },
                "setupType": "Breakout 20 phiên",
                "marketState": "Tích cực",
                "action": "CHỜ THÊM",
                "risk": "Trung bình",
                "close": 107200,
                "rsi14": 43.7,
                "ret20": -4.4,
                "ret60": -1.2,
                "volume_status": "Mẫu",
                "volumeRatio": 1.55,
                "ma20": 105610,
                "ma50": 104020,
                "ma200": 100840,
                "macd": null,
                "macd_signal": null,
                "distanceToMA20": -2.5,
                "atr14": null,
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
                        "topOpportunity": false,
                        "breakout": true,
                        "pullbackMA20": false,
                        "moneyFlow": false,
                        "accumulation": false,
                        "safe": false
                },
                "reason": "Dữ liệu mẫu cho MSH. Chạy GitHub Actions sau khi thêm VNSTOCK_API_KEY để cập nhật tín hiệu thật.",
                "expertSummary": "MSH đang ở trạng thái mẫu. Hệ thống sẽ cập nhật xu hướng, động lượng, dòng tiền, setup và rủi ro sau khi chạy Vnstock API.",
                "buyZone": "Canh quanh MA20 hoặc nền tích lũy gần nhất, không mua đuổi.",
                "stopLoss": "-7% đến -10%",
                "takeProfit": "+12% đến +25%",
                "allocation": "5% - 20%",
                "catalysts": [
                        "Vnstock API",
                        "Hóa chất / Vật liệu / Dệt may"
                ],
                "cautions": [
                        "Đây là dữ liệu mẫu trước khi chạy API",
                        "Không dùng để giao dịch thật",
                        "Chạy workflow để cập nhật"
                ]
        },
        {
                "ticker": "TCM",
                "name": "Dệt may Thành Công",
                "sector": "Hóa chất / Vật liệu / Dệt may",
                "score": 69.5,
                "subscores": {
                        "trend": 14,
                        "momentum": 7.0,
                        "moneyFlow": 15.5,
                        "setup": 8.4,
                        "risk": 12.0,
                        "relativeStrength": 12.6
                },
                "setupType": "Tích lũy biên hẹp",
                "marketState": "Tích cực",
                "action": "THEO DÕI MUA",
                "risk": "Trung bình",
                "close": 108000,
                "rsi14": 45.4,
                "ret20": -3.5,
                "ret60": 0.0,
                "volume_status": "Mẫu",
                "volumeRatio": 1.7,
                "ma20": 106400,
                "ma50": 104800,
                "ma200": 101600,
                "macd": null,
                "macd_signal": null,
                "distanceToMA20": -1.5,
                "atr14": null,
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
                        "topOpportunity": false,
                        "breakout": false,
                        "pullbackMA20": false,
                        "moneyFlow": true,
                        "accumulation": true,
                        "safe": true
                },
                "reason": "Dữ liệu mẫu cho TCM. Chạy GitHub Actions sau khi thêm VNSTOCK_API_KEY để cập nhật tín hiệu thật.",
                "expertSummary": "TCM đang ở trạng thái mẫu. Hệ thống sẽ cập nhật xu hướng, động lượng, dòng tiền, setup và rủi ro sau khi chạy Vnstock API.",
                "buyZone": "Canh quanh MA20 hoặc nền tích lũy gần nhất, không mua đuổi.",
                "stopLoss": "-7% đến -10%",
                "takeProfit": "+12% đến +25%",
                "allocation": "5% - 20%",
                "catalysts": [
                        "Vnstock API",
                        "Hóa chất / Vật liệu / Dệt may"
                ],
                "cautions": [
                        "Đây là dữ liệu mẫu trước khi chạy API",
                        "Không dùng để giao dịch thật",
                        "Chạy workflow để cập nhật"
                ]
        },
        {
                "ticker": "VNM",
                "name": "Vinamilk",
                "sector": "Tiêu dùng / Nông nghiệp / Thủy sản",
                "score": 76.0,
                "subscores": {
                        "trend": 16,
                        "momentum": 8.4,
                        "moneyFlow": 17.0,
                        "setup": 10.1,
                        "risk": 10.8,
                        "relativeStrength": 13.7
                },
                "setupType": "Retest nền",
                "marketState": "Uptrend",
                "action": "CANH MUA / MUA KHI XÁC NHẬN",
                "risk": "Trung bình",
                "close": 108800,
                "rsi14": 47.1,
                "ret20": -2.6,
                "ret60": 1.2,
                "volume_status": "Mẫu",
                "volumeRatio": 1.85,
                "ma20": 107190,
                "ma50": 105580,
                "ma200": 102360,
                "macd": null,
                "macd_signal": null,
                "distanceToMA20": -0.5,
                "atr14": null,
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
                        "topOpportunity": false,
                        "breakout": false,
                        "pullbackMA20": false,
                        "moneyFlow": true,
                        "accumulation": false,
                        "safe": false
                },
                "reason": "Dữ liệu mẫu cho VNM. Chạy GitHub Actions sau khi thêm VNSTOCK_API_KEY để cập nhật tín hiệu thật.",
                "expertSummary": "VNM đang ở trạng thái mẫu. Hệ thống sẽ cập nhật xu hướng, động lượng, dòng tiền, setup và rủi ro sau khi chạy Vnstock API.",
                "buyZone": "Canh quanh MA20 hoặc nền tích lũy gần nhất, không mua đuổi.",
                "stopLoss": "-7% đến -10%",
                "takeProfit": "+12% đến +25%",
                "allocation": "5% - 20%",
                "catalysts": [
                        "Vnstock API",
                        "Tiêu dùng / Nông nghiệp / Thủy sản"
                ],
                "cautions": [
                        "Đây là dữ liệu mẫu trước khi chạy API",
                        "Không dùng để giao dịch thật",
                        "Chạy workflow để cập nhật"
                ]
        },
        {
                "ticker": "MSN",
                "name": "Masan Group",
                "sector": "Tiêu dùng / Nông nghiệp / Thủy sản",
                "score": 63.2,
                "subscores": {
                        "trend": 18,
                        "momentum": 9.8,
                        "moneyFlow": 8.0,
                        "setup": 11.8,
                        "risk": 9.6,
                        "relativeStrength": 6.0
                },
                "setupType": "Vượt lại MA50",
                "marketState": "Uptrend",
                "action": "CHỜ THÊM",
                "risk": "Trung bình",
                "close": 109600,
                "rsi14": 48.8,
                "ret20": -1.7,
                "ret60": 2.4,
                "volume_status": "Mẫu",
                "volumeRatio": 0.8,
                "ma20": 107980,
                "ma50": 106360,
                "ma200": 103120,
                "macd": null,
                "macd_signal": null,
                "distanceToMA20": 0.5,
                "atr14": null,
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
                        "topOpportunity": false,
                        "breakout": false,
                        "pullbackMA20": false,
                        "moneyFlow": false,
                        "accumulation": false,
                        "safe": false
                },
                "reason": "Dữ liệu mẫu cho MSN. Chạy GitHub Actions sau khi thêm VNSTOCK_API_KEY để cập nhật tín hiệu thật.",
                "expertSummary": "MSN đang ở trạng thái mẫu. Hệ thống sẽ cập nhật xu hướng, động lượng, dòng tiền, setup và rủi ro sau khi chạy Vnstock API.",
                "buyZone": "Canh quanh MA20 hoặc nền tích lũy gần nhất, không mua đuổi.",
                "stopLoss": "-7% đến -10%",
                "takeProfit": "+12% đến +25%",
                "allocation": "5% - 20%",
                "catalysts": [
                        "Vnstock API",
                        "Tiêu dùng / Nông nghiệp / Thủy sản"
                ],
                "cautions": [
                        "Đây là dữ liệu mẫu trước khi chạy API",
                        "Không dùng để giao dịch thật",
                        "Chạy workflow để cập nhật"
                ]
        },
        {
                "ticker": "MCH",
                "name": "Masan Consumer",
                "sector": "Tiêu dùng / Nông nghiệp / Thủy sản",
                "score": 69.7,
                "subscores": {
                        "trend": 20,
                        "momentum": 11.2,
                        "moneyFlow": 9.5,
                        "setup": 13.5,
                        "risk": 8.4,
                        "relativeStrength": 7.1
                },
                "setupType": "Chưa có setup rõ",
                "marketState": "Uptrend",
                "action": "THEO DÕI MUA",
                "risk": "Trung bình",
                "close": 110400,
                "rsi14": 50.5,
                "ret20": -0.8,
                "ret60": 3.6,
                "volume_status": "Mẫu",
                "volumeRatio": 0.95,
                "ma20": 108770,
                "ma50": 107140,
                "ma200": 103880,
                "macd": null,
                "macd_signal": null,
                "distanceToMA20": 1.5,
                "atr14": null,
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
                        "topOpportunity": false,
                        "breakout": false,
                        "pullbackMA20": false,
                        "moneyFlow": false,
                        "accumulation": false,
                        "safe": false
                },
                "reason": "Dữ liệu mẫu cho MCH. Chạy GitHub Actions sau khi thêm VNSTOCK_API_KEY để cập nhật tín hiệu thật.",
                "expertSummary": "MCH đang ở trạng thái mẫu. Hệ thống sẽ cập nhật xu hướng, động lượng, dòng tiền, setup và rủi ro sau khi chạy Vnstock API.",
                "buyZone": "Canh quanh MA20 hoặc nền tích lũy gần nhất, không mua đuổi.",
                "stopLoss": "-7% đến -10%",
                "takeProfit": "+12% đến +25%",
                "allocation": "5% - 20%",
                "catalysts": [
                        "Vnstock API",
                        "Tiêu dùng / Nông nghiệp / Thủy sản"
                ],
                "cautions": [
                        "Đây là dữ liệu mẫu trước khi chạy API",
                        "Không dùng để giao dịch thật",
                        "Chạy workflow để cập nhật"
                ]
        },
        {
                "ticker": "SAB",
                "name": "Sabeco",
                "sector": "Tiêu dùng / Nông nghiệp / Thủy sản",
                "score": 54.0,
                "subscores": {
                        "trend": 10,
                        "momentum": 12.6,
                        "moneyFlow": 11.0,
                        "setup": 5.0,
                        "risk": 7.2,
                        "relativeStrength": 8.2
                },
                "setupType": "Pullback MA20",
                "marketState": "Trung tính",
                "action": "TRÁNH MUA MỚI",
                "risk": "Trung bình",
                "close": 111200,
                "rsi14": 52.2,
                "ret20": 0.1,
                "ret60": 4.8,
                "volume_status": "Mẫu",
                "volumeRatio": 1.1,
                "ma20": 109560,
                "ma50": 107920,
                "ma200": 104640,
                "macd": null,
                "macd_signal": null,
                "distanceToMA20": 2.5,
                "atr14": null,
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
                        "topOpportunity": false,
                        "breakout": false,
                        "pullbackMA20": true,
                        "moneyFlow": false,
                        "accumulation": false,
                        "safe": false
                },
                "reason": "Dữ liệu mẫu cho SAB. Chạy GitHub Actions sau khi thêm VNSTOCK_API_KEY để cập nhật tín hiệu thật.",
                "expertSummary": "SAB đang ở trạng thái mẫu. Hệ thống sẽ cập nhật xu hướng, động lượng, dòng tiền, setup và rủi ro sau khi chạy Vnstock API.",
                "buyZone": "Canh quanh MA20 hoặc nền tích lũy gần nhất, không mua đuổi.",
                "stopLoss": "-7% đến -10%",
                "takeProfit": "+12% đến +25%",
                "allocation": "5% - 20%",
                "catalysts": [
                        "Vnstock API",
                        "Tiêu dùng / Nông nghiệp / Thủy sản"
                ],
                "cautions": [
                        "Đây là dữ liệu mẫu trước khi chạy API",
                        "Không dùng để giao dịch thật",
                        "Chạy workflow để cập nhật"
                ]
        },
        {
                "ticker": "KDC",
                "name": "KIDO",
                "sector": "Tiêu dùng / Nông nghiệp / Thủy sản",
                "score": 59.5,
                "subscores": {
                        "trend": 12,
                        "momentum": 7.0,
                        "moneyFlow": 12.5,
                        "setup": 6.7,
                        "risk": 12.0,
                        "relativeStrength": 9.3
                },
                "setupType": "Breakout 20 phiên",
                "marketState": "Tích cực",
                "action": "CHỜ THÊM",
                "risk": "Trung bình",
                "close": 112000,
                "rsi14": 53.9,
                "ret20": 1.0,
                "ret60": 6.0,
                "volume_status": "Mẫu",
                "volumeRatio": 1.25,
                "ma20": 110350,
                "ma50": 108700,
                "ma200": 105400,
                "macd": null,
                "macd_signal": null,
                "distanceToMA20": 3.5,
                "atr14": null,
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
                        "topOpportunity": false,
                        "breakout": true,
                        "pullbackMA20": false,
                        "moneyFlow": false,
                        "accumulation": false,
                        "safe": false
                },
                "reason": "Dữ liệu mẫu cho KDC. Chạy GitHub Actions sau khi thêm VNSTOCK_API_KEY để cập nhật tín hiệu thật.",
                "expertSummary": "KDC đang ở trạng thái mẫu. Hệ thống sẽ cập nhật xu hướng, động lượng, dòng tiền, setup và rủi ro sau khi chạy Vnstock API.",
                "buyZone": "Canh quanh MA20 hoặc nền tích lũy gần nhất, không mua đuổi.",
                "stopLoss": "-7% đến -10%",
                "takeProfit": "+12% đến +25%",
                "allocation": "5% - 20%",
                "catalysts": [
                        "Vnstock API",
                        "Tiêu dùng / Nông nghiệp / Thủy sản"
                ],
                "cautions": [
                        "Đây là dữ liệu mẫu trước khi chạy API",
                        "Không dùng để giao dịch thật",
                        "Chạy workflow để cập nhật"
                ]
        },
        {
                "ticker": "QNS",
                "name": "Đường Quảng Ngãi",
                "sector": "Tiêu dùng / Nông nghiệp / Thủy sản",
                "score": 66.0,
                "subscores": {
                        "trend": 14,
                        "momentum": 8.4,
                        "moneyFlow": 14.0,
                        "setup": 8.4,
                        "risk": 10.8,
                        "relativeStrength": 10.4
                },
                "setupType": "Tích lũy biên hẹp",
                "marketState": "Tích cực",
                "action": "THEO DÕI MUA",
                "risk": "Trung bình",
                "close": 112800,
                "rsi14": 55.6,
                "ret20": 1.9,
                "ret60": 7.2,
                "volume_status": "Mẫu",
                "volumeRatio": 1.4,
                "ma20": 111140,
                "ma50": 109480,
                "ma200": 106160,
                "macd": null,
                "macd_signal": null,
                "distanceToMA20": 4.5,
                "atr14": null,
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
                        "topOpportunity": false,
                        "breakout": false,
                        "pullbackMA20": false,
                        "moneyFlow": false,
                        "accumulation": true,
                        "safe": false
                },
                "reason": "Dữ liệu mẫu cho QNS. Chạy GitHub Actions sau khi thêm VNSTOCK_API_KEY để cập nhật tín hiệu thật.",
                "expertSummary": "QNS đang ở trạng thái mẫu. Hệ thống sẽ cập nhật xu hướng, động lượng, dòng tiền, setup và rủi ro sau khi chạy Vnstock API.",
                "buyZone": "Canh quanh MA20 hoặc nền tích lũy gần nhất, không mua đuổi.",
                "stopLoss": "-7% đến -10%",
                "takeProfit": "+12% đến +25%",
                "allocation": "5% - 20%",
                "catalysts": [
                        "Vnstock API",
                        "Tiêu dùng / Nông nghiệp / Thủy sản"
                ],
                "cautions": [
                        "Đây là dữ liệu mẫu trước khi chạy API",
                        "Không dùng để giao dịch thật",
                        "Chạy workflow để cập nhật"
                ]
        },
        {
                "ticker": "DBC",
                "name": "Dabaco",
                "sector": "Tiêu dùng / Nông nghiệp / Thủy sản",
                "score": 72.5,
                "subscores": {
                        "trend": 16,
                        "momentum": 9.8,
                        "moneyFlow": 15.5,
                        "setup": 10.1,
                        "risk": 9.6,
                        "relativeStrength": 11.5
                },
                "setupType": "Retest nền",
                "marketState": "Uptrend",
                "action": "THEO DÕI MUA",
                "risk": "Trung bình",
                "close": 113600,
                "rsi14": 57.3,
                "ret20": 2.8,
                "ret60": 8.4,
                "volume_status": "Mẫu",
                "volumeRatio": 1.55,
                "ma20": 111930,
                "ma50": 110260,
                "ma200": 106920,
                "macd": null,
                "macd_signal": null,
                "distanceToMA20": 5.5,
                "atr14": null,
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
                        "topOpportunity": false,
                        "breakout": false,
                        "pullbackMA20": false,
                        "moneyFlow": true,
                        "accumulation": false,
                        "safe": false
                },
                "reason": "Dữ liệu mẫu cho DBC. Chạy GitHub Actions sau khi thêm VNSTOCK_API_KEY để cập nhật tín hiệu thật.",
                "expertSummary": "DBC đang ở trạng thái mẫu. Hệ thống sẽ cập nhật xu hướng, động lượng, dòng tiền, setup và rủi ro sau khi chạy Vnstock API.",
                "buyZone": "Canh quanh MA20 hoặc nền tích lũy gần nhất, không mua đuổi.",
                "stopLoss": "-7% đến -10%",
                "takeProfit": "+12% đến +25%",
                "allocation": "5% - 20%",
                "catalysts": [
                        "Vnstock API",
                        "Tiêu dùng / Nông nghiệp / Thủy sản"
                ],
                "cautions": [
                        "Đây là dữ liệu mẫu trước khi chạy API",
                        "Không dùng để giao dịch thật",
                        "Chạy workflow để cập nhật"
                ]
        },
        {
                "ticker": "BAF",
                "name": "BAF Việt Nam",
                "sector": "Tiêu dùng / Nông nghiệp / Thủy sản",
                "score": 79.0,
                "subscores": {
                        "trend": 18,
                        "momentum": 11.2,
                        "moneyFlow": 17.0,
                        "setup": 11.8,
                        "risk": 8.4,
                        "relativeStrength": 12.6
                },
                "setupType": "Vượt lại MA50",
                "marketState": "Uptrend",
                "action": "CANH MUA / MUA KHI XÁC NHẬN",
                "risk": "Trung bình",
                "close": 114400,
                "rsi14": 59.0,
                "ret20": 3.7,
                "ret60": 9.6,
                "volume_status": "Mẫu",
                "volumeRatio": 1.7,
                "ma20": 112720,
                "ma50": 111040,
                "ma200": 107680,
                "macd": null,
                "macd_signal": null,
                "distanceToMA20": 6.5,
                "atr14": null,
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
                        "topOpportunity": false,
                        "breakout": false,
                        "pullbackMA20": false,
                        "moneyFlow": true,
                        "accumulation": false,
                        "safe": false
                },
                "reason": "Dữ liệu mẫu cho BAF. Chạy GitHub Actions sau khi thêm VNSTOCK_API_KEY để cập nhật tín hiệu thật.",
                "expertSummary": "BAF đang ở trạng thái mẫu. Hệ thống sẽ cập nhật xu hướng, động lượng, dòng tiền, setup và rủi ro sau khi chạy Vnstock API.",
                "buyZone": "Canh quanh MA20 hoặc nền tích lũy gần nhất, không mua đuổi.",
                "stopLoss": "-7% đến -10%",
                "takeProfit": "+12% đến +25%",
                "allocation": "5% - 20%",
                "catalysts": [
                        "Vnstock API",
                        "Tiêu dùng / Nông nghiệp / Thủy sản"
                ],
                "cautions": [
                        "Đây là dữ liệu mẫu trước khi chạy API",
                        "Không dùng để giao dịch thật",
                        "Chạy workflow để cập nhật"
                ]
        },
        {
                "ticker": "PAN",
                "name": "PAN Group",
                "sector": "Tiêu dùng / Nông nghiệp / Thủy sản",
                "score": 75.0,
                "subscores": {
                        "trend": 20,
                        "momentum": 12.6,
                        "moneyFlow": 8.0,
                        "setup": 13.5,
                        "risk": 7.2,
                        "relativeStrength": 13.7
                },
                "setupType": "Chưa có setup rõ",
                "marketState": "Uptrend",
                "action": "CANH MUA / MUA KHI XÁC NHẬN",
                "risk": "Trung bình",
                "close": 115200,
                "rsi14": 60.7,
                "ret20": 4.6,
                "ret60": 10.8,
                "volume_status": "Mẫu",
                "volumeRatio": 1.85,
                "ma20": 113510,
                "ma50": 111820,
                "ma200": 108440,
                "macd": null,
                "macd_signal": null,
                "distanceToMA20": 7.5,
                "atr14": null,
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
                        "topOpportunity": false,
                        "breakout": false,
                        "pullbackMA20": false,
                        "moneyFlow": false,
                        "accumulation": false,
                        "safe": false
                },
                "reason": "Dữ liệu mẫu cho PAN. Chạy GitHub Actions sau khi thêm VNSTOCK_API_KEY để cập nhật tín hiệu thật.",
                "expertSummary": "PAN đang ở trạng thái mẫu. Hệ thống sẽ cập nhật xu hướng, động lượng, dòng tiền, setup và rủi ro sau khi chạy Vnstock API.",
                "buyZone": "Canh quanh MA20 hoặc nền tích lũy gần nhất, không mua đuổi.",
                "stopLoss": "-7% đến -10%",
                "takeProfit": "+12% đến +25%",
                "allocation": "5% - 20%",
                "catalysts": [
                        "Vnstock API",
                        "Tiêu dùng / Nông nghiệp / Thủy sản"
                ],
                "cautions": [
                        "Đây là dữ liệu mẫu trước khi chạy API",
                        "Không dùng để giao dịch thật",
                        "Chạy workflow để cập nhật"
                ]
        },
        {
                "ticker": "TAR",
                "name": "Trung An",
                "sector": "Tiêu dùng / Nông nghiệp / Thủy sản",
                "score": 49.5,
                "subscores": {
                        "trend": 10,
                        "momentum": 7.0,
                        "moneyFlow": 9.5,
                        "setup": 5.0,
                        "risk": 12.0,
                        "relativeStrength": 6.0
                },
                "setupType": "Pullback MA20",
                "marketState": "Trung tính",
                "action": "TRÁNH MUA MỚI",
                "risk": "Trung bình",
                "close": 116000,
                "rsi14": 62.4,
                "ret20": 5.5,
                "ret60": 12.0,
                "volume_status": "Mẫu",
                "volumeRatio": 0.8,
                "ma20": 114300,
                "ma50": 112600,
                "ma200": 109200,
                "macd": null,
                "macd_signal": null,
                "distanceToMA20": -3.5,
                "atr14": null,
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
                        "topOpportunity": false,
                        "breakout": false,
                        "pullbackMA20": true,
                        "moneyFlow": false,
                        "accumulation": false,
                        "safe": false
                },
                "reason": "Dữ liệu mẫu cho TAR. Chạy GitHub Actions sau khi thêm VNSTOCK_API_KEY để cập nhật tín hiệu thật.",
                "expertSummary": "TAR đang ở trạng thái mẫu. Hệ thống sẽ cập nhật xu hướng, động lượng, dòng tiền, setup và rủi ro sau khi chạy Vnstock API.",
                "buyZone": "Canh quanh MA20 hoặc nền tích lũy gần nhất, không mua đuổi.",
                "stopLoss": "-7% đến -10%",
                "takeProfit": "+12% đến +25%",
                "allocation": "5% - 20%",
                "catalysts": [
                        "Vnstock API",
                        "Tiêu dùng / Nông nghiệp / Thủy sản"
                ],
                "cautions": [
                        "Đây là dữ liệu mẫu trước khi chạy API",
                        "Không dùng để giao dịch thật",
                        "Chạy workflow để cập nhật"
                ]
        },
        {
                "ticker": "ANV",
                "name": "Nam Việt",
                "sector": "Tiêu dùng / Nông nghiệp / Thủy sản",
                "score": 56.0,
                "subscores": {
                        "trend": 12,
                        "momentum": 8.4,
                        "moneyFlow": 11.0,
                        "setup": 6.7,
                        "risk": 10.8,
                        "relativeStrength": 7.1
                },
                "setupType": "Breakout 20 phiên",
                "marketState": "Tích cực",
                "action": "CHỜ THÊM",
                "risk": "Trung bình",
                "close": 116800,
                "rsi14": 64.1,
                "ret20": 6.4,
                "ret60": 13.2,
                "volume_status": "Mẫu",
                "volumeRatio": 0.95,
                "ma20": 115090,
                "ma50": 113380,
                "ma200": 109960,
                "macd": null,
                "macd_signal": null,
                "distanceToMA20": -2.5,
                "atr14": null,
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
                        "topOpportunity": false,
                        "breakout": true,
                        "pullbackMA20": false,
                        "moneyFlow": false,
                        "accumulation": false,
                        "safe": false
                },
                "reason": "Dữ liệu mẫu cho ANV. Chạy GitHub Actions sau khi thêm VNSTOCK_API_KEY để cập nhật tín hiệu thật.",
                "expertSummary": "ANV đang ở trạng thái mẫu. Hệ thống sẽ cập nhật xu hướng, động lượng, dòng tiền, setup và rủi ro sau khi chạy Vnstock API.",
                "buyZone": "Canh quanh MA20 hoặc nền tích lũy gần nhất, không mua đuổi.",
                "stopLoss": "-7% đến -10%",
                "takeProfit": "+12% đến +25%",
                "allocation": "5% - 20%",
                "catalysts": [
                        "Vnstock API",
                        "Tiêu dùng / Nông nghiệp / Thủy sản"
                ],
                "cautions": [
                        "Đây là dữ liệu mẫu trước khi chạy API",
                        "Không dùng để giao dịch thật",
                        "Chạy workflow để cập nhật"
                ]
        },
        {
                "ticker": "VHC",
                "name": "Vĩnh Hoàn",
                "sector": "Tiêu dùng / Nông nghiệp / Thủy sản",
                "score": 62.5,
                "subscores": {
                        "trend": 14,
                        "momentum": 9.8,
                        "moneyFlow": 12.5,
                        "setup": 8.4,
                        "risk": 9.6,
                        "relativeStrength": 8.2
                },
                "setupType": "Tích lũy biên hẹp",
                "marketState": "Tích cực",
                "action": "CHỜ THÊM",
                "risk": "Trung bình",
                "close": 117600,
                "rsi14": 65.8,
                "ret20": 7.3,
                "ret60": 14.4,
                "volume_status": "Mẫu",
                "volumeRatio": 1.1,
                "ma20": 115880,
                "ma50": 114160,
                "ma200": 110720,
                "macd": null,
                "macd_signal": null,
                "distanceToMA20": -1.5,
                "atr14": null,
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
                        "topOpportunity": false,
                        "breakout": false,
                        "pullbackMA20": false,
                        "moneyFlow": false,
                        "accumulation": true,
                        "safe": false
                },
                "reason": "Dữ liệu mẫu cho VHC. Chạy GitHub Actions sau khi thêm VNSTOCK_API_KEY để cập nhật tín hiệu thật.",
                "expertSummary": "VHC đang ở trạng thái mẫu. Hệ thống sẽ cập nhật xu hướng, động lượng, dòng tiền, setup và rủi ro sau khi chạy Vnstock API.",
                "buyZone": "Canh quanh MA20 hoặc nền tích lũy gần nhất, không mua đuổi.",
                "stopLoss": "-7% đến -10%",
                "takeProfit": "+12% đến +25%",
                "allocation": "5% - 20%",
                "catalysts": [
                        "Vnstock API",
                        "Tiêu dùng / Nông nghiệp / Thủy sản"
                ],
                "cautions": [
                        "Đây là dữ liệu mẫu trước khi chạy API",
                        "Không dùng để giao dịch thật",
                        "Chạy workflow để cập nhật"
                ]
        },
        {
                "ticker": "IDI",
                "name": "IDI Corp",
                "sector": "Tiêu dùng / Nông nghiệp / Thủy sản",
                "score": 69.0,
                "subscores": {
                        "trend": 16,
                        "momentum": 11.2,
                        "moneyFlow": 14.0,
                        "setup": 10.1,
                        "risk": 8.4,
                        "relativeStrength": 9.3
                },
                "setupType": "Retest nền",
                "marketState": "Uptrend",
                "action": "THEO DÕI MUA",
                "risk": "Trung bình",
                "close": 118400,
                "rsi14": 67.5,
                "ret20": 8.2,
                "ret60": 15.6,
                "volume_status": "Mẫu",
                "volumeRatio": 1.25,
                "ma20": 116670,
                "ma50": 114940,
                "ma200": 111480,
                "macd": null,
                "macd_signal": null,
                "distanceToMA20": -0.5,
                "atr14": null,
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
                        "topOpportunity": false,
                        "breakout": false,
                        "pullbackMA20": false,
                        "moneyFlow": false,
                        "accumulation": false,
                        "safe": false
                },
                "reason": "Dữ liệu mẫu cho IDI. Chạy GitHub Actions sau khi thêm VNSTOCK_API_KEY để cập nhật tín hiệu thật.",
                "expertSummary": "IDI đang ở trạng thái mẫu. Hệ thống sẽ cập nhật xu hướng, động lượng, dòng tiền, setup và rủi ro sau khi chạy Vnstock API.",
                "buyZone": "Canh quanh MA20 hoặc nền tích lũy gần nhất, không mua đuổi.",
                "stopLoss": "-7% đến -10%",
                "takeProfit": "+12% đến +25%",
                "allocation": "5% - 20%",
                "catalysts": [
                        "Vnstock API",
                        "Tiêu dùng / Nông nghiệp / Thủy sản"
                ],
                "cautions": [
                        "Đây là dữ liệu mẫu trước khi chạy API",
                        "Không dùng để giao dịch thật",
                        "Chạy workflow để cập nhật"
                ]
        },
        {
                "ticker": "ASM",
                "name": "Sao Mai Group",
                "sector": "Tiêu dùng / Nông nghiệp / Thủy sản",
                "score": 75.5,
                "subscores": {
                        "trend": 18,
                        "momentum": 12.6,
                        "moneyFlow": 15.5,
                        "setup": 11.8,
                        "risk": 7.2,
                        "relativeStrength": 10.4
                },
                "setupType": "Vượt lại MA50",
                "marketState": "Uptrend",
                "action": "CANH MUA / MUA KHI XÁC NHẬN",
                "risk": "Trung bình",
                "close": 119200,
                "rsi14": 69.2,
                "ret20": 9.1,
                "ret60": 16.8,
                "volume_status": "Mẫu",
                "volumeRatio": 1.4,
                "ma20": 117460,
                "ma50": 115720,
                "ma200": 112240,
                "macd": null,
                "macd_signal": null,
                "distanceToMA20": 0.5,
                "atr14": null,
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
                        "topOpportunity": false,
                        "breakout": false,
                        "pullbackMA20": false,
                        "moneyFlow": true,
                        "accumulation": false,
                        "safe": false
                },
                "reason": "Dữ liệu mẫu cho ASM. Chạy GitHub Actions sau khi thêm VNSTOCK_API_KEY để cập nhật tín hiệu thật.",
                "expertSummary": "ASM đang ở trạng thái mẫu. Hệ thống sẽ cập nhật xu hướng, động lượng, dòng tiền, setup và rủi ro sau khi chạy Vnstock API.",
                "buyZone": "Canh quanh MA20 hoặc nền tích lũy gần nhất, không mua đuổi.",
                "stopLoss": "-7% đến -10%",
                "takeProfit": "+12% đến +25%",
                "allocation": "5% - 20%",
                "catalysts": [
                        "Vnstock API",
                        "Tiêu dùng / Nông nghiệp / Thủy sản"
                ],
                "cautions": [
                        "Đây là dữ liệu mẫu trước khi chạy API",
                        "Không dùng để giao dịch thật",
                        "Chạy workflow để cập nhật"
                ]
        },
        {
                "ticker": "HAG",
                "name": "Hoàng Anh Gia Lai",
                "sector": "Tiêu dùng / Nông nghiệp / Thủy sản",
                "score": 81.0,
                "subscores": {
                        "trend": 20,
                        "momentum": 7.0,
                        "moneyFlow": 17.0,
                        "setup": 13.5,
                        "risk": 12.0,
                        "relativeStrength": 11.5
                },
                "setupType": "Chưa có setup rõ",
                "marketState": "Uptrend",
                "action": "CANH MUA / MUA KHI XÁC NHẬN",
                "risk": "Trung bình",
                "close": 120000,
                "rsi14": 70.9,
                "ret20": 10.0,
                "ret60": -12.0,
                "volume_status": "Mẫu",
                "volumeRatio": 1.55,
                "ma20": 118250,
                "ma50": 116500,
                "ma200": 113000,
                "macd": null,
                "macd_signal": null,
                "distanceToMA20": 1.5,
                "atr14": null,
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
                        "topOpportunity": true,
                        "breakout": false,
                        "pullbackMA20": false,
                        "moneyFlow": true,
                        "accumulation": false,
                        "safe": true
                },
                "reason": "Dữ liệu mẫu cho HAG. Chạy GitHub Actions sau khi thêm VNSTOCK_API_KEY để cập nhật tín hiệu thật.",
                "expertSummary": "HAG đang ở trạng thái mẫu. Hệ thống sẽ cập nhật xu hướng, động lượng, dòng tiền, setup và rủi ro sau khi chạy Vnstock API.",
                "buyZone": "Canh quanh MA20 hoặc nền tích lũy gần nhất, không mua đuổi.",
                "stopLoss": "-7% đến -10%",
                "takeProfit": "+12% đến +25%",
                "allocation": "5% - 20%",
                "catalysts": [
                        "Vnstock API",
                        "Tiêu dùng / Nông nghiệp / Thủy sản"
                ],
                "cautions": [
                        "Đây là dữ liệu mẫu trước khi chạy API",
                        "Không dùng để giao dịch thật",
                        "Chạy workflow để cập nhật"
                ]
        },
        {
                "ticker": "HNG",
                "name": "HAGL Agrico",
                "sector": "Tiêu dùng / Nông nghiệp / Thủy sản",
                "score": 54.8,
                "subscores": {
                        "trend": 10,
                        "momentum": 8.4,
                        "moneyFlow": 8.0,
                        "setup": 5.0,
                        "risk": 10.8,
                        "relativeStrength": 12.6
                },
                "setupType": "Pullback MA20",
                "marketState": "Trung tính",
                "action": "TRÁNH MUA MỚI",
                "risk": "Trung bình",
                "close": 120800,
                "rsi14": 42.0,
                "ret20": -8.0,
                "ret60": -10.8,
                "volume_status": "Mẫu",
                "volumeRatio": 1.7,
                "ma20": 119040,
                "ma50": 117280,
                "ma200": 113760,
                "macd": null,
                "macd_signal": null,
                "distanceToMA20": 2.5,
                "atr14": null,
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
                        "topOpportunity": false,
                        "breakout": false,
                        "pullbackMA20": true,
                        "moneyFlow": false,
                        "accumulation": false,
                        "safe": false
                },
                "reason": "Dữ liệu mẫu cho HNG. Chạy GitHub Actions sau khi thêm VNSTOCK_API_KEY để cập nhật tín hiệu thật.",
                "expertSummary": "HNG đang ở trạng thái mẫu. Hệ thống sẽ cập nhật xu hướng, động lượng, dòng tiền, setup và rủi ro sau khi chạy Vnstock API.",
                "buyZone": "Canh quanh MA20 hoặc nền tích lũy gần nhất, không mua đuổi.",
                "stopLoss": "-7% đến -10%",
                "takeProfit": "+12% đến +25%",
                "allocation": "5% - 20%",
                "catalysts": [
                        "Vnstock API",
                        "Tiêu dùng / Nông nghiệp / Thủy sản"
                ],
                "cautions": [
                        "Đây là dữ liệu mẫu trước khi chạy API",
                        "Không dùng để giao dịch thật",
                        "Chạy workflow để cập nhật"
                ]
        },
        {
                "ticker": "SBT",
                "name": "Thành Thành Công Biên Hòa",
                "sector": "Tiêu dùng / Nông nghiệp / Thủy sản",
                "score": 61.3,
                "subscores": {
                        "trend": 12,
                        "momentum": 9.8,
                        "moneyFlow": 9.5,
                        "setup": 6.7,
                        "risk": 9.6,
                        "relativeStrength": 13.7
                },
                "setupType": "Breakout 20 phiên",
                "marketState": "Tích cực",
                "action": "CHỜ THÊM",
                "risk": "Trung bình",
                "close": 121600,
                "rsi14": 43.7,
                "ret20": -7.1,
                "ret60": -9.6,
                "volume_status": "Mẫu",
                "volumeRatio": 1.85,
                "ma20": 119830,
                "ma50": 118060,
                "ma200": 114520,
                "macd": null,
                "macd_signal": null,
                "distanceToMA20": 3.5,
                "atr14": null,
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
                        "topOpportunity": false,
                        "breakout": true,
                        "pullbackMA20": false,
                        "moneyFlow": false,
                        "accumulation": false,
                        "safe": false
                },
                "reason": "Dữ liệu mẫu cho SBT. Chạy GitHub Actions sau khi thêm VNSTOCK_API_KEY để cập nhật tín hiệu thật.",
                "expertSummary": "SBT đang ở trạng thái mẫu. Hệ thống sẽ cập nhật xu hướng, động lượng, dòng tiền, setup và rủi ro sau khi chạy Vnstock API.",
                "buyZone": "Canh quanh MA20 hoặc nền tích lũy gần nhất, không mua đuổi.",
                "stopLoss": "-7% đến -10%",
                "takeProfit": "+12% đến +25%",
                "allocation": "5% - 20%",
                "catalysts": [
                        "Vnstock API",
                        "Tiêu dùng / Nông nghiệp / Thủy sản"
                ],
                "cautions": [
                        "Đây là dữ liệu mẫu trước khi chạy API",
                        "Không dùng để giao dịch thật",
                        "Chạy workflow để cập nhật"
                ]
        },
        {
                "ticker": "GMD",
                "name": "Gemadept",
                "sector": "Logistics / Cảng biển",
                "score": 59.0,
                "subscores": {
                        "trend": 14,
                        "momentum": 11.2,
                        "moneyFlow": 11.0,
                        "setup": 8.4,
                        "risk": 8.4,
                        "relativeStrength": 6.0
                },
                "setupType": "Tích lũy biên hẹp",
                "marketState": "Tích cực",
                "action": "CHỜ THÊM",
                "risk": "Trung bình",
                "close": 122400,
                "rsi14": 45.4,
                "ret20": -6.2,
                "ret60": -8.4,
                "volume_status": "Mẫu",
                "volumeRatio": 0.8,
                "ma20": 120620,
                "ma50": 118840,
                "ma200": 115280,
                "macd": null,
                "macd_signal": null,
                "distanceToMA20": 4.5,
                "atr14": null,
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
                        "topOpportunity": false,
                        "breakout": false,
                        "pullbackMA20": false,
                        "moneyFlow": false,
                        "accumulation": true,
                        "safe": false
                },
                "reason": "Dữ liệu mẫu cho GMD. Chạy GitHub Actions sau khi thêm VNSTOCK_API_KEY để cập nhật tín hiệu thật.",
                "expertSummary": "GMD đang ở trạng thái mẫu. Hệ thống sẽ cập nhật xu hướng, động lượng, dòng tiền, setup và rủi ro sau khi chạy Vnstock API.",
                "buyZone": "Canh quanh MA20 hoặc nền tích lũy gần nhất, không mua đuổi.",
                "stopLoss": "-7% đến -10%",
                "takeProfit": "+12% đến +25%",
                "allocation": "5% - 20%",
                "catalysts": [
                        "Vnstock API",
                        "Logistics / Cảng biển"
                ],
                "cautions": [
                        "Đây là dữ liệu mẫu trước khi chạy API",
                        "Không dùng để giao dịch thật",
                        "Chạy workflow để cập nhật"
                ]
        },
        {
                "ticker": "HAH",
                "name": "Hải An",
                "sector": "Logistics / Cảng biển",
                "score": 65.5,
                "subscores": {
                        "trend": 16,
                        "momentum": 12.6,
                        "moneyFlow": 12.5,
                        "setup": 10.1,
                        "risk": 7.2,
                        "relativeStrength": 7.1
                },
                "setupType": "Retest nền",
                "marketState": "Uptrend",
                "action": "THEO DÕI MUA",
                "risk": "Trung bình",
                "close": 123200,
                "rsi14": 47.1,
                "ret20": -5.3,
                "ret60": -7.2,
                "volume_status": "Mẫu",
                "volumeRatio": 0.95,
                "ma20": 121410,
                "ma50": 119620,
                "ma200": 116040,
                "macd": null,
                "macd_signal": null,
                "distanceToMA20": 5.5,
                "atr14": null,
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
                        "topOpportunity": false,
                        "breakout": false,
                        "pullbackMA20": false,
                        "moneyFlow": false,
                        "accumulation": false,
                        "safe": false
                },
                "reason": "Dữ liệu mẫu cho HAH. Chạy GitHub Actions sau khi thêm VNSTOCK_API_KEY để cập nhật tín hiệu thật.",
                "expertSummary": "HAH đang ở trạng thái mẫu. Hệ thống sẽ cập nhật xu hướng, động lượng, dòng tiền, setup và rủi ro sau khi chạy Vnstock API.",
                "buyZone": "Canh quanh MA20 hoặc nền tích lũy gần nhất, không mua đuổi.",
                "stopLoss": "-7% đến -10%",
                "takeProfit": "+12% đến +25%",
                "allocation": "5% - 20%",
                "catalysts": [
                        "Vnstock API",
                        "Logistics / Cảng biển"
                ],
                "cautions": [
                        "Đây là dữ liệu mẫu trước khi chạy API",
                        "Không dùng để giao dịch thật",
                        "Chạy workflow để cập nhật"
                ]
        },
        {
                "ticker": "VSC",
                "name": "Viconship",
                "sector": "Logistics / Cảng biển",
                "score": 71.0,
                "subscores": {
                        "trend": 18,
                        "momentum": 7.0,
                        "moneyFlow": 14.0,
                        "setup": 11.8,
                        "risk": 12.0,
                        "relativeStrength": 8.2
                },
                "setupType": "Vượt lại MA50",
                "marketState": "Uptrend",
                "action": "THEO DÕI MUA",
                "risk": "Trung bình",
                "close": 124000,
                "rsi14": 48.8,
                "ret20": -4.4,
                "ret60": -6.0,
                "volume_status": "Mẫu",
                "volumeRatio": 1.1,
                "ma20": 122200,
                "ma50": 120400,
                "ma200": 116800,
                "macd": null,
                "macd_signal": null,
                "distanceToMA20": 6.5,
                "atr14": null,
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
                        "topOpportunity": false,
                        "breakout": false,
                        "pullbackMA20": false,
                        "moneyFlow": false,
                        "accumulation": false,
                        "safe": true
                },
                "reason": "Dữ liệu mẫu cho VSC. Chạy GitHub Actions sau khi thêm VNSTOCK_API_KEY để cập nhật tín hiệu thật.",
                "expertSummary": "VSC đang ở trạng thái mẫu. Hệ thống sẽ cập nhật xu hướng, động lượng, dòng tiền, setup và rủi ro sau khi chạy Vnstock API.",
                "buyZone": "Canh quanh MA20 hoặc nền tích lũy gần nhất, không mua đuổi.",
                "stopLoss": "-7% đến -10%",
                "takeProfit": "+12% đến +25%",
                "allocation": "5% - 20%",
                "catalysts": [
                        "Vnstock API",
                        "Logistics / Cảng biển"
                ],
                "cautions": [
                        "Đây là dữ liệu mẫu trước khi chạy API",
                        "Không dùng để giao dịch thật",
                        "Chạy workflow để cập nhật"
                ]
        },
        {
                "ticker": "SGP",
                "name": "Cảng Sài Gòn",
                "sector": "Logistics / Cảng biển",
                "score": 77.5,
                "subscores": {
                        "trend": 20,
                        "momentum": 8.4,
                        "moneyFlow": 15.5,
                        "setup": 13.5,
                        "risk": 10.8,
                        "relativeStrength": 9.3
                },
                "setupType": "Chưa có setup rõ",
                "marketState": "Uptrend",
                "action": "CANH MUA / MUA KHI XÁC NHẬN",
                "risk": "Trung bình",
                "close": 124800,
                "rsi14": 50.5,
                "ret20": -3.5,
                "ret60": -4.8,
                "volume_status": "Mẫu",
                "volumeRatio": 1.25,
                "ma20": 122990,
                "ma50": 121180,
                "ma200": 117560,
                "macd": null,
                "macd_signal": null,
                "distanceToMA20": 7.5,
                "atr14": null,
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
                        "topOpportunity": false,
                        "breakout": false,
                        "pullbackMA20": false,
                        "moneyFlow": true,
                        "accumulation": false,
                        "safe": false
                },
                "reason": "Dữ liệu mẫu cho SGP. Chạy GitHub Actions sau khi thêm VNSTOCK_API_KEY để cập nhật tín hiệu thật.",
                "expertSummary": "SGP đang ở trạng thái mẫu. Hệ thống sẽ cập nhật xu hướng, động lượng, dòng tiền, setup và rủi ro sau khi chạy Vnstock API.",
                "buyZone": "Canh quanh MA20 hoặc nền tích lũy gần nhất, không mua đuổi.",
                "stopLoss": "-7% đến -10%",
                "takeProfit": "+12% đến +25%",
                "allocation": "5% - 20%",
                "catalysts": [
                        "Vnstock API",
                        "Logistics / Cảng biển"
                ],
                "cautions": [
                        "Đây là dữ liệu mẫu trước khi chạy API",
                        "Không dùng để giao dịch thật",
                        "Chạy workflow để cập nhật"
                ]
        },
        {
                "ticker": "PHP",
                "name": "Cảng Hải Phòng",
                "sector": "Logistics / Cảng biển",
                "score": 61.8,
                "subscores": {
                        "trend": 10,
                        "momentum": 9.8,
                        "moneyFlow": 17.0,
                        "setup": 5.0,
                        "risk": 9.6,
                        "relativeStrength": 10.4
                },
                "setupType": "Pullback MA20",
                "marketState": "Trung tính",
                "action": "CHỜ THÊM",
                "risk": "Trung bình",
                "close": 125600,
                "rsi14": 52.2,
                "ret20": -2.6,
                "ret60": -3.6,
                "volume_status": "Mẫu",
                "volumeRatio": 1.4,
                "ma20": 123780,
                "ma50": 121960,
                "ma200": 118320,
                "macd": null,
                "macd_signal": null,
                "distanceToMA20": -3.5,
                "atr14": null,
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
                        "topOpportunity": false,
                        "breakout": false,
                        "pullbackMA20": true,
                        "moneyFlow": true,
                        "accumulation": false,
                        "safe": false
                },
                "reason": "Dữ liệu mẫu cho PHP. Chạy GitHub Actions sau khi thêm VNSTOCK_API_KEY để cập nhật tín hiệu thật.",
                "expertSummary": "PHP đang ở trạng thái mẫu. Hệ thống sẽ cập nhật xu hướng, động lượng, dòng tiền, setup và rủi ro sau khi chạy Vnstock API.",
                "buyZone": "Canh quanh MA20 hoặc nền tích lũy gần nhất, không mua đuổi.",
                "stopLoss": "-7% đến -10%",
                "takeProfit": "+12% đến +25%",
                "allocation": "5% - 20%",
                "catalysts": [
                        "Vnstock API",
                        "Logistics / Cảng biển"
                ],
                "cautions": [
                        "Đây là dữ liệu mẫu trước khi chạy API",
                        "Không dùng để giao dịch thật",
                        "Chạy workflow để cập nhật"
                ]
        },
        {
                "ticker": "VOS",
                "name": "Vosco",
                "sector": "Logistics / Cảng biển",
                "score": 57.8,
                "subscores": {
                        "trend": 12,
                        "momentum": 11.2,
                        "moneyFlow": 8.0,
                        "setup": 6.7,
                        "risk": 8.4,
                        "relativeStrength": 11.5
                },
                "setupType": "Breakout 20 phiên",
                "marketState": "Tích cực",
                "action": "CHỜ THÊM",
                "risk": "Trung bình",
                "close": 126400,
                "rsi14": 53.9,
                "ret20": -1.7,
                "ret60": -2.4,
                "volume_status": "Mẫu",
                "volumeRatio": 1.55,
                "ma20": 124570,
                "ma50": 122740,
                "ma200": 119080,
                "macd": null,
                "macd_signal": null,
                "distanceToMA20": -2.5,
                "atr14": null,
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
                        "topOpportunity": false,
                        "breakout": true,
                        "pullbackMA20": false,
                        "moneyFlow": false,
                        "accumulation": false,
                        "safe": false
                },
                "reason": "Dữ liệu mẫu cho VOS. Chạy GitHub Actions sau khi thêm VNSTOCK_API_KEY để cập nhật tín hiệu thật.",
                "expertSummary": "VOS đang ở trạng thái mẫu. Hệ thống sẽ cập nhật xu hướng, động lượng, dòng tiền, setup và rủi ro sau khi chạy Vnstock API.",
                "buyZone": "Canh quanh MA20 hoặc nền tích lũy gần nhất, không mua đuổi.",
                "stopLoss": "-7% đến -10%",
                "takeProfit": "+12% đến +25%",
                "allocation": "5% - 20%",
                "catalysts": [
                        "Vnstock API",
                        "Logistics / Cảng biển"
                ],
                "cautions": [
                        "Đây là dữ liệu mẫu trước khi chạy API",
                        "Không dùng để giao dịch thật",
                        "Chạy workflow để cập nhật"
                ]
        },
        {
                "ticker": "VTO",
                "name": "VITACO",
                "sector": "Logistics / Cảng biển",
                "score": 64.3,
                "subscores": {
                        "trend": 14,
                        "momentum": 12.6,
                        "moneyFlow": 9.5,
                        "setup": 8.4,
                        "risk": 7.2,
                        "relativeStrength": 12.6
                },
                "setupType": "Tích lũy biên hẹp",
                "marketState": "Tích cực",
                "action": "CHỜ THÊM",
                "risk": "Trung bình",
                "close": 127200,
                "rsi14": 55.6,
                "ret20": -0.8,
                "ret60": -1.2,
                "volume_status": "Mẫu",
                "volumeRatio": 1.7,
                "ma20": 125360,
                "ma50": 123520,
                "ma200": 119840,
                "macd": null,
                "macd_signal": null,
                "distanceToMA20": -1.5,
                "atr14": null,
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
                        "topOpportunity": false,
                        "breakout": false,
                        "pullbackMA20": false,
                        "moneyFlow": false,
                        "accumulation": true,
                        "safe": false
                },
                "reason": "Dữ liệu mẫu cho VTO. Chạy GitHub Actions sau khi thêm VNSTOCK_API_KEY để cập nhật tín hiệu thật.",
                "expertSummary": "VTO đang ở trạng thái mẫu. Hệ thống sẽ cập nhật xu hướng, động lượng, dòng tiền, setup và rủi ro sau khi chạy Vnstock API.",
                "buyZone": "Canh quanh MA20 hoặc nền tích lũy gần nhất, không mua đuổi.",
                "stopLoss": "-7% đến -10%",
                "takeProfit": "+12% đến +25%",
                "allocation": "5% - 20%",
                "catalysts": [
                        "Vnstock API",
                        "Logistics / Cảng biển"
                ],
                "cautions": [
                        "Đây là dữ liệu mẫu trước khi chạy API",
                        "Không dùng để giao dịch thật",
                        "Chạy workflow để cập nhật"
                ]
        },
        {
                "ticker": "SKG",
                "name": "Superdong",
                "sector": "Logistics / Cảng biển",
                "score": 69.8,
                "subscores": {
                        "trend": 16,
                        "momentum": 7.0,
                        "moneyFlow": 11.0,
                        "setup": 10.1,
                        "risk": 12.0,
                        "relativeStrength": 13.7
                },
                "setupType": "Retest nền",
                "marketState": "Uptrend",
                "action": "THEO DÕI MUA",
                "risk": "Trung bình",
                "close": 128000,
                "rsi14": 57.3,
                "ret20": 0.1,
                "ret60": 0.0,
                "volume_status": "Mẫu",
                "volumeRatio": 1.85,
                "ma20": 126150,
                "ma50": 124300,
                "ma200": 120600,
                "macd": null,
                "macd_signal": null,
                "distanceToMA20": -0.5,
                "atr14": null,
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
                        "topOpportunity": false,
                        "breakout": false,
                        "pullbackMA20": false,
                        "moneyFlow": false,
                        "accumulation": false,
                        "safe": true
                },
                "reason": "Dữ liệu mẫu cho SKG. Chạy GitHub Actions sau khi thêm VNSTOCK_API_KEY để cập nhật tín hiệu thật.",
                "expertSummary": "SKG đang ở trạng thái mẫu. Hệ thống sẽ cập nhật xu hướng, động lượng, dòng tiền, setup và rủi ro sau khi chạy Vnstock API.",
                "buyZone": "Canh quanh MA20 hoặc nền tích lũy gần nhất, không mua đuổi.",
                "stopLoss": "-7% đến -10%",
                "takeProfit": "+12% đến +25%",
                "allocation": "5% - 20%",
                "catalysts": [
                        "Vnstock API",
                        "Logistics / Cảng biển"
                ],
                "cautions": [
                        "Đây là dữ liệu mẫu trước khi chạy API",
                        "Không dùng để giao dịch thật",
                        "Chạy workflow để cập nhật"
                ]
        },
        {
                "ticker": "VJC",
                "name": "Vietjet Air",
                "sector": "Hàng không / Dịch vụ sân bay",
                "score": 67.5,
                "subscores": {
                        "trend": 18,
                        "momentum": 8.4,
                        "moneyFlow": 12.5,
                        "setup": 11.8,
                        "risk": 10.8,
                        "relativeStrength": 6.0
                },
                "setupType": "Vượt lại MA50",
                "marketState": "Uptrend",
                "action": "THEO DÕI MUA",
                "risk": "Trung bình",
                "close": 128800,
                "rsi14": 59.0,
                "ret20": 1.0,
                "ret60": 1.2,
                "volume_status": "Mẫu",
                "volumeRatio": 0.8,
                "ma20": 126940,
                "ma50": 125080,
                "ma200": 121360,
                "macd": null,
                "macd_signal": null,
                "distanceToMA20": 0.5,
                "atr14": null,
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
                        "topOpportunity": false,
                        "breakout": false,
                        "pullbackMA20": false,
                        "moneyFlow": false,
                        "accumulation": false,
                        "safe": false
                },
                "reason": "Dữ liệu mẫu cho VJC. Chạy GitHub Actions sau khi thêm VNSTOCK_API_KEY để cập nhật tín hiệu thật.",
                "expertSummary": "VJC đang ở trạng thái mẫu. Hệ thống sẽ cập nhật xu hướng, động lượng, dòng tiền, setup và rủi ro sau khi chạy Vnstock API.",
                "buyZone": "Canh quanh MA20 hoặc nền tích lũy gần nhất, không mua đuổi.",
                "stopLoss": "-7% đến -10%",
                "takeProfit": "+12% đến +25%",
                "allocation": "5% - 20%",
                "catalysts": [
                        "Vnstock API",
                        "Hàng không / Dịch vụ sân bay"
                ],
                "cautions": [
                        "Đây là dữ liệu mẫu trước khi chạy API",
                        "Không dùng để giao dịch thật",
                        "Chạy workflow để cập nhật"
                ]
        },
        {
                "ticker": "HVN",
                "name": "Vietnam Airlines",
                "sector": "Hàng không / Dịch vụ sân bay",
                "score": 74.0,
                "subscores": {
                        "trend": 20,
                        "momentum": 9.8,
                        "moneyFlow": 14.0,
                        "setup": 13.5,
                        "risk": 9.6,
                        "relativeStrength": 7.1
                },
                "setupType": "Chưa có setup rõ",
                "marketState": "Uptrend",
                "action": "CANH MUA / MUA KHI XÁC NHẬN",
                "risk": "Trung bình",
                "close": 129600,
                "rsi14": 60.7,
                "ret20": 1.9,
                "ret60": 2.4,
                "volume_status": "Mẫu",
                "volumeRatio": 0.95,
                "ma20": 127730,
                "ma50": 125860,
                "ma200": 122120,
                "macd": null,
                "macd_signal": null,
                "distanceToMA20": 1.5,
                "atr14": null,
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
                        "topOpportunity": false,
                        "breakout": false,
                        "pullbackMA20": false,
                        "moneyFlow": false,
                        "accumulation": false,
                        "safe": false
                },
                "reason": "Dữ liệu mẫu cho HVN. Chạy GitHub Actions sau khi thêm VNSTOCK_API_KEY để cập nhật tín hiệu thật.",
                "expertSummary": "HVN đang ở trạng thái mẫu. Hệ thống sẽ cập nhật xu hướng, động lượng, dòng tiền, setup và rủi ro sau khi chạy Vnstock API.",
                "buyZone": "Canh quanh MA20 hoặc nền tích lũy gần nhất, không mua đuổi.",
                "stopLoss": "-7% đến -10%",
                "takeProfit": "+12% đến +25%",
                "allocation": "5% - 20%",
                "catalysts": [
                        "Vnstock API",
                        "Hàng không / Dịch vụ sân bay"
                ],
                "cautions": [
                        "Đây là dữ liệu mẫu trước khi chạy API",
                        "Không dùng để giao dịch thật",
                        "Chạy workflow để cập nhật"
                ]
        },
        {
                "ticker": "ACV",
                "name": "Tổng công ty Cảng HKVN",
                "sector": "Hàng không / Dịch vụ sân bay",
                "score": 58.3,
                "subscores": {
                        "trend": 10,
                        "momentum": 11.2,
                        "moneyFlow": 15.5,
                        "setup": 5.0,
                        "risk": 8.4,
                        "relativeStrength": 8.2
                },
                "setupType": "Pullback MA20",
                "marketState": "Trung tính",
                "action": "CHỜ THÊM",
                "risk": "Trung bình",
                "close": 130400,
                "rsi14": 62.4,
                "ret20": 2.8,
                "ret60": 3.6,
                "volume_status": "Mẫu",
                "volumeRatio": 1.1,
                "ma20": 128520,
                "ma50": 126640,
                "ma200": 122880,
                "macd": null,
                "macd_signal": null,
                "distanceToMA20": 2.5,
                "atr14": null,
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
                        "topOpportunity": false,
                        "breakout": false,
                        "pullbackMA20": true,
                        "moneyFlow": true,
                        "accumulation": false,
                        "safe": false
                },
                "reason": "Dữ liệu mẫu cho ACV. Chạy GitHub Actions sau khi thêm VNSTOCK_API_KEY để cập nhật tín hiệu thật.",
                "expertSummary": "ACV đang ở trạng thái mẫu. Hệ thống sẽ cập nhật xu hướng, động lượng, dòng tiền, setup và rủi ro sau khi chạy Vnstock API.",
                "buyZone": "Canh quanh MA20 hoặc nền tích lũy gần nhất, không mua đuổi.",
                "stopLoss": "-7% đến -10%",
                "takeProfit": "+12% đến +25%",
                "allocation": "5% - 20%",
                "catalysts": [
                        "Vnstock API",
                        "Hàng không / Dịch vụ sân bay"
                ],
                "cautions": [
                        "Đây là dữ liệu mẫu trước khi chạy API",
                        "Không dùng để giao dịch thật",
                        "Chạy workflow để cập nhật"
                ]
        },
        {
                "ticker": "SCS",
                "name": "SCSC",
                "sector": "Hàng không / Dịch vụ sân bay",
                "score": 64.8,
                "subscores": {
                        "trend": 12,
                        "momentum": 12.6,
                        "moneyFlow": 17.0,
                        "setup": 6.7,
                        "risk": 7.2,
                        "relativeStrength": 9.3
                },
                "setupType": "Breakout 20 phiên",
                "marketState": "Tích cực",
                "action": "CHỜ THÊM",
                "risk": "Trung bình",
                "close": 131200,
                "rsi14": 64.1,
                "ret20": 3.7,
                "ret60": 4.8,
                "volume_status": "Mẫu",
                "volumeRatio": 1.25,
                "ma20": 129310,
                "ma50": 127420,
                "ma200": 123640,
                "macd": null,
                "macd_signal": null,
                "distanceToMA20": 3.5,
                "atr14": null,
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
                        "topOpportunity": false,
                        "breakout": true,
                        "pullbackMA20": false,
                        "moneyFlow": true,
                        "accumulation": false,
                        "safe": false
                },
                "reason": "Dữ liệu mẫu cho SCS. Chạy GitHub Actions sau khi thêm VNSTOCK_API_KEY để cập nhật tín hiệu thật.",
                "expertSummary": "SCS đang ở trạng thái mẫu. Hệ thống sẽ cập nhật xu hướng, động lượng, dòng tiền, setup và rủi ro sau khi chạy Vnstock API.",
                "buyZone": "Canh quanh MA20 hoặc nền tích lũy gần nhất, không mua đuổi.",
                "stopLoss": "-7% đến -10%",
                "takeProfit": "+12% đến +25%",
                "allocation": "5% - 20%",
                "catalysts": [
                        "Vnstock API",
                        "Hàng không / Dịch vụ sân bay"
                ],
                "cautions": [
                        "Đây là dữ liệu mẫu trước khi chạy API",
                        "Không dùng để giao dịch thật",
                        "Chạy workflow để cập nhật"
                ]
        },
        {
                "ticker": "NCT",
                "name": "Nội Bài Cargo",
                "sector": "Hàng không / Dịch vụ sân bay",
                "score": 59.8,
                "subscores": {
                        "trend": 14,
                        "momentum": 7.0,
                        "moneyFlow": 8.0,
                        "setup": 8.4,
                        "risk": 12.0,
                        "relativeStrength": 10.4
                },
                "setupType": "Tích lũy biên hẹp",
                "marketState": "Tích cực",
                "action": "CHỜ THÊM",
                "risk": "Trung bình",
                "close": 132000,
                "rsi14": 65.8,
                "ret20": 4.6,
                "ret60": 6.0,
                "volume_status": "Mẫu",
                "volumeRatio": 1.4,
                "ma20": 130100,
                "ma50": 128200,
                "ma200": 124400,
                "macd": null,
                "macd_signal": null,
                "distanceToMA20": 4.5,
                "atr14": null,
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
                        "topOpportunity": false,
                        "breakout": false,
                        "pullbackMA20": false,
                        "moneyFlow": false,
                        "accumulation": true,
                        "safe": false
                },
                "reason": "Dữ liệu mẫu cho NCT. Chạy GitHub Actions sau khi thêm VNSTOCK_API_KEY để cập nhật tín hiệu thật.",
                "expertSummary": "NCT đang ở trạng thái mẫu. Hệ thống sẽ cập nhật xu hướng, động lượng, dòng tiền, setup và rủi ro sau khi chạy Vnstock API.",
                "buyZone": "Canh quanh MA20 hoặc nền tích lũy gần nhất, không mua đuổi.",
                "stopLoss": "-7% đến -10%",
                "takeProfit": "+12% đến +25%",
                "allocation": "5% - 20%",
                "catalysts": [
                        "Vnstock API",
                        "Hàng không / Dịch vụ sân bay"
                ],
                "cautions": [
                        "Đây là dữ liệu mẫu trước khi chạy API",
                        "Không dùng để giao dịch thật",
                        "Chạy workflow để cập nhật"
                ]
        },
        {
                "ticker": "SAS",
                "name": "Dịch vụ Hàng không Tân Sơn Nhất",
                "sector": "Hàng không / Dịch vụ sân bay",
                "score": 66.3,
                "subscores": {
                        "trend": 16,
                        "momentum": 8.4,
                        "moneyFlow": 9.5,
                        "setup": 10.1,
                        "risk": 10.8,
                        "relativeStrength": 11.5
                },
                "setupType": "Retest nền",
                "marketState": "Uptrend",
                "action": "THEO DÕI MUA",
                "risk": "Trung bình",
                "close": 132800,
                "rsi14": 67.5,
                "ret20": 5.5,
                "ret60": 7.2,
                "volume_status": "Mẫu",
                "volumeRatio": 1.55,
                "ma20": 130890,
                "ma50": 128980,
                "ma200": 125160,
                "macd": null,
                "macd_signal": null,
                "distanceToMA20": 5.5,
                "atr14": null,
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
                        "topOpportunity": false,
                        "breakout": false,
                        "pullbackMA20": false,
                        "moneyFlow": false,
                        "accumulation": false,
                        "safe": false
                },
                "reason": "Dữ liệu mẫu cho SAS. Chạy GitHub Actions sau khi thêm VNSTOCK_API_KEY để cập nhật tín hiệu thật.",
                "expertSummary": "SAS đang ở trạng thái mẫu. Hệ thống sẽ cập nhật xu hướng, động lượng, dòng tiền, setup và rủi ro sau khi chạy Vnstock API.",
                "buyZone": "Canh quanh MA20 hoặc nền tích lũy gần nhất, không mua đuổi.",
                "stopLoss": "-7% đến -10%",
                "takeProfit": "+12% đến +25%",
                "allocation": "5% - 20%",
                "catalysts": [
                        "Vnstock API",
                        "Hàng không / Dịch vụ sân bay"
                ],
                "cautions": [
                        "Đây là dữ liệu mẫu trước khi chạy API",
                        "Không dùng để giao dịch thật",
                        "Chạy workflow để cập nhật"
                ]
        },
        {
                "ticker": "CIA",
                "name": "Cam Ranh Airport Services",
                "sector": "Hàng không / Dịch vụ sân bay",
                "score": 72.8,
                "subscores": {
                        "trend": 18,
                        "momentum": 9.8,
                        "moneyFlow": 11.0,
                        "setup": 11.8,
                        "risk": 9.6,
                        "relativeStrength": 12.6
                },
                "setupType": "Vượt lại MA50",
                "marketState": "Uptrend",
                "action": "THEO DÕI MUA",
                "risk": "Trung bình",
                "close": 133600,
                "rsi14": 69.2,
                "ret20": 6.4,
                "ret60": 8.4,
                "volume_status": "Mẫu",
                "volumeRatio": 1.7,
                "ma20": 131680,
                "ma50": 129760,
                "ma200": 125920,
                "macd": null,
                "macd_signal": null,
                "distanceToMA20": 6.5,
                "atr14": null,
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
                        "topOpportunity": false,
                        "breakout": false,
                        "pullbackMA20": false,
                        "moneyFlow": false,
                        "accumulation": false,
                        "safe": false
                },
                "reason": "Dữ liệu mẫu cho CIA. Chạy GitHub Actions sau khi thêm VNSTOCK_API_KEY để cập nhật tín hiệu thật.",
                "expertSummary": "CIA đang ở trạng thái mẫu. Hệ thống sẽ cập nhật xu hướng, động lượng, dòng tiền, setup và rủi ro sau khi chạy Vnstock API.",
                "buyZone": "Canh quanh MA20 hoặc nền tích lũy gần nhất, không mua đuổi.",
                "stopLoss": "-7% đến -10%",
                "takeProfit": "+12% đến +25%",
                "allocation": "5% - 20%",
                "catalysts": [
                        "Vnstock API",
                        "Hàng không / Dịch vụ sân bay"
                ],
                "cautions": [
                        "Đây là dữ liệu mẫu trước khi chạy API",
                        "Không dùng để giao dịch thật",
                        "Chạy workflow để cập nhật"
                ]
        },
        {
                "ticker": "REE",
                "name": "REE Corp",
                "sector": "Điện / Hạ tầng",
                "score": 79.3,
                "subscores": {
                        "trend": 20,
                        "momentum": 11.2,
                        "moneyFlow": 12.5,
                        "setup": 13.5,
                        "risk": 8.4,
                        "relativeStrength": 13.7
                },
                "setupType": "Chưa có setup rõ",
                "marketState": "Uptrend",
                "action": "CANH MUA / MUA KHI XÁC NHẬN",
                "risk": "Trung bình",
                "close": 134400,
                "rsi14": 70.9,
                "ret20": 7.3,
                "ret60": 9.6,
                "volume_status": "Mẫu",
                "volumeRatio": 1.85,
                "ma20": 132470,
                "ma50": 130540,
                "ma200": 126680,
                "macd": null,
                "macd_signal": null,
                "distanceToMA20": 7.5,
                "atr14": null,
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
                        "topOpportunity": false,
                        "breakout": false,
                        "pullbackMA20": false,
                        "moneyFlow": false,
                        "accumulation": false,
                        "safe": false
                },
                "reason": "Dữ liệu mẫu cho REE. Chạy GitHub Actions sau khi thêm VNSTOCK_API_KEY để cập nhật tín hiệu thật.",
                "expertSummary": "REE đang ở trạng thái mẫu. Hệ thống sẽ cập nhật xu hướng, động lượng, dòng tiền, setup và rủi ro sau khi chạy Vnstock API.",
                "buyZone": "Canh quanh MA20 hoặc nền tích lũy gần nhất, không mua đuổi.",
                "stopLoss": "-7% đến -10%",
                "takeProfit": "+12% đến +25%",
                "allocation": "5% - 20%",
                "catalysts": [
                        "Vnstock API",
                        "Điện / Hạ tầng"
                ],
                "cautions": [
                        "Đây là dữ liệu mẫu trước khi chạy API",
                        "Không dùng để giao dịch thật",
                        "Chạy workflow để cập nhật"
                ]
        },
        {
                "ticker": "PC1",
                "name": "PC1 Group",
                "sector": "Điện / Hạ tầng",
                "score": 54.8,
                "subscores": {
                        "trend": 10,
                        "momentum": 12.6,
                        "moneyFlow": 14.0,
                        "setup": 5.0,
                        "risk": 7.2,
                        "relativeStrength": 6.0
                },
                "setupType": "Pullback MA20",
                "marketState": "Trung tính",
                "action": "TRÁNH MUA MỚI",
                "risk": "Trung bình",
                "close": 135200,
                "rsi14": 42.0,
                "ret20": 8.2,
                "ret60": 10.8,
                "volume_status": "Mẫu",
                "volumeRatio": 0.8,
                "ma20": 133260,
                "ma50": 131320,
                "ma200": 127440,
                "macd": null,
                "macd_signal": null,
                "distanceToMA20": -3.5,
                "atr14": null,
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
                        "topOpportunity": false,
                        "breakout": false,
                        "pullbackMA20": true,
                        "moneyFlow": false,
                        "accumulation": false,
                        "safe": false
                },
                "reason": "Dữ liệu mẫu cho PC1. Chạy GitHub Actions sau khi thêm VNSTOCK_API_KEY để cập nhật tín hiệu thật.",
                "expertSummary": "PC1 đang ở trạng thái mẫu. Hệ thống sẽ cập nhật xu hướng, động lượng, dòng tiền, setup và rủi ro sau khi chạy Vnstock API.",
                "buyZone": "Canh quanh MA20 hoặc nền tích lũy gần nhất, không mua đuổi.",
                "stopLoss": "-7% đến -10%",
                "takeProfit": "+12% đến +25%",
                "allocation": "5% - 20%",
                "catalysts": [
                        "Vnstock API",
                        "Điện / Hạ tầng"
                ],
                "cautions": [
                        "Đây là dữ liệu mẫu trước khi chạy API",
                        "Không dùng để giao dịch thật",
                        "Chạy workflow để cập nhật"
                ]
        },
        {
                "ticker": "GEX",
                "name": "Gelex",
                "sector": "Điện / Hạ tầng",
                "score": 60.3,
                "subscores": {
                        "trend": 12,
                        "momentum": 7.0,
                        "moneyFlow": 15.5,
                        "setup": 6.7,
                        "risk": 12.0,
                        "relativeStrength": 7.1
                },
                "setupType": "Breakout 20 phiên",
                "marketState": "Tích cực",
                "action": "CHỜ THÊM",
                "risk": "Trung bình",
                "close": 136000,
                "rsi14": 43.7,
                "ret20": 9.1,
                "ret60": 12.0,
                "volume_status": "Mẫu",
                "volumeRatio": 0.95,
                "ma20": 134050,
                "ma50": 132100,
                "ma200": 128200,
                "macd": null,
                "macd_signal": null,
                "distanceToMA20": -2.5,
                "atr14": null,
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
                        "topOpportunity": false,
                        "breakout": true,
                        "pullbackMA20": false,
                        "moneyFlow": true,
                        "accumulation": false,
                        "safe": false
                },
                "reason": "Dữ liệu mẫu cho GEX. Chạy GitHub Actions sau khi thêm VNSTOCK_API_KEY để cập nhật tín hiệu thật.",
                "expertSummary": "GEX đang ở trạng thái mẫu. Hệ thống sẽ cập nhật xu hướng, động lượng, dòng tiền, setup và rủi ro sau khi chạy Vnstock API.",
                "buyZone": "Canh quanh MA20 hoặc nền tích lũy gần nhất, không mua đuổi.",
                "stopLoss": "-7% đến -10%",
                "takeProfit": "+12% đến +25%",
                "allocation": "5% - 20%",
                "catalysts": [
                        "Vnstock API",
                        "Điện / Hạ tầng"
                ],
                "cautions": [
                        "Đây là dữ liệu mẫu trước khi chạy API",
                        "Không dùng để giao dịch thật",
                        "Chạy workflow để cập nhật"
                ]
        },
        {
                "ticker": "POW",
                "name": "PV Power",
                "sector": "Điện / Hạ tầng",
                "score": 66.8,
                "subscores": {
                        "trend": 14,
                        "momentum": 8.4,
                        "moneyFlow": 17.0,
                        "setup": 8.4,
                        "risk": 10.8,
                        "relativeStrength": 8.2
                },
                "setupType": "Tích lũy biên hẹp",
                "marketState": "Tích cực",
                "action": "THEO DÕI MUA",
                "risk": "Trung bình",
                "close": 136800,
                "rsi14": 45.4,
                "ret20": 10.0,
                "ret60": 13.2,
                "volume_status": "Mẫu",
                "volumeRatio": 1.1,
                "ma20": 134840,
                "ma50": 132880,
                "ma200": 128960,
                "macd": null,
                "macd_signal": null,
                "distanceToMA20": -1.5,
                "atr14": null,
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
                        "topOpportunity": false,
                        "breakout": false,
                        "pullbackMA20": false,
                        "moneyFlow": true,
                        "accumulation": true,
                        "safe": false
                },
                "reason": "Dữ liệu mẫu cho POW. Chạy GitHub Actions sau khi thêm VNSTOCK_API_KEY để cập nhật tín hiệu thật.",
                "expertSummary": "POW đang ở trạng thái mẫu. Hệ thống sẽ cập nhật xu hướng, động lượng, dòng tiền, setup và rủi ro sau khi chạy Vnstock API.",
                "buyZone": "Canh quanh MA20 hoặc nền tích lũy gần nhất, không mua đuổi.",
                "stopLoss": "-7% đến -10%",
                "takeProfit": "+12% đến +25%",
                "allocation": "5% - 20%",
                "catalysts": [
                        "Vnstock API",
                        "Điện / Hạ tầng"
                ],
                "cautions": [
                        "Đây là dữ liệu mẫu trước khi chạy API",
                        "Không dùng để giao dịch thật",
                        "Chạy workflow để cập nhật"
                ]
        },
        {
                "ticker": "NT2",
                "name": "Nhiệt điện Nhơn Trạch 2",
                "sector": "Điện / Hạ tầng",
                "score": 62.8,
                "subscores": {
                        "trend": 16,
                        "momentum": 9.8,
                        "moneyFlow": 8.0,
                        "setup": 10.1,
                        "risk": 9.6,
                        "relativeStrength": 9.3
                },
                "setupType": "Retest nền",
                "marketState": "Uptrend",
                "action": "CHỜ THÊM",
                "risk": "Trung bình",
                "close": 137600,
                "rsi14": 47.1,
                "ret20": -8.0,
                "ret60": 14.4,
                "volume_status": "Mẫu",
                "volumeRatio": 1.25,
                "ma20": 135630,
                "ma50": 133660,
                "ma200": 129720,
                "macd": null,
                "macd_signal": null,
                "distanceToMA20": -0.5,
                "atr14": null,
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
                        "topOpportunity": false,
                        "breakout": false,
                        "pullbackMA20": false,
                        "moneyFlow": false,
                        "accumulation": false,
                        "safe": false
                },
                "reason": "Dữ liệu mẫu cho NT2. Chạy GitHub Actions sau khi thêm VNSTOCK_API_KEY để cập nhật tín hiệu thật.",
                "expertSummary": "NT2 đang ở trạng thái mẫu. Hệ thống sẽ cập nhật xu hướng, động lượng, dòng tiền, setup và rủi ro sau khi chạy Vnstock API.",
                "buyZone": "Canh quanh MA20 hoặc nền tích lũy gần nhất, không mua đuổi.",
                "stopLoss": "-7% đến -10%",
                "takeProfit": "+12% đến +25%",
                "allocation": "5% - 20%",
                "catalysts": [
                        "Vnstock API",
                        "Điện / Hạ tầng"
                ],
                "cautions": [
                        "Đây là dữ liệu mẫu trước khi chạy API",
                        "Không dùng để giao dịch thật",
                        "Chạy workflow để cập nhật"
                ]
        },
        {
                "ticker": "QTP",
                "name": "Nhiệt điện Quảng Ninh",
                "sector": "Điện / Hạ tầng",
                "score": 69.3,
                "subscores": {
                        "trend": 18,
                        "momentum": 11.2,
                        "moneyFlow": 9.5,
                        "setup": 11.8,
                        "risk": 8.4,
                        "relativeStrength": 10.4
                },
                "setupType": "Vượt lại MA50",
                "marketState": "Uptrend",
                "action": "THEO DÕI MUA",
                "risk": "Trung bình",
                "close": 138400,
                "rsi14": 48.8,
                "ret20": -7.1,
                "ret60": 15.6,
                "volume_status": "Mẫu",
                "volumeRatio": 1.4,
                "ma20": 136420,
                "ma50": 134440,
                "ma200": 130480,
                "macd": null,
                "macd_signal": null,
                "distanceToMA20": 0.5,
                "atr14": null,
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
                        "topOpportunity": false,
                        "breakout": false,
                        "pullbackMA20": false,
                        "moneyFlow": false,
                        "accumulation": false,
                        "safe": false
                },
                "reason": "Dữ liệu mẫu cho QTP. Chạy GitHub Actions sau khi thêm VNSTOCK_API_KEY để cập nhật tín hiệu thật.",
                "expertSummary": "QTP đang ở trạng thái mẫu. Hệ thống sẽ cập nhật xu hướng, động lượng, dòng tiền, setup và rủi ro sau khi chạy Vnstock API.",
                "buyZone": "Canh quanh MA20 hoặc nền tích lũy gần nhất, không mua đuổi.",
                "stopLoss": "-7% đến -10%",
                "takeProfit": "+12% đến +25%",
                "allocation": "5% - 20%",
                "catalysts": [
                        "Vnstock API",
                        "Điện / Hạ tầng"
                ],
                "cautions": [
                        "Đây là dữ liệu mẫu trước khi chạy API",
                        "Không dùng để giao dịch thật",
                        "Chạy workflow để cập nhật"
                ]
        },
        {
                "ticker": "PPC",
                "name": "Nhiệt điện Phả Lại",
                "sector": "Điện / Hạ tầng",
                "score": 75.8,
                "subscores": {
                        "trend": 20,
                        "momentum": 12.6,
                        "moneyFlow": 11.0,
                        "setup": 13.5,
                        "risk": 7.2,
                        "relativeStrength": 11.5
                },
                "setupType": "Chưa có setup rõ",
                "marketState": "Uptrend",
                "action": "CANH MUA / MUA KHI XÁC NHẬN",
                "risk": "Trung bình",
                "close": 139200,
                "rsi14": 50.5,
                "ret20": -6.2,
                "ret60": 16.8,
                "volume_status": "Mẫu",
                "volumeRatio": 1.55,
                "ma20": 137210,
                "ma50": 135220,
                "ma200": 131240,
                "macd": null,
                "macd_signal": null,
                "distanceToMA20": 1.5,
                "atr14": null,
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
                        "topOpportunity": false,
                        "breakout": false,
                        "pullbackMA20": false,
                        "moneyFlow": false,
                        "accumulation": false,
                        "safe": false
                },
                "reason": "Dữ liệu mẫu cho PPC. Chạy GitHub Actions sau khi thêm VNSTOCK_API_KEY để cập nhật tín hiệu thật.",
                "expertSummary": "PPC đang ở trạng thái mẫu. Hệ thống sẽ cập nhật xu hướng, động lượng, dòng tiền, setup và rủi ro sau khi chạy Vnstock API.",
                "buyZone": "Canh quanh MA20 hoặc nền tích lũy gần nhất, không mua đuổi.",
                "stopLoss": "-7% đến -10%",
                "takeProfit": "+12% đến +25%",
                "allocation": "5% - 20%",
                "catalysts": [
                        "Vnstock API",
                        "Điện / Hạ tầng"
                ],
                "cautions": [
                        "Đây là dữ liệu mẫu trước khi chạy API",
                        "Không dùng để giao dịch thật",
                        "Chạy workflow để cập nhật"
                ]
        }
]
    return {
        "meta": {
            "updated_at": datetime.now(VN_TZ).strftime("%Y-%m-%d %H:%M:%S VN"),
            "source": "fallback sample pro signals",
            "has_api_key": bool(VNSTOCK_API_KEY),
            "success": 0,
            "universe": len(WATCHLIST),
            "note": "Vnstock API lỗi nên dùng dữ liệu mẫu. Xem errors để sửa.",
            "activation_logs": activation_logs,
            "errors": errors,
        },
        "stocks": stocks,
    }

def main():
    activation_logs = try_activate_key()
    print("Activation logs:", activation_logs)

    histories = {}
    errors = {}

    # Lấy dữ liệu VN-Index nếu nguồn hỗ trợ. Nếu lỗi, relative strength vẫn chạy theo ret20/ret60.
    market_ret20 = None
    market_ret60 = None
    try:
        market_df, _ = fetch_history("VNINDEX")
        if len(market_df) > 61:
            market_ret20 = round((market_df.iloc[-1]["close"] / market_df.iloc[-21]["close"] - 1) * 100, 2)
            market_ret60 = round((market_df.iloc[-1]["close"] / market_df.iloc[-61]["close"] - 1) * 100, 2)
    except Exception as exc:
        print("WARN VNINDEX:", exc)

    # Fetch histories trước để tính trung bình ngành.
    for symbol in WATCHLIST:
        try:
            df, src = fetch_history(symbol)
            histories[symbol] = (df, src)
            print(f"FETCH OK {symbol} via {src}")
        except Exception as exc:
            errors[symbol] = str(exc)
            print(f"FETCH ERROR {symbol}: {exc}")

    sector_returns = {}
    for symbol, (df, _) in histories.items():
        sector = SECTORS.get(symbol, "Khác")
        if len(df) > 21:
            ret = round((df.iloc[-1]["close"] / df.iloc[-21]["close"] - 1) * 100, 2)
            sector_returns.setdefault(sector, []).append(ret)
    sector_avg = {k: sum(v)/len(v) for k, v in sector_returns.items() if v}

    results = []
    for symbol, (df, src) in histories.items():
        try:
            sec = SECTORS.get(symbol, "Khác")
            item = score_stock(symbol, df, src, market_ret20, market_ret60, sector_avg.get(sec))
            results.append(item)
            print(f"OK {symbol}: {item['score']} setup={item['setupType']}")
        except Exception as exc:
            errors[symbol] = f"score error: {exc}"
            print(f"SCORE ERROR {symbol}: {exc}")

    if results:
        results = sorted(results, key=lambda x: x.get("score", 0), reverse=True)
        data = {
            "meta": {
                "updated_at": datetime.now(VN_TZ).strftime("%Y-%m-%d %H:%M:%S VN"),
                "source": "Vnstock API pro signals",
                "has_api_key": bool(VNSTOCK_API_KEY),
                "success": len(results),
                "universe": len(WATCHLIST),
                "market_ret20": market_ret20,
                "market_ret60": market_ret60,
                "note": "Bộ lọc nâng cấp: trend, momentum, money flow, setup, risk, relative strength.",
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
