---
name: digital-me
description: Use when 用户希望基于真人照片、外貌描述、已有主形象/cutout 或上一版反馈创建或继续使用 Digital Me，包括个人头像、数字分身、个人品牌角色、内容配图角色、身份与穿搭锚点、场景变体、视频、教程、skill/产品讲解、封面、课程或播客片头。
---

# Digital Me

## 核心定位

把任何人的照片或描述快速转成可复用的个人形象 IP。优先让用户尽快得到能用的主形象，再按需要沉淀身份卡、提示词和素材目录。

默认不要把某个案例套给新用户。每个人的身份锚点都从他们自己的照片、描述、职业气质、穿搭和使用场景里提炼。

## 定位技能目录

先把当前已加载 `SKILL.md` 所在目录解析为绝对路径并记作 `SKILL_DIR`。执行脚本或复制模板时始终使用 `"$SKILL_DIR/scripts/..."` 和 `"$SKILL_DIR/templates/..."`；不要假设当前工作目录就是技能目录。

## 先读这些参考

按任务需要读取，不要一次塞满上下文：

- `references/creation-workflow.md`：快速模式和系统模式的完整流程。
- `references/identity-and-wardrobe-model.md`：如何提炼人物、穿搭和风格锚点。
- `references/prompt-recipes.md`：通用主图、变体和迭代提示词模板。
- `references/avatar-generation-practice.md`：如何用已有个人 IP cutout/主形象和上一版反馈生成 social media 头像；只有用户要继续做头像、改头像、从已有 Digital Me 生成头像、或需要方形/圆形头像交付时再读。
- `references/video-practice.md`：如何用已有 Digital Me 资产完成用户指定的视频；只有用户想“使用这个数字形象做视频/短视频/教程/讲解/片头”等内容实践时再读。
- `references/qa-checklist.md`：生成前后检查与保存规则。
- `references/lightweight-case-note.md`：轻量案例记录；只有用户问案例或需要参考归档方式时再读。
- `references/source-skills.md`：本技能打包时吸收的外部技能/参考资料。

如有示例图，它们只用于低频校准线条密度、留白和归档形态。不要复制示例人物、职业、道具或穿搭。

## 工作流

### 1. 选择模式

**快速模式是默认。** 用户给了照片、现有人物图或足够描述，并且想“生成 / 做图 / 头像 / 个人形象 / 数字分身”时，直接推进：

1. 提炼身份锚点。
2. 写 `identity_card.md` 和 `prompt_seed.md`。
3. 默认只生成用户当前要求的 1 张图；没有指定类型时生成 1 张主形象。
4. 保存图片和可复用提示词。

用户明确要求头像套装、多个场景或完整素材包时，可以在同一轮生成对应数量。否则等用户确认身份方向后，再扩展 social media 头像或 3-5 张常用状态变体，避免无请求地增加生成成本。

**系统模式只在用户明确要素材库时使用。** 例如用户要长期迭代、整理衣橱、批量裁剪、打包团队成员形象库，才建立完整 `clothing_refs/`、`generated_variants/` 和 manifest。

如果没有照片，而且描述缺少外貌视觉锚点，只问一个最关键问题：请给出 2-3 个稳定特征，例如发型/发色、脸型/眼镜、年龄呈现、常穿颜色，或者补一张参考照片。如果用户明确不要求像本人，就按用途生成“概念角色，不宣称像本人”。已有足够外貌锚点但缺少用途时，再问头像、内容配图、课程/产品还是品牌视觉。如果照片和目标已经够清楚，就不要停下来长访谈。

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
└── variants/  # 只有用户要求变体时创建
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

如果用户已有主 cutout、主形象、上一版头像或不满意的生成结果，先读取 `references/avatar-generation-practice.md`。本地脚本只能做圆形裁切、缩放、contact sheet 或 manifest；不要用 Pillow/SVG/canvas 手绘主角。

用户确认身份方向或明确要求多图时，才从真实使用场景里选变体。常见选择：

