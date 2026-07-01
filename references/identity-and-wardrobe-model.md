# Identity And Wardrobe Model

## Person Model Principles

Model the person through recurring features across photos or through the strongest details in the user's description:

- hair shape, hairline, and overall head silhouette.
- face proportions and the few features that matter most for recognition.
- glasses, facial hair, accessories, or other stable identifiers.
- expression, posture, and social energy.
- body silhouette and clothing fit.
- professional, cultural, or creative context.
- visual style requested by the user.

Do not overfit exact photo lighting, lens distortion, one accidental facial expression, or a temporary prop.

## Identity Card Contract

The identity card should be short enough to reuse but specific enough to generate from:

```markdown
# Identity Card

## Anchors
- [stable face/hair feature]
- [expression/posture]
- [public role or vibe]

## Optional
- [glasses, hat, bag, tool, etc.]

## Avoid
- [styles or details the user rejected]

## Usage
- [avatar, content illustrations, course, social, team page, etc.]
```

## Prompt Seed Contract

The prompt seed turns the identity card into one reusable paragraph:

```text
[person identity], [face/hair anchors], [expression/posture], [wardrobe/style anchors], [use case], [visual style], avoid [must-avoid list].
```

Prefer concrete image language over biography. A job title matters only when it changes the visual mood, outfit, prop, or scenario.

## Wardrobe Categories

Use these categories when the user wants clothing extraction or a reusable asset library:

- `outfits_full`: full silhouettes and complete looks.
- `tops`: shirts, sweaters, hoodies, tees, fleece, blouses.
- `outerwear`: coats, jackets, structured layers.
- `bottoms_shoes`: pants, skirts, dresses when lower-body framing matters, and shoes.
- `accessories`: glasses, hats, bags, watches, tools, devices, microphones, books, instruments, or other personal props.

Categories can be adapted to the person. Do not force every user into the same wardrobe taxonomy if their style needs different buckets.

## Real vs Generated Wardrobe

Keep the two wardrobes separate:

- `clothing_refs/`: from user-provided original photos.
- `generated_clothing_refs/`: from successful AI-generated variants.

The real wardrobe grounds the character in the user. The generated wardrobe preserves what worked in the drawn IP style.

## Tiny Example

A minimal example might be: clean hand-drawn personal avatar, visible face and hair, neutral outfit, simple background, one personal prop only when it supports the user's real use case.

This is not a default template. New user inputs always override the example.
