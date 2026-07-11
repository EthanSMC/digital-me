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

## Avoid Case Drift

When using built-in examples only as quality references, keep them out of the generation prompt. Do not say "avoid looking like [case name]" inside the prompt; naming a case can still pull the image toward that case. Instead, write positive anchors for the new person:

```text
Use [new person's specific age range, face shape, hair silhouette, expression, wardrobe, color language, and real-use prop].
```

For text-only users, do not default to the example's broad silhouette. If no photo is available, choose neutral placeholders or ask for the missing visual anchors rather than falling back to short dark hair, round glasses, white shirt, creator posture, or any other case-specific cluster.

## Variant Prompt

Use the same prompt seed, then add one scene-specific state:

```text
Keep the same identity: [人物身份锚点], [脸部和发型锚点]. Create a [使用场景] variant: [动作/姿势], wearing [衣服/气质锚点], with [真实相关道具或无道具]. Preserve the main avatar's drawing style and recognition anchors. Avoid [禁止项].
```

Good default variant set:

- social media avatar: square-safe and round-crop safe, clear face and hair, readable at small size, no tiny text or busy props.
- profile/avatar: clear face, strong recognition for non-social profile pages.
- working/creating: a real tool or object from the user's work only if useful.
- explaining/teaching: one hand gesture, simple diagram or note element if needed.
- social/community: approachable posture, lighter mood.
- professional/brand: cleaner outfit, more composed pose.

## Reference-Driven Social Avatar Prompt

When the user has an existing cutout, approved main avatar, or rejected previous attempt, read `avatar-generation-practice.md` and use this shape:

```text
Create a fresh square 1:1 social media profile avatar for [person/IP name], using the provided [primary identity reference] as the primary identity reference.
Keep the likeness close: [face shape], [hair silhouette], [glasses/accessories], [expression], [wardrobe/color anchors], [public vibe].
Use a head-and-shoulders close portrait, centered composition, clean light background, round-crop safe framing, and refined [style direction].
Make it suitable for [platform/use case].
Improve from the previous attempt by [specific feedback translated into positive constraints].
No text, no logo, no watermark, no chibi, no anime exaggeration, no 3D render, no overly cute or generic look.
```

Omit the previous-attempt sentence when there is no rejected attempt.

## Text-Only User Prompt

When no photos are available and the prompt lacks 外貌视觉锚点, ask for one concise input first:

```text
Please share 2-3 stable visual traits, such as hair shape/color, face shape/glasses, age presentation, and usual clothing colors, or provide one reference photo.
```

Then build the prompt from the answer. Do not invent sensitive traits. If the user explicitly does not need a likeness, create a “概念角色，不宣称像本人” and use neutral, non-specific identity language.

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
