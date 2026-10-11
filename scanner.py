"""Công cụ quét cổ phiếu Việt Nam theo hệ thống 5 trụ cột (Khỏe / Yếu).
Chạy tự động bằng GitHub Actions. Kết quả ghi vào thư mục reports/.
Chỉ mang tính tham khảo kỹ thuật, không phải khuyến nghị đầu tư.

Điểm tối đa 100 = Trụ cột 1 (25) + Trụ cột 2 (25) + Trụ cột 3 (30) + Trụ cột 4 (20).
Trụ cột 5 (cơ bản) và Buy Active % được lấy cho nhóm top đầu để xác nhận thêm.
"""
import os
import time
import json
import importlib.util
import urllib.request
from datetime import datetime, timedelta, timezone

import numpy as np
import pandas as pd

VN_TZ = timezone(timedelta(hours=7))
SLEEP_BETWEEN = 0.4        # giây nghỉ giữa các mã khi gọi API VNDirect
STAGE2_SLEEP = 3.5         # giây nghỉ khi gọi vnstock (chỉ dùng nếu vnstock có cài)
HAS_VNSTOCK = importlib.util.find_spec("vnstock") is not None
DCHART_URL = "https://dchart-api.vndirect.com.vn/dchart/history"
LISTING_URL = "https://finfo-api.vndirect.com.vn/v4/stocks"
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
      "Chrome/124.0.0.0 Safari/537.36")
# Thử lần lượt các kiểu header (một số máy chủ trả 406/403 nếu header không giống trình duyệt)
HEADER_VARIANTS = [
    {"User-Agent": UA, "Accept": "application/json, text/plain, */*",
     "Accept-Language": "vi-VN,vi;q=0.9,en;q=0.8",
     "Origin": "https://dchart.vndirect.com.vn", "Referer": "https://dchart.vndirect.com.vn/"},
    {"User-Agent": UA, "Accept": "*/*", "Referer": "https://trade.vndirect.com.vn/"},
    {"User-Agent": UA},
]
MIN_AVG_VOLUME = 100_000   # KLTB 20 phiên < ngưỡng này = loại (tiêu chí YẾU)
MIN_HISTORY = 130          # số phiên tối thiểu để tính đủ MA100/Ichimoku
STRESS_DROP = -0.6         # % VN-Index giảm để coi là "phiên áp lực" (~10 điểm)
TOP_N_DETAIL = 15          # số mã top được lấy thêm Buy Active % + cơ bản
MAX_SYMBOLS = 1000         # số mã tối đa mỗi lần quét
EXCHANGES = {"HOSE", "HNX", "UPCOM"}   # các sàn được quét (bỏ bớt nếu muốn thu hẹp)
DISCOVER_NOTE = ""
BUY_MAX_RISK = 8.0         # 'Đáng mua': rủi ro tới mức cắt lỗ tham khảo tối đa (%)
BUY_MAX_EXT = 10.0         # 'Đáng mua': giá không cao hơn MA20 quá số % này (tránh mua đuổi)
BUY_MIN_VALUE_BN = 5.0     # 'Đáng mua': giá trị giao dịch TB tối thiểu (tỷ đồng/phiên)
TIME_BUDGET_SEC = 26 * 60  # dừng quét nếu quá thời gian này (tránh GitHub tự ngắt)
REJECT_DAYS = 30           # mã bị loại (thanh khoản thấp...) được kiểm tra lại sau số ngày này
STATE_FILE = "reports/universe.json"
KHOE_SCORE = 70            # điểm tối thiểu để xếp KHỎE (kèm >= 5/6 tiêu chí cốt lõi)


# ----------------------------------------------------------------------------
# Lấy dữ liệu
# ----------------------------------------------------------------------------
def login():
    """Chỉ cần khi có cài vnstock (dùng cho Buy Active % và chỉ số cơ bản)."""
    global STAGE2_SLEEP
    if not HAS_VNSTOCK:
        print("Không cài vnstock: bỏ qua Buy Active % và chỉ số cơ bản (Trụ cột 5).")
        return
    key = os.environ.get("VNSTOCK_API_KEY", "").strip()
    if not key:
        print("Không có VNSTOCK_API_KEY, dùng chế độ khách (giới hạn chậm hơn).")
        return
    try:
        from vnstock import register_user
        register_user(api_key=key)
        STAGE2_SLEEP = 1.5   # có API key thì hạn mức cao hơn
        print("Đã đăng nhập vnstock bằng API key.")
    except Exception as e:
        print(f"Không đăng nhập được API key: {e}")


def load_symbols():
    with open("symbols.txt", encoding="utf-8") as f:
        return [l.strip().upper() for l in f if l.strip() and not l.startswith("#")]


