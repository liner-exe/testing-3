import json
import os
import unittest
from core import SurveyManager


class TestSurveyManagerSDD(unittest.TestCase):
    def setUp(self) -> None:
        spec_path = os.path.join(os.path.dirname(__file__), "specs.json")
        with open(spec_path, "r", encoding="utf-8") as f:
            self.specs = json.load(f)

    def test_survey_analytics_specifications(self) -> None:
        for spec in self.specs:
            with self.subTest(case_id=spec["case_id"], desc=spec["description"]):
                manager = SurveyManager()
                survey = manager.create_survey(spec["question"], spec["options"])
                survey_id = survey["id"]

                for ans in spec["answers"]:
                    manager.submit_answer(survey_id, ans)

                analytics = manager.get_analytics(survey_id)
                self.assertEqual(analytics["total_votes"], spec["expected_total"])
                self.assertEqual(analytics["percentages"], spec["expected_percentages"])
                self.assertEqual(analytics["leading_option"], spec["expected_leader"])


if __name__ == "__main__":
    unittest.main()