---
type: 情报
tags: [知识管理, 工具, 备份, 同步, Git, Syncthing]
created: 2026-08-21
status: 可用
source: "自建 + 参考 [[Obsidian学习资源索引]] 中 Syncthing / Git 视频"
converter: "审计方法地图配套 — 蓝带（多端同步 + 离机备份）落地方案"
---

# vault 备份与多端同步方案

> 配套 [[审计程序库]] 的"审计方法地图"蓝图 —— 把贯穿全库的**蓝带**（多端同步 + 离机备份）落成可操作步骤。

## 一、现状盘点

| 项目 | 状态 | 说明 |
|---|---|---|
| Git 本地仓库 | ✅ 已有 | vault 已 `git init`，分支 `main` |
| 离机备份（GitHub 远程） | ✅ 已有 | 远程 `origin = git@github.com:zhaojuan888/test-repo.git`，有 **daily backup 自动化**每日提交（最近 2026-08-21） |
| 微信内容同步 | ✅ 已有 | Obsync 把微信收藏同步进 vault（**仅微信，不是整库多端同步**）|
| **整库多端实时同步** | ⚠️ 缺口 | 手机/另一台电脑实时看改整个 vault，目前没有 |

**结论：** 离机备份已解决（Git→GitHub）；唯一真实缺口是**整库多端同步**。

## 二、缺口：整库多端同步（推荐 Syncthing）

Syncthing 是 P2P、免费、国内可用、不依赖中心云的文件夹同步，**最适合 vault 这类小文件多、要实时双向同步的场景**。

**步骤（每台设备一次）：**
1. 安装：官网 syncthing.net（Win/macOS/Linux 均有）；手机用 F-Droid 或官网 apk（iOS 无官方客户端，可用 Möbius Sync）。
2. 主机（D 盘 vault）打开 Syncthing → 添加文件夹（指向 vault 根）→ 设"共享"→ 复制本机**设备 ID**。
3. 另一台设备安装后 → 添加"远程设备"（粘贴主机设备 ID）→ 添加同一文件夹（读写权限）→ 双向同步建立。
4. 两端都装 Obsidian 打开同一 vault；**Syncthing 只管文件同步，Obsidian 管编辑**。
5. 避坑：
   - 别让 Git 与 Syncthing 同时狂改同一文件产生冲突——vault 依赖 daily backup 提交即可，Syncthing 同步工作区文件，二者通常不冲突（提交是偶发动作）。
   - 在 Syncthing 忽略 `.trash/`、`*.tmp` 等，减少大附件（PDF/图片）同步流量。
   - 冲突文件 Syncthing 会生成 `.sync-conflict` 副本，定期清理即可。

**备选方案：** 国内云盘做"同步盘"（如资源索引 🟢 第 4 条），更省心但依赖中心云服务、隐私性弱于 P2P。

## 三、Git 提交纪律（已自动化，补一次手工提交）

- 今日新增的知识库笔记（IPO 知识库整理 13 篇、行业会计处理手册 2 篇、行业审计对照 2 篇、Obsidian 学习资源索引、入门练习）已在 WorkBuddy 协助下 `git add -A` + 提交并推送，确保离机备份为最新。
- 日常：依赖既有 **daily backup** 自动化即可；大批量手工整理后手动补一次提交更稳。

## 四、三者关系（蓝带全景）

```
捕获(Web Clipper / MinerU / Obsync / IMA MCP)
   → 加工(staging 自动转 md)
   → 组织(2-知识库 PARA+JD，原子笔记)
   → 导航(Dataview MOC，见 [[审计程序库]])
   → 产出(9-产出)
        └─ 贯穿蓝带：Syncthing 多端同步（随时在哪台设备都能看/改）
                       + Git→GitHub 离机备份（防丢）
```

## 关联

- [[Obsidian学习资源索引]]（Syncthing / Git 视频入口）
- [[Obsidian入门练习-7天上手计划]]（每日闭环练习）
- [[审计程序库]]（审计方法地图主入口）
