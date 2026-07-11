# personal_[name]

## Core Logic

1. Build the identity card from the user's photos or description.
2. Create a reusable prompt seed.
3. Generate the one asset currently requested; default to the main avatar when unspecified.
4. Generate a social media avatar for square and circular crops only when requested.
5. After identity confirmation, generate practical variants when requested.
6. Save successful variants and prompts for future reuse.

## Identity Anchor

- ...

## Prompt Seed

```text
...
```

## Variants

- `main-avatar.png`
- `variants/01-social-media-avatar.png`
- `variants/01-social-media-avatar-circle.png`
- `variants/02-profile.png`
- `variants/03-working.png`
- `variants/04-explaining.png`

## Avatar References

- Primary identity reference: ...
- Previous attempt feedback: ...
- External copy targets: copy only after user confirmation.

## Optional Full Library Folders

- `source_photos/`
- `clothing_refs/`
- `generated_variants/`
- `generated_clothing_refs/`
