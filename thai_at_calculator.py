"""
Tính số Thái Ất - an sao và các mục tiêu tính toán theo năm Dương lịch

Các module:
  - Quẻ năm: Thái Ất, Văn Xương, Kể Định, Kể Thần
  - Toán Định, Toán Thần, Thủy Kích

Cách dùng:
  python thai_at_calculator.py --year 2026
"""

import argparse
import sys

# ============================================================
# CUNG: bàn Thái Ất 16 cung (chiều kim đồng hồ từ Tốn)
# ============================================================
CUNG_MASTER = [
    "Tốn",
    "Tỵ",
    "Ngọ",
    "Mùi",
    "Khôn",
    "Thân",
    "Dậu",
    "Tuất",
    "Càn",
    "Hợi",
    "Tý",
    "Sửu",
    "Cấn",
    "Dần",
    "Mão",
    "Thìn",
]

CUNG_INDEX = {c: i for i, c in enumerate(CUNG_MASTER)}

CUNG_CAM_KD = {"Càn", "Khôn", "Cấn", "Tốn"}

CUNG_HOP_LE = [c for c in CUNG_MASTER if c not in CUNG_CAM_KD]
CUNG_HOP_LE_INDEX = {c: i for i, c in enumerate(CUNG_HOP_LE)}

CUNG_CHINH_MAP = {
    1: "Càn",
    2: "Ngọ",
    3: "Cấn",
    4: "Mão",
    6: "Dậu",
    7: "Khôn",
    8: "Tý",
    9: "Tốn",
}
CUNG_CHINH_SO = [1, 2, 3, 4, 6, 7, 8, 9]

# Thứ tự 16 cung bắt đầu từ Thân (dùng cho Văn Xương)
VX_CUNG_ORDER = CUNG_MASTER[5:] + CUNG_MASTER[:5]
VX_STEP = {c: (2 if c in ("Càn", "Khôn") else 1) for c in VX_CUNG_ORDER}

CUNG_TEN_DAY_DU = {
    "Tốn": "Đại Quang",
    "Tỵ": "Đại thần",
    "Ngọ": "Đại uy",
    "Mùi": "Thiên đạo",
    "Khôn": "Đại vũ",
    "Thân": "Vũ đức",
    "Dậu": "Thái tộc",
    "Tuất": "Thái Âm",
    "Càn": "Đức âm",
    "Hợi": "Đại nghĩa",
    "Tý": "Đại chủ",
    "Sửu": "Dương đức",
    "Cấn": "Hòa Đức",
    "Dần": "Lã thân",
    "Mão": "Cao tùng",
    "Thìn": "Thái dương",
}

# ============================================================
# ĐỊA CHI & LỤC HỢP
# ============================================================
DIA_CHI = [
    "Tý",
    "Sửu",
    "Dần",
    "Mão",
    "Thìn",
    "Tỵ",
    "Ngọ",
    "Mùi",
    "Thân",
    "Dậu",
    "Tuất",
    "Hợi",
]

LUC_HOP = {
    "Tý": "Sửu",
    "Sửu": "Tý",
    "Dần": "Hợi",
    "Hợi": "Dần",
    "Mão": "Tuất",
    "Tuất": "Mão",
    "Thìn": "Dậu",
    "Dậu": "Thìn",
    "Tỵ": "Thân",
    "Thân": "Tỵ",
    "Ngọ": "Mùi",
    "Mùi": "Ngọ",
}

# Ánh xạ địa chi -> index trong CUNG_MASTER
DIA_CHI_CUNG_MAP = {
    "Tỵ": 1,
    "Ngọ": 2,
    "Mùi": 3,
    "Thân": 5,
    "Dậu": 6,
    "Tuất": 7,
    "Hợi": 9,
    "Tý": 10,
    "Sửu": 11,
    "Dần": 13,
    "Mão": 14,
    "Thìn": 15,
}

BASE_YEAR = 1972
BASE_TICH_TUE = 10_155_889

# ============================================================
# HÀM TIỆN ÍCH
# ============================================================


def dia_chi_cua_nam(year: int) -> str:
    return DIA_CHI[(year - 4) % 12]


def cung_index(cung: str) -> int:
    return CUNG_INDEX[cung]


def buoc_thuan(from_idx: int, steps: int, total: int = 16) -> int:
    return (from_idx + steps) % total


