#!/usr/bin/env python3
"""
ASCII Monitor Geometry Viewer — Windows Edition
Detects all monitors via Win32 API and draws them in the terminal.
"""

import math
import os
import sys
import shutil
import ctypes
from ctypes import wintypes

# ── Win32 structs ────────────────────────────────────────────────────────────

class RECT(ctypes.Structure):
    _fields_ = [("left", ctypes.c_long), ("top", ctypes.c_long),
                ("right", ctypes.c_long), ("bottom", ctypes.c_long)]

class MONITORINFOEX(ctypes.Structure):
    _fields_ = [("cbSize", wintypes.DWORD),
                ("rcMonitor", RECT),
                ("rcWork", RECT),
                ("dwFlags", wintypes.DWORD),
                ("szDevice", ctypes.c_wchar * 32)]

MONITORENUMPROC = ctypes.WINFUNCTYPE(
    ctypes.c_bool,
    ctypes.c_ulong,   # hMonitor
    ctypes.c_ulong,   # hdcMonitor
    ctypes.POINTER(RECT),
    ctypes.c_double   # dwData
)

MONITORINFOF_PRIMARY = 0x00000001

# ── Monitor detection ────────────────────────────────────────────────────────

def get_monitors():
    user32 = ctypes.windll.user32
    monitors = []

    def callback(hMonitor, hdcMonitor, lprcMonitor, dwData):
        info = MONITORINFOEX()
        info.cbSize = ctypes.sizeof(MONITORINFOEX)
        if user32.GetMonitorInfoW(hMonitor, ctypes.byref(info)):
            r = info.rcMonitor
            w = r.right  - r.left
            h = r.bottom - r.top
            name = info.szDevice.strip()
            is_primary = bool(info.dwFlags & MONITORINFOF_PRIMARY)
            monitors.append({
                "name":    name,
                "w":       w,
                "h":       h,
                "x":       r.left,
                "y":       r.top,
                "primary": is_primary,
            })
        return True

    proc = MONITORENUMPROC(callback)
    user32.EnumDisplayMonitors(None, None, proc, 0)

    # Sort: primary first, then left-to-right, top-to-bottom
    monitors.sort(key=lambda m: (not m["primary"], m["x"], m["y"]))
    return monitors

# ── Canvas drawing ───────────────────────────────────────────────────────────

def draw_monitors(monitors):
    TERM_W, TERM_H = shutil.get_terminal_size((120, 40))
    CANVAS_W = min(TERM_W - 4, 108)
    CANVAS_H = 30

    all_x = [m["x"] for m in monitors] + [m["x"] + m["w"] for m in monitors]
    all_y = [m["y"] for m in monitors] + [m["y"] + m["h"] for m in monitors]
    px_min_x, px_max_x = min(all_x), max(all_x)
    px_min_y, px_max_y = min(all_y), max(all_y)
    px_w = px_max_x - px_min_x or 1
    px_h = px_max_y - px_min_y or 1

    scale_x = (CANVAS_W - 4) / px_w
    scale_y = (CANVAS_H - 4) / px_h
    scale   = min(scale_x, scale_y) * 0.90

    def col(px): return int((px - px_min_x) * scale) + 2
    def row(py): return int((py - px_min_y) * scale) + 1

    grid = [[" "] * CANVAS_W for _ in range(CANVAS_H)]

    def put(r, c, ch):
        if 0 <= r < CANVAS_H and 0 <= c < CANVAS_W:
            grid[r][c] = ch

    def hline(r, c1, c2, ch):
        for c in range(c1, c2 + 1): put(r, c, ch)

    def vline(c, r1, r2, ch):
        for r in range(r1, r2 + 1): put(r, c, ch)

    def text(r, c, s, max_w=None):
        s = s[:max_w] if max_w else s
        for i, ch in enumerate(s): put(r, c + i, ch)

    for idx, m in enumerate(monitors):
        r1 = row(m["y"]);       r2 = row(m["y"] + m["h"]) - 1
        c1 = col(m["x"]);       c2 = col(m["x"] + m["w"]) - 1
        r2 = max(r1 + 4, r2);  c2 = max(c1 + 10, c2)

        # Box walls
        put(r1, c1, "╔"); put(r1, c2, "╗")
        put(r2, c1, "╚"); put(r2, c2, "╝")
        hline(r1, c1+1, c2-1, "═")
        hline(r2, c1+1, c2-1, "═")
        vline(c1, r1+1, r2-1, "║")
        vline(c2, r1+1, r2-1, "║")

        iw = c2 - c1 - 2   # inner width
        ih = r2 - r1 - 2   # inner height
        mr = r1 + 1 + ih // 2

        name_label = ("* " if m["primary"] else "  ") + m["name"]
        res_label  = f"{m['w']} x {m['h']}"
        pos_label  = f"x={m['x']},  y={m['y']}"
        ori_label  = "Portrait" if m["h"] > m["w"] else "Landscape"

        rows_needed = 4
        start_r = mr - rows_needed // 2

        if ih >= 1: text(start_r,     c1+1, name_label[:iw])
        if ih >= 2: text(start_r + 1, c1+1, res_label[:iw])
        if ih >= 3: text(start_r + 2, c1+1, pos_label[:iw])
        if ih >= 4: text(start_r + 3, c1+1, ori_label[:iw])

        text(r1, c1+1, f"[{idx+1}]")

    return ["  " + "".join(row) for row in grid]

