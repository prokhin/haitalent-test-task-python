import uuid
from fastapi.testclient import TestClient


def test_create_question(client: TestClient):
    """Тест создания вопроса."""
    response = client.post("/questions/", json={"text": "What is FastAPI?"})
    assert response.status_code == 201
    data = response.json()
    assert data["text"] == "What is FastAPI?"
    assert "id" in data


def test_read_question(client: TestClient):
    """Тест чтения вопроса."""
    response = client.post("/questions/", json={"text": "Test Question"})
    assert response.status_code == 201
    question_id = response.json()["id"]

    response = client.get(f"/questions/{question_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["text"] == "Test Question"
    assert data["id"] == question_id


def test_read_questions(client: TestClient):
    """Тест чтения списка вопросов."""
    client.post("/questions/", json={"text": "Question 1"})
    client.post("/questions/", json={"text": "Question 2"})

    response = client.get("/questions/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 2


def test_delete_question_cascade(client: TestClient):
    """Тест каскадного удаления: при удалении вопроса удаляются и ответы."""
    # 1. Создаем вопрос
    q_response = client.post("/questions/", json={"text": "Question to be deleted"})
    assert q_response.status_code == 201
    question_id = q_response.json()["id"]

    # 2. Добавляем к нему ответ
    user_id = str(uuid.uuid4())
    a_response = client.post(
        f"/questions/{question_id}/answers/",
        json={"text": "An answer", "user_id": user_id}
    )
    assert a_response.status_code == 201
    answer_id = a_response.json()["id"]

    # 3. Удаляем вопрос
    del_response = client.delete(f"/questions/{question_id}")
    assert del_response.status_code == 200

    # 4. Проверяем, что вопрос удален (404)
    get_q_response = client.get(f"/questions/{question_id}")
    assert get_q_response.status_code == 404

    # 5. Проверяем, что ответ тоже удален (404)
    get_a_response = client.get(f"/answers/{answer_id}")
    assert get_a_response.status_code == 404
