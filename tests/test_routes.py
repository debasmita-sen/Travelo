from app import create_app


def test_home_route():
    app = create_app()
    app.testing = True
    client = app.test_client()
    response = client.get("/")
    assert response.status_code == 200


def test_conversation_flow():
    app = create_app()
    app.testing = True
    client = app.test_client()

    # 1. Start a new chat (which should fallback to general chat)
    response = client.post("/api/chat", json={
        "message": "Hello, tell me a travel joke",
        "use_tools": False
    })
    assert response.status_code == 200
    data = response.get_json()
    assert data["type"] == "chat"
    conversation_id = data["conversation_id"]
    assert conversation_id is not None

    # 2. Send a follow-up message in the same conversation
    response_follow_up = client.post("/api/chat", json={
        "message": "Tell me another one",
        "conversation_id": conversation_id
    })
    assert response_follow_up.status_code == 200
    data_follow_up = response_follow_up.get_json()
    assert data_follow_up["type"] == "chat"
    assert data_follow_up["conversation_id"] == conversation_id

    # 3. Delete the entire conversation
    response_delete = client.delete(f"/api/conversation/{conversation_id}")
    assert response_delete.status_code == 200
    assert response_delete.get_json()["deleted"] is True

    # 4. Verify getting conversation returns empty list
    response_get = client.get(f"/api/conversation/{conversation_id}")
    assert response_get.status_code == 200
    assert len(response_get.get_json()["conversation"]) == 0
