---
name: asoul-support
description: "A-SOUL 粉丝应援工具 — 自动佩戴粉丝牌+直播间签到、视频点赞/投币/收藏、动态点赞。触发词：A-SOUL、asoul、签到、点赞、三连、应援、动态、嘉然、贝拉、乃琳、心宜、思诺。"
---

# A-SOUL Support

A-SOUL 粉丝自动应援工具 — 直播间签到 + 视频互动 + 动态点赞，一句话搞定。

## 触发规则

| 模式 | 示例 |
|------|------|
| 包含 `A-SOUL` / `asoul` + `签到` | "帮我给asoul签到" |
| 包含 `A-SOUL` / `asoul` + `点赞` / `三连` | "给asoul视频点赞" |
| 包含 `A-SOUL` / `asoul` + `动态` | "给asoul动态点赞" |
| 包含成员名 + `签到` / `点赞` | "给嘉然签到" |
| 包含 `应援` | "A-SOUL每日应援" |

## 内置成员

| 成员 | UID | 直播间 |
|------|-----|--------|
| 嘉然 | 672328094 | 22637261 |
| 贝拉 | 672353429 | 22632424 |
| 乃琳 | 672342685 | 22625027 |
| 心宜 | 3537115310721181 | 30849777 |
| 思诺 | 3537115310721781 | 30858592 |

## 功能 1 — 直播间签到（自动佩戴粉丝牌）

签到前自动切换佩戴对应成员的粉丝牌，最大化亲密度收益。

```bash
python3 {baseDir}/scripts/checkin.py
python3 {baseDir}/scripts/checkin.py --msg "打卡"
python3 {baseDir}/scripts/checkin.py --members 嘉然,贝拉
python3 {baseDir}/scripts/checkin.py --no-medal
python3 {baseDir}/scripts/checkin.py --list
```

## 功能 2 — 视频点赞/投币/收藏

给成员新发布的视频批量互动。默认仅点赞，投币和收藏需明确指定。

```bash
python3 {baseDir}/scripts/videos.py --month 3
python3 {baseDir}/scripts/videos.py --days 7 --coin --fav
python3 {baseDir}/scripts/videos.py --month 3 --members 嘉然 --coin --fav
python3 {baseDir}/scripts/videos.py --month 3 --no-like --coin
```

## 功能 3 — 动态点赞

给成员发布的图文/视频/转发等动态批量点赞。

```bash
python3 {baseDir}/scripts/dynamics.py --month 3
python3 {baseDir}/scripts/dynamics.py --days 7
python3 {baseDir}/scripts/dynamics.py --days 7 --members 嘉然,贝拉
```

## Cookie 设置

与 `bilibili-live-checkin` 共用 Cookie。如果已在那个 skill 设置过，无需重复操作。

手动设置：
```bash
python3 {baseDir}/scripts/checkin.py --save-cookie --sessdata "{SESSDATA}" --bili-jct "{bili_jct}"
```
