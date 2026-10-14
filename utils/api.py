"""Клиент актуального API LingvoGameOs для игровой сессии портала."""

import os
import requests
from flask import request, session

from constants import API_URL


TIMEOUT = 10


class ApiError(Exception):
    """Ошибка сети, HTTP или формата ответа портала."""


def get_game_session_id() -> int | None:
    """Читает ID новой сессии из query либо возвращает подтверждённый ID."""
    raw_session_id = request.args.get("session")
    if raw_session_id is not None:
        if not raw_session_id.isdigit() or int(raw_session_id) <= 0:
            raise ApiError("Портал передал некорректный ID игровой сессии.")
        return int(raw_session_id)
    return session.get("game_session_id")


def get_game_session():
    """Проверяет HMAC и сохраняет профиль пользователя портала."""
    game_session_id = get_game_session_id()
    if not game_session_id:
        return None
    token = (
        request.args.get("token")
        if request.args.get("session") is not None
        else session.get("game_session_token")
    )

    try:
        response = requests.post(
            f"{API_URL}/game/session/resolve",
            json={
                "gameSessionId": game_session_id,
                "token": token,
            },
            timeout=TIMEOUT,
        )
    except requests.RequestException as exc:
        raise ApiError(f"Портал недоступен: {exc}") from exc

    if response.status_code == 401:
        raise ApiError("Портал отклонил подпись игровой сессии.")
    if response.status_code == 404:
        raise ApiError("Игровая сессия не найдена.")
    if response.status_code != 200:
        raise ApiError(f"Ошибка API ({response.status_code}): {response.text}")

    data = response.json()
    if not isinstance(data, dict) or not data.get("valid") or not data.get("userId"):
        raise ApiError("Некорректный ответ API игровой сессии.")
    expected_game_id = os.environ.get("LINGVO_GAME_ID")
    if not expected_game_id or not expected_game_id.isdigit():
        raise ApiError("LINGVO_GAME_ID не настроен для этой игры.")
    if str(data.get("gameId")) != expected_game_id:
        raise ApiError("Игровая сессия выдана для другой игры.")

    session["game_session_id"] = game_session_id
    session["game_session_token"] = token
    session["portal_user_id"] = data["userId"]
    session["portal_user_name"] = data.get("userName") or "Игрок"
    session["portal_total_points"] = data.get("totalUserPoints", 0)
    return data


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
    session["portal_total_points"] = points
    return int(points)
