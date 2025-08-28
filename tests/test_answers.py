import uuid
from fastapi.testclient import TestClient


def test_create_answer_for_question(client: TestClient):
    """Тест создания ответа для вопроса."""
    # Сначала создаем вопрос
    q_response = client.post("/questions/", json={"text": "A question for an answer"})
    assert q_response.status_code == 201
    question_id = q_response.json()["id"]

    # Теперь создаем ответ
    user_id = str(uuid.uuid4())
    response = client.post(
        f"/questions/{question_id}/answers/",
        json={"text": "This is my answer", "user_id": user_id}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["text"] == "This is my answer"
    assert data["question_id"] == question_id
    assert data["user_id"] == user_id


def test_create_answer_for_nonexistent_question(client: TestClient):
    """Тест: нельзя создать ответ для несуществующего вопроса."""
    user_id = str(uuid.uuid4())
    response = client.post(
        "/questions/9999/answers/",
        json={"text": "A lonely answer", "user_id": user_id}
    )
    assert response.status_code == 404


def test_read_question_with_answers(client: TestClient):
    """Тест: при чтении вопроса возвращаются и его ответы."""
    # 1. Создаем вопрос
    q_response = client.post("/questions/", json={"text": "Question with answers"})
    question_id = q_response.json()["id"]

    # 2. Создаем ответы
    client.post(f"/questions/{question_id}/answers/", json={"text": "Answer 1", "user_id": str(uuid.uuid4())})
    client.post(f"/questions/{question_id}/answers/", json={"text": "Answer 2", "user_id": str(uuid.uuid4())})

    # 3. Получаем вопрос и проверяем ответы
    response = client.get(f"/questions/{question_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["text"] == "Question with answers"
    assert len(data["answers"]) == 2
    assert data["answers"][0]["text"] == "Answer 1"
    assert data["answers"][1]["text"] == "Answer 2"
