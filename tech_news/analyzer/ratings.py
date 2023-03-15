from tech_news.database import db


# Requisito 10
def get_categories(list):
    categories = []
    for dict in list:
        if dict["category"] not in categories:
            categories.append(dict["category"])

    return categories


def get_quantity(categories, list):
    quantity = []
    for category in categories:
        number = 0
        for dict in list:
            if dict["category"] == category:
                number += 1

        quantity.append(number)

    return quantity


def category_list(categories, quantity):
    list = []
    index = 0
    while index < len(categories):
        list.append(
            {"category": categories[index], "quantity": quantity[index]}
        )
        index += 1

    return list


def sort_categories(e):
    return -e["quantity"], e["category"]


def top_5_categories():
    list_db = db.news.find({}, {"_id": False, "category": True})
    list = [dict for dict in list_db]
    categories = get_categories(list)
    quantity = get_quantity(categories, list)
    all_categories = category_list(categories, quantity)
    all_categories.sort(key=sort_categories)
    top_5 = all_categories[:5]
    result = [e["category"] for e in top_5]

    return result
