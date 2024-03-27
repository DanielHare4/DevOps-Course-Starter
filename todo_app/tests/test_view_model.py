from todo_app.data.view_model import ViewModel
from todo_app.data.trello_items import Item
import pytest

test_cards = [
    {'id': 1, 'status': 'Done', 'name': 'Test1', 'card_id': 'test_card_id_1', 'list_id': 'done_list_id'},
    {'id': 2, 'status': 'To Do', 'name': 'Test2', 'card_id': 'test_card_id_2', 'list_id': 'todo_list_id'}
]

@pytest.fixture
def view_model() -> ViewModel:
    test_items = [Item.from_trello_card(card) for card in test_cards]
    return ViewModel(test_items)

def test_view_model_done_property(view_model: ViewModel):
    done_items = view_model.done_items
    for item in done_items:
        assert item.status == 'Done'

def test_view_model_todo_property(view_model: ViewModel):
    todo_items = view_model.todo_items
    for item in todo_items:
        assert item.status == 'To Do'