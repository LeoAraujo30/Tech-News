from tech_news.database import db
import datetime


# Requisito 7
def search_by_title(title):
    list = db.news.find(
        {"title": {"$regex": title, "$options": "i"}},
        {"_id": False, "title": True, "url": True}
    )
    result = [tuple((dict["title"], dict["url"])) for dict in list]
    return result


# Requisito 8
def validate_date(date):
    try:
        datetime.date.fromisoformat(date)
        return True
    except ValueError:
        return False


def search_by_date(date):
    if validate_date(date):
        list_date = date.split("-")
        list = db.news.find(
            {"timestamp": f"{list_date[2]}/{list_date[1]}/{list_date[0]}"},
            {"_id": False, "title": True, "url": True}
        )
        result = [tuple((dict["title"], dict["url"])) for dict in list]
        return result
    else:
        raise ValueError("Data inválida")


# Requisito 9
def search_by_category(category):
    list = db.news.find(
        {"category": {"$regex": category, "$options": "i"}},
        {"_id": False, "title": True, "url": True}
    )
    result = [tuple((dict["title"], dict["url"])) for dict in list]
    return result
