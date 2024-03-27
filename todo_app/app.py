from flask import Flask, render_template, request, redirect
from todo_app.data.trello_items import TrelloItems, Item
from todo_app.data.view_model import ViewModel

from todo_app.flask_config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config())
    trello = TrelloItems()

    @app.route('/')
    def index():
        items = trello.get_items()
        item_view_model = ViewModel(items)
        return render_template("index.html", view_model=item_view_model)

    @app.route('/add-item', methods=["GET"])
    def add_item_page():
        return render_template("add_item.html")

    @app.route('/add-item', methods=["POST"])
    def add_item():
        title = request.form.get("title", "")
        trello.add_card(title)
        return redirect('/')

    @app.route('/change-status/<id>', methods=["POST"])
    def change_status(id):
        trello.change_card(id)
        return redirect('/')

    @app.route('/delete-item/<id>')
    def delete_item(id):
        trello.delete_card(id)
        return redirect('/')
    
    return app
