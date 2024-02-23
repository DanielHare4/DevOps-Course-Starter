from todo_app.flask_config import Config
import requests
import json


class Item:
    def __init__(self, id, name, status = 'To Do'):
        self.id = id
        self.name = name
        self.status = status

    @classmethod
    def from_trello_card(cls, card):
        return cls(card['id'], card['name'], card['status'])
    
    @classmethod
    def get_items(cls):
        cards = TrelloItems().get_cards()
        return [Item.from_trello_card(card) for card in cards]


class TrelloItems:
    def __init__(self):
        self.url = 'https://api.trello.com/1/'
        self.board_id = Config().TRELLO_BOARD_ID
        self.todo = Config().TRELLO_LIST_ID_TODO
        self.done = Config().TRELLO_LIST_ID_DONE
        self.query = {
            'key': Config().TRELLO_API_KEY,
            'token': Config().TRELLO_API_TOKEN
        }
        self.headers = {
            "Accept": "application/json"
        }

    def get_cards(self):
        url = self.url + f'boards/{self.board_id}/cards'

        response = requests.request(
            "GET",
            url,
            params=self.query
        )
        cards = []
        for card in response.json():
            cards.append({
                'id': int(card['idShort']),
                'status': self.get_status_from_list_id(card['idList']),
                'name': card['name'],
                'card_id': card['id'],
                'list_id': card['idList']
            })
        return cards
    
    def add_card(self, title):
        url = self.url + f'cards'

        self.query['idList'] = self.todo
        self.query['name'] = title

        response = requests.request(
        "POST",
        url,
        headers=self.headers,
        params=self.query
        )
        return response.status_code
    
    def delete_card(self, id):
        card = self.get_card_from_id(id)
        url = self.url + f'cards/{card['card_id']}'

        response = requests.request(
        "DELETE",
        url,
        params=self.query
        )
        return response.status_code
    
    def change_card(self, id):
        card = self.get_card_from_id(id)
        new_list = self.get_changed_list(card['list_id'])
        url = self.url + f'cards/{card['card_id']}'

        self.query['idList'] = new_list

        response = requests.request(
            "PUT",
            url,
            headers=self.headers,
            params=self.query
        )
        return response.status_code

    def get_changed_list(self, list_id):
        if list_id == self.todo:
            return self.done
        elif list_id == self.done:
            return self.todo

    def get_status_from_list_id(self, list_id):
        if list_id == self.todo:
            return 'To Do'
        elif list_id == self.done:
            return 'Done'
    
    def get_card_from_id(self, id):
        cards = self.get_cards()
        for card in cards:
            if int(id) == card['id']:
                return card
