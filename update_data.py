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
    "VCB", "BID", "CTG", "TCB", "MBB", "ACB", "VPB", "STB", "HDB", "VIB", "SHB", "LPB", "MSB", "EIB", "OCB", "TPB", "SSB", "NAB", "BAB", "BVB", "ABB", "VAB", "KLB", "PGB",
    "SSI", "VND", "HCM", "VCI", "MBS", "FTS", "BSI", "CTS", "SHS", "ORS", "AGR", "APG", "VDS", "BVS", "TVS", "AAS", "CSI", "EVS", "VIX", "APS", "WSS", "SBS", "IVS", "TVC",
    "VHM", "VIC", "VRE", "KDH", "NLG", "DXG", "PDR", "DIG", "CEO", "NVL", "TCH", "SCR", "HDC", "HDG", "KBC", "SZC", "BCM", "IDC", "VGC", "IJC", "CII", "NBB", "NTL", "SIP", "TIP", "LHG", "HQC", "ITA", "LDG", "AGG", "CRE", "DRH", "QCG", "SJS", "TDC", "D2D", "SZL", "NTC", "HLD", "HAR", "HPX", "NHA", "API", "CSC", "DTA", "FIR",
    "HPG", "HSG", "NKG", "TLH", "SMC", "VGS", "TVN", "TIS",
    "KSB", "DHA", "HT1", "BCC", "HOM", "CLH", "C32", "PLC", "VCS", "PTB", "ACC", "BTS", "HLY", "YBM",
    "FPT", "CMG", "ELC", "CTR", "VGI", "FOX", "SAM", "ITD", "ICT", "ONE", "SGT", "TTN", "VNZ", "DST", "HPT",
    "MWG", "FRT", "DGW", "PNJ", "PET", "PSD", "AST", "SVC", "HAX", "CTF", "TMT", "HTC", "COM", "PIT", "TNA", "BTT",
    "GAS", "PVD", "PVS", "PLX", "BSR", "OIL", "PVC", "PVB", "PVT", "PVP", "CNG", "PGC", "POW", "NT2", "QTP", "PPC", "REE", "GEG", "PC1", "VSH", "TTA", "SBA", "TMP", "CHP", "HND",
    "DGC", "DCM", "DPM", "CSV", "LAS", "DDV", "BFC", "GVR", "PHR", "DPR", "DRC", "BMP", "NTP", "AAA", "APH", "DHC", "GIL", "TNG", "MSH", "TCM", "STK", "ADS", "HII", "PLP", "RDP", "DAG", "VTZ", "CSM", "SRC",
    "VNM", "MSN", "MCH", "SAB", "KDC", "QNS", "DBC", "BAF", "PAN", "TAR", "ANV", "VHC", "IDI", "ASM", "HAG", "HNG", "SBT", "LSS", "SLS", "MML", "VOC", "NAF", "HSL", "AFX", "LTG", "MPC", "FMC", "ACL", "CMX", "KHS", "HAP", "HHC", "BBC", "VLC", "VSN",
    "GMD", "HAH", "VSC", "SGP", "PHP", "VOS", "VTO", "SKG", "VTP", "TMS", "SFI", "DVP", "PDN", "CDN", "SCS", "NCT", "GSP", "VIP", "VNS", "TCO", "TCL", "PCT", "TJC",
    "VJC", "HVN", "ACV", "SAS", "CIA", "MAS", "SGN", "NCS",
    "CTD", "HBC", "FCN", "HHV", "LCG", "C4G", "VCG", "DPG", "HUT", "PHC", "HTN", "C47", "G36", "TCD", "L14", "MST",
    "DHG", "IMP", "TRA", "DCL", "DBD", "DMC", "TNH", "JVC", "DVN", "AMV", "DP3", "OPC", "PME", "VMD", "FIT",
    "BVH", "BMI", "PVI", "BIC", "MIG", "ABI", "PTI", "PRE", "VNR",
    "VGT", "M10", "EVE", "KMR", "TDT",
    "BWE", "TDM", "GEX", "SJD", "TBC",
    "RAL", "PAC", "SAV"
]

