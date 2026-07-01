# QA Checklist

## Before Generating

- Is there a clear identity anchor from photos or description?
- Is the intended use clear: avatar, content illustration, social profile, course, product, team page, or brand visual?
- Are required traits separated from optional style details?
- Is the outfit or visual mood grounded in the user rather than a built-in example?
- Are must-avoid styles explicit?

## After Generating

Check:

- Face, hair, expression, and posture still match the identity card.
- Outfit follows the selected real or intended wardrobe source.
- Main image does not hide the face with heavy glasses, mask, hat, shadow, or cropping unless the user asked for it.
- Clothing and props are not over-decorated.
- The style matches the requested visual direction.
- There is enough white space or clean framing for the target use.
- It is not an app landing page, PPT icon, generic mascot, or anime portrait unless requested.
- The image feels like this person, not like the built-in example.

## When To Save

Save to `variants/` or `generated_variants/curated/` when:

- the user explicitly likes it, or
- it clearly improves the character system, and
- it has a reusable outfit, pose, expression, state, or prompt pattern.

Extract to `generated_clothing_refs/` only after the variant is worth keeping.

## Naming

Use descriptive names:

```text
01-main-avatar.png
02-profile-half-body.png
03-working-state.png
04-explaining-state.png
05-social-state.png
06-professional-state.png
```

Avoid names that only preserve random generation ids.
