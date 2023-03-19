import pytest
from tech_news.analyzer.reading_plan import ReadingPlanService


@pytest.fixture
def list():
    return [
        {
            "title": "titulo 1",
            "reading_time": 5,
        },
        {
            "title": "titulo 2",
            "reading_time": 10,
        },
        {
            "title": "titulo 3",
            "reading_time": 20,
        },
    ]


@pytest.fixture
def dict():
    return {
        "readable": [
            {
                "unfilled_time": 10,
                "chosen_news": [
                    ("titulo 1", 5),
                ],
            },
            {
                "unfilled_time": 5,
                "chosen_news": [
                    ("titulo 2", 10),
                ],
            },
        ],
        "unreadable": [
            ("titulo 3", 20),
        ],
    }


def test_reading_plan_group_news(mocker, dict, list):
    mocker.patch(
        "tech_news.analyzer.reading_plan.ReadingPlanService._db_news_proxy",
        return_value=list,
    )
    result = ReadingPlanService.group_news_for_available_time(15)
    assert result["readable"] == dict["readable"]
    assert result["readable"][0]["unfilled_time"] == 10
    assert result["unreadable"] == dict["unreadable"]

    with pytest.raises(
        ValueError,
        match="Valor 'available_time' deve ser maior que zero"
    ):
        ReadingPlanService.group_news_for_available_time(0)
