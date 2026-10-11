"""Клиент актуального API LingvoGameOs для игровой сессии портала."""

import requests
from flask import request, session

from constants import API_URL


TIMEOUT = 10


class ApiError(Exception):
    """Ошибка сети, HTTP или формата ответа портала."""


def get_game_session_id() -> int | None:
    """Сохраняет session/token из query iframe и возвращает session id."""
    raw_session_id = request.args.get("session")
    if raw_session_id is not None and raw_session_id.isdigit():
        session["game_session_id"] = int(raw_session_id)
        session["game_session_token"] = request.args.get("token")
    return session.get("game_session_id")


def login(email: str, password: str) -> str:
    """Совместимый ручной вход без устаревшего статического ключа."""
    if not (email and password):
        raise ApiError("Неправильные данные.")

    try:
        response = requests.post(
            f"{API_URL}/account/login",
            json={"email": email, "password": password},
            timeout=TIMEOUT,
        )
    except requests.RequestException as exc:
        raise ApiError(f"Портал недоступен: {exc}") from exc

    if response.status_code == 401:
        raise ApiError("Неправильный логин или пароль.")
    if response.status_code != 200:
        raise ApiError(f"Ошибка API ({response.status_code}): {response.text}")

    data = response.json()
    user_id = data.get("userId") if isinstance(data, dict) else None
    if not user_id:
        raise ApiError("Не получен ID пользователя.")
    session["user_id"] = user_id
    return str(user_id)


def add_points(amount: int) -> int:
    """Однократно начисляет целые положительные баллы игровой сессии."""
    game_session_id = session.get("game_session_id")
    if not game_session_id:
        raise ApiError("Игра запущена не с портала: сессия не выдана.")
    if not isinstance(amount, int) or amount <= 0:
        raise ApiError("Количество баллов должно быть положительным целым числом.")

    try:
        response = requests.post(
            f"{API_URL}/score",
            json={
                "gameSessionId": game_session_id,
                "score": amount,
                "token": session.get("game_session_token"),
            },
            timeout=TIMEOUT,
        )
    except requests.RequestException as exc:
        raise ApiError(f"Портал недоступен: {exc}") from exc

    if response.status_code != 200:
        raise ApiError(f"Ошибка API ({response.status_code}): {response.text}")

    data = response.json()
    points = data.get("newTotalPoints") if isinstance(data, dict) else None
    if points is None:
        raise ApiError("Некорректный ответ API.")
    return int(points)