def load_state():
    try:
        with open(STATE_FILE, encoding="utf-8") as f:
            st = json.load(f)
        return {"liquid": list(st.get("liquid", [])), "rejected": dict(st.get("rejected", {}))}
    except Exception:
        return {"liquid": [], "rejected": {}}


def save_state(state):
    os.makedirs("reports", exist_ok=True)
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=0, sort_keys=True)


def discover_symbols():
    """Lấy danh sách mã niêm yết từ VNDirect (thử nhiều địa chỉ). Lỗi thì trả danh sách rỗng."""
    global DISCOVER_NOTE
    urls = [
        "https://finfo-api.vndirect.com.vn/v4/stocks?q=type:STOCK~status:LISTED&fields=code,floor&size=3000",
        "https://api-finfo.vndirect.com.vn/v4/stocks?q=type:STOCK~status:LISTED&fields=code,floor&size=3000",
        "https://finfo-api.vndirect.com.vn/v4/stocks?q=type:STOCK&size=3000",
    ]
    for url in urls:
        d = http_json(url, retries=3)
        try:
            rows = d["data"]
            out = sorted({str(x["code"]).upper() for x in rows
                          if len(str(x.get("code", ""))) == 3 and str(x["code"]).isalpha()
                          and (not x.get("floor") or str(x["floor"]).upper() in EXCHANGES)})
            if len(out) > 50:
                DISCOVER_NOTE = f"Danh sách sàn: {len(out)} mã từ VNDirect"
                print(DISCOVER_NOTE)
                return out
        except Exception as e:
            print(f"Danh sách mã không đọc được từ {url[:60]}: {str(e)[:80]}")
    DISCOVER_NOTE = "KHÔNG lấy được danh sách mã từ sàn (đang chỉ quét symbols.txt)"
    print(DISCOVER_NOTE)
    return []


def build_universe(state):
    """symbols.txt (luôn quét) + mã thanh khoản đạt chuẩn đã biết + mã mới chưa kiểm tra."""
    today = datetime.now(VN_TZ).date()
    rejected = {}
    for sym, d in state["rejected"].items():
        try:
            if (today - datetime.fromisoformat(d).date()).days < REJECT_DAYS:
                rejected[sym] = d
        except Exception:
            pass
    state["rejected"] = rejected

    universe = list(dict.fromkeys(load_symbols() + state["liquid"]))
    if len(universe) < MAX_SYMBOLS:
        known = set(universe) | set(rejected)
        new = [s for s in discover_symbols() if s not in known]
        added = new[:MAX_SYMBOLS - len(universe)]
        universe += added
        print(f"Thêm {len(added)} mã mới cần kiểm tra thanh khoản.")
    return universe[:MAX_SYMBOLS]


LAST_ERROR = ""


def http_json(url, retries=3):  # mỗi lần thử dùng một kiểu header khác nhau
    global LAST_ERROR
    for attempt in range(retries):
        try:
            req = urllib.request.Request(url, headers=HEADER_VARIANTS[attempt % len(HEADER_VARIANTS)])
            with urllib.request.urlopen(req, timeout=25) as r:
                return json.loads(r.read().decode("utf-8"))
        except Exception as e:
            LAST_ERROR = f"{type(e).__name__}: {str(e)[:150]} | {url[:90]}"
            print(f"  lỗi tải dữ liệu (lần {attempt + 1}): {LAST_ERROR}")
            time.sleep(1 + attempt)
    return None


def fetch(symbol):
    """Giá ngày (OHLCV) từ API công khai VNDirect. Giá tính theo nghìn đồng."""
    now = int(time.time())
    url = f"{DCHART_URL}?resolution=D&symbol={symbol}&from={now - 430 * 86400}&to={now}"
    d = http_json(url)
    try:
        if not d or d.get("s") != "ok" or not d.get("t"):
            return None
        df = pd.DataFrame({
            "time": (pd.to_datetime(d["t"], unit="s") + pd.Timedelta(hours=7)).normalize(),
            "open": d["o"], "high": d["h"], "low": d["l"], "close": d["c"], "volume": d["v"],
        })
        df = df.dropna().drop_duplicates("time", keep="last")
        return df.sort_values("time").reset_index(drop=True) if len(df) >= 30 else None
    except Exception as e:
        print(f"  {symbol}: dữ liệu không đúng định dạng: {str(e)[:100]}")
        return None


# ----------------------------------------------------------------------------
# Chỉ báo
# ----------------------------------------------------------------------------
def rsi(close, n=14):
    d = close.diff()
    up = d.clip(lower=0).ewm(alpha=1 / n, adjust=False).mean()
    down = (-d.clip(upper=0)).ewm(alpha=1 / n, adjust=False).mean()
    return 100 - 100 / (1 + up / down.replace(0, np.nan))


