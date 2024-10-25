from todo_app.flask_config import Config
from todo_app.data.items import Item
from enum import Enum, unique
import pymongo

class MongoDBItems:
    def __init__(self):
        self.config = Config()
        self.client = pymongo.MongoClient(self.config.MONGODB_CONNECTION_STRING)
        self.db = self.client[self.config.MONGODB_DB_NAME]
        self.collection = self.db[self.config.MONGODB_COLLECTION_NAME]

    def get_items(self):
        mongodb_documents = list(self.collection.find())
        items = []
        for document in mongodb_documents:
            item = Item.from_mongodb_document(document)
            items.append(item)
        return items

    def add_item(self, title):
        item = {
            "id": str(len(list(self.collection.find())) + 1),
            "name": title,
            "status": "To Do"
        }
        self.collection.insert_one(item)

    def change_item_status(self, id):
        current_status = self.collection.find_one({"id": id})["status"]
        new_status = Status.change_status(current_status)
        self.collection.update_one({"id": id}, {"$set": {"status": new_status}})

    def delete_item(self, id):
        self.collection.delete_one({"id": id})

    def drop_collection(self, collection_name):
        self.db.drop_collection(collection_name)

@unique
class Status(Enum):
    TODO = "To Do"
    DONE = "Done"

    def change_status(self):
        if self == Status.TODO.value:
            return Status.DONE.value
        elif self == Status.DONE.value:
            return Status.TODO.value
