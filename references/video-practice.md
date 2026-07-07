# Video Practice

## 目的

用已经形成的 Digital Me 资产，完成用户要求的视频。这个模块不是“做某一条固定小红书视频”，也不是探索过程复盘；它是 Digital Me 的使用层：当用户已经有主形象、变体、身份卡和素材库后，把这些资产调度成不同类型的视频。

核心判断永远是：

```text
用户要什么视频？
这个 Digital Me 资产库里哪些东西能服务这个视频？
缺什么，最小补什么？
```

## 触发条件

当用户说这些需求时读取本文件：

- “用我的 Digital Me 做一条视频”
- “让这个形象介绍某个 skill / 产品 / 项目”
- “用这个数字形象做教程 / 发布预告 / 课程开场 / 播客片头”
- “根据已有头像和变体剪一个短视频”
- “发小红书 / Reels / Shorts / B 站 / 视频号”

如果用户还没有稳定主形象和至少几个可用状态，先回到主工作流创建或补齐 Digital Me。

## 可用资产

优先盘点这些资产，不要一上来重新生成：

- `README.md` 或 `person_model/identity_card.md`：人物身份、气质、语气、边界。
- `person_model/prompt_seed.md`：生成新关键帧时的身份约束。
- `main-avatar.png`：最稳的识别锚点。
- `variants/` 或 `generated_variants/curated/`：工作、讲解、思考、生活、出行等状态。
- `clothing_refs/` 和 `generated_clothing_refs/`：衣服、道具、配饰、场景一致性。
- 已有视频、音频、字幕、文章或产品资料：用户这次视频真正要讲的内容。

资产是素材，不是脚本。不要因为模板里有“自我介绍”，就把所有视频都做成自我介绍。

## 先识别视频任务

根据用户目标选结构：

- **自我介绍 / origin story**：说明 Digital Me 是谁、怎么诞生、能做什么。
- **skill / 产品介绍**：让 Digital Me 作为讲解者，围绕用户指定的 skill、功能或使用场景展开。
- **教程 / how-to**：用 Digital Me 做步骤主持人，重点是动作、步骤、前后结果。
- **观点 / 解读 / reaction**：用 Digital Me 承载观点和情绪，配合图表、截图或关键词。
- **发布预告 / trailer**：强调即将发生什么、为什么值得看、下一步去哪。
- **课程 / 播客 / 系列片头**：建立识别度和栏目语气，不要塞太多信息。
- **封面动效 / motion poster**：更重视觉钩子和一句话标题，旁白可以很少或没有。

如果用户没有指定平台，按内容目标推断。只有平台会显著影响比例、时长或字幕风格时，才问一个问题。

## 资产到镜头的映射

按镜头意图选择形象状态：

- 开场/身份锚定：用 `main-avatar.png` 或最稳定正面变体。
- 讲解/教程：用拿电脑、指向卡片、写白板、操作工具的变体。
- 思考/观点：用坐姿、侧脸、观察、城市或安静状态。
- 生活/个人品牌：用更松弛的日常、校园、旅行、街景状态。
- 专业/产品：用干净工作状态，减少装饰。

已有变体不够时，沿用 `prompt_seed.md` 生成缺失关键帧。新图只补当前视频需要的动作或场景，不扩展无关素材库。

## 生成视频方案

先写一个轻量 brief：

```text
目标：这条视频要让观众知道/相信/行动什么？
平台：竖屏短视频、横屏讲解、课程片头、封面动效等。
受众：谁会看？
主角：Digital Me 扮演讲述者、主持人、示范者还是视觉符号？
素材：哪些现有图、变体、文档、音频可用？
缺口：需要补哪些关键帧、截图、旁白或字幕？
交付：MP4、封面、字幕、shot plan、素材包。
```

再写 shot plan。不要固定 6 镜头，根据时长决定：

```text
10-20 秒：3-4 个镜头，适合预告、封面动效、单点观点。
30-45 秒：5-7 个镜头，适合短视频、skill/产品简述。
60-90 秒：7-10 个镜头，适合教程或完整解释。
```

每个镜头包含：