def pct(a, b):
    return float((a / b - 1) * 100) if b and not np.isnan(b) else np.nan


def stress_test(df, idx):
    """So sánh cổ phiếu với VN-Index trong các phiên VN-Index giảm mạnh."""
    if idx is None:
        return np.nan, np.nan, 0
    s = df[["time", "close"]].rename(columns={"close": "s"}).merge(
        idx[["time", "close"]].rename(columns={"close": "i"}), on="time")
    s["rs"] = s["s"].pct_change() * 100
    s["ri"] = s["i"].pct_change() * 100
    s = s.dropna().tail(120)
    down = s[s["ri"] <= STRESS_DROP]
    if len(down) < 3:
        down = s[s["ri"] <= STRESS_DROP / 2]
    if len(down) < 3:
        return np.nan, np.nan, len(down)
    rel = float((down["rs"] - down["ri"]).mean())
    res = float((down["rs"] > down["ri"]).mean() * 100)
    return rel, res, len(down)


def compute_metrics(symbol, df, idx):
    if len(df) < MIN_HISTORY:
        return None
    o, h, l, c, v = (df[k].astype(float) for k in ["open", "high", "low", "close", "volume"])
    last = len(df) - 1

    avg_vol20 = float(v.iloc[-21:-1].mean())
    if avg_vol20 < MIN_AVG_VOLUME:
        return None

    ma20, ma50, ma100 = (c.rolling(n).mean() for n in (20, 50, 100))

    # MACD
    macd = c.ewm(span=12, adjust=False).mean() - c.ewm(span=26, adjust=False).mean()
    sig = macd.ewm(span=9, adjust=False).mean()
    hist = macd - sig

    # Ichimoku
    tenkan = (h.rolling(9).max() + l.rolling(9).min()) / 2
    kijun = (h.rolling(26).max() + l.rolling(26).min()) / 2
    span_a_now = ((tenkan + kijun) / 2).shift(26).iloc[last]
    span_b_now = ((h.rolling(52).max() + l.rolling(52).min()) / 2).shift(26).iloc[last]
    span_a_fut = ((tenkan + kijun) / 2).iloc[last]
    span_b_fut = ((h.rolling(52).max() + l.rolling(52).min()) / 2).iloc[last]
    cloud_top, cloud_bot = max(span_a_now, span_b_now), min(span_a_now, span_b_now)

    # Bollinger
    mid = ma20
    sd = c.rolling(20).std()
    upper, lower = mid + 2 * sd, mid - 2 * sd
    pctb = (c - lower) / (upper - lower)
    width = (upper - lower) / mid
    last5 = pctb.iloc[-5:]
    bb_walk = bool(((last5 >= 0.8).sum() >= 3) and (c.iloc[last] > mid.iloc[last])
                   and (width.iloc[last] > width.iloc[last - 5]))
    bb_down = bool(((last5 <= 0.2).sum() >= 3) and (c.iloc[last] < mid.iloc[last]))

    # Dòng tiền tạo lập (xấp xỉ MCDX): tỷ lệ tích lũy theo khối lượng 20 phiên
    rng = (h - l).replace(0, np.nan)
    mfv = (((c - l) - (h - c)) / rng).fillna(0) * v
    tot = mfv.iloc[-20:].abs().sum()
    acc = float(mfv.iloc[-20:].clip(lower=0).sum() / tot * 100) if tot > 0 else 50.0

    # Nến
    body = abs(c.iloc[last] - o.iloc[last])
    full = h.iloc[last] - l.iloc[last]
    lower_shadow = min(o.iloc[last], c.iloc[last]) - l.iloc[last]
    vr = float(v.iloc[last] / avg_vol20)
    near_sup = any(abs(l.iloc[last] - m.iloc[last]) / m.iloc[last] < 0.015
                   for m in (ma20, ma50))
    pinbar = bool(full > 0 and lower_shadow >= 2 * body and lower_shadow / full >= 0.6
                  and near_sup and vr < 0.8)
    marubozu_break = bool(full > 0 and o.iloc[last] > c.iloc[last] and body / full >= 0.85
                          and c.iloc[last] < ma20.iloc[last])
    up_day = bool(c.iloc[last] > c.iloc[last - 1])
    red_day = bool(c.iloc[last] < o.iloc[last] and c.iloc[last] < c.iloc[last - 1])

    # Relative strength thô (O'Neil): 3/6/9/12 tháng, trọng số 40/20/20/20
    parts, weights = [], []
    for n, w in ((63, 0.4), (126, 0.2), (189, 0.2), (252, 0.2)):
        if last - n >= 0:
            parts.append(pct(c.iloc[last], c.iloc[last - n]) * w)
            weights.append(w)
    rs_raw = sum(parts) / sum(weights) if weights else np.nan

    rel, res, n_down = stress_test(df, idx)
    idx_r1m = pct(idx["close"].iloc[-1], idx["close"].iloc[-21]) if idx is not None and len(idx) > 21 else np.nan

    return dict(
        symbol=symbol, close=float(c.iloc[last]), chg1d=pct(c.iloc[last], c.iloc[last - 1]),
        r1w=pct(c.iloc[last], c.iloc[last - 5]), r1m=pct(c.iloc[last], c.iloc[last - 20]),
        idx_r1m=idx_r1m, avg_vol20=avg_vol20,
        value_bn=float((c.iloc[-21:-1] * v.iloc[-21:-1]).mean() * 1000 / 1e9),
        rsi=float(rsi(c).iloc[last]), vr=vr, up_day=up_day, red_day=red_day, acc=acc,
        macd=float(macd.iloc[last]), sig=float(sig.iloc[last]),
        hist=float(hist.iloc[last]), hist_prev=float(hist.iloc[last - 1]),
        low10=float(l.iloc[-10:].min()),
        ma20=float(ma20.iloc[last]), ma50=float(ma50.iloc[last]), ma100=float(ma100.iloc[last]),
        ma20_up=bool(ma20.iloc[last] > ma20.iloc[last - 5]),
        ma50_up=bool(ma50.iloc[last] > ma50.iloc[last - 5]),
        ichi_above=bool(c.iloc[last] > cloud_top), ichi_below=bool(c.iloc[last] < cloud_bot),
        ichi_tk=bool(tenkan.iloc[last] > kijun.iloc[last]), ichi_fut=bool(span_a_fut > span_b_fut),
        bb_walk=bb_walk, bb_down=bb_down,
        bb_ok=bool(c.iloc[last] > mid.iloc[last] and pctb.iloc[last] > 0.5),
        pinbar=pinbar, marubozu=marubozu_break,
        stress_rel=rel, stress_res=res, stress_n=n_down, rs_raw=rs_raw,
    )