def buoc_nghich(from_idx: int, steps: int, total: int = 16) -> int:
    return (from_idx - steps) % total


def snap_hop_le(cung: str) -> str:
    while cung in CUNG_CAM_KD:
        cung = CUNG_MASTER[buoc_thuan(cung_index(cung), 1)]
    return cung


def khoang_cach_dia_chi(from_cung: str, to_cung: str) -> int:
    n = len(CUNG_HOP_LE)
    return (CUNG_HOP_LE_INDEX[to_cung] - CUNG_HOP_LE_INDEX[from_cung]) % n


def buoc_thuan_dia_chi(from_cung: str, steps: int) -> str:
    idx = (CUNG_HOP_LE_INDEX[from_cung] + steps) % len(CUNG_HOP_LE)
    return CUNG_HOP_LE[idx]


def buoc_nghich_dia_chi(from_cung: str, steps: int) -> str:
    idx = (CUNG_HOP_LE_INDEX[from_cung] - steps) % len(CUNG_HOP_LE)
    return CUNG_HOP_LE[idx]


def khoang_cach_16(from_idx: int, to_idx: int) -> int:
    return (to_idx - from_idx) % 16


# ============================================================
# TÍNH TOÁN CƠ BẢN
# ============================================================


def tinh_tich_tue(year: int) -> int:
    return BASE_TICH_TUE + (year - BASE_YEAR)


def tinh_ky_du(year: int) -> int:
    return tinh_tich_tue(year) % 360


def tinh_nguyen_cuc(ky_du: int) -> tuple[int, int]:
    nguyen = ky_du // 72 + 1
    cuc = ky_du % 72
    if cuc == 0:
        nguyen -= 1
        cuc = 72
    return nguyen, cuc


# ============================================================
# SAO THÁI ẤT
# ============================================================


def tinh_thai_at(ky_du: int) -> dict:
    r = ky_du % 24
    if r == 0:
        r = 24
    index = (r - 1) // 3
    nam_trong_cung = (r - 1) % 3 + 1
    so_cung = CUNG_CHINH_SO[index]
    ten_cung = CUNG_CHINH_MAP[so_cung]
    return {
        "so_cung": so_cung,
        "ten_cung": ten_cung,
        "ten_day_du": CUNG_TEN_DAY_DU[ten_cung],
        "nam_trong_cung": nam_trong_cung,
        "tong_nam": 3,
        "index": CUNG_INDEX[ten_cung],
    }


# ============================================================
# SAO VĂN XƯƠNG (Thiên Mục)
# ============================================================


def tinh_van_xuong(ky_du: int) -> dict:
    r = ky_du % 18
    if r == 0:
        r = 18
    count = 0
    for cung in VX_CUNG_ORDER:
        count += VX_STEP[cung]
        if count >= r:
            return {
                "ten_cung": cung,
                "ten_day_du": CUNG_TEN_DAY_DU[cung],
                "buoc_dem": r,
                "index": CUNG_INDEX[cung],
            }
    cung = "Khôn"
    return {
        "ten_cung": cung,
        "ten_day_du": CUNG_TEN_DAY_DU[cung],
        "buoc_dem": r,
        "index": CUNG_INDEX[cung],
    }


# ============================================================
# KỂ ĐỊNH (Định Mục)
# ============================================================


def tinh_ke_dinh(ky_du: int, thai_tue: str, van_xuong: dict) -> dict:
    than_hop = LUC_HOP[thai_tue]
    vx_dc = snap_hop_le(van_xuong["ten_cung"])
    buoc = khoang_cach_dia_chi(than_hop, vx_dc) + 1
    ket_qua = buoc_thuan_dia_chi(thai_tue, buoc - 1)

    return {
        "than_hop": than_hop,
        "buoc": buoc,
        "ten_cung": ket_qua,
        "ten_day_du": CUNG_TEN_DAY_DU[ket_qua],
        "index": CUNG_INDEX[ket_qua],
        "canh_bao": "",
    }


# ============================================================
# KỂ THẦN
# ============================================================


def tinh_ke_than(ky_du: int) -> dict:
    r = ky_du % 12
    if r == 0:
        r = 12
    idx = (CUNG_HOP_LE_INDEX["Dần"] - (r - 1)) % len(CUNG_HOP_LE)
    cung = CUNG_HOP_LE[idx]
    return {
        "du": r,
        "ten_cung": cung,
        "ten_day_du": CUNG_TEN_DAY_DU[cung],
        "index": CUNG_INDEX[cung],
    }


