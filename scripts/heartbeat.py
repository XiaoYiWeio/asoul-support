#!/usr/bin/env python3
"""
A-SOUL 直播心跳挂机 — 检测成员开播 → 模拟观看涨亲密度。
每 5 分钟观看 +6 亲密度，25 分钟挂满 30 亲密度/天/成员。
需要成员正在直播才有效。零外部依赖，纯标准库。
"""

import argparse
import json
import os
import sys
import time
import urllib.request
import urllib.parse
from pathlib import Path
from typing import Optional, Dict, List

_UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"

MEMBERS = [
    {"name": "嘉然",   "uid": 672328094,         "room": 22637261},
    {"name": "贝拉",   "uid": 672353429,         "room": 22632424},
    {"name": "乃琳",   "uid": 672342685,         "room": 22625027},
    {"name": "心宜",   "uid": 3537115310721181,  "room": 30849777},
    {"name": "思诺",   "uid": 3537115310721781,  "room": 30858592},
]

WATCH_MINUTES = 25
HEARTBEAT_INTERVAL = 60

_COOKIE_PATHS = [
    Path(__file__).resolve().parent.parent / ".cookies.json",
    Path(__file__).resolve().parent.parent.parent / "bilibili-live-checkin" / ".cookies.json",
]


def load_cookies() -> Optional[Dict[str, str]]:
    for p in _COOKIE_PATHS:
        if p.exists():
            try:
                with open(p, "r") as f:
                    data = json.load(f)
                if data.get("SESSDATA") and data.get("bili_jct"):
                    return data
            except Exception:
                continue
    return None


def _make_headers(sessdata: str, bili_jct: str, referer: str = "https://live.bilibili.com") -> dict:
    return {
        "User-Agent": _UA,
        "Cookie": f"SESSDATA={sessdata}; bili_jct={bili_jct}",
        "Origin": "https://live.bilibili.com",
        "Referer": referer,
    }


def _get_json(url: str, headers: dict, timeout: int = 10) -> Optional[dict]:
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except Exception:
        return None