# ----------------------------------------------------------------------------
# Chấm điểm theo 5 trụ cột
# ----------------------------------------------------------------------------
def score_row(m):
    notes = []
    rs = m["RS"]

    # TRỤ CỘT 1 (25 điểm): RS, hiệu suất 1T, 1 tuần, thanh khoản
    p1 = 12 if rs >= 85 else 10 if rs >= 80 else 5 if rs >= 60 else 0
    if rs >= 80:
        notes.append(f"RS {rs}")
    r1m, r1w = m["r1m"], m["r1w"]
    if 5 <= r1m <= 15:
        p1 += 6; notes.append("1T +5~15%")
    elif r1m > 15:
        p1 += 3; notes.append("1T >15% (nóng)")
    elif r1m > 0:
        p1 += 3
    if 3 <= r1w <= 12:
        p1 += 4; notes.append("Tuần xác nhận sóng")
    elif -3 <= r1w < 3:
        p1 += 3; notes.append("Tuần nén chặt")
    elif r1w > 12:
        p1 += 2
    elif r1w >= -5:
        p1 += 1
    else:
        notes.append("Tuần < -5%")
    p1 += 3 if m["avg_vol20"] >= 200_000 else 1

    # TRỤ CỘT 2 (25 điểm): xu hướng & hành động giá
    c, ma20, ma50, ma100 = m["close"], m["ma20"], m["ma50"], m["ma100"]
    if c > ma20 > ma50 > ma100:
        p2 = 10; notes.append("Giá>MA20>MA50>MA100")
    elif c > ma20 > ma50:
        p2 = 7; notes.append("Giá>MA20>MA50")
    elif c > ma20:
        p2 = 3
    else:
        p2 = 0
    p2 += (2 if m["ma20_up"] else 0) + (2 if m["ma50_up"] else 0)
    if m["ichi_above"]:
        p2 += 3; notes.append("Trên mây")
    if m["ichi_tk"]:
        p2 += 2
    if m["ichi_fut"]:
        p2 += 2
    if m["bb_walk"]:
        p2 += 4; notes.append("Walking the Bands")
    elif m["bb_ok"]:
        p2 += 2
    if m["pinbar"]:
        notes.append("Pinbar tại hỗ trợ (cạn cung)")

    # TRỤ CỘT 3 (30 điểm): dòng tiền, MACD, RSI, khối lượng
    acc = m["acc"]
    p3 = 10 if acc >= 70 else 5 if acc >= 55 else 0
    if acc >= 70:
        notes.append(f"Tích lũy {acc:.0f}%")
    if m["macd"] > 0 and m["sig"] > 0:
        p3 += 5; notes.append("MACD>0")
        if m["hist"] > 0 and m["hist"] > m["hist_prev"]:
            p3 += 3
    elif m["macd"] > 0:
        p3 += 2
    rv = m["rsi"]
    if 55 <= rv <= 68:
        p3 += 6; notes.append("RSI khoẻ")
    elif 50 <= rv < 55 or 68 < rv <= 75:
        p3 += 3
    if m["up_day"] and 1.5 <= m["vr"] <= 2.5:
        p3 += 6; notes.append("Vol đột biến nến xanh")
    elif m["up_day"] and m["vr"] > 2.5:
        p3 += 4; notes.append("Vol rất lớn nến xanh")
    elif m["up_day"] and m["vr"] >= 1:
        p3 += 3

    # TRỤ CỘT 4 (20 điểm): phản ứng với VN-Index
    p4 = 0
    rel, res = m["stress_rel"], m["stress_res"]
    if not np.isnan(rel):
        p4 += 10 if rel > 0 else 5 if rel > -0.3 else 0
        p4 += 5 if res >= 60 else 2 if res >= 50 else 0
        if rel > 0 and res >= 60:
            notes.append("Chống chịu tốt khi VNI giảm")
    if not np.isnan(m["idx_r1m"]) and r1m > m["idx_r1m"]:
        p4 += 5; notes.append("Mạnh hơn VN-Index 1T")

    # Điểm trừ
    penalty = 0
    if m["marubozu"]:
        penalty += 5; notes.append("⚠ Marubozu đỏ thủng MA20")
    if m["vr"] >= 1.5 and m["red_day"]:
        penalty += 5; notes.append("⚠ Vol lớn nến đỏ (phân phối?)")
    if rv > 80:
        notes.append("⚠ RSI>80 quá mua")
    total = max(0, p1 + p2 + p3 + p4 - penalty)

    # 6 tiêu chí KHỎE / 6 tiêu chí YẾU (bảng đối chiếu nhanh)
    has_idx = not np.isnan(m["idx_r1m"]) and not np.isnan(rel)
    core = [
        rs > 80,
        c > ma20 > ma50,
        m["macd"] > 0 and m["sig"] > 0,
        55 <= rv <= 68,
        acc >= 70,
        bool(has_idx and r1m > m["idx_r1m"] and rel >= 0),
    ]
    weak = [
        rs < 60,
        c < ma20 < ma50,
        m["macd"] < 0,
        rv < 45,
        acc <= 30,
        bool(has_idx and r1m < m["idx_r1m"] and rel < 0),
    ]
    k, w = sum(core), sum(weak)
    if k >= 5 and total >= KHOE_SCORE:
        label = "🟢 KHỎE"
    elif w >= 5 or total < 35:
        label = "🔴 YẾU"
    elif total >= 55 or k >= 4:
        label = "🟡 THEO DÕI"
    else:
        label = "⚪ TRUNG LẬP"

    stop = min(m["ma20"], m["low10"]) * 0.985
    risk = (c - stop) / c * 100
    return {
        "Cách MA20%": round((c / ma20 - 1) * 100, 1), "Cắt lỗ": round(stop, 2),
        "Rủi ro%": round(risk, 1), "Mục tiêu": round(c + 2 * (c - stop), 2), "pen": penalty,
        "Mã": m["symbol"], "Điểm": total, "Phân loại": label, "Khỏe": f"{k}/6", "Yếu": f"{w}/6",
        "RS": rs, "Giá": round(c, 2), "%Phiên": round(m["chg1d"], 2), "%1T": round(r1m, 1),
        "%1Tuần": round(r1w, 1), "RSI": round(rv, 1), "Vol/TB20": round(m["vr"], 2),
        "Tích lũy%": round(acc), "GTGD tỷ": round(m["value_bn"], 1),
        "T1": p1, "T2": p2, "T3": p3, "T4": p4, "Tín hiệu": ", ".join(notes),
    }


