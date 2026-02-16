import requests
import pytest

BASE_URL = "https://postman-echo.com"


class TestPostmanEchoGet:


    # ──────────────────────────────────────────────
    # ТЕСТ 1: GET-запрос с query-параметрами
    # ──────────────────────────────────────────────
    def test_get_with_query_params(self):

        params = {"name": "Alice", "age": "30"}

        response = requests.get(f"{BASE_URL}/get", params=params)

        assert response.status_code == 200

        data = response.json()
        # Сервер должен вернуть наши параметры в поле "args"
        assert data["args"]["name"] == "Alice"
        assert data["args"]["age"] == "30"

    # ──────────────────────────────────────────────
    # ТЕСТ 2: GET-запрос без параметров
    # ──────────────────────────────────────────────
    def test_get_without_params(self):

        response = requests.get(f"{BASE_URL}/get")

        assert response.status_code == 200

        data = response.json()
        # Без параметров — args должен быть пустым
        assert data["args"] == {}
        # Проверяем, что URL совпадает
        assert data["url"] == f"{BASE_URL}/get"

    # ──────────────────────────────────────────────
    # ТЕСТ 3: GET-запрос с кастомными заголовками
    # ──────────────────────────────────────────────
    def test_get_with_custom_headers(self):

        custom_headers = {
            "X-Custom-Header": "TestValue123",
            "Accept-Language": "ru-RU"
        }

        response = requests.get(f"{BASE_URL}/get", headers=custom_headers)

        assert response.status_code == 200

        data = response.json()
        # Postman Echo возвращает заголовки в нижнем регистре
        assert data["headers"]["x-custom-header"] == "TestValue123"
        assert data["headers"]["accept-language"] == "ru-RU"


class TestPostmanEchoPost:
    """Тесты для POST-запросов к postman-echo.com/post"""

    # ──────────────────────────────────────────────
    # ТЕСТ 4: POST-запрос с JSON-телом
    # ──────────────────────────────────────────────
    def test_post_with_json_body(self):

        payload = {
            "username": "john_doe",
            "email": "john@example.com",
            "roles": ["admin", "user"],
            "active": True
        }

        response = requests.post(f"{BASE_URL}/post", json=payload)

        assert response.status_code == 200

        data = response.json()
        # Сервер возвращает распарсенный JSON в поле "json"
        assert data["json"]["username"] == "john_doe"
        assert data["json"]["email"] == "john@example.com"
        assert data["json"]["roles"] == ["admin", "user"]
        assert data["json"]["active"] is True
        # Content-Type должен быть application/json
        assert "application/json" in data["headers"]["content-type"]

    # ──────────────────────────────────────────────
    # ТЕСТ 5: POST-запрос с query-параметрами И телом одновременно
    # ──────────────────────────────────────────────
    def test_post_with_params_and_json_body(self):

        params = {"source": "mobile", "version": "2"}
        payload = {"action": "login", "timestamp": 1700000000}

        response = requests.post(
            f"{BASE_URL}/post",
            params=params,
            json=payload
        )

        assert response.status_code == 200

        data = response.json()
        # Query-параметры в "args"
        assert data["args"]["source"] == "mobile"
        assert data["args"]["version"] == "2"
        # JSON-тело в "json"
        assert data["json"]["action"] == "login"
        assert data["json"]["timestamp"] == 1700000000

    # ──────────────────────────────────────────────
    # ТЕСТ 6: POST-запрос с plain text телом
    # ──────────────────────────────────────────────
    def test_post_with_plain_text(self):

        text_body = "Hello, this is a plain text message!"
        headers = {"Content-Type": "text/plain"}

        response = requests.post(
            f"{BASE_URL}/post",
            data=text_body,
            headers=headers
        )

        assert response.status_code == 200

        data = response.json()
        # При text/plain тело попадает в "data"
        assert data["data"] == text_body
        # form и json должны быть пустыми
        assert data["json"] is None


class TestPostmanEchoResponseStructure:
    """Тесты структуры и форматы ответов"""


# ──────────────────────────────────────────────────
# Запуск из командной строки
# ──────────────────────────────────────────────────
if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])