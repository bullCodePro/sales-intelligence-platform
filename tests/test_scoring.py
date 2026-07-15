import unittest
from types import SimpleNamespace

from packages.scoring.service import score_company


class ScoringTest(unittest.TestCase):
    def test_score_company_assigns_high_fit_tier(self) -> None:
        company = SimpleNamespace(
            id="company-1",
            name="Acme",
            industry="SaaS",
            country="United States",
            employee_count=220,
            confidence=0.8,
        )

        score = score_company(
            company,
            {
                "industries": ["SaaS"],
                "countries": ["United States"],
                "min_employees": 200,
                "max_employees": 1000,
            },
        )

        self.assertEqual(score["tier"], "A")
        self.assertGreaterEqual(score["score"], 80)
        self.assertIn("industry match", score["reasons"])


if __name__ == "__main__":
    unittest.main()
