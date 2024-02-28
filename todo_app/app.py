from flask import Flask, render_template, request, redirect
from todo_app.data.trello_items import TrelloItems, Item

from todo_app.flask_config import Config

app = Flask(__name__)
app.config.from_object(Config())
trello = TrelloItems()

@app.route('/')
def index():
    items = trello.get_items()
    items = sorted(items, key=lambda x: x.id)
    items = sorted(items, key=lambda x: x.status, reverse=True)
    return render_template("index.html", items=items)

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