# ----------------------------------------------------------------------------
# Giai đoạn 2: Buy Active % và cơ bản (chỉ cho nhóm top, gọi tốn API hơn)
# ----------------------------------------------------------------------------
def buy_active(symbol):
    """% khối lượng khớp mua chủ động của phiên giao dịch gần nhất."""
    try:
        from vnstock import Vnstock
        df = Vnstock().stock(symbol=symbol, source="VCI").quote.intraday(page_size=30000)
        if df is None or df.empty or "match_type" not in df.columns:
            return np.nan
        t = df["match_type"].astype(str).str.lower().str[0]
        buy = df.loc[t == "b", "volume"].sum()
        sell = df.loc[t == "s", "volume"].sum()
        return float(buy / (buy + sell) * 100) if buy + sell > 0 else np.nan
    except Exception as e:
        print(f"  {symbol}: không lấy được Buy Active: {str(e)[:80]}")
        return np.nan


def flatten_cols(df):
    if isinstance(df.columns, pd.MultiIndex):
        df = df.copy()
        df.columns = [" | ".join(str(x) for x in col if not str(x).startswith("Unnamed"))
                      for col in df.columns]
    return df


def find_col(df, *keys):
    for col in df.columns:
        name = str(col).lower()
        if all(k in name for k in keys):
            return col
    return None


