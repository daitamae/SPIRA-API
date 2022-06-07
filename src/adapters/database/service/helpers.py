from typing import Union

from domain.model.user import User, AuthenticationUser
from domain.model.inference import Inference
from domain.model.model import Model


def user_helper(data) -> Union[User, None]:
    if data == None:
        return None
    return User(
        **{
            "id": str(data["_id"]),
            "username": data["username"],
            "email": data["email"],
        }
    )


def auth_user_helper(data) -> Union[AuthenticationUser, None]:
    if data == None:
        return None
    return AuthenticationUser(
        **{
            "id": str(data["_id"]),
            "username": data["username"],
            "email": data["email"],
            "hashed_password": data["hashed_password"],
        }
    )


def inference_helper(data) -> Union[Inference, None]:
    if data == None:
        return None
    return Inference(
        **{
            "id": str(data["_id"]),
            "age": data["age"],
            "sex": data["sex"],
            "user_id": data["user_id"],
        }
    )


def model_helper(data) -> Union[Model, None]:
    if data == None:
        return None
    return Model(
        **{
            "id": str(data["_id"]),
            "name": data["name"],
            "subscribing_topic": data["subscribing_topic"],
            "publishing_topic": data["publishing_topic"],
        }
    )
