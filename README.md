<h1 align="center">Vitrine · 简体中文汉化版</h1>

<p align="center"><b>让 Spotify iOS 焕然一新：Liquid Glass 风格、丰富的播放器增强功能与简体中文 Mod 界面。</b></p>

<p align="center">
  <img alt="iOS" src="https://img.shields.io/badge/iOS-16.1%2B-black?logo=apple">
  <img alt="Liquid Glass" src="https://img.shields.io/badge/Liquid_Glass-iOS_26%2B-0a84ff">
  <img alt="汉化" src="https://img.shields.io/badge/语言-简体中文-EA4335">
  <img alt="Spotify 9.1.78/9.1.88/9.1.90" src="https://img.shields.io/badge/Spotify-9.1.78_%7C_9.1.88_%7C_9.1.90-1DB954?logo=spotify&logoColor=white">
  <a href="LICENSE"><img alt="GPL-3.0" src="https://img.shields.io/github/license/HypnosysNyx/vitrine"></a>
</p>

> 🇨🇳 **非官方简体中文社区汉化。**本仓库基于 [Vitrine 原项目（My-Name-Is-Jeff/vitrine）](https://github.com/My-Name-Is-Jeff/vitrine)；汉化源代码位于 [`i18n/zh-hans` 分支](https://github.com/HypnosysNyx/vitrine/tree/i18n/zh-hans)。只翻译 **Vitrine 自己绘制的 Mod 界面**，不代表 Spotify 全部官方界面均已汉化。项目与 Spotify、Vitrine 原作者均无官方合作关系。

<p align="center">
  <a href="https://github.com/HypnosysNyx/vitrine/releases"><b>📦 查看汉化版本与发布说明</b></a> ·
  <a href="https://github.com/HypnosysNyx/vitrine/tree/i18n/zh-hans"><b>🀄 汉化源码</b></a> ·
  <a href="https://github.com/HypnosysNyx/vitrine/actions/workflows/build-ipa.yml"><b>🛠 自行构建 IPA</b></a> ·
  <a href="https://github.com/HypnosysNyx/vitrine/issues"><b>🐛 问题反馈</b></a> ·
  <a href="README.en.md"><b>English README</b></a>
</p>

<p align="center">
  <img src="docs/screenshots/now-playing.webp" width="16%" alt="全屏播放界面与歌词">
  <img src="docs/screenshots/album.webp" width="16%" alt="专辑界面">
  <img src="docs/screenshots/playlist.webp" width="16%" alt="播放列表">
  <img src="docs/screenshots/queue.webp" width="16%" alt="播放队列">
  <img src="docs/screenshots/live-activity.webp" width="16%" alt="锁屏实时活动">
  <img src="docs/screenshots/home.webp" width="16%" alt="首页">
</p>

*截图沿用原项目，仅用于展示界面设计；截图为英文并不表示本汉化版本未支持中文，截图也不能代替实机汉化验证。*

## Vitrine 是什么？

Vitrine 是一个不要求越狱的 iOS Theos 插件，通过注入**使用者自行合法取得的 Spotify IPA**，为 Spotify 提供 Liquid Glass 重设计及功能扩展；生成的 IPA 需要使用自己的证书签名后才能安装。

Vitrine 基于 Vojtěch Škopek 的 [spoti.pw](https://github.com/skopevoj/spoti.pw) GPL-3.0 版本（`0.21.1`，提交 `c790445`，2026-09-23）继续开发。本汉化仓库则在 [Vitrine 原作者](https://github.com/My-Name-Is-Jeff/vitrine)的版本上增加简体中文 Mod 界面本地化。

**本仓库不发布包含 Spotify 本体的公共 IPA，也不提供 Spotify IPA 的解密下载来源。** Releases 若提供源码或发布说明，**不等于可以直接安装的 IPA**；需要按以下步骤自行构建并签名。

## 主要功能

Vitrine 在 Spotify iOS 上提供两种相互独立的界面外观，以及播放器与歌词等扩展功能。其实际表现仍取决于 Spotify 版本、iOS 版本及运行模式。

### ✨ Liquid Glass 全新设计

- 重新设计的玻璃质感标签栏、搜索栏、迷你播放器。
- 全屏播放器、Apple Music 风格歌词界面。
- 全新的首页、分类搜索、音乐库、歌手、专辑与播放列表。
- 可用的深色外观与主题强调色。
- **Liquid Glass 重设计适用于 iOS 26+**。旧系统可在警告后尝试实验性模式，但不保证兼容；遇到启动异常时原项目设计了回退机制。

### 🎵 保留原生界面并增强功能

不启用重设计时，使用 Spotify 自身界面，并根据原项目提供隐藏部分界面元素、修改配色、玻璃效果按钮等功能。两套外观不能同时启用。

### 🎤 歌词、播放和其他增强功能

- 同步、逐字、翻译及罗马化歌词（取决于歌词来源与翻译服务）。
- 部分歌词翻译、卡拉 OK、播放控制与动态提示支持简体中文。
- 锁屏实时活动（Live Activity）、音乐触感反馈、手势及播放控制。
- 根据原项目的设置，还包括播放速度与音高、屏蔽艺人、隐私、Flags、音频相关增强等。
- 部分功能要求较新的系统、具体兼容的 Spotify 版本或另外配置；切勿据此认为所有功能在任何设备都可用。

## 兼容性与版本

| 项目 | 条件或说明 |
|---|---|
| 汉化代码基线 | **Vitrine 1.0.0-beta.16**（并非独立正式版号） |
| Spotify iOS | 原项目明确构建、测试的版本：**9.1.78、9.1.88、9.1.90** |
| 原生外观 | **iOS 16.1+** |
| Liquid Glass 重设计 | **iOS 26+**；较旧系统仅能实验性尝试 |
| Live Activity | **iOS 17+** |
| 汉化语言 | 简体中文（例如 `zh-Hans`、`zh-CN`、`zh-SG`） |
| 汉化分支 | [`i18n/zh-hans`](https://github.com/HypnosysNyx/vitrine/tree/i18n/zh-hans) |
| 构建检查 | [汉化 QA 工作流](https://github.com/HypnosysNyx/vitrine/actions/workflows/check-zh-hans.yml) |
| 安装分发 | 用户自行准备 IPA、构建并签名；**无公共可直接安装 IPA** |

**注意：**Vitrine 通过修改 Spotify 内部类工作。即使其他 Spotify 版本能够成功构建，也可能在启动或使用时出现错误。原版更新日志中提及新版本 Flag 并不表示已经验证支持对应 Spotify 版本。

### 本汉化修改了什么？

对 **Vitrine Mod 自有 UI** 的设置项、说明提示、部分播放器与歌词控件、卡拉 OK、动态状态、错误消息、语言名称等加入简体中文翻译。翻译词库在 [`localization/zh-Hans.json`](https://github.com/HypnosysNyx/vitrine/blob/i18n/zh-hans/localization/zh-Hans.json)。

**不会：**修改 Spotify 官方界面的所有文字、翻译歌曲名或任何第三方网页；也不保证歌词源一定有中文字幕或翻译结果。不更改 Spotify 账号、数据标识符和核心播放行为。当前没有独立的 Mod 语言切换按钮，语言选择主要取决于系统提供的首选语言。

## 如何构建与安装汉化版？

**建议使用 GitHub Actions：无需在本机配置 Mac 与 Theos。** 构建需要由你提供自己有权使用的、版本兼容的 Spotify IPA；仓库不提供该文件。

### 方案 A：GitHub Actions 在线构建

1. 先 [Fork 本仓库](https://github.com/HypnosysNyx/vitrine/fork)，确认你的 Fork 中存在 `i18n/zh-hans` 分支，并在 Fork 中启用 **Actions**。
2. 自行依法取得兼容版本的 Spotify IPA，使用你可控制的 HTTPS 直接下载地址。**不要把个人签名文件、私有 IPA、访问令牌或敏感地址提交进 Git 历史或公开日志。**
3. 建议在自己 Fork 的 **Settings → Secrets and variables → Actions** 中设置 `SPOTIFY_IPA_URL`；最好同时设置你对该 IPA 计算得到的 `SPOTIFY_IPA_SHA256`。
4. 打开自己 Fork 中的 **Actions → Build IPA from your own Spotify IPA → Run workflow**，选择 **`i18n/zh-hans` 分支**。也可按工作流实际表单填写 `ipa_url`、`ipa_sha256`。建议保持 `upload_method = artifacts`。
5. 等待构建完成，进入该次 Actions 运行记录下载 `vitrine.ipa` Artifact；解压 Artifact 后得到构建的 IPA。**Artifact 有保存期限，并不是永久公开的 Releases 附件。**
6. 使用 SideStore、Feather、AltStore 或其他你信任的方式对 IPA **自行签名并安装**。未经签名的 IPA 不能直接在普通 iPhone 上安装。

构建脚本会验证 IPA 文件的 SHA-256、Bundle ID 和支持的版本；省略 SHA-256 时只接受工作流中预置校验过的一份基线文件哈希。**不要为绕过校验而禁用安全检查。**

在 Windows 上检查本地 IPA 的哈希：

```powershell
(Get-FileHash -Algorithm SHA256 "C:\path\to\Spotify.ipa").Hash
```

在 macOS 上检查：

```bash
shasum -a 256 Spotify.ipa
```

### 方案 B：在 Mac 上本地构建

需要 [Theos](https://theos.dev)、Xcode，以及 iPhoneOS 26+ SDK；使用其他 SDK 的构建可能缺少 Live Activity 功能。依赖可参照上游的完整构建指南：

```bash
brew install make ldid dpkg zsign libimobiledevice
uv tool install "cyan @ git+https://github.com/asdfzxcvbn/pyzule-rw"
git clone --branch i18n/zh-hans https://github.com/HypnosysNyx/vitrine.git
cd vitrine
# 自行准备合法来源的 Spotify IPA，并放入 ipa/ 目录
make release
# 生成 out/vitrine-<版本>.ipa，仍需自行签名
```

如需使用 `make install` 通过 USB 或 Wi‑Fi 在已配置设备上签名安装，请先复制 `.signing.env.example` 为 `.signing.env`，设置 `SIGN_P12`、`SIGN_PROFILE`、`SIGN_P12_PASSWORD` 并按照项目脚本完成本地配置。不要上传这些凭据。

首次构建可能需要从 IPA 提取 Spotify 的 Flag 表；可使用 `make flags` 重新生成。具体技术细节见 [`docs/tweaks.md`](docs/tweaks.md) 与 [英文原版 README](README.en.md)。

### 签名、覆盖安装与 Apple Watch

- 签名时使用与证书 App ID 匹配的 Bundle ID。否则锁屏播放器点击跳转可能失效。
- Feather 中需正确设置 **Identifier**，上游文档还提示关闭 **PPQ protection**；其他签名软件行为可能不同。
- 原项目通常沿用 Spotify 的 Bundle ID，可能与已安装的 Spotify 互相覆盖或冲突；是否保留应用数据取决于签名和安装方式。请先备份重要内容。
- `scripts/pipeline.sh <ipa> --no-flex --keep-watch` 可尝试保留 Apple Watch 应用，但原项目明确标为**未经验证**，还涉及手表芯片架构与单独签名；不要假定手表版本可直接使用。

## beta.16 更新概览

基于上游正式发布标签 `v1.0.0-beta.16` 的功能与修复包括：20 周年纪念图标、专辑/列表封面增强、首页精选标题、歌词页面调整、锁屏歌词译文、专辑/列表批量翻译、歌词罗马化、设备端语言包提示，以及随机播放、导入 LRC 时间轴、音量控制、歌词滚动与动态封面等方面的修复。

完整历史见 [CHANGELOG.md](CHANGELOG.md)，对应[上游 beta.16](https://github.com/My-Name-Is-Jeff/vitrine/releases/tag/v1.0.0-beta.16)。**上游版本的新增功能不代表本仓库已提供新签名的 IPA，也不能取代实机兼容性检查。**

## 常见问题

**需要越狱吗？** 原项目采用无需越狱的侧载安装方式，但仍须准备可用 IPA、签名证书及适配的设备。

**下载 Releases 的 ZIP 就可以安装吗？** 不可以。源码 ZIP 不是 IPA，更不是已经签名的安装包。本汉化仓库不发布包含 Spotify 的现成公共 IPA。

**为什么还有英文？** 本项目翻译的是 Vitrine 自有 Mod 界面，而非 Spotify/iOS/第三方页面。若属于 Mod 自有控件，请在本仓库 [Issues](https://github.com/HypnosysNyx/vitrine/issues)中附上截图、进入路径、Spotify 版本、iOS 版本与原生/重设计模式。

**中文设置没有生效？** 优先确认系统或应用实际使用简体中文首选语言，然后重新启动应用；原版的某些界面不是 Mod 自己控制，可能继续保持原语言。

**能保证 iPhone 上没有漏译或崩溃吗？** 不能。静态词库检查、编译成功、一次构建产物都不等于在所有机型、所有页面上完成了实机验证。

## 开发者与汉化贡献

汉化检验入口：

```bash
python3 scripts/sync-zh-hans.py --check
python3 scripts/check-zh-hans-coverage.py
python3 scripts/check-zh-hans-placeholders.py
python3 scripts/audit-mod-ui-literals.py
python3 scripts/audit-mod-ui-renderers.py
```

当前汉化分支已配置 [CI 静态检查与无 IPA 编译](https://github.com/HypnosysNyx/vitrine/actions/workflows/check-zh-hans.yml)。**编译通过不等于实际 IPA 或所有机型可用**。修订翻译时需保留资源键、格式占位符、选择器和内部存储标识。缺失界面的历史与回归检查见 [`localization/qa-history.md`](https://github.com/HypnosysNyx/vitrine/blob/i18n/zh-hans/localization/qa-history.md)。

## 原作者、第三方贡献与许可证

- **Vitrine 原项目：**[My-Name-Is-Jeff/vitrine](https://github.com/My-Name-Is-Jeff/vitrine)。
- **更早的基础项目：**[Vojtěch Škopek 的 spoti.pw](https://github.com/skopevoj/spoti.pw)，基于 GPL-3.0 授权版本。
- **构建与注入工具：**[Theos](https://theos.dev)、[cyan](https://github.com/asdfzxcvbn/pyzule-rw)。
- **界面检查工具：**[FLEX](https://github.com/FLEXTool/FLEX)，仓库中的 `vendor/` 版本来自 hopeless 的 AutoFLEX。
- **部分扩展代码来源：**[EeveeSpotify Reincarnated](https://github.com/SideloadLabs/EeveeSpotifyReincarnated) 提供了广告处理及 Premium 状态相关代码。
- **中文汉化维护：**本仓库的社区贡献。出现 Mod 汉化问题请向[本仓库](https://github.com/HypnosysNyx/vitrine/issues)反馈，不要默认归咎于原作者。

项目遵循 [GNU GPL-3.0](LICENSE)。本仓库与 Spotify AB 无隶属、赞助或授权关系。使用第三方插件可能违反相关服务条款，用户须自行评估账号和设备风险。

[**English README（保留原版项目介绍）**](README.en.md) · [**Vitrine 上游仓库**](https://github.com/My-Name-Is-Jeff/vitrine) · [**汉化源码**](https://github.com/HypnosysNyx/vitrine/tree/i18n/zh-hans)