def fundamentals(symbol):
    """P/E, P/B, tăng trưởng EPS YoY, xu hướng biên lợi nhuận gộp (nếu lấy được)."""
    out = {}
    try:
        from vnstock import Vnstock
        r = flatten_cols(Vnstock().stock(symbol=symbol, source="VCI").finance.ratio(
            period="quarter", lang="vi", dropna=True))
        y = find_col(r, "năm") or find_col(r, "year")
        q = find_col(r, "kỳ") or find_col(r, "quý") or find_col(r, "quarter")
        if y is not None and q is not None:
            r = r.sort_values([y, q], ascending=False).reset_index(drop=True)

        def num(col, i):
            try:
                return float(r[col].iloc[i])
            except Exception:
                return np.nan

        pe, pb = find_col(r, "p/e"), find_col(r, "p/b")
        eps = find_col(r, "eps (vnd)") or find_col(r, "eps")
        gm = find_col(r, "gross") or find_col(r, "biên lợi nhuận gộp") or find_col(r, "biên gộp")
        if pe is not None:
            out["pe"] = num(pe, 0)
        if pb is not None:
            out["pb"] = num(pb, 0)
        if eps is not None and len(r) >= 5:
            now_, prev = num(eps, 0), num(eps, 4)
            if prev > 0:
                out["eps_yoy"] = (now_ / prev - 1) * 100
        if gm is not None and len(r) >= 3:
            g0, g1, g2 = num(gm, 0), num(gm, 1), num(gm, 2)
            if not np.isnan([g0, g1, g2]).any():
                out["gm_up"] = bool(g0 > g1 > g2)
    except Exception as e:
        print(f"  {symbol}: không lấy được chỉ số cơ bản: {str(e)[:80]}")
    return out


def stage2(res):
    rows = {}
    top = res.head(TOP_N_DETAIL)["Mã"].tolist()
    print(f"Lấy thêm Buy Active % và chỉ số cơ bản cho {len(top)} mã top...")
    for s in top:
        print(f"  chi tiết {s}")
        ba = buy_active(s)
        time.sleep(STAGE2_SLEEP)
        f = fundamentals(s)
        time.sleep(STAGE2_SLEEP)
        flags = []
        if not np.isnan(ba):
            flags.append("Mua CĐ ✅" if ba > 52 else "Bán CĐ ⚠" if ba < 48 else "")
        if f.get("eps_yoy", np.nan) >= 25:
            flags.append("EPS +25% ✅")
        if f.get("gm_up"):
            flags.append("Biên gộp mở rộng ✅")
        if f.get("pb", np.nan) < 1:
            flags.append("P/B<1")
        rows[s] = {
            "Mua CĐ%": round(ba, 1) if not np.isnan(ba) else np.nan,
            "P/E": round(f["pe"], 1) if "pe" in f and not np.isnan(f["pe"]) else np.nan,
            "P/B": round(f["pb"], 2) if "pb" in f and not np.isnan(f["pb"]) else np.nan,
            "EPS YoY%": round(f["eps_yoy"]) if "eps_yoy" in f else np.nan,
            "Xác nhận": ", ".join(x for x in flags if x),
        }
    extra = pd.DataFrame.from_dict(rows, orient="index").rename_axis("Mã").reset_index()
    return res.merge(extra, on="Mã", how="left")


# ----------------------------------------------------------------------------
# Báo cáo
# ----------------------------------------------------------------------------
def send_telegram(text):
    token, chat = os.environ.get("TELEGRAM_BOT_TOKEN"), os.environ.get("TELEGRAM_CHAT_ID")
    if not token or not chat:
        return
    try:
        data = json.dumps({"chat_id": chat, "text": text}).encode()
        req = urllib.request.Request(
            f"https://api.telegram.org/bot{token}/sendMessage",
            data=data, headers={"Content-Type": "application/json"})
        urllib.request.urlopen(req, timeout=20)
    except Exception as e:
        print(f"Không gửi được Telegram: {e}")


def md_table(df, cols):
    cols = [c for c in cols if c in df.columns]
    return df[cols].fillna("–").to_markdown(index=False)