# ============================================================
# TOÁN ĐỊNH
# ============================================================


def tinh_toan_dinh(thai_at: dict, ke_dinh: dict) -> int:
    ta_idx = thai_at["index"]
    kd_idx = ke_dinh["index"]
    return (ta_idx - kd_idx - 1) % 16


# ============================================================
# TOÁN THẦN
# ============================================================


def tinh_toan_than(thai_at: dict, ke_than: dict) -> int:
    ta_idx = thai_at["index"]
    kt_idx = ke_than["index"]
    return (ta_idx - kt_idx - 1) % 16


# ============================================================
# BIỆT SỐ (dùng cho Toán Chủ / Toán Khách)
# ============================================================
BIET_SO = {
    "Càn": 1,
    "Ngọ": 2,
    "Cấn": 3,
    "Mão": 4,
    "Dậu": 6,
    "Khôn": 7,
    "Tý": 8,
    "Tốn": 9,
}
CUNG_CHINH_NAMES = set(BIET_SO.keys())

BIET_SO_CUNG = {v: k for k, v in BIET_SO.items()}
BIET_SO_CUNG[5] = "Cung giữa"


def giam_toan(so: int) -> int:
    if so % 10 == 0:
        return so // 10
    if so > 10:
        return so % 10
    return so


# ============================================================
# TOÁN CHỦ & CHỦ ĐẠI TƯỚNG
# ============================================================


def tinh_toan_chu(thai_at: dict, van_xuong: dict) -> int:
    vx_idx = van_xuong["index"]
    ta_idx = thai_at["index"]

    if vx_idx == ta_idx:
        cung = CUNG_MASTER[vx_idx]
        return BIET_SO[cung] if cung in CUNG_CHINH_NAMES else 1

    truoc_ta_idx = (ta_idx - 1) % 16

    tong = 0
    idx = vx_idx
    while True:
        cung = CUNG_MASTER[idx]
        if cung in CUNG_CHINH_NAMES:
            tong += BIET_SO[cung]
        elif idx == vx_idx:
            tong += 1

        if idx == truoc_ta_idx:
            break
        idx = (idx + 1) % 16

    return tong


def tinh_chu_dai_tuong(toan_chu: int) -> dict:
    so = giam_toan(toan_chu)

    if so == 5:
        return {
            "biet_so": 5,
            "ten_cung": "Cung giữa",
            "ten_day_du": "",
        }

    ten = BIET_SO_CUNG.get(so)
    if ten is None:
        return {"biet_so": so, "ten_cung": f"Không xác định", "ten_day_du": ""}

    return {
        "biet_so": so,
        "ten_cung": ten,
        "ten_day_du": CUNG_TEN_DAY_DU.get(ten, ""),
    }


def tinh_chu_tham_tuong(chu_dai_tuong: dict) -> dict:
    bs = chu_dai_tuong["biet_so"]
    so = giam_toan(bs * 3)

    if so == 5:
        return {"biet_so": 5, "ten_cung": "Cung giữa", "ten_day_du": ""}

    ten = BIET_SO_CUNG.get(so)
    if ten is None:
        return {"biet_so": so, "ten_cung": f"Không xác định", "ten_day_du": ""}

    return {
        "biet_so": so,
        "ten_cung": ten,
        "ten_day_du": CUNG_TEN_DAY_DU.get(ten, ""),
    }


# ============================================================
# TOÁN KHÁCH & KHÁCH ĐẠI TƯỚNG
# ============================================================


def tinh_toan_khach(thai_at: dict, thuy_kich: dict) -> int:
    tk_idx = thuy_kich["index"]
    ta_idx = thai_at["index"]

    if tk_idx == ta_idx:
        cung = CUNG_MASTER[tk_idx]
        return BIET_SO[cung] if cung in CUNG_CHINH_NAMES else 1

    truoc_ta_idx = (ta_idx - 1) % 16

    tong = 0
    idx = tk_idx
    while True:
        cung = CUNG_MASTER[idx]
        if cung in CUNG_CHINH_NAMES:
            tong += BIET_SO[cung]
        elif idx == tk_idx:
            tong += 1

        if idx == truoc_ta_idx:
            break
        idx = (idx + 1) % 16

    return tong


