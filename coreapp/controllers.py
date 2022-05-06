from datetime import datetime
from todob.settings import DB
from .constants import collections
from .utils import create_new_sequential_id

users_collection = DB[collections.get("users")]
todos_collection = DB[collections.get("todos")]


def get_user_by_mobile(mobile):
    """
    get user by mobile number
    :param mobile: mobile number of user
    :return: user object
    """
    user = users_collection.find_one({"mobile": mobile}, {"_id": 0, "created_at": 0, "updated_at": 0, "password": 0})
    return user


def create_user(full_name, mobile, password):
    id = create_new_sequential_id(users_collection)
    users_collection.insert_one({
        "id": id,
        "full_name": full_name,
        "mobile": mobile,
        "password": password,
        "created_at": datetime.now(),
        "updated_at": datetime.now()
    })

    user = users_collection.find_one(
        {
            "mobile": mobile, "password": password
        },
        {
            "_id": 0, "createdAt": 0, "updated_at": 0, "password": 0
        }
    )
    return user


def get_user_by_mobile_and_password(mobile, password):
    user = users_collection.find_one({"mobile": mobile, "password":password}, {"_id": 0, "created_at": 0, "updated_at": 0, "password": 0})
    return user


def get_all_todo(user_id):
    todos = list(todos_collection.find({"user_id": user_id}, {"_id": 0}).sort("updated_at", -1))
    return todos


def create_new_todo(user_id, body):
    id = create_new_sequential_id(todos_collection)
    todo = todos_collection.insert_one({
        "id": id,
        "body": body,
        "user_id": user_id,
        "created_at": datetime.now(),
        "updated_at": datetime.now()
    })
    data = {
        "id":id,
        "user_id": user_id,
        "body": body,
    }
    return data


def update_todo(id, user_id, body):
    todos_collection.update_one(
        {"user_id": user_id, "id": id},
        {"$set": {"body": body}}
    )
    todo = todos_collection.find_one({"id": id}, {"_id": 0})
    return todo






