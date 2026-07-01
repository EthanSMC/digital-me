# Digital Me

一个用于创建个人形象 IP 的 **Codex 技能**。

把真人照片或简短描述，快速变成一个可持续复用的个人形象 IP。

目标不是做一张“一次性头像”，而是帮每个人沉淀一套自己的数字形象系统：主形象、身份锚点、提示词种子、常用状态变体，以及可继续扩展的衣服/道具/场景参考。

## 核心定位

这个 Codex skill 适合用来做：

- 个人头像、社交媒体头像、播客/视频/课程形象
- 个人品牌角色、数字分身、内容配图角色
- 从真人照片中提取脸、发型、气质和穿搭锚点
- 生成主形象和 3-5 个常用状态变体
- 把成功图片沉淀成后续可复用的 prompt seed 和素材库

默认是快速模式：先做出能用的主形象，再决定要不要进一步整理衣橱、manifest、contact sheet 和长期素材库。

## 案例：Digital Ethan

这是一个完整案例，用来展示这个 skill 能产出什么。案例不是模板；别人使用时，身份锚点应该来自他们自己的照片、职业气质、穿搭和使用场景。

### 主形象

从真实照片中提炼脸部、发型、表情、穿搭和气质锚点后，先生成一个稳定主形象。

![Digital Ethan main avatar](examples/ethan/main-avatar.png)

### 变体组

主形象稳定后，再生成不同状态：工作、城市、校园、观察、日常等。重点是每张图都保持同一个人的识别度，而不是变成不同角色。

![Digital Ethan generated variants](examples/ethan/generated-variants-contact-sheet.jpg)

### 生成版衣橱

从成功生成图里再提取衣服、道具和造型，作为“这个 IP 画风里已经跑通”的参考。

![Digital Ethan generated wardrobe contact sheet](examples/ethan/generated-wardrobe-contact-sheet.jpg)

## 工作流

### 1. 读照片或描述

先提炼这个人真正稳定的身份锚点：

- 脸型、发型、五官里最有识别度的部分
- 表情、姿态和社交气质
- 常见穿搭、色彩、配饰和道具
- 使用场景：头像、内容配图、课程、产品、品牌视觉等
- 必须避免的偏差：太幼稚、太二次元、太商业插画、太不像本人

### 2. 写身份卡

把照片里的观察落成 `identity_card.md`。不要只写“像本人”，要写成可以继续生成的约束。

### 3. 写提示词种子

把身份卡压缩成 `prompt_seed.md`，以后每张图都可以复用这段 seed。

### 4. 生成主形象

主形象优先稳住识别度：脸和发型清楚、姿态简单、背景干净、穿搭符合本人气质。

### 5. 生成变体

默认生成 3-5 张常用状态。每张图单独生成，不拼九宫格。

### 6. 沉淀素材库

如果用户要长期复用，再整理：

- `clothing_refs/`：来自真人照片的真实衣橱
- `generated_variants/`：已确认可用的角色变体
- `generated_clothing_refs/`：来自成功生成图的衣服和道具参考

## 仓库内容

- `SKILL.md`：Codex skill 主入口
- `references/`：工作流、身份建模、提示词、QA 规则
- `templates/`：身份卡和裁剪配置模板
- `scripts/`：裁剪、contact sheet、manifest 辅助脚本
- `examples/ethan/`：Digital Ethan 案例图
- `digital-me.skill`：可安装到 Codex 的技能包

## 验证

```bash
python3 -m unittest tests/test_generic_skill.py
```

## 原则

案例只用于说明方法，不是默认人设。每次创建都应该从当前用户的照片和目标重新提炼，不要复制案例里的职业、道具、穿搭或生活背景。
