import hashlib
import re
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]


class SiteContentTests(unittest.TestCase):
    def test_2026_teaching_and_service_are_visible(self):
        page = (ROOT / "index.html").read_text(encoding="utf-8")

        for text in ("MOPTA 2026", "GradOpt", "ColOpt", "OptML", "LLMs", "Hugging Face"):
            with self.subTest(text=text):
                self.assertIn(text, page)

        self.assertNotIn("Co-chairing the 2026 MOPTA", page)
        self.assertNotIn("© 2025", page)

    def test_current_publications_and_projects_are_linked(self):
        page = (ROOT / "index.html").read_text(encoding="utf-8")

        for url in (
            "https://arxiv.org/abs/2505.15788",
            "https://arxiv.org/abs/2605.06945",
            "https://github.com/zahrakhatti/fairget",
            "https://github.com/zahrakhatti/fairget/releases/tag/v0.1.0",
            "https://github.com/zahrakhatti/as-ipm",
            "https://coral.ise.lehigh.edu/mopta2026/committee/",
        ):
            with self.subTest(url=url):
                self.assertIn(url, page)

        self.assertNotIn("Fair Clustering", page)
        self.assertNotIn("fair-clustering", page)
        self.assertIn("Open-source Python package · v0.1.0", page)
        self.assertIn(
            "Low-Order Explicit Hessian Imitation Method for Large-Scale Supervised Machine Learning",
            page,
        )
        for removed_text in (
            "Co-authored a new preprint on low-order Hessian imitation",
            "Constrained LoRA Fine-Tuning for Bias-Controlled LLMs",
            "Hugging Face PEFT/LoRA",
            "<h4>Low-Order Hessian Imitation</h4>",
        ):
            with self.subTest(removed_text=removed_text):
                self.assertNotIn(removed_text, page)

    def test_local_assets_exist(self):
        page = (ROOT / "index.html").read_text(encoding="utf-8")
        references = re.findall(r'(?:href|src)="([^"]+)"', page)

        local_references = [
            reference
            for reference in references
            if not reference.startswith(("http://", "https://", "mailto:", "#"))
        ]
        self.assertGreater(len(local_references), 0)
        for reference in local_references:
            with self.subTest(reference=reference):
                self.assertTrue((ROOT / reference).is_file())

    def test_resume_is_the_supplied_2026_version(self):
        resume = ROOT / "Zahra_Khatti_Resume.pdf"
        digest = hashlib.sha256(resume.read_bytes()).hexdigest()

        self.assertEqual(
            digest,
            "0317fa123c753ca2464f273884012c1072df5ad2f5b374ffe13983c2c571aa14",
        )


if __name__ == "__main__":
    unittest.main()
