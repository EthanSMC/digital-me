---
name: digital-me
description: 用于从真人照片或简短描述快速创建 Digital Me：任何人的可复用个人形象 IP。适合用户要做个人头像、数字分身、人物形象、个人品牌角色、内容配图角色、根据照片提取身份锚点/穿搭、生成主形象和场景变体、保存 prompt seed 和素材目录时。
compatibility: Requires image generation for final art; Python 3 with Pillow is recommended for cropping, contact sheets, and manifests.
---

# Digital Me

## 核心定位

把任何人的照片或描述快速转成可复用的个人形象 IP。优先让用户尽快得到能用的主形象，再按需要沉淀身份卡、提示词和素材目录。

默认不要把某个案例套给新用户。每个人的身份锚点都从他们自己的照片、描述、职业气质、穿搭和使用场景里提炼。

## 先读这些参考

按任务需要读取，不要一次塞满上下文：

- `references/creation-workflow.md`：快速模式和系统模式的完整流程。
- `references/identity-and-wardrobe-model.md`：如何提炼人物、穿搭和风格锚点。
- `references/prompt-recipes.md`：通用主图、变体和迭代提示词模板。
- `references/qa-checklist.md`：生成前后检查与保存规则。
- `references/lightweight-case-note.md`：轻量案例记录；只有用户问案例或需要参考归档方式时再读。
- `references/source-skills.md`：本技能打包时吸收的外部技能/参考资料。

如有示例图，它们只用于低频校准线条密度、留白和归档形态。不要复制示例人物、职业、道具或穿搭。

## 工作流

### 1. 选择模式

**快速模式是默认。** 用户给了照片、现有人物图或足够描述，并且想“生成 / 做图 / 头像 / 个人形象 / 数字分身”时，直接推进：

1. 提炼身份锚点。
2. 写 `identity_card.md` 和 `prompt_seed.md`。
3. 生成 1 张主形象。
4. 生成 3-5 张常用状态变体。
5. 保存图片和可复用提示词。

**系统模式只在用户明确要素材库时使用。** 例如用户要长期迭代、整理衣橱、批量裁剪、打包团队成员形象库，才建立完整 `clothing_refs/`、`generated_variants/` 和 manifest。

如果信息不足，只问一个最关键问题：这个形象主要用于头像、内容配图、社交媒体、课程/产品，还是品牌视觉？如果照片和目标已经够清楚，就不要停下来长访谈。

### 2. 建立工作目录

如果用户没有指定目录，使用：

```text
personal_<name>/
```

快速模式推荐结构：

```text
personal_<name>/
├── README.md
├── main-avatar.png
├── person_model/
│   ├── identity_card.md
│   └── prompt_seed.md
└── variants/
```

系统模式再扩展：

```text
personal_<name>/
├── source_photos/
├── clothing_refs/
├── generated_variants/
└── generated_clothing_refs/
```

### 3. 提炼身份卡

先看用户提供的照片或描述，提炼重复出现、能指导生成的锚点：

- 脸部和发型：脸型、发量、发型轮廓、眼镜、五官中最稳定的特征。
- 表情和姿态：亲和、冷静、幽默、专业、松弛、强表达等。
- 穿搭和色彩：常见衣服类型、颜色、配饰、整体干净度。
- 使用场景：头像、文章配图、课程页、社交媒体、团队页、产品内容。
- 必须避免：不像本人、太幼稚、太二次元、太商业插画、过度装饰等。

把结果写进 `person_model/identity_card.md`。不要只写“像本人”，要写成可执行的生成约束。

### 4. 写提示词种子

把身份卡压缩成 `person_model/prompt_seed.md`，供后续每张图复用。提示词种子必须包括：

- 人物身份锚点。
- 脸部和发型锚点。
- 穿搭/气质锚点。
- 默认画风。
- 禁止项。

如果用户没有指定画风，默认使用干净手绘、白底或极简背景、少量准确颜色、真实比例。不要默认套用任何案例角色。

### 5. 生成主形象与变体

主形象先稳住身份：正面或三分之二视角，脸和发型清楚，穿搭符合本人气质，背景尽量干净。

变体从用户的真实使用场景里选 3-5 个。常见选择：

- 头像状态：半身、清楚、识别度高。
- 工作/创作状态：拿着或使用与本人工作相关的真实道具。
- 讲解/表达状态：适合文章、课程、播客或视频封面。
- 生活/社交状态：更松弛，但仍保留身份锚点。
- 专业/品牌状态：更正式，用于官网、简历、团队页。

每张图单独生成，不要一次拼成九宫格。成功图保存到 `variants/` 或 `generated_variants/curated/`。

### 6. 系统模式：沉淀衣服和素材

当用户要长期复用时，再从真人照片中抽取真实穿搭，按类型保存：

- `tops/`
- `outerwear/`
- `bottoms_shoes/`
- `accessories/`
- `outfits_full/`

需要批量裁剪时，用：

```bash
python scripts/extract_photo_wardrobe_refs.py --config photo_wardrobe_config.json --output personal_<name>/clothing_refs
```

用户确认某批生成图可用后，再从生成图里抽取生成版衣服和道具：

```bash
python scripts/extract_generated_clothing_refs.py --config generated_variants_config.json --output personal_<name>/generated_clothing_refs
```

配置可参考 `templates/photo_wardrobe_config.example.json` 和 `templates/generated_variants_config.example.json`。

## 示例不是模板

内置示例只说明“从真人特征到稳定手绘形象”的方法。不要复用示例人物的履历、职业、道具或衣橱。新用户的照片和目标永远优先。

## 交付口径

交付时简短说明：

- 主形象和变体保存在哪。
- `identity_card.md` 和 `prompt_seed.md` 保存在哪。
- 哪张最适合当头像，哪些适合内容或品牌场景。
- 下一轮生成应该沿用哪些身份锚点，避免哪些偏差。

不要把风格理论讲太长。用户更需要清楚知道“我已经能怎么用，下一次怎么继续生成”。
