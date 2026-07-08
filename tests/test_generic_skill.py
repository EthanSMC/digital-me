from pathlib import Path
import importlib.util
import json
import tempfile
import unittest
import zipfile

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]


def read(relative_path: str) -> str:
    return (ROOT / relative_path).read_text(encoding="utf-8")


def load_module(relative_path: str):
    path = ROOT / relative_path
    spec = importlib.util.spec_from_file_location(path.stem, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not load module from {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class GenericSkillTests(unittest.TestCase):
    def test_readme_version_matches_version_file(self):
        version = read("VERSION").strip()
        readme = read("README.md")
        package = json.loads(read("package.json"))

        self.assertEqual(version, "0.2.0")
        self.assertEqual(package["version"], version)
        self.assertIn(f"当前版本：`v{version}`", readme)
        self.assertIn(f"## v{version} 新功能", readme)
        self.assertIn("@ethansmc/digital-me", readme)
        self.assertIn(f"github:EthanSMC/digital-me#v{version}", readme)

    def test_main_skill_is_generic_fast_creator(self):
        text = read("SKILL.md")

        required_phrases = [
            "任何人",
            "快速模式",
            "系统模式",
            "主形象",
            "social media 头像",
            "identity_card.md",
            "prompt_seed.md",
        ]
        for phrase in required_phrases:
            self.assertIn(phrase, text)

    def test_main_skill_does_not_default_to_ethan_details(self):
        text = read("SKILL.md")

        banned_phrases = [
            "WUSTL",
            "MSF",
            "MacBook 作为主工作道具",
            "金融科技 / 留学生 / builder",
            "默认案例是 digital Ethan",
        ]
        for phrase in banned_phrases:
            self.assertNotIn(phrase, text)

    def test_prompt_recipes_are_placeholder_driven(self):
        text = read("references/prompt-recipes.md")

        required_phrases = [
            "[人物身份锚点]",
            "[脸部和发型锚点]",
            "[衣服/气质锚点]",
            "[使用场景]",
            "social media avatar",
            "Avoid Case Drift",
            "Do not say \"avoid looking like [case name]\"",
            "short dark hair, round glasses, white shirt",
        ]
        for phrase in required_phrases:
            self.assertIn(phrase, text)

        banned_phrases = [
            "digital Ethan",
            "WUSTL",
            "MSF",
            "silver MacBook",
        ]
        for phrase in banned_phrases:
            self.assertNotIn(phrase, text)

    def test_templates_do_not_ship_ethan_as_default_persona(self):
        template_paths = [
            "templates/photo_wardrobe_config.example.json",
            "templates/generated_variants_config.example.json",
        ]

        for template_path in template_paths:
            text = read(template_path)
            self.assertNotIn("digital Ethan", text)
            self.assertNotIn("digital_Ethan", text)
            self.assertNotIn("MacBook", text)

    def test_builtin_case_stays_lightweight(self):
        text = read("references/lightweight-case-note.md")

        banned_phrases = [
            "WUSTL",
            "MSF",
            "MacBook",
            "gray coat",
            "beige hoodie",
            "black crewneck",
            "finance background",
        ]
        for phrase in banned_phrases:
            self.assertNotIn(phrase, text)

    def test_video_practice_is_request_driven(self):
        skill_text = read("SKILL.md")
        practice_text = read("references/video-practice.md")
        readme_text = read("README.md")

        required_phrases = [
            "用户要什么视频",
            "资产是素材，不是脚本",
            "根据用户目标选结构",
            "中间 70% 高度",
            "不要把所有视频都套成",
        ]
        for phrase in required_phrases:
            self.assertIn(phrase, practice_text)

        old_paths = [
            "references/xiaohongshu-video-practice.md",
            "templates/xiaohongshu_video_shot_plan.example.json",
            "templates/xiaohongshu_video_narration.example.txt",
        ]
        for path in old_paths:
            self.assertNotIn(path, skill_text)
            self.assertNotIn(path, readme_text)

    def test_default_assets_include_social_media_avatar(self):
        creation = read("references/creation-workflow.md")
        qa = read("references/qa-checklist.md")
        project_template = read("templates/project_readme.template.md")

        required_phrases = [
            "social media avatar",
            "square and circular crops",
            "01-social-media-avatar.png",
            "01-social-media-avatar-circle.png",
            "Social media avatar stays recognizable",
        ]
        combined = "\n".join([creation, qa, project_template])
        for phrase in required_phrases:
            self.assertIn(phrase, combined)

    def test_avatar_generation_practice_is_reference_driven(self):
        skill_text = read("SKILL.md")
        practice = read("references/avatar-generation-practice.md")
        prompt_recipes = read("references/prompt-recipes.md")

        required_phrases = [
            "primary_identity_reference",
            "previous_attempt",
            "Do not hand-draw the avatar with local scripts",
            "square 1:1 social media profile avatar",
            "export_circle_avatar.py",
            "Do not replace a site or product's default avatar until the user confirms",
        ]
        combined = "\n".join([skill_text, practice, prompt_recipes])
        for phrase in required_phrases:
            self.assertIn(phrase, combined)

    def test_circle_avatar_export_makes_transparent_corners(self):
        exporter = load_module("scripts/export_circle_avatar.py")

        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp = Path(tmp_dir)
            source = tmp / "source.png"
            out = tmp / "circle.png"
            Image.new("RGBA", (64, 64), (10, 120, 200, 255)).save(source)

            exporter.export_circle_avatar(source, out, 64)

            result = Image.open(out).convert("RGBA")
            self.assertEqual(result.size, (64, 64))
            self.assertEqual(result.getpixel((0, 0))[3], 0)
            self.assertGreater(result.getpixel((32, 32))[3], 240)

    def test_rendered_narration_keeps_subtitle_boundaries(self):
        renderer = load_module("scripts/render_still_video.py")

        shots = [
            {"subtitle": ["第一句。", "第二句。"]},
            {"subtitle": "第三句。"},
        ]
        with tempfile.TemporaryDirectory() as tmp_dir:
            out = Path(tmp_dir) / "narration.txt"
            renderer.write_narration(shots, out)
            self.assertEqual(
                out.read_text(encoding="utf-8"),
                "第一句。\n第二句。\n第三句。\n",
            )

    def test_skill_package_contains_only_runtime_skill_files(self):
        with zipfile.ZipFile(ROOT / "digital-me.skill") as package:
            names = set(package.namelist())

        required_paths = [
            "SKILL.md",
            "references/creation-workflow.md",
            "references/avatar-generation-practice.md",
            "references/identity-and-wardrobe-model.md",
            "references/prompt-recipes.md",
            "references/qa-checklist.md",
            "references/video-practice.md",
            "templates/identity_model.template.md",
            "scripts/export_circle_avatar.py",
            "scripts/render_still_video.py",
            "examples/ethan/main-avatar.png",
        ]
        for path in required_paths:
            self.assertIn(path, names)

        banned_paths = [
            "README.md",
            ".gitignore",
            "tests/test_generic_skill.py",
        ]
        for path in banned_paths:
            self.assertNotIn(path, names)

        self.assertFalse(any(path.startswith("tests/") for path in names))
        self.assertFalse(any("__pycache__" in path or path.endswith(".pyc") for path in names))


if __name__ == "__main__":
    unittest.main()