# ── Info table ───────────────────────────────────────────────────────────────

def print_table(monitors):
    COL_W = [3, 24, 7, 7, 8, 8, 11, 9, 10]
    HDR   = ["#", "Device", "Width", "Height", "X", "Y", "Resolution", "Aspect", "Orient."]

    top = "+-".join("-" * w for w in COL_W)
    sep = "+-".join("-" * w for w in COL_W)

    def rowfmt(cells):
        parts = [str(c).ljust(w) for c, w in zip(cells, COL_W)]
        return "| " + " | ".join(parts) + " |"

    def divider(left, mid, right):
        parts = ["-" * (w + 2) for w in COL_W]
        return left + (mid).join(parts) + right

    print("  " + divider("+", "+", "+"))
    print("  " + rowfmt(HDR))
    print("  " + divider("+", "+", "+"))
    for i, m in enumerate(monitors, 1):
        gcd  = math.gcd(m["w"], m["h"])
        ar   = f"{m['w']//gcd}:{m['h']//gcd}"
        ori  = "Portrait" if m["h"] > m["w"] else "Landscape"
        name = ("*" + m["name"] if m["primary"] else m["name"])[:22]
        print("  " + rowfmt([i, name, m["w"], m["h"], m["x"], m["y"],
                              f"{m['w']}x{m['h']}", ar, ori]))
    print("  " + divider("+", "+", "+"))

# ── Summary ───────────────────────────────────────────────────────────────────

def print_summary(monitors):
    span_w = max(m["x"] + m["w"] for m in monitors) - min(m["x"] for m in monitors)
    span_h = max(m["y"] + m["h"] for m in monitors) - min(m["y"] for m in monitors)
    total  = sum(m["w"] * m["h"] for m in monitors)
    prim   = next((m["name"] for m in monitors if m["primary"]), "?")
    print(f"\n  Monitors found   : {len(monitors)}")
    print(f"  Primary          : {prim}")
    print(f"  Desktop span     : {span_w} x {span_h} px")
    print(f"  Total pixel area : {total:,} px^2")
    print(f"  Portrait screens : {sum(1 for m in monitors if m['h'] > m['w'])}")

# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    if sys.platform != "win32":
        print("  This script uses the Windows API (ctypes.windll).")
        print("  Run it on Windows.")
        sys.exit(1)

    try:
        monitors = get_monitors()
    except Exception as e:
        print(f"  Error reading monitors: {e}")
        sys.exit(1)

    if not monitors:
        print("  No monitors detected.")
        sys.exit(1)

    TERM_W = shutil.get_terminal_size((100, 40)).columns
    title  = "  ASCII MONITOR GEOMETRY VIEWER  "
    pad    = (TERM_W - len(title)) // 2
    bar    = "=" * pad + title + "=" * max(0, TERM_W - pad - len(title))
    print(bar)
    print()

    for line in draw_monitors(monitors):
        print(line)
    print()

    print_table(monitors)
    print_summary(monitors)
    print()

if __name__ == "__main__":
    main()