def _post_form(url: str, data: dict, headers: dict, timeout: int = 10) -> Optional[dict]:
    form = urllib.parse.urlencode(data).encode("utf-8")
    headers = {**headers, "Content-Type": "application/x-www-form-urlencoded"}
    req = urllib.request.Request(url, data=form, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except Exception as e:
        return {"code": -1, "message": str(e)}


# ──────────────────────────────────────────
# Live Status Detection
# ──────────────────────────────────────────

def check_live_status(room_ids: List[int], sessdata: str, bili_jct: str) -> Dict[int, Dict]:
    """批量查询直播间状态，返回 {room_id: {live_status, title, ...}}"""
    uids = ",".join(str(m["uid"]) for m in MEMBERS if m["room"] in room_ids)
    url = f"https://api.live.bilibili.com/room/v1/Room/get_status_info_by_uids"
    headers = _make_headers(sessdata, bili_jct)
    data = {"uids[]": [str(m["uid"]) for m in MEMBERS if m["room"] in room_ids]}

    form_parts = []
    for m in MEMBERS:
        if m["room"] in room_ids:
            form_parts.append(f"uids[]={m['uid']}")
    form_body = "&".join(form_parts).encode("utf-8")

    headers_with_ct = {**headers, "Content-Type": "application/x-www-form-urlencoded"}
    req = urllib.request.Request(url, data=form_body, headers=headers_with_ct)

    result = {}
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            body = json.loads(resp.read().decode("utf-8"))
        if body.get("code") == 0 and body.get("data"):
            uid_to_room = {m["uid"]: m["room"] for m in MEMBERS}
            for uid_str, info in body["data"].items():
                uid = int(uid_str)
                if uid in uid_to_room:
                    result[uid_to_room[uid]] = {
                        "live_status": info.get("live_status", 0),
                        "title": info.get("title", ""),
                        "area_name": info.get("area_v2_name", ""),
                    }
    except Exception:
        pass

    for room_id in room_ids:
        if room_id not in result:
            info = _get_single_room_status(room_id, sessdata, bili_jct)
            if info:
                result[room_id] = info

    return result


def _get_single_room_status(room_id: int, sessdata: str, bili_jct: str) -> Optional[Dict]:
    url = f"https://api.live.bilibili.com/room/v1/Room/get_info?room_id={room_id}"
    headers = _make_headers(sessdata, bili_jct)
    resp = _get_json(url, headers)
    if resp and resp.get("code") == 0:
        data = resp["data"]
        return {
            "live_status": data.get("live_status", 0),
            "title": data.get("title", ""),
            "area_name": data.get("area_name", ""),
        }
    return None


# ──────────────────────────────────────────
# Room Entry & Heartbeat
# ──────────────────────────────────────────

def enter_room(room_id: int, sessdata: str, bili_jct: str) -> bool:
    url = "https://api.live.bilibili.com/xlive/web-room/v1/index/roomEntryAction"
    headers = _make_headers(sessdata, bili_jct, f"https://live.bilibili.com/{room_id}")
    data = {
        "room_id": str(room_id),
        "platform": "pc",
        "csrf": bili_jct,
        "csrf_token": bili_jct,
    }
    resp = _post_form(url, data, headers)
    return resp is not None and resp.get("code") == 0


def send_web_heartbeat(room_id: int, sessdata: str, bili_jct: str) -> bool:
    """发送 web 端心跳，维持"观看中"状态"""
    url = "https://api.live.bilibili.com/User/userOnlineHeart"
    headers = _make_headers(sessdata, bili_jct, f"https://live.bilibili.com/{room_id}")
    data = {
        "csrf": bili_jct,
        "csrf_token": bili_jct,
    }
    resp = _post_form(url, data, headers)
    if resp and resp.get("code") == 0:
        return True

    url2 = "https://api.live.bilibili.com/relation/v1/Feed/heartBeat"
    resp2 = _post_form(url2, data, headers)
    return resp2 is not None and resp2.get("code") == 0


# ──────────────────────────────────────────
# Fan Medal (from checkin.py)
# ──────────────────────────────────────────

def wear_medal(medal_id: int, sessdata: str, bili_jct: str) -> bool:
    url = "https://api.live.bilibili.com/xlive/web-room/v1/fansMedal/wear"
    headers = _make_headers(sessdata, bili_jct)
    data = {"medal_id": str(medal_id), "csrf": bili_jct, "csrf_token": bili_jct}
    resp = _post_form(url, data, headers)
    return resp is not None and resp.get("code") == 0


def get_my_medals(sessdata: str, bili_jct: str) -> Dict[int, Dict]:
    medals = {}
    page = 1
    while True:
        url = f"https://api.live.bilibili.com/xlive/app-ucenter/v1/fansMedal/panel?page={page}&page_size=50"
        headers = _make_headers(sessdata, bili_jct)
        resp = _get_json(url, headers)
        if not resp or resp.get("code") != 0:
            break
        data = resp.get("data", {})
        for item in (data.get("special_list", []) or []) + (data.get("list", []) or []):
            info = item.get("medal", item)
            target_id = info.get("target_id", 0)
            if target_id:
                medals[target_id] = {
                    "medal_id": info.get("medal_id"),
                    "medal_name": info.get("medal_name", ""),
                    "level": info.get("level", 0),
                    "today_intimacy": info.get("today_feed", info.get("today_intimacy", 0)),
                    "day_limit": info.get("day_limit", 0),
                }
        total_page = data.get("page_info", {}).get("total_page", 1)
        if page >= total_page:
            break
        page += 1
    return medals


# ──────────────────────────────────────────
# Watch Loop
# ──────────────────────────────────────────

def watch_room(member: Dict, sessdata: str, bili_jct: str,
               duration_min: int = WATCH_MINUTES, interval: int = HEARTBEAT_INTERVAL) -> Dict:
    """对一个直播间进行心跳挂机"""
    room_id = member["room"]
    name = member["name"]
    total_beats = (duration_min * 60) // interval

    entered = enter_room(room_id, sessdata, bili_jct)
    if not entered:
        return {"name": name, "room": room_id, "success": False, "error": "进入直播间失败",
                "beats_ok": 0, "beats_total": total_beats, "minutes": 0}

    print(f"    ⏱  开始挂机 {duration_min} 分钟（每 {interval}s 心跳一次，共 {total_beats} 次）...",
          file=sys.stderr)

    beats_ok = 0
    for i in range(total_beats):
        ok = send_web_heartbeat(room_id, sessdata, bili_jct)
        if ok:
            beats_ok += 1
        elapsed_min = ((i + 1) * interval) // 60
        if (i + 1) % 5 == 0 or i == total_beats - 1:
            print(f"    💓 心跳 {i+1}/{total_beats}  已挂 {elapsed_min} 分钟", file=sys.stderr)
        if i < total_beats - 1:
            time.sleep(interval)

    actual_minutes = (total_beats * interval) // 60
    return {
        "name": name,
        "room": room_id,
        "success": beats_ok > 0,
        "beats_ok": beats_ok,
        "beats_total": total_beats,
        "minutes": actual_minutes,
    }


def format_output(live_results: List[Dict], offline_members: List[str],
                  medal_info: Dict[int, Dict], members: List[Dict]) -> str:
    lines = ["🌟 A-SOUL 直播心跳挂机结果", ""]

    if live_results:
        lines.append("  📺 在播成员：")
        for r in live_results:
            uid = next((m["uid"] for m in members if m["name"] == r["name"]), 0)
            medal = medal_info.get(uid)
            medal_str = f"  🏅{medal['medal_name']}Lv{medal['level']}" if medal else ""
            intimacy_str = ""
            if medal:
                intimacy_str = f"  今日亲密度:{medal['today_intimacy']}"

            if r["success"]:
                lines.append(
                    f"    ✅ {r['name']}{medal_str}  — 挂机 {r['minutes']}min"
                    f"  💓{r['beats_ok']}/{r['beats_total']}{intimacy_str}"
                )
            else:
                lines.append(f"    ❌ {r['name']}  — {r.get('error', '心跳失败')}")

    if offline_members:
        lines.append("")
        lines.append(f"  💤 未开播：{', '.join(offline_members)}")

    lines.append("")
    if live_results:
        ok_count = sum(1 for r in live_results if r["success"])
        lines.append(f"📊 在播 {len(live_results)} 人，挂机成功 {ok_count} 人")
        lines.append("⚠️  亲密度是否实际增长请到 B 站粉丝牌页面确认")
    else:
        lines.append("ℹ️  当前没有成员在播，本次跳过")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="A-SOUL 直播心跳挂机（检测开播 → 模拟观看涨亲密度）",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 检测所有成员，在播的自动挂机 25 分钟
  python3 heartbeat.py

  # 只检测嘉然和贝拉
  python3 heartbeat.py --members 嘉然,贝拉

  # 只检测开播状态，不挂机
  python3 heartbeat.py --check-only

  # 自定义挂机时长
  python3 heartbeat.py --duration 30
""",
    )
    parser.add_argument("--members", help="指定成员（逗号分隔）")
    parser.add_argument("--duration", type=int, default=WATCH_MINUTES,
                        help=f"挂机时长（分钟，默认 {WATCH_MINUTES}）")
    parser.add_argument("--interval", type=int, default=HEARTBEAT_INTERVAL,
                        help=f"心跳间隔（秒，默认 {HEARTBEAT_INTERVAL}）")
    parser.add_argument("--check-only", action="store_true",
                        help="只检测开播状态，不挂机")
    parser.add_argument("--sessdata", help="SESSDATA cookie")
    parser.add_argument("--bili-jct", help="bili_jct cookie")
    parser.add_argument("--json", action="store_true", help="JSON 输出")
    args = parser.parse_args()

    sessdata = args.sessdata
    bili_jct = args.bili_jct
    if not sessdata or not bili_jct:
        saved = load_cookies()
        if saved:
            sessdata = saved["SESSDATA"]
            bili_jct = saved["bili_jct"]
        else:
            print("❌ 没有找到 Cookie。")
            sys.exit(1)

    targets = MEMBERS
    if args.members:
        names = [n.strip() for n in args.members.split(",")]
        targets = [m for m in MEMBERS if m["name"] in names]
        if not targets:
            print(f"❌ 未找到成员: {args.members}")
            sys.exit(1)

    print("  📡 正在检测直播状态...", file=sys.stderr)
    room_ids = [m["room"] for m in targets]
    statuses = check_live_status(room_ids, sessdata, bili_jct)

    live_members = []
    offline_names = []
    for m in targets:
        status = statuses.get(m["room"], {})
        if status.get("live_status") == 1:
            live_members.append(m)
            title = status.get("title", "")
            print(f"  🔴 {m['name']} 正在直播：{title}", file=sys.stderr)
        else:
            offline_names.append(m["name"])
            print(f"  ⚫ {m['name']} 未开播", file=sys.stderr)

    if args.check_only:
        if args.json:
            result = {
                "live": [{"name": m["name"], "room": m["room"],
                          "title": statuses.get(m["room"], {}).get("title", "")}
                         for m in live_members],
                "offline": offline_names,
            }
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            if live_members:
                print(f"\n🔴 在播：{', '.join(m['name'] for m in live_members)}")
            if offline_names:
                print(f"⚫ 未开播：{', '.join(offline_names)}")
        return

    if not live_members:
        print("\nℹ️  当前没有成员在播，本次跳过")
        return

    print("  🏅 正在获取粉丝牌信息...", file=sys.stderr)
    medals = get_my_medals(sessdata, bili_jct)

    live_results = []
    for i, m in enumerate(live_members):
        print(f"\n  📺 [{i+1}/{len(live_members)}] {m['name']} 直播间 {m['room']}", file=sys.stderr)

        if m["uid"] in medals:
            medal = medals[m["uid"]]
            worn = wear_medal(medal["medal_id"], sessdata, bili_jct)
            if worn:
                print(f"    🏅 已佩戴 {medal['medal_name']}Lv{medal['level']}", file=sys.stderr)
            time.sleep(1)

        result = watch_room(m, sessdata, bili_jct,
                            duration_min=args.duration, interval=args.interval)
        live_results.append(result)

        if i < len(live_members) - 1:
            time.sleep(3)

    if args.json:
        print(json.dumps({"results": live_results, "offline": offline_names},
                          ensure_ascii=False, indent=2))
    else:
        print("")
        print(format_output(live_results, offline_names, medals, targets))


if __name__ == "__main__":
    main()
