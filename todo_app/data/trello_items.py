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


class TrelloItems:
    def __init__(self):
        self.url = "https://api.trello.com/1/"
        self.config = Config()
        self.board_id = self.config.TRELLO_BOARD_ID
        self.todo = self.config.TRELLO_LIST_ID_TODO
        self.done = self.config.TRELLO_LIST_ID_DONE
        self.headers = {
            "Accept": "application/json"
        }

    def query(self):
        return {
            'key': self.config.TRELLO_API_KEY,
            'token': self.config.TRELLO_API_TOKEN
        }

    def get_cards(self):
        url = self.url + f"boards/{self.board_id}/cards"

        response = requests.get(
            url,
            params=self.query()
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
    
    def get_items(self):
        cards = self.get_cards()
        return [Item.from_trello_card(card) for card in cards]
    
    def add_card(self, title):
        url = self.url + "cards"

        query = self.query()
        query['idList'] = self.todo
        query['name'] = title

        response = requests.post(
        url,
        headers=self.headers,
        params=query
        )
        return response.status_code
    
    def delete_card(self, id):
        card = self.get_card_from_id(id)
        url = self.url + f"cards/{card['card_id']}"

        response = requests.delete(
        url,
        params=self.query()
        )
        return response.status_code
    
    def change_card(self, id):
        card = self.get_card_from_id(id)
        new_list = self.get_changed_list(card['list_id'])
        url = self.url + f"cards/{card['card_id']}"

        query = self.query()
        query['idList'] = new_list

        response = requests.put(
            url,
            headers=self.headers,
            params=query
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

# Test functions
    def create_test_board(self):
        url = self.url + 'boards'
        query = self.query()
        query['name'] = 'TEST'

        response = requests.post(
            url,
            params=query
        )
        id = response.json()['shortUrl']
        # shortUrl = 'https://trello.com/b/{board_id}'
        id = id.replace('https://trello.com/b/','')
        return id
    
    def get_todo_and_done_lists(self, board_id):
        url = self.url + f'boards/{board_id}/lists'
        headers = {
            "Accept": "application/json"
        }
        response = requests.get(
            url,
            headers=headers,
            params=self.query()
        )
        for item in response.json():
            if item['name'] == 'To Do':
                todo = item['id']
            elif item['name'] == 'Done':
                done = item['id']
        return todo, done

    
    def delete_test_board(self, board_id):
        url = self.url + f'boards/{board_id}'
        response = requests.delete(
            url,
            params=self.query()
        )
        return response.status_code
