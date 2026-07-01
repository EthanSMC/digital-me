# Prompt Recipes

## Main Avatar Prompt

Use this as the generic starting point, replacing every bracketed slot with details from the user's photos or description:

```text
Create a personal IP character illustration of [人物身份锚点]: [脸部和发型锚点], [表情/姿态锚点], wearing [衣服/气质锚点], for [使用场景]. Use [默认画风], clear recognizable face, simple readable silhouette, clean background, restrained colors. Avoid [禁止项].
```

If the user wants a fast first version and has not chosen a style, use:

```text
clean hand-drawn black ink line, sparse accurate color, white or near-white background, realistic but simplified proportions, not a cute mascot, not anime, not corporate stock art
```

## Variant Prompt

Use the same prompt seed, then add one scene-specific state:

```text
Keep the same identity: [人物身份锚点], [脸部和发型锚点]. Create a [使用场景] variant: [动作/姿势], wearing [衣服/气质锚点], with [真实相关道具或无道具]. Preserve the main avatar's drawing style and recognition anchors. Avoid [禁止项].
```

Good default variant set:

- profile/avatar: clear face, strong recognition.
- working/creating: a real tool or object from the user's work only if useful.
- explaining/teaching: one hand gesture, simple diagram or note element if needed.
- social/community: approachable posture, lighter mood.
- professional/brand: cleaner outfit, more composed pose.

## Text-Only User Prompt

When no photos are available, ask for one concise input first if the prompt lacks visual anchors:

```text
What should this person's image mainly communicate: professional, friendly, playful, expert, creator, teacher, founder, or something else?
```

Then build the prompt from the answer. Do not invent sensitive traits. If visual identity is missing, use neutral, non-specific language.

## Generated Wardrobe Reuse

When using a generated clothing crop:

```text
Keep the same person identity and drawing style. Borrow the clothing shape, color, and silhouette from [selected generated clothing reference], but redraw it naturally on the new pose. Do not copy the old pose unless requested.
```

## Iteration Language

Useful user feedback translations:

- "更像本人" -> strengthen face, hair, posture, and expression anchors; reduce generic styling.
- "太幼稚" -> use more realistic proportions, calmer expression, fewer playful details.
- "太商业插画" -> reduce polished stock-art gradients, keep hand-drawn line and simpler background.
- "太二次元" -> reduce anime eyes/hair exaggeration, keep real face proportions.
- "更专业" -> cleaner silhouette, fewer accessories, more composed posture.
- "更亲和" -> softer expression, relaxed shoulders, warmer but restrained color.
- "颜色线条不如上一版" -> preserve previous line density and color restraint while changing only the requested feature.
- "只要主要角色" -> remove props/background that do not support identity.
