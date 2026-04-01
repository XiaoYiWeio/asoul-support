<p align="center">
  <img src="assets/asoul-logo.png" width="120" alt="A-SOUL Logo" />
</p>

<h1 align="center">A-SOUL Support</h1>

<p align="center">
  <strong>A-SOUL 粉丝全自动应援工具</strong> — 开播自动挂机涨亲密度 + 点亮粉丝牌 + 视频/动态点赞
</p>

<p align="center">
  <a href="https://clawhub.ai/skills/asoul-support">🦞 ClawHub</a> ·
  <a href="https://github.com/XiaoYiWeio/asoul-support">📦 GitHub</a> ·
  <a href="https://openclaw.ai">🌐 OpenClaw</a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/version-4.0.0-blue" alt="version" />
  <img src="https://img.shields.io/badge/python-3.9+-green" alt="python" />
  <img src="https://img.shields.io/badge/license-MIT-orange" alt="license" />
</p>

---

## 一句话安装

复制下面这句话，发给你的 [OpenClaw](https://openclaw.ai)，它会帮你搞定一切：

> 帮我安装这个 skill：https://github.com/XiaoYiWeio/asoul-support ，然后帮我设置 A-SOUL 自动挂机

就这样，装好了。OpenClaw 会引导你配置 B站 Cookie 和定时任务。

<details>
<summary>🔧 也可以用命令行安装</summary>

```bash
npx clawhub install asoul-support
```

</details>

---

## 它能做什么？

| 功能 | 使用条件 | 说明 |
|------|----------|------|
| 💓 **心跳挂机涨亲密度** | 需要开播 | 检测开播 → 移动端心跳 → 每 5 分钟 +6，每天 30 满额 |
| 🏅 **粉丝牌自动点亮** | 需要开播 | 开播后发 10 条弹幕，牌子保持 3 天可见 |
| 👍 **视频自动点赞** | 无 | 每 2 天自动给成员新视频点赞 |
| 💬 **动态自动点赞** | 无 | 每 2 天自动给成员新动态点赞 |

### v4.0 核心升级

> 使用 B站最新 **移动端心跳协议**（`mobileHeartBeat`），纯 Python 签名，零外部依赖。
>
> 实测亲密度 **0 → 30/30 满额**，粉丝牌直接升级。

---

## 使用教程（OpenClaw）

这是**推荐方式**，全自动检测开播 + 挂机涨亲密度 + 点亮粉丝牌。

### 环境要求

| 依赖 | 版本 | 说明 |
|------|------|------|
| [OpenClaw](https://openclaw.ai) | 最新版 | AI agent 平台 |
| Python | 3.9+ | macOS/Linux 自带 |

### 第 1 步：安装 Skill

对你的 OpenClaw 说：

> "帮我安装这个 skill：https://github.com/XiaoYiWeio/asoul-support"

或者命令行：

```bash
npx clawhub install asoul-support
```

### 第 2 步：配置 Cookie

对 OpenClaw 说：

> "帮我设置 A-SOUL 自动挂机"

它会引导你获取 B站 Cookie（SESSDATA 和 bili_jct），跟着做就行。

<details>
<summary>📋 手动获取 Cookie 的方法（点击展开）</summary>

1. 用 Chrome 打开 [bilibili.com](https://www.bilibili.com)，确保已登录
2. 按 **F12**（Mac: **Cmd + Option + I**）打开开发者工具
3. 点击 **Application** 标签 → 左侧 **Cookies** → **https://www.bilibili.com**
4. 找到并复制这两个值：
   - **SESSDATA** — 一长串字母数字
   - **bili_jct** — 32 位字母数字

> ⚠️ 这两个值相当于登录凭证，不要分享给任何人。约 6 个月后过期，届时更新即可。

</details>

### 第 3 步：设置定时任务

对 OpenClaw 说：

> "帮我设置一个定时任务，每 30 分钟检测 A-SOUL 成员是否在直播，如果在播就帮我挂机涨亲密度并点亮粉丝牌"

搞定！OpenClaw 会 24/7 自动工作：

```
每 30 分钟检测开播
      │
      ├─ 没人在播 → 静默等待
      │
      └─ 有人在播 → 1. 发 10 条弹幕点亮粉丝牌
                     2. 移动端心跳挂机直到下播
                     3. 下播后通知你
```

### 手动命令（可选）

```bash
# 检测谁在播
python3 scripts/heartbeat.py --check-only

# 挂机指定成员
python3 scripts/heartbeat.py --members 嘉然,贝拉

# 挂机直到下播
python3 scripts/heartbeat.py --until-offline

# 发弹幕点亮粉丝牌（只对在播成员）
python3 scripts/checkin.py --live-only
```

---

## GitHub Actions 自动点赞（不需要 OpenClaw）

如果你只需要**视频/动态自动点赞**（不涨亲密度），可以只用 GitHub Actions，不需要安装任何东西。

<details>
<summary>📋 GitHub Actions 设置教程（点击展开）</summary>

### 第 1 步：Fork 仓库

1. 登录 GitHub（没有账号就注册一个，免费的）
2. 点击本页面右上角的 **Fork** → **Create fork**

### 第 2 步：配置 Cookie

1. 打开你 Fork 后的仓库 → **Settings** → **Secrets and variables** → **Actions**
2. 点 **New repository secret**，添加两个：
   - `SESSDATA` — 你的 SESSDATA 值
   - `BILI_JCT` — 你的 bili_jct 值

### 第 3 步：启用 Actions

1. 点击 **Actions** 标签
2. 点击 **I understand my workflows, go ahead and enable them**

### 验证

1. **Actions** → 左侧选 **A-SOUL 自动应援** → **Run workflow**
2. 等 1-2 分钟，看到绿色勾就成功了

之后每 2 天自动执行一次。

### 开启动态点赞（可选）

编辑 `.github/workflows/daily.yml`，把 `ENABLE_DYNAMIC_LIKE` 改为 `'true'`。

</details>

---

## 关于亲密度和粉丝牌

- **涨亲密度**：观看直播（每 5 分钟 +6，上限 30/天）或投币（1 币 = 10 亲密度）
- **点亮粉丝牌**：发 10 条弹幕 / 观看 15 分钟 / 投币，有效期 3 天
- **以上操作都需要成员正在直播**，视频/动态点赞不受限制

## 技术方案

v4.0 使用 B站 **移动端心跳协议**（`mobileHeartBeat`）：

- 签名算法：`sha512 → sha3_512 → sha384 → sha3_384 → blake2b` 链式 hash
- **纯 Python 标准库**实现，不依赖任何外部签名服务
- 不需要 Node.js、pm2、Docker 或任何额外进程

## 内置成员

| 成员 | 直播间 | 主页 |
|------|--------|------|
| 嘉然 | [22637261](https://live.bilibili.com/22637261) | [space](https://space.bilibili.com/672328094) |
| 贝拉 | [22632424](https://live.bilibili.com/22632424) | [space](https://space.bilibili.com/672353429) |
| 乃琳 | [22625027](https://live.bilibili.com/22625027) | [space](https://space.bilibili.com/672342685) |
| 心宜 | [30849777](https://live.bilibili.com/30849777) | [space](https://space.bilibili.com/3537115310721181) |
| 思诺 | [30858592](https://live.bilibili.com/30858592) | [space](https://space.bilibili.com/3537115310721781) |

## 安全说明

- Cookie **加密存储**在本地（权限 600）或 GitHub Secrets 中
- 所有代码**完全开源**，可自行检查
- 只做点赞和弹幕操作，不投币、不送礼、不关注陌生人
- GitHub Actions 对公开仓库完全免费

## 写在最后

做这个工具不是为了让大家躺平不看直播。

我自己是工作太忙，经常加班错过开播，眼睁睁看着粉丝牌熄灭、亲密度一天天没涨，才写了这个让它在我忙的时候帮我守着。

**如果你有时间，还是建议去直播间看直播**，跟大家一起刷弹幕、跟嘉然贝拉她们互动，那种快乐是工具给不了的。

这个工具更适合：
- 工作日白天没法看直播的打工人
- 出差途中没法挂机的
- 偶尔忘了签到怕牌子熄灭的

能亲自去当然亲自去，这个只是你的备用方案。魂们加油，一个都不能少。

## 常见问题

**Q: Cookie 过期了怎么办？**
重新获取 SESSDATA 和 bili_jct，告诉 OpenClaw 更新就行。过期后 GitHub 会发邮件通知你。

**Q: 需要电脑一直开着吗？**
OpenClaw 在后台运行（类似服务），不需要你盯着。GitHub Actions 在云端跑，完全不需要你的电脑。

**Q: 投币会消耗硬币吗？**
默认不投币，不会消耗你的硬币。

**Q: 需要安装 Node.js 吗？**
不需要。v4.0 纯 Python 实现，只需要 Python 3.9+。

## 更新日志

### v4.0（2026-03-31）

- **心跳协议升级**：`x25Kn` → `mobileHeartBeat` 移动端协议
- **纯 Python 签名**：`sha512→sha3_512→sha384→sha3_384→blake2b`，零外部依赖
- **移除 Node.js 依赖**：不再需要 pcheartbeat / pm2
- **亲密度实测可涨**：0 → 30/30 满额
- **新增 `--until-offline`**：挂机直到下播，自动弹幕 + 心跳 + 通知

### v3.0（2026-03-23）

- 新增开播检测 + 心跳挂机
- 新增 Discord 开播/下播通知

### v2.0（2026-03-20）

- 粉丝牌点亮（10 条弹幕，3 天有效期）

### v1.0

- 视频点赞 + 动态点赞 + GitHub Actions

## License

MIT
