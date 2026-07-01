from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]


def read(relative_path: str) -> str:
    return (ROOT / relative_path).read_text(encoding="utf-8")


class GenericSkillTests(unittest.TestCase):
    def test_main_skill_is_generic_fast_creator(self):
        text = read("SKILL.md")

        required_phrases = [
            "任何人",
            "快速模式",
            "系统模式",
            "主形象",
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


if __name__ == "__main__":
    unittest.main()