NAMES = {
    "VCB": "Vietcombank", "BID": "BIDV", "CTG": "VietinBank", "TCB": "Techcombank", "MBB": "Ngân hàng Quân đội", "ACB": "Ngân hàng Á Châu", "VPB": "VPBank", "STB": "Sacombank", "HDB": "HDBank", "VIB": "VIB", "SHB": "SHB", "LPB": "LPBank", "MSB": "MSB", "EIB": "Eximbank", "OCB": "OCB", "TPB": "TPBank", "SSB": "SeABank", "NAB": "Nam A Bank", "BAB": "Bac A Bank", "BVB": "VietCapital Bank", "ABB": "ABB", "VAB": "VAB", "KLB": "KLB", "PGB": "PGB",
    "SSI": "Chứng khoán SSI", "VND": "VNDIRECT", "HCM": "Chứng khoán HSC", "VCI": "Vietcap", "MBS": "Chứng khoán MB", "FTS": "FTS", "BSI": "BSI", "CTS": "CTS", "SHS": "SHS", "ORS": "ORS", "AGR": "AGR", "APG": "APG", "VDS": "VDS", "BVS": "BVS", "TVS": "TVS", "AAS": "AAS", "CSI": "CSI", "EVS": "EVS", "VIX": "VIX", "APS": "APS", "WSS": "WSS", "SBS": "SBS", "IVS": "IVS", "TVC": "TVC",
    "VHM": "Vinhomes", "VIC": "Vingroup", "VRE": "Vincom Retail",
    "KDH": "Khang Điền", "NLG": "Nam Long", "DXG": "Đất Xanh", "PDR": "Phát Đạt", "DIG": "DIC Corp", "CEO": "CEO Group", "NVL": "Novaland", "TCH": "TCH", "SCR": "SCR", "HDC": "HDC", "HDG": "HDG", "KBC": "Kinh Bắc", "SZC": "Sonadezi Châu Đức", "BCM": "Becamex IDC", "IDC": "IDICO", "VGC": "Viglacera", "IJC": "IJC", "CII": "CII", "NBB": "NBB", "NTL": "NTL", "SIP": "SIP", "TIP": "TIP", "LHG": "LHG", "HQC": "HQC", "ITA": "ITA", "LDG": "LDG", "AGG": "AGG", "CRE": "CRE", "DRH": "DRH", "QCG": "QCG", "SJS": "SJS", "TDC": "TDC", "D2D": "D2D", "SZL": "SZL", "NTC": "NTC", "HLD": "HLD", "HAR": "HAR", "HPX": "HPX", "NHA": "NHA", "API": "API", "CSC": "CSC", "DTA": "DTA", "FIR": "FIR",
    "HPG": "Tập đoàn Hòa Phát", "HSG": "Hoa Sen Group", "NKG": "Thép Nam Kim", "TLH": "TLH", "SMC": "SMC", "VGS": "VGS", "TVN": "TVN", "TIS": "TIS", "KSB": "KSB", "DHA": "DHA", "HT1": "HT1", "BCC": "BCC", "HOM": "HOM", "CLH": "CLH", "C32": "C32", "PLC": "PLC", "VCS": "VCS", "PTB": "PTB", "ACC": "ACC", "BTS": "BTS", "HLY": "HLY", "YBM": "YBM",
    "FPT": "FPT Corp", "CMG": "CMG", "ELC": "ELC", "CTR": "CTR", "VGI": "VGI", "FOX": "FOX", "SAM": "SAM", "ITD": "ITD", "ICT": "ICT", "ONE": "ONE", "SGT": "SGT", "TTN": "TTN", "VNZ": "VNZ", "DST": "DST", "HPT": "HPT",
    "MWG": "Thế Giới Di Động", "FRT": "FPT Retail", "DGW": "Digiworld", "PNJ": "Vàng bạc Đá quý Phú Nhuận", "PET": "PET", "PSD": "PSD", "AST": "AST", "SVC": "SVC", "HAX": "HAX", "CTF": "CTF", "TMT": "TMT", "HTC": "HTC", "COM": "COM", "PIT": "PIT", "TNA": "TNA", "BTT": "BTT",
    "GAS": "PV GAS", "PVD": "PV Drilling", "PVS": "PTSC", "PLX": "Petrolimex", "BSR": "Lọc hóa dầu Bình Sơn", "OIL": "OIL", "PVC": "PVC", "PVB": "PVB", "PVT": "PVT", "PVP": "PVP", "CNG": "CNG", "PGC": "PGC", "POW": "PV Power", "NT2": "Nhiệt điện Nhơn Trạch 2", "QTP": "Nhiệt điện Quảng Ninh", "PPC": "Nhiệt điện Phả Lại", "REE": "REE Corp", "GEG": "GEG", "PC1": "PC1 Group", "VSH": "VSH", "TTA": "TTA", "SBA": "SBA", "TMP": "TMP", "CHP": "CHP", "HND": "HND",
    "DGC": "Hóa chất Đức Giang", "DCM": "Đạm Cà Mau", "DPM": "Đạm Phú Mỹ", "CSV": "CSV", "LAS": "LAS", "DDV": "DDV", "BFC": "BFC", "GVR": "Tập đoàn Cao su Việt Nam", "PHR": "Cao su Phước Hòa", "DPR": "Cao su Đồng Phú", "DRC": "DRC", "BMP": "BMP", "NTP": "NTP", "AAA": "AAA", "APH": "APH", "DHC": "DHC", "GIL": "GIL", "TNG": "TNG", "MSH": "MSH", "TCM": "TCM", "STK": "STK", "ADS": "ADS", "HII": "HII", "PLP": "PLP", "RDP": "RDP", "DAG": "DAG", "VTZ": "VTZ", "CSM": "CSM", "SRC": "SRC",
    "VNM": "Vinamilk", "MSN": "Masan Group", "MCH": "Masan Consumer", "SAB": "Sabeco", "KDC": "KDC", "QNS": "Đường Quảng Ngãi", "DBC": "Dabaco", "BAF": "BAF Việt Nam", "PAN": "PAN", "TAR": "TAR", "ANV": "Nam Việt", "VHC": "Vĩnh Hoàn", "IDI": "IDI", "ASM": "ASM", "HAG": "HAG", "HNG": "HNG", "SBT": "SBT", "LSS": "LSS", "SLS": "SLS", "MML": "MML", "VOC": "VOC", "NAF": "NAF", "HSL": "HSL", "AFX": "AFX", "LTG": "LTG", "MPC": "MPC", "FMC": "FMC", "ACL": "ACL", "CMX": "CMX", "KHS": "KHS", "HAP": "HAP", "HHC": "HHC", "BBC": "BBC", "VLC": "VLC", "VSN": "VSN",
    "GMD": "Gemadept", "HAH": "Hải An", "VSC": "Viconship", "SGP": "SGP", "PHP": "PHP", "VOS": "VOS", "VTO": "VTO", "SKG": "SKG", "VTP": "VTP", "TMS": "TMS", "SFI": "SFI", "DVP": "DVP", "PDN": "PDN", "CDN": "CDN", "SCS": "SCS", "NCT": "NCT", "GSP": "GSP", "VIP": "VIP", "VNS": "VNS", "TCO": "TCO", "TCL": "TCL", "PCT": "PCT", "TJC": "TJC",
    "VJC": "Vietjet Air", "HVN": "Vietnam Airlines", "ACV": "Tổng công ty Cảng HKVN", "SAS": "SAS", "CIA": "CIA", "MAS": "MAS", "SGN": "SGN", "NCS": "NCS",
    "CTD": "Coteccons", "HBC": "Hòa Bình Construction", "FCN": "FCN", "HHV": "Đèo Cả", "LCG": "Lizen", "C4G": "C4G", "VCG": "Vinaconex", "DPG": "DPG", "HUT": "HUT", "PHC": "PHC", "HTN": "HTN", "C47": "C47", "G36": "G36", "TCD": "TCD", "L14": "L14", "MST": "MST",
    "DHG": "Dược Hậu Giang", "IMP": "Imexpharm", "TRA": "Traphaco", "DCL": "DCL", "DBD": "DBD", "DMC": "DMC", "TNH": "TNH", "JVC": "JVC", "DVN": "DVN", "AMV": "AMV", "DP3": "DP3", "OPC": "OPC", "PME": "PME", "VMD": "VMD", "FIT": "FIT",
    "BVH": "Bảo Việt Holdings", "BMI": "Bảo Minh", "PVI": "PVI Holdings", "BIC": "BIC", "MIG": "MIG", "ABI": "ABI", "PTI": "PTI", "PRE": "PRE", "VNR": "VNR",
    "VGT": "VGT", "M10": "M10", "EVE": "EVE", "KMR": "KMR", "TDT": "TDT",
    "BWE": "Biwase", "TDM": "Nước Thủ Dầu Một", "GEX": "Gelex", "SJD": "SJD", "TBC": "TBC",
    "RAL": "RAL", "PAC": "PAC", "SAV": "SAV"
}

