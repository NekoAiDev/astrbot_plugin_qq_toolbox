# QQ 功能工具箱

<p align="center">
  <img src="./logo.png" width="120" alt="Logo">
</p>

<p align="center">
  <strong>娱乐 / 实用查询 / 内容生成 / 群管工具，20+ 指令一站式集成</strong>
</p>

<p align="center">
  <a href="https://github.com/xiaohondan/astrbot_plugin_qq_toolbox/releases">
    <img src="https://img.shields.io/github/v/release/xiaohondan/astrbot_plugin_qq_toolbox?style=flat-square" alt="Release">
  </a>
  <a href="https://github.com/xiaohondan/astrbot_plugin_qq_toolbox">
    <img src="https://img.shields.io/badge/AstrBot-Plugin-blue?style=flat-square" alt="AstrBot">
  </a>
  <a href="https://github.com/xiaohondan/astrbot_plugin_qq_toolbox/blob/main/main.py">
    <img src="https://img.shields.io/badge/License-MIT-green?style=flat-square" alt="License">
  </a>
</p>

---

## 功能一览

### 🎮 娱乐趣味

| 指令 | 说明 | 示例 |
|------|------|------|
| `/毒鸡汤` | 随机毒鸡汤，治愈你的不开心 | `/毒鸡汤` |
| `/彩虹屁` | 随机彩虹屁，夸就完事了 | `/彩虹屁` |
| `/土味情话` | 随机土味情话 | `/土味情话` |
| `/抽签` | 今日签运（每天结果固定） | `/抽签` |
| `/运势` | 今日运势详情（五大维度评分） | `/运势` |
| `/骰子 [ndm]` | 掷骰子，支持 ndm 格式 | `/骰子 2d6` |
| `/抛硬币` | 抛硬币 | `/抛硬币` |
| `/摇一摇` | 随机选人（群聊可用，30s冷却） | `/摇一摇` |
| `/猜数字` | 猜数字游戏 | `/猜数字 start` |
| `/复读 <内容>` | 复读一句话 | `/复读 你好世界` |

### 🌐 实用查询

| 指令 | 说明 | 示例 |
|------|------|------|
| `/天气 [城市]` | 查询实时天气 | `/天气 Beijing` |
| `/黄历` | 今日黄历宜忌 | `/黄历` |
| `/汇率 <源> <目标>` | 查询实时汇率 | `/汇率 USD CNY` |
| `/查IP <地址>` | 查询 IP 归属地 | `/查IP 8.8.8.8` |
| `/GitHub <用户名>` | 查询 GitHub 用户信息 | `/GitHub xiaohondan` |

### 🎨 内容生成

| 指令 | 说明 | 示例 |
|------|------|------|
| `/二维码 <内容>` | 生成二维码图片 | `/二维码 https://github.com` |
| `/名言` | 随机古诗词名言 | `/名言` |
| `/歌词` | 随机歌曲歌词 | `/歌词` |
| `/文字转图片 <内容>` | 将文字生成渐变背景图片 | `/文字转图片 今天加油鸭` |

### 🧮 工具

| 指令 | 说明 | 示例 |
|------|------|------|
| `/计算 <表达式>` | 安全计算器 | `/计算 (3+5)*2` |
| `/helpme` | 显示帮助菜单 | `/helpme` |

### 🤖 自动功能

| 功能 | 说明 |
|------|------|
| 自动复读 | 群内连续相同消息达到阈值（默认3次）时自动复读 |

---

## 安装

在 AstrBot 中执行：

```
plugin install https://github.com/xiaohondan/astrbot_plugin_qq_toolbox
```

## 配置

在 AstrBot 后台 → 插件配置 → QQ 功能工具箱 中进行以下设置：

| 配置项 | 默认值 | 说明 |
|--------|--------|------|
| 默认天气城市 | `Beijing` | 未指定城市时查询该城市天气 |
| 复读触发次数阈值 | `3` | 连续相同消息达到此次数触发复读 |
| 每日运势按用户ID固定 | `true` | 开启后同一用户每天运势/抽签结果固定 |

## 兼容性

- ✅ QQ 官方机器人
- ✅ OneBot v11（aiocqhttp）
- ✅ 其他平台（文字指令均可用）

## 文件结构

```
astrbot_plugin_qq_toolbox/
├── main.py              # 插件主代码
├── metadata.yaml        # 插件元数据
├── requirements.txt     # 依赖列表
├── _conf_schema.json    # 配置项定义
├── logo.png             # 插件图标
└── README.md            # 说明文档
```

## 更新日志

### v1.0.0 (2026-05-01)
- 首次发布
- 20+ 功能指令
- 娱乐趣味：毒鸡汤、彩虹屁、土味情话、抽签、运势、骰子、抛硬币、摇一摇、猜数字、复读
- 实用查询：天气、黄历、汇率、IP查询、GitHub用户查询
- 内容生成：二维码、名言、歌词、文字转图片
- 工具：计算器、帮助菜单
- 自动功能：群内自动复读

## 作者

**小红蛋** · [GitHub](https://github.com/xiaohondan)

## 许可证

[MIT License](LICENSE)
