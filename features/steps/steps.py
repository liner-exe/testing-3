from behave import given, when, then
from core import SurveyManager


@given('опрос создан с вопросом "{question}" и вариантами "{options_str}"')
def step_given_survey_created(context, question, options_str):
    context.manager = SurveyManager()
    options = [opt.strip() for opt in options_str.split(",")]
    survey = context.manager.create_survey(question, options)
    context.survey_id = survey["id"]


@when('участник отвечает "{option}"')
def step_when_participant_answers(context, option):
    context.manager.submit_answer(context.survey_id, option)


@then("данные обновляются и общее число ответов равно {expected_total:d}")
def step_then_total_updated(context, expected_total):
    analytics = context.manager.get_analytics(context.survey_id)
    assert analytics["total_votes"] == expected_total, (
        f"Ожидалось {expected_total}, получено {analytics['total_votes']}"
    )


@then('количество голосов за вариант "{option}" составляет {expected_count:d}')
def step_then_option_count(context, option, expected_count):
    analytics = context.manager.get_analytics(context.survey_id)
    actual = analytics["counts"][option]
    assert actual == expected_count, f"Ожидалось {expected_count}, получено {actual}"


@then('доля варианта "{option}" в аналитике составляет {expected_pct:f} процентов')
def step_then_option_percentage(context, option, expected_pct):
    analytics = context.manager.get_analytics(context.survey_id)
    actual = analytics["percentages"][option]
    assert actual == expected_pct, f"Ожидалось {expected_pct}%, получено {actual}%"