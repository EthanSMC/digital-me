# Creation Workflow

## Intent

Use this workflow when the user wants a reusable personal IP character based on their own photos, an existing portrait, or a short identity description.

Default to quick creation. The useful loop is:

1. Read photos or the user's description.
2. Extract a compact identity card.
3. Create a reusable prompt seed.
4. Generate only the one asset the user currently requested; use a main avatar when no type was specified.
5. Save the output so future sessions can continue.
6. After the user confirms the identity direction, generate more variants when requested.

Only switch to the full library workflow when the user asks for ongoing reuse, wardrobe extraction, batch variants, or a reusable asset package.

## Quick Mode Directory

Use a stable folder so future sessions can continue without guessing:

```text
personal_<name>/
├── README.md
├── main-avatar.png
├── person_model/
│   ├── identity_card.md
│   └── prompt_seed.md
└── variants/
    ├── 01-social-media-avatar.png
    ├── 01-social-media-avatar-circle.png
    ├── 02-profile.png
    ├── 03-working.png
    └── 04-explaining.png
```

## Full Library Directory

Use this only when the user wants a durable asset system:

```text
personal_<name>/
├── README.md
├── main-avatar.png
├── source_photos/
├── person_model/
│   ├── identity_card.md
│   ├── face_hair_notes.md
│   └── prompt_seed.md
├── clothing_refs/
│   ├── sources/
│   ├── cropped/
│   ├── clothing-contact-sheet.jpg
│   ├── wardrobe_manifest.json
│   └── prompts.md
├── generated_variants/
│   ├── curated/
│   ├── generated-variants-contact-sheet.jpg
│   ├── variants_manifest.json
│   └── README.md
└── generated_clothing_refs/
    ├── outfits_full/
    ├── tops/
    ├── outerwear/
    ├── bottoms_shoes/
    ├── accessories/
    ├── generated-clothing-contact-sheet.jpg
    ├── generated_clothing_manifest.json
    └── generated_clothing_prompts.md
```

## Step 1: Read Inputs

For each provided photo or existing character image, note:

- face/hair: repeated identity features, not one-photo noise.
- outfit: top, outerwear, pants, shoes, accessories.
- expression/posture: calm, energetic, friendly, analytical, playful, formal.
- context: creator, teacher, founder, student, designer, operator, community host, etc.
- unusable details: blur, mask hiding identity, bad angle, cropped body.

If the input is an existing IP cutout, approved main avatar, or previous generated avatar, route social avatar generation through `avatar-generation-practice.md`. Use the strongest image as `primary_identity_reference`; use rejected or weaker attempts only as feedback.

For text-only requests without appearance anchors, ask for 2-3 stable visual identity anchors or a reference photo. If the user does not need a likeness, label the output as a concept character rather than claiming it resembles them. Ask about intended usage only after identity information is sufficient.

## Step 2: Write The Identity Card

Create a short model that can be reused:

```markdown
# Identity Card

## Anchors
- ...

## Optional
- ...

## Avoid
- ...

## Usage
- ...
```

The identity card should describe the person in image-generation language. Avoid vague phrases like "looks like the user" unless they are backed by concrete anchors.

## Step 3: Write The Prompt Seed

Create one paragraph that can be reused in every generation:

```markdown
# Prompt Seed

[identity anchors], [face/hair anchors], [wardrobe/style anchors], [default visual style], [must-avoid list].
```

Keep this compact. A future agent should be able to paste it into a new prompt without rereading the whole project.

## Step 4: Generate Main Avatar

The main avatar should prioritize recognition:

- face and hair visible.
- simple pose.
- clear silhouette.
- no heavy background.
- clothing that matches the person's real or intended public image.

If image generation is available and the user asked for output, generate directly. If not, produce the exact prompt and save it.

## Step 5: Generate Variants

Include a social media avatar when requested:

- square-safe composition.
- round-crop safe face, hair, and shoulder framing.
- no tiny text, busy props, or important details near the corners.
- clear recognition at small sizes.
- generated with an image model when identity matters; local scripts can only export the circular crop.

After the user confirms the identity direction, pick 3-5 states from the user's actual use case when requested:

- profile/avatar for non-social profile pages.
- working/creating.
- explaining/teaching.
- social/community.
- product/brand/professional.
- relaxed/daily.

Name files by use case, not random generation ids.

## Step 6: Full Library Mode

When the user wants a long-term asset system, create real wardrobe references from user photos first. Separate them by type and create a contact sheet so the user can see the wardrobe language at a glance.

When a generated variant works, extract reusable clothing, prop, pose, or state references from that generated image too:

- real wardrobe = what the user has actually worn or provided.
- generated wardrobe = what worked visually in the IP system.

Keep both. Future generations can choose either.