- `purpose`：这个镜头解决什么信息。
- `asset`：用哪个已有形象或需要生成什么新关键帧。
- `visual`：画面动作和构图。
- `voiceover`：旁白。
- `onscreen_text`：本地绘制的标题、关键词或字幕。
- `duration`：秒数。

## 视觉规则

- Digital Me 必须服务用户这次的视频主题，不能抢走内容重点。
- 视频主要内容尽量集中在画面中间 70% 高度内；主角脸、手、关键动作、核心道具和主要信息不要贴近顶部或底部，给平台 UI、标题、字幕和裁切留安全空间。
- 中文标题、关键词和字幕优先本地绘制，不依赖图像模型生成准确文字。
- 新关键帧必须沿用身份锚点和 wardrobe refs，不能为了某个场景牺牲人物一致性。
- 如果是运营短视频，保留强钩子和高可读字幕。
- 如果是课程/产品/讲解，优先清晰结构和节奏，不要过度装饰。

## 配音和字幕

优先顺序：

1. 用户真人录音。
2. 用户指定 TTS 声音。
3. MiniMax 等自然中文 TTS。
4. 本地系统语音只作为临时占位。

不要把 API key 写进文件，只使用环境变量。

```bash
export MINIMAX_API_KEY="..."
python scripts/generate_minimax_tts.py \
  --text video_project/audio/narration.txt \
  --out video_project/audio/voice.mp3 \
  --voice-id "Chinese (Mandarin)_Sincere_Adult" \
  --speed 0.98 \
  --api-url https://api.minimaxi.com/v1/t2a_v2
```

如果账号使用国际 endpoint，把 `--api-url` 改为 `https://api.minimax.io/v1/t2a_v2`。

## 合成方式

轻量版本使用静帧关键帧 + 本地烧字 + TTS：

```bash
cp templates/video_shot_plan.example.json video_project/shot_plan.json
cp templates/video_narration.example.txt video_project/audio/narration.txt

python scripts/render_still_video.py \
  --project-dir . \
  --shots video_project/shot_plan.json \
  --audio video_project/audio/voice.mp3 \
  --out video_project/final.mp4 \
  --narration-out video_project/audio/narration_from_shots.txt
```

当前 `render_still_video.py` 默认适合竖屏 `1080x1920` 静帧视频。若用户要求横屏、多轨、BGM、复杂剪辑或更自然动效，先整理素材包，再考虑改脚本或交给视频编辑后端。

## 平台 preset

平台只影响约束，不决定内容：

- 小红书 / Reels / Shorts / TikTok：竖屏、强字幕、开头 3 秒清楚，通常 15-60 秒。
- B 站 / YouTube 横屏：结构更完整，字幕和画面信息密度可更高。
- 课程/播客片头：短、稳定、可复用，少讲细节。
- 产品/skill demo：重点是问题、动作、结果，不要只讲身份故事。

## video-use 扩展点

默认不要引入 `video-use`。当本地脚本能出首版，但遇到下面的问题时提醒用户：

- 需要更自然的推拉、节拍点、转场、BGM 或多轨声音。
- 素材多到需要比较多个 pacing 版本。
- 用户明确要“像正式短视频/剪辑师处理过”的质感。
- 需要把关键帧、截图、录屏、字幕、BGM 和配音统一编排。

触发后只把素材包交给 `video-use` 精剪；不要让它负责人物建模、文案判断和资产一致性。

## QA

检查：

- 视频是否回答了用户这次的具体需求。
- Digital Me 是否像同一个人，且没有偏离身份卡。
- 已有资产是否被合理复用，而不是无谓重生。
- 主要人物、动作和信息是否落在中间 70% 高度内，顶部和底部是否保留安全区。
- 字幕是否可读，且不遮挡脸、手、道具或关键动作。
- 声音是否自然；生硬时先改文案，再换声音或调 speed。
- 没有把 TTS/API key 写进任何文件。

## 避免

- 不要把所有视频都套成“我是谁、我怎么诞生”的自我介绍。
- 不要把一次探索视频当成通用模板。
- 不要因为平台叫小红书，就忽略用户真正要求的视频任务。
- 不要为了做视频重做整个 Digital Me；缺什么补什么。