SECTORS = {
    "VCB": "Ngân hàng", "BID": "Ngân hàng", "CTG": "Ngân hàng", "TCB": "Ngân hàng", "MBB": "Ngân hàng", "ACB": "Ngân hàng", "VPB": "Ngân hàng", "STB": "Ngân hàng", "HDB": "Ngân hàng", "VIB": "Ngân hàng", "SHB": "Ngân hàng", "LPB": "Ngân hàng", "MSB": "Ngân hàng", "EIB": "Ngân hàng", "OCB": "Ngân hàng", "TPB": "Ngân hàng", "SSB": "Ngân hàng", "NAB": "Ngân hàng", "BAB": "Ngân hàng", "BVB": "Ngân hàng", "ABB": "Ngân hàng", "VAB": "Ngân hàng", "KLB": "Ngân hàng", "PGB": "Ngân hàng",
    "SSI": "Chứng khoán", "VND": "Chứng khoán", "HCM": "Chứng khoán", "VCI": "Chứng khoán", "MBS": "Chứng khoán", "FTS": "Chứng khoán", "BSI": "Chứng khoán", "CTS": "Chứng khoán", "SHS": "Chứng khoán", "ORS": "Chứng khoán", "AGR": "Chứng khoán", "APG": "Chứng khoán", "VDS": "Chứng khoán", "BVS": "Chứng khoán", "TVS": "Chứng khoán", "AAS": "Chứng khoán", "CSI": "Chứng khoán", "EVS": "Chứng khoán", "VIX": "Chứng khoán", "APS": "Chứng khoán", "WSS": "Chứng khoán", "SBS": "Chứng khoán", "IVS": "Chứng khoán", "TVC": "Chứng khoán",
    "VHM": "Họ nhà VIN", "VIC": "Họ nhà VIN", "VRE": "Họ nhà VIN",
    "KDH": "Bất động sản / KCN", "NLG": "Bất động sản / KCN", "DXG": "Bất động sản / KCN", "PDR": "Bất động sản / KCN", "DIG": "Bất động sản / KCN", "CEO": "Bất động sản / KCN", "NVL": "Bất động sản / KCN", "TCH": "Bất động sản / KCN", "SCR": "Bất động sản / KCN", "HDC": "Bất động sản / KCN", "HDG": "Bất động sản / KCN", "KBC": "Bất động sản / KCN", "SZC": "Bất động sản / KCN", "BCM": "Bất động sản / KCN", "IDC": "Bất động sản / KCN", "VGC": "Bất động sản / KCN", "IJC": "Bất động sản / KCN", "CII": "Bất động sản / KCN", "NBB": "Bất động sản / KCN", "NTL": "Bất động sản / KCN", "SIP": "Bất động sản / KCN", "TIP": "Bất động sản / KCN", "LHG": "Bất động sản / KCN", "HQC": "Bất động sản / KCN", "ITA": "Bất động sản / KCN", "LDG": "Bất động sản / KCN", "AGG": "Bất động sản / KCN", "CRE": "Bất động sản / KCN", "DRH": "Bất động sản / KCN", "QCG": "Bất động sản / KCN", "SJS": "Bất động sản / KCN", "TDC": "Bất động sản / KCN", "D2D": "Bất động sản / KCN", "SZL": "Bất động sản / KCN", "NTC": "Bất động sản / KCN", "HLD": "Bất động sản / KCN", "HAR": "Bất động sản / KCN", "HPX": "Bất động sản / KCN", "NHA": "Bất động sản / KCN", "API": "Bất động sản / KCN", "CSC": "Bất động sản / KCN", "DTA": "Bất động sản / KCN", "FIR": "Bất động sản / KCN",
    "HPG": "Thép / Vật liệu xây dựng", "HSG": "Thép / Vật liệu xây dựng", "NKG": "Thép / Vật liệu xây dựng", "TLH": "Thép / Vật liệu xây dựng", "SMC": "Thép / Vật liệu xây dựng", "VGS": "Thép / Vật liệu xây dựng", "TVN": "Thép / Vật liệu xây dựng", "TIS": "Thép / Vật liệu xây dựng", "KSB": "Thép / Vật liệu xây dựng", "DHA": "Thép / Vật liệu xây dựng", "HT1": "Thép / Vật liệu xây dựng", "BCC": "Thép / Vật liệu xây dựng", "HOM": "Thép / Vật liệu xây dựng", "CLH": "Thép / Vật liệu xây dựng", "C32": "Thép / Vật liệu xây dựng", "PLC": "Thép / Vật liệu xây dựng", "VCS": "Thép / Vật liệu xây dựng", "PTB": "Thép / Vật liệu xây dựng", "ACC": "Thép / Vật liệu xây dựng", "BTS": "Thép / Vật liệu xây dựng", "HLY": "Thép / Vật liệu xây dựng", "YBM": "Thép / Vật liệu xây dựng",
    "FPT": "Công nghệ / Viễn thông", "CMG": "Công nghệ / Viễn thông", "ELC": "Công nghệ / Viễn thông", "CTR": "Công nghệ / Viễn thông", "VGI": "Công nghệ / Viễn thông", "FOX": "Công nghệ / Viễn thông", "SAM": "Công nghệ / Viễn thông", "ITD": "Công nghệ / Viễn thông", "ICT": "Công nghệ / Viễn thông", "ONE": "Công nghệ / Viễn thông", "SGT": "Công nghệ / Viễn thông", "TTN": "Công nghệ / Viễn thông", "VNZ": "Công nghệ / Viễn thông", "DST": "Công nghệ / Viễn thông", "HPT": "Công nghệ / Viễn thông",
    "MWG": "Bán lẻ / Phân phối", "FRT": "Bán lẻ / Phân phối", "DGW": "Bán lẻ / Phân phối", "PNJ": "Bán lẻ / Phân phối", "PET": "Bán lẻ / Phân phối", "PSD": "Bán lẻ / Phân phối", "AST": "Bán lẻ / Phân phối", "SVC": "Bán lẻ / Phân phối", "HAX": "Bán lẻ / Phân phối", "CTF": "Bán lẻ / Phân phối", "TMT": "Bán lẻ / Phân phối", "HTC": "Bán lẻ / Phân phối", "COM": "Bán lẻ / Phân phối", "PIT": "Bán lẻ / Phân phối", "TNA": "Bán lẻ / Phân phối", "BTT": "Bán lẻ / Phân phối",
    "GAS": "Dầu khí / Năng lượng", "PVD": "Dầu khí / Năng lượng", "PVS": "Dầu khí / Năng lượng", "PLX": "Dầu khí / Năng lượng", "BSR": "Dầu khí / Năng lượng", "OIL": "Dầu khí / Năng lượng", "PVC": "Dầu khí / Năng lượng", "PVB": "Dầu khí / Năng lượng", "PVT": "Dầu khí / Năng lượng", "PVP": "Dầu khí / Năng lượng", "CNG": "Dầu khí / Năng lượng", "PGC": "Dầu khí / Năng lượng", "POW": "Dầu khí / Năng lượng", "NT2": "Dầu khí / Năng lượng", "QTP": "Dầu khí / Năng lượng", "PPC": "Dầu khí / Năng lượng", "REE": "REE Corp", "GEG": "GEG", "PC1": "PC1 Group", "VSH": "VSH", "TTA": "TTA", "SBA": "SBA", "TMP": "TMP", "CHP": "CHP", "HND": "HND",
    "DGC": "Hóa chất / Phân bón / Cao su / Nhựa", "DCM": "Hóa chất / Phân bón / Cao su / Nhựa", "DPM": "Hóa chất / Phân bón / Cao su / Nhựa", "CSV": "Hóa chất / Phân bón / Cao su / Nhựa", "LAS": "Hóa chất / Phân bón / Cao su / Nhựa", "DDV": "Hóa chất / Phân bón / Cao su / Nhựa", "BFC": "Hóa chất / Phân bón / Cao su / Nhựa", "GVR": "Hóa chất / Phân bón / Cao su / Nhựa", "PHR": "Hóa chất / Phân bón / Cao su / Nhựa", "DPR": "Hóa chất / Phân bón / Cao su / Nhựa", "DRC": "Hóa chất / Phân bón / Cao su / Nhựa", "BMP": "Hóa chất / Phân bón / Cao su / Nhựa", "NTP": "Hóa chất / Phân bón / Cao su / Nhựa", "AAA": "Hóa chất / Phân bón / Cao su / Nhựa", "APH": "Hóa chất / Phân bón / Cao su / Nhựa", "DHC": "Hóa chất / Phân bón / Cao su / Nhựa", "GIL": "Hóa chất / Phân bón / Cao su / Nhựa", "TNG": "Hóa chất / Phân bón / Cao su / Nhựa", "MSH": "Hóa chất / Phân bón / Cao su / Nhựa", "TCM": "Hóa chất / Phân bón / Cao su / Nhựa", "STK": "Hóa chất / Phân bón / Cao su / Nhựa", "ADS": "Hóa chất / Phân bón / Cao su / Nhựa", "HII": "Hóa chất / Phân bón / Cao su / Nhựa", "PLP": "Hóa chất / Phân bón / Cao su / Nhựa", "RDP": "Hóa chất / Phân bón / Cao su / Nhựa", "DAG": "Hóa chất / Phân bón / Cao su / Nhựa", "VTZ": "Hóa chất / Phân bón / Cao su / Nhựa", "CSM": "Hóa chất / Phân bón / Cao su / Nhựa", "SRC": "Hóa chất / Phân bón / Cao su / Nhựa",
    "VNM": "Tiêu dùng / Thực phẩm / Nông nghiệp", "MSN": "Tiêu dùng / Thực phẩm / Nông nghiệp", "MCH": "Tiêu dùng / Thực phẩm / Nông nghiệp", "SAB": "Tiêu dùng / Thực phẩm / Nông nghiệp", "KDC": "Tiêu dùng / Thực phẩm / Nông nghiệp", "QNS": "Đường Quảng Ngãi", "DBC": "Dabaco", "BAF": "BAF Việt Nam", "PAN": "PAN", "TAR": "TAR", "ANV": "Nam Việt", "VHC": "Vĩnh Hoàn", "IDI": "IDI", "ASM": "ASM", "HAG": "HAG", "HNG": "HNG", "SBT": "SBT", "LSS": "LSS", "SLS": "SLS", "MML": "MML", "VOC": "VOC", "NAF": "NAF", "HSL": "HSL", "AFX": "AFX", "LTG": "LTG", "MPC": "MPC", "FMC": "FMC", "ACL": "ACL", "CMX": "CMX", "KHS": "KHS", "HAP": "HAP", "HHC": "HHC", "BBC": "BBC", "VLC": "VLC", "VSN": "VSN",
    "GMD": "Logistics / Cảng biển / Vận tải", "HAH": "Logistics / Cảng biển / Vận tải", "VSC": "Logistics / Cảng biển / Vận tải", "SGP": "Logistics / Cảng biển / Vận tải", "PHP": "Logistics / Cảng biển / Vận tải", "VOS": "Logistics / Cảng biển / Vận tải", "VTO": "Logistics / Cảng biển / Vận tải", "SKG": "Logistics / Cảng biển / Vận tải", "VTP": "Logistics / Cảng biển / Vận tải", "TMS": "Logistics / Cảng biển / Vận tải", "SFI": "Logistics / Cảng biển / Vận tải", "DVP": "Logistics / Cảng biển / Vận tải", "PDN": "Logistics / Cảng biển / Vận tải", "CDN": "Logistics / Cảng biển / Vận tải", "SCS": "Logistics / Cảng biển / Vận tải", "NCT": "Logistics / Cảng biển / Vận tải", "GSP": "Logistics / Cảng biển / Vận tải", "VIP": "Logistics / Cảng biển / Vận tải", "VNS": "Logistics / Cảng biển / Vận tải", "TCO": "Logistics / Cảng biển / Vận tải", "TCL": "Logistics / Cảng biển / Vận tải", "PCT": "Logistics / Cảng biển / Vận tải", "TJC": "Logistics / Cảng biển / Vận tải",
    "VJC": "Hàng không / Dịch vụ sân bay", "HVN": "Hàng không / Dịch vụ sân bay", "ACV": "Hàng không / Dịch vụ sân bay", "SAS": "Hàng không / Dịch vụ sân bay", "CIA": "Hàng không / Dịch vụ sân bay", "MAS": "Hàng không / Dịch vụ sân bay", "SGN": "Hàng không / Dịch vụ sân bay", "NCS": "Hàng không / Dịch vụ sân bay",
    "CTD": "Xây dựng / Hạ tầng", "HBC": "Xây dựng / Hạ tầng", "FCN": "Xây dựng / Hạ tầng", "HHV": "Xây dựng / Hạ tầng", "LCG": "Xây dựng / Hạ tầng", "C4G": "Xây dựng / Hạ tầng", "VCG": "Vinaconex", "DPG": "Xây dựng / Hạ tầng", "HUT": "Xây dựng / Hạ tầng", "PHC": "Xây dựng / Hạ tầng", "HTN": "Xây dựng / Hạ tầng", "C47": "Xây dựng / Hạ tầng", "G36": "Xây dựng / Hạ tầng", "TCD": "Xây dựng / Hạ tầng", "L14": "Xây dựng / Hạ tầng", "MST": "Xây dựng / Hạ tầng",
    "DHG": "Dược / Y tế", "IMP": "Dược / Y tế", "TRA": "Dược / Y tế", "DCL": "Dược / Y tế", "DBD": "Dược / Y tế", "DMC": "Dược / Y tế", "TNH": "Dược / Y tế", "JVC": "Dược / Y tế", "DVN": "Dược / Y tế", "AMV": "Dược / Y tế", "DP3": "Dược / Y tế", "OPC": "Dược / Y tế", "PME": "Dược / Y tế", "VMD": "Dược / Y tế", "FIT": "Dược / Y tế",
    "BVH": "Bảo hiểm", "BMI": "Bảo hiểm", "PVI": "Bảo hiểm", "BIC": "Bảo hiểm", "MIG": "Bảo hiểm", "ABI": "Bảo hiểm", "PTI": "Bảo hiểm", "PRE": "Bảo hiểm", "VNR": "Bảo hiểm",
    "VGT": "Dệt may / Xuất khẩu", "M10": "Dệt may / Xuất khẩu", "EVE": "Dệt may / Xuất khẩu", "KMR": "Dệt may / Xuất khẩu", "TDT": "Dệt may / Xuất khẩu",
    "BWE": "Điện / Nước / Tiện ích", "TDM": "Nước Thủ Dầu Một", "GEX": "Gelex", "SJD": "SJD", "TBC": "TBC",
    "RAL": "Khác / Công nghiệp", "PAC": "PAC", "SAV": "SAV"
}

