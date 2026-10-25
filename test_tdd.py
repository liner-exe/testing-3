import unittest
from core import SurveyManager


class TestSurveyManagerTDD(unittest.TestCase):
    def setUp(self) -> None:
        self.manager = SurveyManager()

    def test_create_survey_success(self) -> None:
        survey = self.manager.create_survey("Ваш любимый язык?", ["Python", "Go", "Rust"])
        self.assertEqual(survey["id"], 1)
        self.assertEqual(survey["question"], "Ваш любимый язык?")
        self.assertEqual(survey["options"], ["Python", "Go", "Rust"])
        self.assertEqual(survey["total_votes"], 0)
        self.assertEqual(survey["votes"], {"Python": 0, "Go": 0, "Rust": 0})

    def test_create_survey_validation_errors(self) -> None:
        with self.assertRaises(ValueError):
            self.manager.create_survey("   ", ["Да", "Нет"])
        with self.assertRaises(ValueError):
            self.manager.create_survey("Один вариант?", ["Да"])
        with self.assertRaises(ValueError):
            self.manager.create_survey("Дубликаты?", ["Да", "Да"])

    def test_submit_answer_success(self) -> None:
        survey = self.manager.create_survey("Формат обучения?", ["Очно", "Онлайн"])
        updated = self.manager.submit_answer(survey["id"], "Онлайн")
        self.assertEqual(updated["total_votes"], 1)
        self.assertEqual(updated["votes"]["Онлайн"], 1)
        self.assertEqual(updated["votes"]["Очно"], 0)

    def test_submit_answer_errors(self) -> None:
        survey = self.manager.create_survey("Оценка курса?", ["Отлично", "Хорошо"])
        with self.assertRaises(KeyError):
            self.manager.submit_answer(999, "Отлично")
        with self.assertRaises(ValueError):
            self.manager.submit_answer(survey["id"], "Плохо")


if __name__ == "__main__":
    unittest.main()