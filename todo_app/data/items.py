class Item:
    def __init__(self, id, name, status = 'To Do'):
        self.id = id
        self.name = name
        self.status = status

    @classmethod
    def from_trello_card(cls, card):
        return cls(card['id'], card['name'], card['status'])
    
    @classmethod
    def from_mongodb_document(cls, document):
        return cls(document['id'], document['name'], document['status'])