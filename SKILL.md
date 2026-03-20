---
name: asoul-support
description: "A-SOUL 粉丝应援工具 — 一键给嘉然、贝拉、乃琳、心宜、思诺的直播间签到 + 给新视频点赞/投币/收藏。触发词：A-SOUL、asoul、签到、点赞、三连、应援、嘉然、贝拉、乃琳、心宜、思诺。"
---

# A-SOUL Support

A-SOUL 粉丝自动应援工具 — 直播间签到 + 视频互动，一句话搞定。

## 触发规则

| 模式 | 示例 |
|------|------|
| 包含 `A-SOUL` / `asoul` + `签到` | "帮我给asoul签到" |
| 包含 `A-SOUL` / `asoul` + `点赞` / `三连` | "给asoul视频点赞" |
| 包含成员名 + `签到` / `点赞` | "给嘉然签到", "给乃琳视频三连" |
| 包含 `直播间签到` + 成员名 | "直播间签到嘉然贝拉" |
| 包含 `应援` | "A-SOUL每日应援" |

## 内置成员

| 成员 | UID | 直播间 |
|------|-----|--------|
| 嘉然 | 672328094 | 22637261 |
| 贝拉 | 672353429 | 22632424 |
| 乃琳 | 672342685 | 22625027 |
| 心宜 | 3537115310721181 | 30849777 |
| 思诺 | 3537115310721781 | 30858592 |

## 功能 1 — 直播间弹幕签到

给全部成员直播间发送签到弹幕，刷亲密度。

```bash
python3 {baseDir}/scripts/checkin.py
python3 {baseDir}/scripts/checkin.py --msg "打卡"
python3 {baseDir}/scripts/checkin.py --members 嘉然,贝拉
python3 {baseDir}/scripts/checkin.py --list
```

## 功能 2 — 视频点赞/投币/收藏

给成员新发布的视频批量互动。默认仅点赞，投币和收藏需明确指定。

```bash
# 给本月新视频全部点赞
python3 {baseDir}/scripts/videos.py --month 3

# 给最近7天视频点赞+投币+收藏
python3 {baseDir}/scripts/videos.py --days 7 --coin --fav

# 只给嘉然的视频三连
python3 {baseDir}/scripts/videos.py --month 3 --members 嘉然 --coin --fav

# 不点赞，仅投币
python3 {baseDir}/scripts/videos.py --month 3 --no-like --coin
```

## Cookie 设置

与 `bilibili-live-checkin` 共用 Cookie。如果已在那个 skill 设置过，无需重复操作。

手动设置：
```bash
python3 {baseDir}/scripts/checkin.py --save-cookie --sessdata "{SESSDATA}" --bili-jct "{bili_jct}"
```