def pick_buy(res):
    """Lọc cổ phiếu 'đáng mua': KHỎE + chưa quá mua + chưa chạy xa MA20 + rủi ro cắt lỗ nhỏ."""
    r = res
    cond = ((r["Phân loại"] == "🟢 KHỎE") & r["RSI"].between(50, 70)
            & (r["Cách MA20%"] <= BUY_MAX_EXT) & (r["Tích lũy%"] >= 55) & (r["pen"] == 0)
            & (r["GTGD tỷ"] >= BUY_MIN_VALUE_BN) & (r["Rủi ro%"] > 0) & (r["Rủi ro%"] <= BUY_MAX_RISK)
            & (r["%1Tuần"] >= -5))
    return r[cond].sort_values(["Điểm", "Rủi ro%"], ascending=[False, True])


def build_report(res, idx, now):
    show = ["Mã", "Điểm", "Khỏe", "RS", "Giá", "%Phiên", "%1T", "RSI", "Vol/TB20",
            "Tích lũy%", "Mua CĐ%", "P/E", "P/B", "EPS YoY%", "Tín hiệu", "Xác nhận"]
    buy_cols = ["Mã", "Điểm", "RS", "Giá", "Cách MA20%", "RSI", "Vol/TB20", "Tích lũy%",
                "GTGD tỷ", "Cắt lỗ", "Rủi ro%", "Mục tiêu", "Tín hiệu"]
    md = f"# Kết quả quét {now} (giờ VN)\n\n"
    weak_market = False
    if idx is not None and len(idx) > 50:
        ic = idx["close"]
        below = ic.iloc[-1] < ic.tail(20).mean()
        m1 = pct(ic.iloc[-1], ic.iloc[-21])
        weak_market = bool(below and m1 < 0)
        md += (f"**VN-Index:** {ic.iloc[-1]:,.2f} ({pct(ic.iloc[-1], ic.iloc[-2]):+.2f}% phiên, "
               f"{m1:+.1f}% 1 tháng), {'dưới' if below else 'trên'} MA20.\n\n")
    n = res["Phân loại"].value_counts()
    md += (f"Đã quét {len(res)} mã: 🟢 {n.get('🟢 KHỎE', 0)} khỏe · 🟡 {n.get('🟡 THEO DÕI', 0)} theo dõi · "
           f"⚪ {n.get('⚪ TRUNG LẬP', 0)} trung lập · 🔴 {n.get('🔴 YẾU', 0)} yếu.\n\n")

    buy = pick_buy(res)
    md += "## ⭐ ĐÁNG MUA (KHỎE + RSI 50–70 + chưa chạy xa MA20 + rủi ro cắt lỗ ≤ 8%)\n\n"
    if weak_market:
        md += ("> ⚠ VN-Index đang dưới MA20 và giảm trong 1 tháng: thị trường chung yếu, "
               "nên giảm tỷ trọng và ưu tiên quản trị rủi ro.\n\n")
    if len(buy):
        md += md_table(buy, buy_cols)
        md += ("\n\n_Cắt lỗ tham khảo = dưới thấp hơn của (đáy 10 phiên, MA20) khoảng 1,5%. "
               "Mục tiêu = tỷ lệ lời/lỗ 2:1. Đây là mức kỹ thuật để tính rủi ro, không phải lệnh khuyến nghị._")
    else:
        md += "_Hiện chưa có mã nào đạt đủ điều kiện (thị trường thiếu điểm vào an toàn)._"

    khoe = res[res["Phân loại"] == "🟢 KHỎE"]
    md += "\n\n## 🟢 Cổ phiếu KHỎE (≥ 5/6 tiêu chí và ≥ 70 điểm)\n\n"
    md += md_table(khoe, show) if len(khoe) else "_Chưa có mã nào đạt chuẩn._"
    watch = res[res["Phân loại"] == "🟡 THEO DÕI"].head(12)
    md += "\n\n## 🟡 Theo dõi (gần đạt chuẩn)\n\n"
    md += md_table(watch, show) if len(watch) else "_Không có._"
    weak = res[res["Phân loại"] == "🔴 YẾU"]
    md += "\n\n## 🔴 Cổ phiếu YẾU (nên tránh)\n\n"
    md += (", ".join(f"{r['Mã']} ({r['Điểm']}đ)" for _, r in weak.iterrows()) or "_Không có._")
    md += ("\n\n---\n**Chú thích:** Điểm = Trụ cột 1 (thể lực giá, 25) + Trụ cột 2 (xu hướng, 25) + "
           "Trụ cột 3 (động lượng & dòng tiền, 30) + Trụ cột 4 (so với VN-Index, 20). "
           "RS xếp hạng trong danh sách đang quét (không phải toàn thị trường). "
           "'Tích lũy%' là chỉ báo xấp xỉ MCDX tự tính từ giá & khối lượng, không phải MCDX gốc. "
           "Dữ liệu trong phiên có thể chưa đủ khối lượng; giá tính theo nghìn đồng.\n"
           "_Chỉ mang tính tham khảo kỹ thuật, không phải khuyến nghị đầu tư._\n")
    return md, khoe, buy


