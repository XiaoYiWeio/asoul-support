# A-SOUL Support

A-SOUL 粉丝自动应援工具 — 每天自动给嘉然、贝拉、乃琳、心宜、思诺的直播间佩戴粉丝牌并签到。

可选开启：视频自动点赞、动态自动点赞。

不需要安装任何软件，不需要会编程，只要有 GitHub 账号就行。

## 功能

| 功能 | 默认 | 说明 |
|------|------|------|
| 🏅 直播间签到 | ✅ 开启 | 自动佩戴粉丝牌 → 发弹幕签到，刷亲密度 |
| 👍 视频点赞 | ❌ 关闭 | 给成员最近发布的视频自动点赞 |
| 💬 动态点赞 | ❌ 关闭 | 给成员最近发布的动态自动点赞 |

## 设置教程

### 第 1 步：Fork 仓库

1. 确保你已经登录了 GitHub（没有账号的话先注册一个，免费的）
2. 点击本页面右上角的 **Fork** 按钮
3. 在弹出的页面直接点击 **Create fork**
4. 等几秒钟，你的账号下就会出现一个一模一样的仓库

### 第 2 步：获取 B 站 Cookie

1. 打开 Chrome 浏览器，进入 [bilibili.com](https://www.bilibili.com)
2. 确保你已经登录了 B 站账号
3. 按键盘上的 **F12**（Mac 用户按 **Cmd + Option + I**），会弹出开发者工具
4. 点击开发者工具顶部的 **Application**（应用程序）标签
   - 如果看不到这个标签，点击 **>>** 展开更多标签找到它
5. 在左侧面板展开 **Cookies** → 点击 **https://www.bilibili.com**
6. 在右侧列表中找到这两项，双击 Value 列复制它们的值：
   - **SESSDATA** — 一长串字母数字和符号
   - **bili_jct** — 32 位字母数字

> ⚠️ 这两个值相当于你的登录凭证，不要分享给任何人。
> Cookie 大约 1 个月后会过期，届时更新一下就好。

### 第 3 步：配置 Secrets（把 Cookie 填进去）

1. 打开你 Fork 后的仓库页面（就是你自己账号下的 asoul-support）
2. 点击顶部的 **Settings**（设置）标签
3. 在左侧菜单找到 **Secrets and variables**，点击展开
4. 点击 **Actions**
5. 点击右上角的 **New repository secret** 按钮
6. 第一个 Secret：
   - **Name** 填：`SESSDATA`
   - **Secret** 填：你刚才复制的 SESSDATA 值
   - 点击 **Add secret**
7. 再点 **New repository secret**，添加第二个：
   - **Name** 填：`BILI_JCT`
   - **Secret** 填：你刚才复制的 bili_jct 值
   - 点击 **Add secret**

### 第 4 步：启用 Actions

1. 点击顶部的 **Actions** 标签
2. 你会看到一个黄色提示：「Workflows aren't being run on this forked repository」
3. 点击 **I understand my workflows, go ahead and enable them**
4. 搞定！

### 验证是否成功

1. 在 **Actions** 标签页面，左侧选择 **A-SOUL 每日应援**
2. 点击右侧 **Run workflow** → 再点绿色 **Run workflow** 按钮
3. 等大约 30 秒，页面会出现一条新的运行记录
4. 点进去，展开 **🏅 直播间签到** 那一步
5. 如果看到 `✅ 嘉然 ... 签到成功` 之类的输出，就说明一切正常！

之后每天北京时间 10:30 会自动执行。

## 可选功能：开启视频/动态点赞

默认只做直播间签到。如果你还想自动给成员的新视频和动态点赞：

1. 在你的仓库中打开 `.github/workflows/daily.yml` 文件
2. 点击右上角的铅笔图标（Edit）
3. 找到这两行，把 `false` 改成 `true`：

```
  ENABLE_VIDEO_LIKE: 'true'
  ENABLE_DYNAMIC_LIKE: 'true'
```

4. 点击右上角 **Commit changes** 保存

就这样，下次运行时就会自动点赞了。

你也可以只开其中一个，比如只开视频点赞。

## 安全说明

- 你的 Cookie **只存储在你自己的 GitHub Secrets 中**，加密保存
- 任何人（包括本仓库作者）都**无法看到**你的 Cookie
- 所有代码完全开源，你可以自行检查每一行
- 只做签到和点赞操作，不会修改账号设置，不会发私信，不会关注陌生人
- GitHub Actions 对公开仓库完全免费

## 常见问题

**Q: Cookie 过期了怎么办？**
重新按第 2 步获取新值，然后在 Settings → Secrets 里更新 SESSDATA 和 BILI_JCT。

**Q: 怎么知道每天有没有成功？**
进入 Actions 标签，每次运行都有记录。绿色 ✓ = 成功，红色 ✗ = 失败。失败时 GitHub 会自动发邮件通知你。

**Q: 可以改签到时间吗？**
打开 `.github/workflows/daily.yml`，修改 `cron: '30 2 * * *'` 中的数字。注意这里用的是 UTC 时间，北京时间需要减 8 小时。例如想改成下午 3 点执行，就写 `cron: '0 7 * * *'`。

**Q: 可以改签到弹幕吗？**
打开 `.github/workflows/daily.yml`，修改 `CHECKIN_MSG: '签到'` 里的内容。

**Q: 投币会消耗硬币吗？**
默认不投币。本工具不会消耗你的硬币。

## 内置成员

| 成员 | 直播间 | 主页 |
|------|--------|------|
| 嘉然 | [22637261](https://live.bilibili.com/22637261) | [space](https://space.bilibili.com/672328094) |
| 贝拉 | [22632424](https://live.bilibili.com/22632424) | [space](https://space.bilibili.com/672353429) |
| 乃琳 | [22625027](https://live.bilibili.com/22625027) | [space](https://space.bilibili.com/672342685) |
| 心宜 | [30849777](https://live.bilibili.com/30849777) | [space](https://space.bilibili.com/3537115310721181) |
| 思诺 | [30858592](https://live.bilibili.com/30858592) | [space](https://space.bilibili.com/3537115310721781) |

## License

MIT
