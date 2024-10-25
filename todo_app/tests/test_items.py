import pytest
import os
import mongomock
import pymongo
from dotenv import load_dotenv, find_dotenv
from todo_app import app

@pytest.fixture
def client():
    file_path = find_dotenv('.env.test')
    load_dotenv(file_path, override=True)
    
    with mongomock.patch(servers=(('fakemongo.com', 27017),)):
        test_app = app.create_app()
        with test_app.test_client() as client:
            yield client

def test_index_page(client):
    db_client = pymongo.MongoClient(os.environ.get('MONGODB_CONNECTION_STRING'))
    db = db_client[os.environ.get('MONGODB_DB_NAME')]
    collection = db[os.environ.get('MONGODB_COLLECTION_NAME')]

    test_item = {
        "id": str(1),
        "name": "Test item",
        "status": "To Do"
    }

    collection.insert_one(test_item)

    response = client.get('/')

    assert response.status_code == 200
    assert 'Test item' in response.data.decode()