def tinh_khach_dai_tuong(toan_khach: int) -> dict:
    so = giam_toan(toan_khach)

    if so == 5:
        return {
            "biet_so": 5,
            "ten_cung": "Cung giữa",
            "ten_day_du": "",
        }

    ten = BIET_SO_CUNG.get(so)
    if ten is None:
        return {"biet_so": so, "ten_cung": f"Không xác định", "ten_day_du": ""}

    return {
        "biet_so": so,
        "ten_cung": ten,
        "ten_day_du": CUNG_TEN_DAY_DU.get(ten, ""),
    }


def tinh_khach_tham_tuong(khach_dai_tuong: dict) -> dict:
    bs = khach_dai_tuong["biet_so"]
    so = giam_toan(bs * 3)

    if so == 5:
        return {"biet_so": 5, "ten_cung": "Cung giữa", "ten_day_du": ""}

    ten = BIET_SO_CUNG.get(so)
    if ten is None:
        return {"biet_so": so, "ten_cung": f"Không xác định", "ten_day_du": ""}

    return {
        "biet_so": so,
        "ten_cung": ten,
        "ten_day_du": CUNG_TEN_DAY_DU.get(ten, ""),
    }


# ============================================================
# THỦY KÍCH (Địa Mục)
# ============================================================


def tinh_thuy_kich(ke_than: dict, van_xuong: dict, la_am_cuc: bool = False) -> dict:
    kt_idx = ke_than["index"]
    vx_idx = van_xuong["index"]

    so_cung = 0
    idx = kt_idx
    while True:
        cung = CUNG_MASTER[idx]
        so_cung += 2 if cung in ("Càn", "Khôn") else 1
        if idx == vx_idx:
            break
        idx = buoc_thuan(idx, 1)

    if la_am_cuc:
        raw_idx = buoc_nghich(CUNG_INDEX["Khôn"], so_cung - 1)
    else:
        raw_idx = buoc_thuan(CUNG_INDEX["Cấn"], so_cung - 1)

    cung = CUNG_MASTER[raw_idx]
    return {
        "so_cung": so_cung,
        "ten_cung": cung,
        "ten_day_du": CUNG_TEN_DAY_DU[cung],
        "index": raw_idx,
    }


# ============================================================
# TỔNG HỢP
# ============================================================


def tinh(year: int) -> dict:
    tich_tue = tinh_tich_tue(year)
    ky_du = tinh_ky_du(year)
    nguyen, cuc = tinh_nguyen_cuc(ky_du)

    thai_tue = dia_chi_cua_nam(year)

    thai_at = tinh_thai_at(ky_du)
    van_xuong = tinh_van_xuong(ky_du)
    ke_dinh = tinh_ke_dinh(ky_du, thai_tue, van_xuong)
    ke_than = tinh_ke_than(ky_du)
    toan_dinh = tinh_toan_dinh(thai_at, ke_dinh)
    toan_than = tinh_toan_than(thai_at, ke_than)
    thuy_kich = tinh_thuy_kich(ke_than, van_xuong)

    toan_chu = tinh_toan_chu(thai_at, van_xuong)
    chu_dai_tuong = tinh_chu_dai_tuong(toan_chu)
    chu_tham_tuong = tinh_chu_tham_tuong(chu_dai_tuong)

    toan_khach = tinh_toan_khach(thai_at, thuy_kich)
    khach_dai_tuong = tinh_khach_dai_tuong(toan_khach)
    khach_tham_tuong = tinh_khach_tham_tuong(khach_dai_tuong)

    return {
        "nam": year,
        "thai_tue": thai_tue,
        "tich_tue": tich_tue,
        "ky_du": ky_du,
        "nguyen": nguyen,
        "cuc": cuc,
        "thai_at": thai_at,
        "van_xuong": van_xuong,
        "ke_dinh": ke_dinh,
        "ke_than": ke_than,
        "toan_dinh": toan_dinh,
        "toan_than": toan_than,
        "thuy_kich": thuy_kich,
        "toan_chu": toan_chu,
        "chu_dai_tuong": chu_dai_tuong,
        "chu_tham_tuong": chu_tham_tuong,
        "toan_khach": toan_khach,
        "khach_dai_tuong": khach_dai_tuong,
        "khach_tham_tuong": khach_tham_tuong,
    }


# ============================================================
# HIỂN THỊ
# ============================================================


