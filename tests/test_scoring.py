import unittest

from packages.scoring.service import score_company


class ScoringTest(unittest.TestCase):
    def test_score_company_assigns_high_fit_tier(self) -> None:
        score = score_company(
            {
                "id": 1,
                "name": "Acme",
                "domain": "acme.com",
                "industry": "SaaS",
                "country": "United States",
                "employee_count": 120,
                "revenue_usd": 2_000_000,
                "tech_stack": "HubSpot, Stripe",
            }
        )

        self.assertEqual(score["tier"], "A")
        self.assertGreaterEqual(score["score"], 80)
        self.assertIn("target industry", score["reasons"])


if __name__ == "__main__":
    unittest.main()
