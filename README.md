# A-SOUL Support

A-SOUL 粉丝自动应援工具 — 直播间签到 + 视频点赞 + 动态点赞，每天自动执行。

## 功能

| 功能 | 说明 |
|------|------|
| 🏅 直播间签到 | 自动佩戴粉丝牌 → 给嘉然/贝拉/乃琳/心宜/思诺的直播间发弹幕签到 |
| 👍 视频点赞 | 给成员最近发布的视频自动点赞 |
| 💬 动态点赞 | 给成员最近发布的动态（图文/转发等）自动点赞 |
| 🪙 投币/收藏 | 可选功能，需要手动开启 |

零依赖，纯 Python 标准库，不需要安装任何包。

## 快速开始（GitHub Actions，推荐）

**不需要装任何软件，只要有 GitHub 账号就行。每天自动运行。**

### 第 1 步：Fork 仓库

点击本页面右上角的 **Fork** 按钮，把仓库复制到你自己的账号下。

### 第 2 步：获取 B 站 Cookie

1. 在 Chrome 浏览器打开 [bilibili.com](https://www.bilibili.com)，确保已登录
2. 按 **F12** 打开开发者工具
3. 点击顶部的 **Application**（应用）标签
4. 左侧展开 **Cookies** → 点击 **https://www.bilibili.com**
5. 找到并复制这两个值：
   - `SESSDATA` — 一长串字母数字
   - `bili_jct` — 32位字母数字

> ⚠️ Cookie 大约 1 个月过期，过期后需要重新获取并更新。

### 第 3 步：配置 Secrets

1. 进入你 Fork 后的仓库页面
2. 点击 **Settings** → 左侧 **Secrets and variables** → **Actions**
3. 点击 **New repository secret**，添加两个：

| Name | Value |
|------|-------|
| `SESSDATA` | 你复制的 SESSDATA 值 |
| `BILI_JCT` | 你复制的 bili_jct 值 |

### 第 4 步：启用 Actions

1. 进入你 Fork 后的仓库，点击顶部 **Actions** 标签
2. 如果看到提示「Workflows aren't being run on this forked repository」，点击 **I understand my workflows, go ahead and enable them**
3. 完成！每天北京时间 10:30 会自动执行

### 手动触发

不想等定时？可以手动跑一次：

1. 进入 **Actions** 标签
2. 左侧选择 **A-SOUL 每日应援**
3. 点击右侧 **Run workflow**
4. 选择要执行的操作（all = 全部）
5. 点击绿色 **Run workflow** 按钮

运行完后点进去可以看到每一步的输出结果。

## 内置成员

| 成员 | 直播间 | 主页 |
|------|--------|------|
| 嘉然 | [22637261](https://live.bilibili.com/22637261) | [space](https://space.bilibili.com/672328094) |
| 贝拉 | [22632424](https://live.bilibili.com/22632424) | [space](https://space.bilibili.com/672353429) |
| 乃琳 | [22625027](https://live.bilibili.com/22625027) | [space](https://space.bilibili.com/672342685) |
| 心宜 | [30849777](https://live.bilibili.com/30849777) | [space](https://space.bilibili.com/3537115310721181) |
| 思诺 | [30858592](https://live.bilibili.com/30858592) | [space](https://space.bilibili.com/3537115310721781) |

## 本地使用

如果你更喜欢在自己电脑上跑（需要 Python 3.8+）：

```bash
# 签到
python3 scripts/checkin.py --sessdata "你的SESSDATA" --bili-jct "你的bili_jct"

# 视频点赞（最近7天）
python3 scripts/videos.py --days 7 --sessdata "你的SESSDATA" --bili-jct "你的bili_jct"

# 动态点赞（本月）
python3 scripts/dynamics.py --month 3 --sessdata "你的SESSDATA" --bili-jct "你的bili_jct"

# 视频三连（点赞+投币+收藏）
python3 scripts/videos.py --days 7 --coin --fav --sessdata "你的SESSDATA" --bili-jct "你的bili_jct"
```

## OpenClaw 用户

如果你已经在用 [OpenClaw](https://openclaw.ai)，可以直接安装 Skill：

```bash
clawhub install asoul-support
```

然后对话即可：「给 A-SOUL 签到」「给 A-SOUL 视频点赞」

## 安全说明

- 你的 Cookie **只存储在你自己的 GitHub Secrets 中**，加密保存，任何人（包括仓库作者）都无法看到
- 所有代码完全开源，可以自行审查
- 不会修改你的 B 站账号设置，只做签到/点赞操作
- Cookie 约 1 个月过期，过期后 Actions 会失败，更新 Secret 即可

## 常见问题

**Q: Cookie 过期了怎么办？**
A: 重新按第 2 步获取新的 SESSDATA 和 bili_jct，然后在 Settings → Secrets 里更新。

**Q: 怎么知道有没有成功？**
A: 进入 Actions 标签，点击最近一次运行，展开每个步骤可以看到详细结果。

**Q: 投币会消耗硬币吗？**
A: 默认不投币。如果你想投币，需要修改 workflow 文件，在 videos.py 命令后加上 `--coin`。

**Q: 可以只给某个成员签到吗？**
A: 可以，在命令后加 `--members 嘉然,贝拉`。

## License

MIT
