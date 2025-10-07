from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

# def test_read_events():

def test_read_events():
    #Create an item
    response_post = client.post("/event/", json={
        "sport_id": 1,
        "location_id": 1,
        "date_event": "2025-10-08"
    })
    assert response_post.status_code == 200, response_post.text
    response_get = client.get("/event/")
    data = response_get.json()
    assert response_get.status_code == 200
    assert isinstance(data, list)
    # assert data == []
    assert len(data) == 1
    assert data[0]["date_event"] == "2025-10-08"
    # Check that the related sport and location are included
    assert response_get.json()[0]["sport"] is not None
    assert response_get.json()[0]["location"] is not None
    #Check that the related sport and location have correct data
    assert response_get.json()[0]["sport"]["name"] == "Athlétisme"
    assert response_get.json()[0]["location"]["name"] == "Stade de France"
    assert response_get.json()[0]["location"]["nb_places"] == 80000

def test_create_event():
    response = client.post("/event/", json={
        "sport_id": 3,
        "location_id": 3,
        "date_event": "2025-10-08"
    })
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["sport_id"] == 3
    assert data["location_id"] == 3
    assert data["date_event"] == "2025-10-08"



