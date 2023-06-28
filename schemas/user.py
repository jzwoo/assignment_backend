def user_entity(item) -> dict:
    return {
        "user_id": int(item["user_id"]),
        "name": item["name"],
        "role": item["role"],
        "locked": bool(item["locked"]),
        "date_of_creation": item["date_of_creation"],
    }


def users_entity(entity) -> list:
    return [user_entity(item) for item in entity]

