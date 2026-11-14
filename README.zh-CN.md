# Vitrine 简体中文汉化 · 技术补充说明

> **完整版中文介绍、六张原版截图、功能、兼容性、构建和安装方法现已整理至 [README.md](README.md)**。本文件只保留汉化开发者需要的补充信息。英文原版文档保存为 [README.en.md](README.en.md)。

## 汉化源码

- 原版项目：[My-Name-Is-Jeff/vitrine](https://github.com/My-Name-Is-Jeff/vitrine)
- 汉化分支：[i18n/zh-hans](https://github.com/HypnosysNyx/vitrine/tree/i18n/zh-hans)
- 上游版本基线：**1.0.0-beta.16**
- 中文词库：[localization/zh-Hans.json](https://github.com/HypnosysNyx/vitrine/blob/i18n/zh-hans/localization/zh-Hans.json)
- [汉化质量与实机截图回归记录](https://github.com/HypnosysNyx/vitrine/blob/i18n/zh-hans/localization/qa-history.md)

仅汉化 Vitrine Mod **自己负责显示的文字**；不会把 Spotify 官方 UI、系统提示或第三方界面强制改成中文。

## 自行构建与签名

**本仓库不公开分发包含 Spotify 的可安装 IPA。** GitHub Release 附带的 Source code ZIP 只是源码，不是安装包。

1. Fork 本仓库并确保有 `i18n/zh-hans` 分支，启用 Actions。
2. 自行依法准备兼容 Spotify IPA，在 Fork 的 Secrets 配置 `SPOTIFY_IPA_URL`，最好同时配置对应 `SPOTIFY_IPA_SHA256`。
3. 运行 [Build IPA from your own Spotify IPA](https://github.com/HypnosysNyx/vitrine/actions/workflows/build-ipa.yml)，选择中文分支。
4. 从该次 Actions 运行获取构建 Artifact，使用自己的签名证书安装。Artifact 会过期；构建成功也不等于实机所有功能经过验证。

已确认适配的 Spotify 版本以 [README](README.md) 所列 **9.1.78、9.1.88、9.1.90** 为准；重设计为 iOS 26+，旧版 iOS 有实验性限制。

## 回归检查

```bash
python3 scripts/sync-zh-hans.py --check
python3 scripts/check-zh-hans-coverage.py
python3 scripts/check-zh-hans-placeholders.py
python3 scripts/audit-mod-ui-literals.py
python3 scripts/audit-mod-ui-renderers.py
```

[CI 检查](https://github.com/HypnosysNyx/vitrine/actions/workflows/check-zh-hans.yml) · [Releases](https://github.com/HypnosysNyx/vitrine/releases) · [问题反馈](https://github.com/HypnosysNyx/vitrine/issues)

静态检查、编译成功或单次 IPA 构建均不能替代真机截图验收。不要在公开仓库上传个人 IPA、签名证书、密码或私有资源。

遵循 [GPL-3.0](LICENSE)，保留原 Vitrine、spoti.pw 及其他来源的许可与致谢。本项目不是 Spotify/Vitrine 官方发行版。