def main():
    t0 = time.time()
    login()
    state = load_state()
    symbols = build_universe(state)
    print(f"Quét {len(symbols)} mã...")
    idx = fetch("VNINDEX")
    time.sleep(SLEEP_BETWEEN)
    if idx is None:
        print("Không lấy được VN-Index: bỏ qua Trụ cột 4.")

    today = datetime.now(VN_TZ).date().isoformat()
    metrics, scanned, cut, fails = [], 0, False, 0
    for i, s in enumerate(symbols, 1):
        if fails >= 15 and not metrics:
            print("Liên tiếp 15 mã không tải được dữ liệu: dừng sớm để tránh lãng phí thời gian.")
            break
        if time.time() - t0 > TIME_BUDGET_SEC:
            cut = True
            print("Hết thời gian cho phép, dừng quét; các mã còn lại sẽ quét ở lần sau.")
            break
        print(f"[{i}/{len(symbols)}] {s}")
        df = fetch(s)
        scanned += 1
        fails = 0 if df is not None else fails + 1
        if df is not None:
            try:
                m = compute_metrics(s, df, idx)
            except Exception as e:
                print(f"  {s}: lỗi phân tích: {e}")
                m = None
            if m:
                metrics.append(m)
                if s not in state["liquid"]:
                    state["liquid"].append(s)
                state["rejected"].pop(s, None)
            else:
                state["rejected"][s] = today
                if s in state["liquid"]:
                    state["liquid"].remove(s)
        time.sleep(SLEEP_BETWEEN)
    state["liquid"] = sorted(set(state["liquid"]))
    save_state(state)

    now = datetime.now(VN_TZ).strftime("%d/%m/%Y %H:%M")
    os.makedirs("reports", exist_ok=True)
    if not metrics:
        md = (f"# Kết quả quét {now}\n\n**Không lấy được dữ liệu giá.**\n\n"
              f"Lỗi gần nhất: `{LAST_ERROR or 'API trả về dữ liệu rỗng'}`\n")
        khoe = buy = pd.DataFrame()
    else:
        t = pd.DataFrame(metrics)
        t["RS"] = (t["rs_raw"].fillna(-999).rank(pct=True) * 98 + 1).round().astype(int)
        res = pd.DataFrame([score_row(r) for r in t.to_dict("records")])
        res = res.sort_values(["Điểm", "RS"], ascending=False).reset_index(drop=True)
        if HAS_VNSTOCK:
            res = stage2(res)
        res = res.sort_values(["Điểm", "RS"], ascending=False).reset_index(drop=True)
        res.to_csv("reports/latest.csv", index=False, encoding="utf-8-sig")
        md, khoe, buy = build_report(res, idx, now)
        if not HAS_VNSTOCK:
            md += ("\n_Lưu ý: chưa có vnstock nên bỏ qua Buy Active % và chỉ số cơ bản "
                   "(P/E, P/B, EPS). Dữ liệu giá lấy từ API công khai của VNDirect._\n")
        md = md.replace(
            "\n\nĐã quét ",
            f"\n\n_Đã duyệt {scanned}/{len(symbols)} mã trong {(time.time() - t0) / 60:.0f} phút"
            f"{' (bị cắt do hết thời gian)' if cut else ''}; "
            f"{len(state['rejected'])} mã bị loại vì thanh khoản thấp/thiếu dữ liệu. "
            f"{DISCOVER_NOTE}._\n\nĐã quét ", 1)
        if len(buy) or len(khoe):
            tb = "\n".join(f"{r['Mã']} - {r['Điểm']}đ - giá {r['Giá']} - cắt lỗ TK {r['Cắt lỗ']} ({r['Rủi ro%']}%)"
                           for _, r in buy.head(10).iterrows()) or "(chưa có)"
            tk = ", ".join(khoe.head(15)["Mã"])
            send_telegram(f"Quét CK {now}\n⭐ Đáng mua:\n{tb}\n\n🟢 Khỏe: {tk}")

    with open("reports/latest.md", "w", encoding="utf-8") as f:
        f.write(md)
    summary = os.environ.get("GITHUB_STEP_SUMMARY")
    if summary:
        with open(summary, "a", encoding="utf-8") as f:
            f.write(md)
    print(md)


if __name__ == "__main__":
    main()
