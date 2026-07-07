# Source Skills And References

This skill packages the useful parts of a personal image creation workflow and the references used to make it reusable.

## imagegen

Used for raster image generation and image editing.

Key habits carried into this skill:

- Generate one final image per asset, not a multi-image collage, unless the user asks for a contact sheet.
- For local image edits, inspect the image first.
- Copy useful generated outputs into the project folder instead of leaving them only in temporary generation folders.

## ian-xiaohei-illustrations

Used as the structural reference for a lean visual-generation skill.

Useful borrowed principles:

- Keep `SKILL.md` short and route details into `references/`.
- Preserve a clear visual DNA.
- Avoid PPT-style diagrams, cute mascot drift, and over-explaining.
- Save generated assets with stable semantic names.

## brainstorming

Used during early IP exploration.

Useful borrowed habit:

- Treat fuzzy identity work as a collaborative narrowing process.
- Extract user corrections as rules, not one-off preferences.

## skill-creator

Used to package this process into a reusable skill.

Useful borrowed structure:

```text
skill-name/
├── SKILL.md
├── references/
├── scripts/
├── templates/
└── examples/  # optional low-frequency case assets
```

## digital-me-video-practice

Generalized from the first short-video experiment into a request-driven video practice for Digital Me after the avatar system is stable.

Useful carried-over workflow:

- Treat the digital person as the protagonist, not as a product demo prop.
- Start from the user's requested video, then map existing Digital Me assets to the right shots.
- Use first-person structure only when the request is a self-introduction or origin story.
- Keep Chinese text out of generated images where possible; burn readable titles and subtitles locally.
- Use MiniMax or a real recording for Mandarin voiceover, and avoid shipping API keys in files.
- Keep `video-use` optional for later precision editing when local still-frame video is no longer enough.

## reference-driven-avatar-practice

Generalized from generating a more accurate personal IP avatar from an existing character cutout plus feedback on a rejected prior attempt.

Useful carried-over workflow:

- Treat the strongest approved cutout or main avatar as the primary identity reference.
- Treat rejected avatar versions as feedback artifacts, not identity truth.
- Use image generation for the character image; use local scripts only for deterministic exports such as circular masks.
- Deliver both a square avatar and a circular transparent export.
- Copy into external projects with versioned filenames, and replace defaults only after user confirmation.
