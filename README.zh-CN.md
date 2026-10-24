# Vitrine 简体中文汉化版（社区非官方）

> 基于 [Vitrine 原项目](https://github.com/My-Name-Is-Jeff/vitrine) 的**简体中文界面本地化分支**。这不是 Spotify 或 Vitrine 原作者发布的官方中文版。

**[查看汉化源码](https://github.com/HypnosysNyx/vitrine/tree/i18n/zh-hans)** · **[自行构建 IPA](https://github.com/HypnosysNyx/vitrine/actions/workflows/build-ipa.yml)** · **[提交反馈](https://github.com/HypnosysNyx/vitrine/issues/new/choose)** · **[英文原版说明](README.md)**

## 这是什么？

这个版本对 **Vitrine 自己绘制的 Mod 界面**进行简体中文本地化：设置菜单、说明、部分播放器与歌词控件、Karaoke（卡拉 OK）提示、歌词翻译目标语言名称，以及动态提示与错误消息等。翻译词库见 [`localization/zh-Hans.json`](localization/zh-Hans.json)。

- **不是 Spotify 官方客户端的整体汉化**：Spotify 自带的界面、iOS 系统弹窗和第三方原生页面不在此汉化范围内。
- **不是“任何歌曲都自动出现中文字幕”**：歌词、中文翻译取决于可用歌词源和所配置的翻译功能。
- **仍在完善**：不能保证每个页面都已翻译、所有手机都无问题。请通过截图反馈漏译。
- **没有 Root / 越狱要求**：按照 Vitrine 的原有方案，由用户自行准备、注入并签名 IPA。
- **非简体中文环境保持原有文案**：目前根据 iOS 提供的首选语言判断，`zh-Hans`、`zh-CN`、`zh-SG` 等识别为简体中文；没有单独的语言切换按钮。

## 适配范围与现状

| 项目 | 情况 |
| --- | --- |
| Vitrine 代码基线 | **1.0.0-beta.14**（已同步上游源码；非独立的正式汉化版号） |
| Spotify iOS 版本 | 原项目明确支持 **9.1.78、9.1.88、9.1.90**；其他版本未验证 |
| iOS / 原生界面 | iOS **16.1+** |
| iOS / Liquid Glass 重设计 | **iOS 26+**；较低系统有实验性警告和回退机制 |
| 汉化源代码 | [`i18n/zh-hans` 分支](https://github.com/HypnosysNyx/vitrine/tree/i18n/zh-hans) |
| 自动化检查 | [汉化源码与编译检查](https://github.com/HypnosysNyx/vitrine/actions/workflows/check-zh-hans.yml) |

原 beta.13 汉化在 2026-10-23 的基线提交 [`acac43a`](https://github.com/HypnosysNyx/vitrine/commit/acac43a6337e8646d07fbbe8c304371d489a2967) 的[静态检查与编译](https://github.com/HypnosysNyx/vitrine/actions/runs/39942001448)以及[一次完整 IPA 构建](https://github.com/HypnosysNyx/vitrine/actions/runs/39946414229)均成功；**编译成功不代表已经完成所有机型的实机汉化验收**。后续提交需分别检查对应工作流。

同步状态（2026-10-24）：上游 beta.14 及截至 `f5473f7` 的后续提交已经通过 [PR #1](https://github.com/HypnosysNyx/vitrine/pull/1) 正式合并进 `i18n/zh-hans`（合并提交 [`c217a3f`](https://github.com/HypnosysNyx/vitrine/commit/c217a3ff1674223026460114b69c6fae2f2f8af4)）。[macOS 静态检查、界面测试和 tweak 编译链接](https://github.com/HypnosysNyx/vitrine/actions/runs/39991312030)均已通过。本次同步尚未执行对应 IPA 的安装及 iPhone 实机界面验收，不应当据此标称为实机测试完成的正式安装版。

## 如何自行构建、安装

**本项目不提供含 Spotify 应用本体的公开 IPA 下载，也不提供解密 Spotify IPA 的下载地址。** 你需要自行依法取得可用于构建的 Spotify iOS IPA，并遵守原软件的许可及适用规则。

### 路线 A：GitHub Actions（无需自己配置 Mac）

1. Fork 本仓库；确保你的副本中有 `i18n/zh-hans` 分支，启用 **Actions**。公开仓库工作流和产物可能被有访问权限的人看到，不要使用不允许分享的文件公开构建。
2. 准备你有权使用的、与上表兼容的 **Spotify 解密 IPA**，以及能供工作流读取的 HTTPS 直链。建议使用你自己的受控下载地址，在 fork 的 **Settings → Secrets and variables → Actions** 新增 `SPOTIFY_IPA_URL`，而不是在公开的运行表单中填写敏感 URL。
3. 为确保下载文件没有被替换，计算**你自己的 IPA 文件**的 SHA-256。Windows PowerShell：`(Get-FileHash -Algorithm SHA256 "C:\\path\\to\\Spotify.ipa").Hash`；Mac：`shasum -a 256 Spotify.ipa`。将计算结果填到 `ipa_sha256` 输入框，或者添加 fork 的 `SPOTIFY_IPA_SHA256` secret。如果两者都不填，工作流只接受此前校验过的一份特定 9.1.90 IPA 的哈希值，其他 IPA 会被拒绝。
4. 打开 [**Build IPA from your own Spotify IPA**](https://github.com/HypnosysNyx/vitrine/actions/workflows/build-ipa.yml)，在自己的 fork 中选择 **Run workflow**，并选择 **`i18n/zh-hans` 分支**。如界面仍要求 `ipa_url`，按需填写自己的 HTTPS 直链；建议 `upload_method` 保持 **artifacts**，避免上传到第三方文件托管服务。
5. 构建成功后，到自己的 Action 运行页面下载 `vitrine.ipa` 产物（下载后解压可取得实际 IPA）。**Actions 产物不是永久下载链接**。
6. 使用 SideStore、Feather 或其他你信任的 iOS 签名安装方式，为得到的 IPA 签名并安装。需要有效的签名凭据，**构建出的 IPA 不是已签名的即装版**。

> 如 GitHub Actions 表单没有出现新增加的 `ipa_sha256` 字段，使用 `SPOTIFY_IPA_SHA256` 仓库 secret 即可；以实际运行分支中的工作流为准。不要把个人签名文件、证书密码或私有 IPA 提交到仓库。

### 路线 B：Mac 本地编译

根据 [原项目 README 的 Build on a Mac](README.md#build-on-a-mac) 和 [技术文档](docs/tweaks.md) 配置 Theos 与 Xcode。先切换到 `i18n/zh-hans` 分支，把自行准备的 IPA 放在 `ipa/`，然后运行 `make release`，获得需要自行签名的 `out/vitrine-<版本>.ipa`。相关依赖和系统限制以英文说明为准。

### 安装和保留数据提醒

原项目默认保留 `com.spotify.client` 的 Bundle ID，可能与已安装的 Spotify 或其他修改版冲突。**不同签名/安装方式不一定允许直接覆盖安装，不能保证保留旧版的数据**。安装前备份可备份的资料；如要保留原有安装，先确认签名、Bundle ID 和侧载工具的覆盖行为。不要直接删除有重要本地数据的旧版本。

使用汉化时，请把 iOS 的首选语言设置为简体中文（或确认应用实际返回的首选语言为简体中文）；本地化仅改变 Vitrine 控制的可见文案，不改变原有选择器、账号、保存键或功能配置。

## 漏译与问题反馈

在 [Issues](https://github.com/HypnosysNyx/vitrine/issues) 提交：**原始英文或问题截图、出现路径、Vitrine 版本、Spotify 版本、iPhone 型号/iOS 版本、Native 或 Redesigned 模式**。建议写清“点开哪个菜单、点击哪个按钮后出现英文”。相关修复历史见 [`localization/qa-history.md`](localization/qa-history.md)。编译和静态文本检查不能代替实机截图验收。

## 来源、许可与免责声明

- 上游项目：[My-Name-Is-Jeff/vitrine](https://github.com/My-Name-Is-Jeff/vitrine)，原始 Vitrine 说明、功能和构建指导以该项目为准。
- Vitrine 进一步基于 [spoti.pw](https://github.com/skopevoj/spoti.pw) 的 GPL-3.0 版本演进；其他工具与贡献者署名见 [原始 README](README.md#credits)。
- 汉化改动保留仓库现有的 [GNU GPL-3.0 许可证](LICENSE)。请保留原作者署名、许可证和相关源码义务。
- 本项目是**非官方社区修改版**，不隶属于 Spotify、Vitrine 原作者或其关联方；不要把汉化版误称为官方发行版。