def in_ket_qua(kq: dict) -> None:
    print("=" * 52)
    print(f"  TÍNH SỐ THÁI ẤT - NĂM {kq['nam']} ({kq['thai_tue']})")
    print("=" * 52)
    print(f"  Tích Tuế      : {kq['tich_tue']:,}")
    print(f"  Kỷ dư         : {kq['ky_du']}")
    print(f"  Nguyên        : {kq['nguyen']}")
    print(f"  Cục           : {kq['cuc']}")
    print()

    ta = kq["thai_at"]
    vx = kq["van_xuong"]
    kd = kq["ke_dinh"]
    kt = kq["ke_than"]
    tk = kq["thuy_kich"]

    print(f"  ▶ SAO THÁI ẤT")
    print(f"    Cung         : {ta['so_cung']} - {ta['ten_cung']} ({ta['ten_day_du']})")
    print(f"    Năm thứ      : {ta['nam_trong_cung']}/{ta['tong_nam']}")
    print()
    print(f"  ▶ SAO VĂN XƯƠNG (Thiên Mục)")
    print(f"    Cung         : {vx['ten_cung']} ({vx['ten_day_du']})")
    print(f"    Bước đếm     : {vx['buoc_dem']}")
    print()
    print(f"  ▶ KỂ ĐỊNH (Định Mục)")
    print(f"    Thần hợp     : {kd['than_hop']}")
    print(f"    Bước đếm     : {kd['buoc']} (từ {kd['than_hop']} → {vx['ten_cung']})")
    print(f"    Cung         : {kd['ten_cung']} ({kd['ten_day_du']})")
    print()
    print(f"  ▶ KỂ THẦN")
    print(f"    Số dư 12     : {kt['du']}")
    print(f"    Cung         : {kt['ten_cung']} ({kt['ten_day_du']})")
    print()
    print(f"  ▶ TOÁN ĐỊNH")
    print(f"    Số toán      : {kq['toan_dinh']}")
    print()
    print(f"  ▶ TOÁN THẦN")
    print(f"    Số toán      : {kq['toan_than']}")
    print()
    print(f"  ▶ THỦY KÍCH (Địa Mục)")
    print(
        f"    Số cung      : {tk['so_cung']} (từ {kt['ten_cung']} → {vx['ten_cung']})"
    )
    print(f"    Cung         : {tk['ten_cung']} ({tk['ten_day_du']})")
    print()
    print("=" * 52)
    print()

    tc = kq["toan_chu"]
    cdt = kq["chu_dai_tuong"]
    ctt = kq["chu_tham_tuong"]
    print(f"  ▶ TOÁN CHỦ")
    print(f"    Số toán      : {tc}")
    print(
        f"    Chủ Đại Tướng: cung {cdt['biet_so']} - {cdt['ten_cung']} ({cdt['ten_day_du']})"
    )
    print(
        f"    Chủ Tham Tướng: cung {ctt['biet_so']} - {ctt['ten_cung']} ({ctt['ten_day_du']})"
    )
    print()

    so_toan_khach = kq["toan_khach"]
    kdt = kq["khach_dai_tuong"]
    ktt = kq["khach_tham_tuong"]
    print(f"  ▶ TOÁN KHÁCH")
    print(f"    Số toán      : {so_toan_khach}")
    print(
        f"    Khách Đại Tướng: cung {kdt['biet_so']} - {kdt['ten_cung']} ({kdt['ten_day_du']})"
    )
    print(
        f"    Khách Tham Tướng: cung {ktt['biet_so']} - {ktt['ten_cung']} ({ktt['ten_day_du']})"
    )
    print("=" * 52)


# ============================================================
# MAIN
# ============================================================


def main():
    if sys.stdout.encoding and sys.stdout.encoding.upper() not in ("UTF-8", "UTF8"):
        try:
            sys.stdout.reconfigure(encoding="utf-8")
        except Exception:
            pass

    parser = argparse.ArgumentParser(
        description="Tính số Thái Ất - an sao Thái Ất, Văn Xương, Kể Định, Kể Thần, Thủy Kích"
    )
    parser.add_argument(
        "--year", type=int, required=True, help="Năm Dương lịch cần tính"
    )
    args = parser.parse_args()

    ket_qua = tinh(args.year)
    in_ket_qua(ket_qua)


if __name__ == "__main__":
    main()