SECTOR_LEADERS = {
    "Ngân hàng": ["VCB", "BID", "TCB", "MBB", "ACB"],
    "Chứng khoán": ["SSI", "VCI", "HCM", "FTS"],
    "Bất động sản / KCN": ["VHM", "VIC", "KDH", "NLG"],
    "Logistics / Cảng biển / Vận tải": ["GMD", "HAH"],
    "Công nghệ / Viễn thông": ["FPT", "CMG"]
}

VIN_GROUP = ["VIC", "VHM", "VRE"]

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

def obv(df: pd.DataFrame) -> pd.Series:
    df = df.copy()
    df['direction'] = 0
    df.loc[df['close'] > df['close'].shift(1), 'direction'] = 1
    df.loc[df['close'] < df['close'].shift(1), 'direction'] = -1
    return (df['volume'] * df['direction']).cumsum()

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

def score_stock(
    symbol: str, 
    df: pd.DataFrame, 
    src: str, 
    market_ret60: float | None, 
    vin_above_ma20: bool = False,
    all_symbols_df: dict[str, pd.DataFrame] = None
) -> dict[str, Any]:
    close = df["close"]
    volume = df["volume"]

    df["ma20"] = close.rolling(20).mean()
    df["ma50"] = close.rolling(50).mean()
    df["ma100"] = close.rolling(100).mean()
    df["ma200"] = close.rolling(200).mean()
    df["rsi14"] = rsi(close)
    df["macd"], df["macd_signal"] = macd(close)
    df["high52w"] = close.rolling(min(len(df), 250)).max()
    df["obv"] = obv(df)

    last = df.iloc[-1]
    prev = df.iloc[-2] if len(df) > 1 else last
    
    c = float(last["close"])
    v = float(last["volume"])
    
    ma20 = safe_float(last.get("ma20"), 0)
    ma50 = safe_float(last.get("ma50"), 0)
    ma100 = safe_float(last.get("ma100"), 0)
    ma200 = safe_float(last.get("ma200"), 0)
    rsi14 = safe_float(last.get("rsi14"))
    macd_line = safe_float(last.get("macd"))
    macd_sig = safe_float(last.get("macd_signal"))
    high52w = float(last["high52w"]) if pd.notna(last.get("high52w")) else c

    # Tính toán cơ bản
    vol20 = float(volume.rolling(20).mean().iloc[-1]) if len(df) >= 20 else v
    avg_value_20 = float((close * volume).rolling(20).mean().iloc[-1]) if len(df) >= 20 else (c * v)
    vol_ratio = round(v / vol20, 2) if vol20 else 1.0
    dist_high52w_pct = round(((high52w - c) / high52w) * 100, 2) if high52w else 0.0
    
    prev20_close = float(df.iloc[-21]["close"]) if len(df) > 20 else float(df.iloc[0]["close"])
    prev60_close = float(df.iloc[-61]["close"]) if len(df) > 60 else float(df.iloc[0]["close"])
    ret3 = round((c / float(df.iloc[-4]["close"]) - 1) * 100, 2) if len(df) > 3 else 0.0
    ret20 = round((c / prev20_close - 1) * 100, 2) if prev20_close else 0.0
    ret60 = round((c / prev60_close - 1) * 100, 2) if prev60_close else 0.0
    close_pos = round((c - float(last["low"])) / max(1.0, float(last["high"]) - float(last["low"])), 2)

    # VIII. WATCHLIST PHÂN TẦNG & SYSTEM FILTERS (LỌC RỦI RO CHIẾN LƯỢC QUỸ)
    is_filtered_out = False
    fail_reason = ""
    
    if avg_value_20 < 50_000_000_000:
        is_filtered_out = True
        fail_reason = "Avg Value 20d < 50B (Thanh khoản rác)"
    elif c < ma50:
        is_filtered_out = True
        fail_reason = "Price < MA50 (Dưới xu hướng trung hạn)"
    elif rsi14 is not None and rsi14 > 82:
        is_filtered_out = True
        fail_reason = "RSI > 82 (Quá bốc hỏa/Quá mua nặng)"
    elif ret3 > 18.0:
        is_filtered_out = True
        fail_reason = "3-day Return > 18% (Rủi ro FOMO đỉnh ngắn hạn)"

    # I. TREND STRUCTURE SCORE (Tối đa: 30 điểm)
    trend_score = 0
    if ma20 and c > ma20: trend_score += 5
    if ma20 and ma50 and ma20 > ma50: trend_score += 10
    if ma50 and ma100 and ma50 > ma100: trend_score += 5
    if ma100 and ma200 and ma100 > ma200: trend_score += 5
    
    # Golden Cross ngắn hạn (MA20 cắt lên MA50 trong 3 phiên gần đây)
    ma20_s = df["ma20"]
    ma50_s = df["ma50"]
    golden_cross = False
    for i in range(-1, -4, -1):
        if len(df) >= abs(i) + 1:
            if ma20_s.iloc[i] >= ma50_s.iloc[i] and ma20_s.iloc[i-1] < ma50_s.iloc[i-1]:
                golden_cross = True
                break
    if golden_cross: trend_score += 5
    
    # Vị trí giá đối với đỉnh 52 tuần
    if dist_high52w_pct < 10.0: trend_score += 5
    elif dist_high52w_pct <= 20.0: trend_score += 2
    if dist_high52w_pct > 25.0: trend_score -= 10  # Trừ nặng mã giảm sâu khỏi đỉnh

    # II. INSTITUTIONAL MONEY FLOW (Tối đa: 25 điểm)
    money_score = 0
    if avg_value_20 > 200_000_000_000: money_score += 10
    elif avg_value_20 > 100_000_000_000: money_score += 7
    elif avg_value_20 > 50_000_000_000: money_score += 4
    
    if vol_ratio >= 2.0: money_score += 10
    elif vol_ratio >= 1.5: money_score += 7
    elif vol_ratio >= 1.2: money_score += 4
    
    # OBV dốc lên 5 phiên
    if len(df) >= 5 and (df["obv"].tail(5).diff().dropna() > 0).all(): money_score += 5

    # III. SUPER ALPHA & RELATIVE STRENGTH (Tối đa: 20 điểm)
    rs_score = 0
    stock_alpha = ret60 - (market_ret60 if market_ret60 is not None else 0.0)
    if stock_alpha > 20.0: rs_score += 10
    elif stock_alpha > 10.0: rs_score += 7
    elif stock_alpha > 5.0: rs_score += 4
    
    # RS Line Phá Đỉnh 60 phiên (Sức mạnh tương đối tối mật)
    rs_line_break_high = False
    if all_symbols_df and "VNINDEX" in all_symbols_df:
        m_df = all_symbols_df["VNINDEX"]
        merged = pd.merge(df[['time', 'close']], m_df[['time', 'close']], on='time', suffixes=('_s', '_m'))
        if len(merged) >= 60:
            merged['rs_line'] = merged['close_s'] / merged['close_m']
            if merged['rs_line'].iloc[-1] == merged['rs_line'].tail(60).max():
                rs_line_break_high = True
    if rs_line_break_high: rs_score += 10

    # IV. MOMENTUM & PRICE POSITION (Tối đa: 15 điểm)
    mom_score = 0
    if rsi14 is not None and 52.0 <= rsi14 <= 72.0: mom_score += 5
    if macd_line is not None and macd_sig is not None and macd_line > macd_sig and macd_line > 0: mom_score += 5
    if close_pos >= 0.75: mom_score += 5

    # V & VI. MARKET LEADERS & VIN GROUP LAYER
    bonus_score = 0
    sector = SECTORS.get(symbol, "Khác")
    if symbol in SECTOR_LEADERS.get(sector, []): bonus_score += 5
    if symbol in VIN_GROUP: bonus_score += 5
    if symbol in VIN_GROUP and vin_above_ma20: bonus_score += 5 # Thưởng thêm hiệu ứng sóng dòng VIN

    # Tổng điểm V3.0 tối đa chặn 100
    total_score = clamp(round(trend_score + money_score + rs_score + mom_score + bonus_score, 1), 0, 100)
    if is_filtered_out: total_score = 0.0 # Bị loại rủi ro ép về 0 điểm

    # X. TOP 3 EAGLE RULE (Quy tắc tiệm cận Alpha tuyệt đối)
    is_top3_eligible = bool(
        total_score >= 85 
        and ma20 and ma50 and c > ma20 > ma50 
        and avg_value_20 > 100_000_000_000 
        and stock_alpha > 10.0 
        and macd_line is not None and macd_sig is not None and macd_line > macd_sig
    )

    # Phân tầng hành động hiển thị lên giao diện
    if total_score >= 85:
        action, allocation = "Tier A: MUA CHIẾN LƯỢC / LEADER", "15% - 25%"
    elif total_score >= 72:
        action, allocation = "Tier B: CANH NỀN / CHỜ BREAKOUT", "10% - 15%"
    elif total_score >= 60:
        action, allocation = "Tier C: QUAN SÁT / CHỜ DÒNG TIỀN", "0% - 5%"
    else:
        action, allocation = "TRÁNH MUA MỚI / VI PHẠM RISK FILTER", "0%"

    signals, warnings = [], []
    if is_filtered_out:
        warnings.append(f"VI PHẠM BỘ LỌC QUỸ: {fail_reason}")
    else:
        if c >= high52w * 0.95: signals.append("Alpha King: Giá tiệm cận hoặc neo ngay đỉnh 52 tuần")
        if rs_line_break_high: signals.append("Super Alpha: Đường RS Line thiết lập đỉnh cao mới 60 phiên")
        if golden_cross: signals.append("Tín hiệu Golden Cross ngắn hạn (MA20 vượt MA50)")
        if close_pos >= 0.75: signals.append("Cầu áp đảo: Nến đóng cửa ở vùng giá cao nhất phiên")
        if vin_above_ma20 and symbol in VIN_GROUP: signals.append("Sóng dòng Vin kích hoạt: Dòng tiền đồng thuận cả họ")
        if is_top3_eligible: signals.append("🔥 ĐẠT TIÊU CHUẨN VÀNG TOP 3 EAGLE RULE")

    if rsi14 and rsi14 > 75: warnings.append("RSI tiệm cận vùng nóng, hạn chế giải ngân đuổi")
    if dist_high52w_pct > 25: warnings.append("Mã gãy trend sâu từ đỉnh 52w, chỉ thích hợp quan sát kỹ thuật")

    expertSummary = (
        f"{symbol} đạt hệ điểm V3.0 Quỹ: {total_score}/100. RS Alpha: {round(stock_alpha,1)}%. "
        f"GTGD đạt {round(avg_value_20/1e9,1)} tỷ/phiên. "
        f"Hành động chiến thuật: {action}."
    )

    # Đóng gói bộ lọc tương thích giao diện HTML của Sếp
    filters = {
        "topOpportunity": total_score >= 85,
        "cycleTurnaround": total_score >= 75 and dist_high52w_pct < 15.0,
        "tplus": is_top3_eligible,
        "breakout": vol_ratio >= 1.5 and close_pos >= 0.7,
        "pullbackMA20": bool(ma20 and 0 <= ((c/ma20)-1)*100 <= 3.0),
        "moneyFlow": money_score >= 15,
        "accumulation": bool(dist_high52w_pct <= 12.0 and abs(ret20) < 8.0),
        "safe": total_score >= 72 and c > ma20
    }

    return {
        "ticker": symbol, "name": NAMES.get(symbol, symbol), "sector": sector,
        "score": total_score,
        "subscores": {
            "trend": trend_score, "momentum": mom_score, "moneyFlow": money_score,
            "setup": bonus_score, "risk": int(not is_filtered_out) * 15, "relativeStrength": rs_score
        },
        "setupType": "Alpha Leader" if is_top3_eligible else "Nền đà tăng" if total_score >= 72 else "Theo dõi",
        "marketState": "Thượng tầng Alpha" if total_score >= 85 else "Tích cực" if total_score >= 72 else "Yếu",
        "action": action, "risk": "Quản trị chặt" if sector in ["Chứng khoán", "Họ nhà VIN"] else "Theo thị trường",
        "close": safe_float(c, 0), "rsi14": rsi14, "ret20": ret20, "ret60": ret60,
        "volume_status": "Bùng nổ" if vol_ratio >= 1.5 else "Khá" if vol_ratio >= 1.2 else "Kiệt Vol",
        "volumeRatio": vol_ratio, "ma20": ma20, "ma50": ma50, "ma200": ma200,
        "macd": macd_line, "macd_signal": macd_sig, "distanceToMA20": round(((c/ma20)-1)*100, 2) if ma20 else 0,
        "signals": signals if signals else ["Duy trì cấu trúc nền tích lũy ổn định"], 
        "warnings": warnings, "filters": filters,
        "reason": expertSummary, "expertSummary": expertSummary, "buyZone": f"Quanh vùng MA20 ~ {int(ma20):,}".replace(",", "."),
        "stopLoss": "Thủng MA50 hoặc mất nền giá gần nhất -5%", "takeProfit": "Kỳ vọng Alpha ngắn hạn +15% hoặc trailing theo đường MA20",
        "allocation": allocation
    }

