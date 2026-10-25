import unittest
from core import SurveyManager


class TestSurveyManagerATDD(unittest.TestCase):
    def setUp(self) -> None:
        self.service = SurveyManager()

    def test_scenario_analytics_calculation_accuracy(self) -> None:
        """Сценарий 1. Проверка корректности расчёта долей и лидера после голосования."""
        resp_create = self.service.request_create_survey(
            "Какую СУБД выбрать?", ["PostgreSQL", "MySQL", "SQLite"]
        )
        self.assertEqual(resp_create.status_code, 200)
        survey_id = resp_create.body["survey"]["id"]

        self.service.request_submit_answer(survey_id, "PostgreSQL")
        self.service.request_submit_answer(survey_id, "PostgreSQL")
        self.service.request_submit_answer(survey_id, "MySQL")
        self.service.request_submit_answer(survey_id, "SQLite")

        resp_analytics = self.service.request_analytics(survey_id)
        self.assertEqual(resp_analytics.status_code, 200)
        data = resp_analytics.body["analytics"]

        self.assertEqual(data["total_votes"], 4)
        self.assertEqual(data["percentages"]["PostgreSQL"], 50.0)
        self.assertEqual(data["percentages"]["MySQL"], 25.0)
        self.assertEqual(data["percentages"]["SQLite"], 25.0)
        self.assertEqual(data["leading_option"], "PostgreSQL")

    def test_scenario_analytics_for_empty_survey(self) -> None:
        """Сценарий 2. Аналитика для опроса без ответов (защита от деления на ноль)."""
        resp_create = self.service.request_create_survey("Нужен ли перерыв?", ["Да", "Нет"])
        survey_id = resp_create.body["survey"]["id"]

        resp_analytics = self.service.request_analytics(survey_id)
        self.assertEqual(resp_analytics.status_code, 200)
        data = resp_analytics.body["analytics"]

        self.assertEqual(data["total_votes"], 0)
        self.assertEqual(data["percentages"], {"Да": 0.0, "Нет": 0.0})
        self.assertIsNone(data["leading_option"])

    def test_scenario_analytics_nonexistent_survey(self) -> None:
        """Сценарий 3. Запрос аналитики для несуществующего опроса."""
        resp = self.service.request_analytics(404)
        self.assertEqual(resp.status_code, 400)
        self.assertIn("Опрос с ID 404 не найден", resp.body["error"])


if __name__ == "__main__":
    unittest.main()