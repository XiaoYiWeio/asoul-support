#!/usr/bin/env python3
"""
A-SOUL 直播间批量弹幕签到。
内置全部现役成员直播间，一键签到。
零外部依赖，纯标准库。
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
_SEND_URL = "https://api.live.bilibili.com/msg/send"

MEMBERS = [
    {"name": "嘉然",   "uid": 672328094,         "room": 22637261},
    {"name": "贝拉",   "uid": 672353429,         "room": 22632424},
    {"name": "乃琳",   "uid": 672342685,         "room": 22625027},
    {"name": "心宜",   "uid": 3537115310721181,  "room": 30849777},
    {"name": "思诺",   "uid": 3537115310721781,  "room": 30858592},
]

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


def save_cookies(sessdata: str, bili_jct: str):
    path = _COOKIE_PATHS[0]
    with open(path, "w") as f:
        json.dump({"SESSDATA": sessdata, "bili_jct": bili_jct}, f)
    os.chmod(path, 0o600)
    print(f"💾 Cookie 已保存到 {path}")


def send_danmaku(room_id: int, msg: str, sessdata: str, bili_jct: str) -> Dict:
    form_data = urllib.parse.urlencode({
        "bubble": "0",
        "msg": msg,
        "color": "16777215",
        "mode": "1",
        "room_type": "0",
        "jumpfrom": "0",
        "reply_mid": "0",
        "reply_attr": "0",
        "replay_dmid": "",
        "statistics": json.dumps({"appId": 100, "platform": 5}),
        "fontsize": "25",
        "rnd": str(int(time.time())),
        "roomid": str(room_id),
        "csrf": bili_jct,
        "csrf_token": bili_jct,
    }).encode("utf-8")

    headers = {
        "User-Agent": _UA,
        "Content-Type": "application/x-www-form-urlencoded",
        "Cookie": f"SESSDATA={sessdata}; bili_jct={bili_jct}",
        "Origin": "https://live.bilibili.com",
        "Referer": f"https://live.bilibili.com/{room_id}",
    }

    req = urllib.request.Request(_SEND_URL, data=form_data, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        return {"code": e.code, "message": f"HTTP {e.code}", "data": body}
    except Exception as e:
        return {"code": -1, "message": str(e)}


def batch_checkin(members: List[Dict], msg: str, sessdata: str, bili_jct: str) -> List[Dict]:
    results = []
    for m in members:
        resp = send_danmaku(m["room"], msg, sessdata, bili_jct)
        success = resp.get("code") == 0
        results.append({
            "name": m["name"],
            "room": m["room"],
            "url": f"https://live.bilibili.com/{m['room']}",
            "msg": msg,
            "success": success,
            "error": None if success else resp.get("message", resp.get("msg", "未知错误")),
            "raw": resp,
        })
        if len(members) > 1:
            time.sleep(2)
    return results


def format_output(results: List[Dict]) -> str:
    lines = ["🌟 A-SOUL 直播间签到结果", ""]
    ok = sum(1 for r in results if r["success"])
    fail = len(results) - ok

    for r in results:
        if r["success"]:
            lines.append(f"  ✅ {r['name']}  — 签到成功  💬「{r['msg']}」")
        else:
            err = r["error"] or "未知错误"
            if "login" in err.lower() or "-101" in str(r.get("raw", {}).get("code", "")):
                lines.append(f"  ❌ {r['name']}  — Cookie 过期，请重新设置")
            elif "msg in 1s" in str(r.get("raw", {}).get("data", {}).get("message", "")):
                lines.append(f"  ⚠️ {r['name']}  — 发送太频繁，请稍后重试")
            else:
                lines.append(f"  ❌ {r['name']}  — {err}")

    lines.append("")
    if fail == 0:
        lines.append(f"🎉 全部签到成功！({ok}/{len(results)})")
    elif ok > 0:
        lines.append(f"📊 部分成功：{ok} 成功 / {fail} 失败")
    else:
        lines.append(f"💔 全部失败，请检查 Cookie 是否有效")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="A-SOUL 直播间批量签到")
    parser.add_argument("--msg", default="签到", help="弹幕内容（默认：签到）")
    parser.add_argument("--members", help="指定成员（逗号分隔，如：嘉然,贝拉）默认全部")
    parser.add_argument("--sessdata", help="SESSDATA cookie")
    parser.add_argument("--bili-jct", help="bili_jct cookie")
    parser.add_argument("--save-cookie", action="store_true", help="保存 cookie")
    parser.add_argument("--json", action="store_true", help="JSON 输出")
    parser.add_argument("--list", action="store_true", help="列出所有成员")
    args = parser.parse_args()

    if args.list:
        print("🌟 A-SOUL 现役成员：")
        for m in MEMBERS:
            print(f"  {m['name']}  UID:{m['uid']}  直播间:{m['room']}  https://live.bilibili.com/{m['room']}")
        return

    sessdata = args.sessdata
    bili_jct = args.bili_jct

    if args.save_cookie:
        if not sessdata or not bili_jct:
            print("❌ --save-cookie 需要同时提供 --sessdata 和 --bili-jct")
            sys.exit(1)
        save_cookies(sessdata, bili_jct)
        return

    if not sessdata or not bili_jct:
        saved = load_cookies()
        if saved:
            sessdata = saved["SESSDATA"]
            bili_jct = saved["bili_jct"]
        else:
            print("❌ 没有找到 Cookie。请先设置：")
            print("  python3 checkin.py --save-cookie --sessdata \"你的SESSDATA\" --bili-jct \"你的bili_jct\"")
            print("")
            print("或在 bilibili-live-checkin skill 中已保存的 Cookie 会自动复用。")
            sys.exit(1)

    targets = MEMBERS
    if args.members:
        names = [n.strip() for n in args.members.split(",")]
        targets = [m for m in MEMBERS if m["name"] in names]
        if not targets:
            print(f"❌ 未找到指定成员：{args.members}")
            print(f"   可用成员：{', '.join(m['name'] for m in MEMBERS)}")
            sys.exit(1)

    results = batch_checkin(targets, args.msg, sessdata, bili_jct)

    if args.json:
        print(json.dumps(results, ensure_ascii=False, indent=2))
    else:
        print(format_output(results))


if __name__ == "__main__":
    main()