- social media 头像：方形安全、圆形裁切安全，脸和发型清楚，无小字或复杂道具。
- 头像/个人资料状态：半身、清楚、识别度高，可用于非社交平台的 profile 或介绍页。
- 工作/创作状态：拿着或使用与本人工作相关的真实道具。
- 讲解/表达状态：适合文章、课程、播客或视频封面。
- 生活/社交状态：更松弛，但仍保留身份锚点。
- 专业/品牌状态：更正式，用于官网、简历、团队页。

每张图单独生成，不要一次拼成九宫格。成功图保存到 `variants/` 或 `generated_variants/curated/`。用户要求 social media 头像时，生成方形图后再用本地脚本导出圆形版本：

```bash
python3 "$SKILL_DIR/scripts/export_circle_avatar.py" --input variants/01-social-media-avatar.png --out variants/01-social-media-avatar-circle.png --size 1024
```

### 6. 系统模式：沉淀衣服和素材

当用户要长期复用时，再从真人照片中抽取真实穿搭，按类型保存：

- `tops/`
- `outerwear/`
- `bottoms_shoes/`
- `accessories/`
- `outfits_full/`

需要批量裁剪时，用：

```bash
python3 "$SKILL_DIR/scripts/extract_photo_wardrobe_refs.py" --config photo_wardrobe_config.json --output personal_<name>/clothing_refs
```

用户确认某批生成图可用后，再从生成图里抽取生成版衣服和道具：

```bash
python3 "$SKILL_DIR/scripts/extract_generated_clothing_refs.py" --config generated_variants_config.json --output personal_<name>/generated_clothing_refs
```

配置可参考 `"$SKILL_DIR/templates/photo_wardrobe_config.example.json"` 和 `"$SKILL_DIR/templates/generated_variants_config.example.json"`。

### 7. 使用实践：让 Digital Me 出现在内容里

当用户已经有主形象和变体，并且问“怎么使用这个数字形象”“帮我做一个视频/介绍一个 skill/做教程/做封面/发到某个平台”时，进入使用实践，而不是重新创建人物。

先识别用户要交付的内容类型，再调用 Digital Me 资产：

- 视频、短视频、教程、讲解、片头：读取 `references/video-practice.md`。
- 文章或封面配图：沿用 `prompt_seed.md`，围绕当前内容生成单张配图。
- 课程、播客、产品页：先明确受众和场景，再选择讲解、工作、思考或生活变体。

视频实践可复用：

```bash
python3 "$SKILL_DIR/scripts/generate_minimax_tts.py" --help
python3 "$SKILL_DIR/scripts/render_still_video.py" --help
```

如果视频只是首版可发布内容，默认用本地脚本合成。遇到多轨剪辑、转场精修、素材太多、静帧节奏不自然或用户明确要更正式的剪辑质感时：如果当前环境有视频编辑技能或后端，就交付素材包继续精剪；否则仍输出完整素材包和 shot plan，不依赖未安装的技能名。

## 运行依赖

最终图像生成需要图像生成能力。Python 3 和 Pillow 是必需依赖；先运行 `python3 -m pip install -r "$SKILL_DIR/requirements.txt"`。视频合成还需要本地 `ffmpeg`，MiniMax 配音需要 `MINIMAX_API_KEY` 环境变量。中文字幕字体会自动查找 macOS、Windows 和 Linux 常见字体；也可用 `DIGITAL_ME_FONT` 指定字体文件绝对路径。

## 示例不是模板

内置示例只说明“从真人特征到稳定手绘形象”的方法。不要复用示例人物的履历、职业、道具或衣橱。新用户的照片和目标永远优先。

## 交付口径

交付时简短说明：

- 主形象和变体保存在哪。
- `identity_card.md` 和 `prompt_seed.md` 保存在哪。
- 如果用户要求了 social media 头像，说明方形头像和圆形导出保存在哪。
- 如果用户要继续做内容，推荐一个最自然的 practice，例如“用 Digital Me 做教程视频”“介绍某个 skill”或“文章配图”。
- 下一轮生成应该沿用哪些身份锚点，避免哪些偏差。

不要把风格理论讲太长。用户更需要清楚知道“我已经能怎么用，下一次怎么继续生成”。