def fallback_data(errors: dict[str, str], activation_logs: list[str]):
    return {
        "meta": {
            "updated_at": datetime.now(VN_TZ).strftime("%Y-%m-%d %H:%M:%S VN"),
            "source": "fallback sample system V3.0",
            "has_api_key": bool(VNSTOCK_API_KEY), "success": 0, "universe": len(WATCHLIST),
            "note": "Hệ thống Quỹ đang đợi kích hoạt cào từ GitHub Actions.",
            "activation_logs": activation_logs, "errors": errors,
        },
        "stocks": []
    }

def main():
    activation_logs = try_activate_key()
    print("Activation logs:", activation_logs)

    all_dfs = {}
    errors = {}

    # Tải trước VNINDEX làm mốc đối chiếu sức mạnh tương đối (Relative Strength Alpha)
    market_ret60 = 0.0
    try:
        m_df, _ = fetch_history("VNINDEX")
        all_dfs["VNINDEX"] = m_df
        if len(m_df) > 60:
            market_ret60 = round((m_df.iloc[-1]["close"] / m_df.iloc[-61]["close"] - 1) * 100, 2)
    except Exception as exc:
        print("WARN VNINDEX FETCH FAILED:", exc)

    # Tiến hành quét vũ trụ danh mục của Sếp
    for symbol in WATCHLIST:
        try:
            df, src = fetch_history(symbol)
            all_dfs[symbol] = df
            print(f"FETCH OK -> {symbol}")
        except Exception as exc:
            errors[symbol] = str(exc)
            print(f"FETCH ERROR {symbol}: {exc}")

    # Lớp Layer kiểm tra hiệu ứng sóng dòng họ Vin: Kiểm tra đồng thời VIC > MA20 và VHM > MA20
    vin_above_ma20 = False
    try:
        if "VIC" in all_dfs and "VHM" in all_dfs:
            vic_close = all_dfs["VIC"].iloc[-1]["close"]
            vic_ma20 = all_dfs["VIC"]["close"].rolling(20).mean().iloc[-1]
            vhm_close = all_dfs["VHM"].iloc[-1]["close"]
            vhm_ma20 = all_dfs["VHM"]["close"].rolling(20).mean().iloc[-1]
            if vic_close > vic_ma20 and vhm_close > vhm_ma20:
                vin_above_ma20 = True
                print(">>> ĐÃ KÍCH HOẠT HIỆU ỨNG SÓNG DÒNG VIN GROUP (+5 PTS) <<<")
    except Exception as e:
        print("WARN VIN LAYER COMPUTE:", e)

    results = []
    for symbol, df in all_dfs.items():
        if symbol == "VNINDEX":
            continue
        try:
            item = score_stock(symbol, df, "Vnstock API", market_ret60, vin_above_ma20, all_dfs)
            results.append(item)
        except Exception as exc:
            errors[symbol] = f"Scoring exception: {exc}"
            print(f"SCORE ERROR {symbol}: {exc}")

    if results:
        # Sắp xếp điểm hệ thống quét từ cao xuống thấp
        results = sorted(results, key=lambda x: x.get("score", 0), reverse=True)
        data = {
            "meta": {
                "updated_at": datetime.now(VN_TZ).strftime("%Y-%m-%d %H:%M:%S VN"),
                "source": "VN Stock Eagle Picker Pro V3.0",
                "has_api_key": bool(VNSTOCK_API_KEY),
                "success": len(results), "universe": len(WATCHLIST),
                "market_ret60": market_ret60,
                "note": "STOCK SCORING V3.0: Hệ thống quét dòng tiền tổ chức, Alpha và bộ lọc rủi ro Trading Quỹ.",
                "activation_logs": activation_logs, "errors": errors,
            },
            "stocks": results,
        }
    else:
        data = fallback_data(errors, activation_logs)

    Path("data.json").write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Successfully deployed System V3.0! Output {len(data['stocks'])} signals to data.json")

if __name__ == "__main__":
    main()
