from dataclasses import dataclass
from typing import Dict, Any, List


@dataclass
class Response:
    status_code: int
    body: Dict[str, Any]


class SurveyManager:
    def __init__(self):
        self._surveys: Dict[int, Dict[str, Any]] = {}
        self._next_id: int = 1

    @staticmethod
    def _validate_survey_input(question: str, options: List[str]) -> List[str]:
        if not question or not question.strip():
            raise ValueError("Текст вопроса не может быть пустым")
        if not options or len(options) < 2:
            raise ValueError("Опрос должен содержать минимум 2 варианта ответа")
        cleaned = [opt.strip() for opt in options if opt and opt.strip()]
        if len(cleaned) != len(options) or len(set(cleaned)) != len(cleaned):
            raise ValueError("Варианты ответа должны быть непустыми и уникальными")
        return cleaned

    def create_survey(self, question: str, options: List[str]) -> Dict[str, Any]:
        cleaned_options = self._validate_survey_input(question, options)
        survey = {
            "id": self._next_id,
            "question": question.strip(),
            "options": cleaned_options,
            "votes": {opt: 0 for opt in cleaned_options},
            "total_votes": 0,
        }
        self._surveys[self._next_id] = survey
        self._next_id += 1
        return survey

    def submit_answer(self, survey_id: int, option: str) -> Dict[str, Any]:
        if survey_id not in self._surveys:
            raise KeyError(f"Опрос с ID {survey_id} не найден")
        survey = self._surveys[survey_id]
        if option not in survey["votes"]:
            raise ValueError(f"Вариант ответа '{option}' отсутствует в опросе")
        survey["votes"][option] += 1
        survey["total_votes"] += 1
        return survey

    def get_analytics(self, survey_id: int) -> Dict[str, Any]:
        if survey_id not in self._surveys:
            raise KeyError(f"Опрос с ID {survey_id} не найден")
        survey = self._surveys[survey_id]
        total = survey["total_votes"]
        distribution = {
            opt: round((count / total) * 100.0, 2) if total > 0 else 0.0
            for opt, count in survey["votes"].items()
        }
        leading_option = (
            max(survey["votes"], key=survey["votes"].get) if total > 0 else None
        )
        return {
            "survey_id": survey["id"],
            "question": survey["question"],
            "total_votes": total,
            "counts": dict(survey["votes"]),
            "percentages": distribution,
            "leading_option": leading_option,
        }

    def request_create_survey(self, question: str, options: List[str]) -> Response:
        try:
            survey = self.create_survey(question, options)
            return Response(200, {"message": "Опрос создан", "survey": survey})
        except ValueError as e:
            return Response(400, {"error": str(e)})

    def request_submit_answer(self, survey_id: int, option: str) -> Response:
        try:
            survey = self.submit_answer(survey_id, option)
            return Response(200, {"message": "Ответ принят", "survey": survey})
        except (KeyError, ValueError) as e:
            return Response(400, {"error": str(e).strip("'")})

    def request_analytics(self, survey_id: int) -> Response:
        try:
            analytics = self.get_analytics(survey_id)
            return Response(200, {"message": "Аналитика сформирована", "analytics": analytics})
        except KeyError as e:
            return Response(400, {"error": str(e).strip("'")})