# Avatar Generation Practice

## Purpose

Use this when the user wants a social media avatar from an existing Digital Me / personal IP asset, or wants to refine a previous avatar attempt.

This practice turns real usage into a repeatable loop:

```text
primary identity reference + previous attempt feedback -> new square avatar -> circular export -> user review
```

## Input Roles

Separate input images by role before generating:

- `primary_identity_reference`: the strongest existing image of the person/IP, such as a main cutout, main avatar, or approved character render.
- `secondary_style_reference`: optional image that shows line density, color mood, or rendering style.
- `previous_attempt`: optional avatar that the user rejected or wants improved.

Inspect local image references first so they are visible before image generation. Treat `primary_identity_reference` as the identity anchor. Treat `previous_attempt` as feedback, not as identity truth.

## Generation Rule

Use image generation for the character image. Do not hand-draw the avatar with local scripts, Pillow, SVG, or canvas; those are only for deterministic export tasks such as circular masking, resizing, contact sheets, or manifests.

The square avatar should be:

- 1:1 square.
- head-and-shoulders or close portrait.
- square-crop safe and round-crop safe.
- recognizable at small sizes.
- free of text, logos, watermarks, and tiny props.

## Refinement Loop

If the user says a previous version is too young, too cute, too generic, too anime, too polished, or not enough like the source, convert that feedback into positive generation constraints:

- "too young" -> more mature face proportions, calmer expression, less rounded face, fewer playful details.
- "too cute" -> reduce oversized eyes, reduce bounce in hair, keep posture quieter.
- "not like the source" -> strengthen the source's face shape, hair silhouette, glasses/accessories, expression, and wardrobe anchors.
- "too busy" -> simpler background, no decorative marks, fewer props.

Do not overfit the rejected attempt. It is a diagnostic artifact.

## Prompt Shape

Use this shape, replacing placeholders with the current person's anchors:

```text
Create a fresh square 1:1 social media profile avatar for [person/IP name], using the provided [primary identity reference] as the primary identity reference.
Keep the likeness close: [face shape], [hair silhouette], [glasses/accessories], [expression], [wardrobe/color anchors], [public vibe].
Use a head-and-shoulders close portrait, centered composition, clean light background, round-crop safe framing, and refined [style direction].
Make it suitable for [platform/use case].
Improve from the previous attempt by [specific feedback translated into positive constraints].
No text, no logo, no watermark, no chibi, no anime exaggeration, no 3D render, no overly cute or generic look.
```

If there is no previous attempt, omit that sentence.

## Export

Save the model-generated square image first:

```text
variants/01-social-media-avatar.png
```

Then export a transparent circular version:

```bash
python3 "$SKILL_DIR/scripts/export_circle_avatar.py" \
  --input variants/01-social-media-avatar.png \
  --out variants/01-social-media-avatar-circle.png \
  --size 1024
```

If the user wants to copy the avatar into another project, copy the reviewed asset to a versioned filename. Do not replace a site or product's default avatar until the user confirms.
