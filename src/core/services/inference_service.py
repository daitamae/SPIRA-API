from typing import List, Union
from fastapi import status
from core.model.token import Token
from core.ports.authentication_port import AuthenticationPort

from core.ports.database_port import DatabasePort
from core.model.inference import Inference, InferenceCreation
from core.model.exception import LogicException

import core.services.model_service as model_service


def get_by_id(
    authentication_port: AuthenticationPort,
    database_port: DatabasePort,
    inference_id: str,
    user_id: str,
    token: Token,
) -> Union[Inference, LogicException]:
    try:
        if not authentication_port.validate_token(token):
            raise
        decode_token_content = authentication_port.decode_token(token)
        user = database_port.get_user_by_username(decode_token_content.username)
    except:
        raise LogicException(
            "could not validate the credentials", status.HTTP_401_UNAUTHORIZED
        )
    if user.id != user_id:
        raise LogicException("Forbidden operation", status.HTTP_403_FORBIDDEN)
    try:
        inference = database_port.get_inference_by_id(inference_id, user_id)
    except:
        raise LogicException(
            "inference id is not valid", status.HTTP_422_UNPROCESSABLE_ENTITY
        )
    if inference is None:
        raise LogicException("inference not found", status.HTTP_404_NOT_FOUND)
    return inference


def get_list(
    authentication_port: AuthenticationPort,
    database_port: DatabasePort,
    user_id: str,
    token: Token,
) -> Union[List[Inference], LogicException]:
    try:
        if not authentication_port.validate_token(token):
            raise
        decode_token_content = authentication_port.decode_token(token)
        user = database_port.get_user_by_username(decode_token_content.username)
    except:
        raise LogicException(
            "could not validate the credentials", status.HTTP_401_UNAUTHORIZED
        )
    if user.id != user_id:
        raise LogicException("Forbidden operation", status.HTTP_403_FORBIDDEN)
    try:
        inference_list = database_port.get_inference_list(user_id)
    except:
        raise LogicException(
            "cound not retrieve inference list", status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    return inference_list


def _validate_new_inference(
    authentication_port: AuthenticationPort,
    database_port: DatabasePort,
    inference_form: InferenceCreation,
):
    try:
        model = database_port.get_model_by_id(inference_form.model_id)
    except:
        raise LogicException(
            "model id is not valid", status.HTTP_422_UNPROCESSABLE_ENTITY
        )
    if model is None:
        raise LogicException("model not found", status.HTTP_404_NOT_FOUND)


def create_new_inference(
    authentication_port: AuthenticationPort,
    database_port: DatabasePort,
    user_id: str,
    inference_form: InferenceCreation,
    token: Token,
):
    try:
        if not authentication_port.validate_token(token):
            raise
        decode_token_content = authentication_port.decode_token(token)
        user = database_port.get_user_by_username(decode_token_content.username)
    except:
        raise LogicException(
            "could not validate the credentials", status.HTTP_401_UNAUTHORIZED
        )
    if user.id != user_id:
        raise LogicException("Forbidden operation", status.HTTP_403_FORBIDDEN)
    try:
        _validate_new_inference(authentication_port, database_port, inference_form)
    except LogicException as e:
        raise e
    database_port.insert_inference(inference_form)
    try:
        database_port.insert_inference(inference_form)
    except:
        raise LogicException(
            "cound not create new inference", status.HTTP_500_INTERNAL_SERVER_ERROR
        )