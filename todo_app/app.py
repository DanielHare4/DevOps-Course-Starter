from flask import Flask, render_template, request, redirect
from todo_app.data.mongodb_items import MongoDBItems
from todo_app.data.view_model import ViewModel
from todo_app.flask_config import Config
from loggly.handlers import HTTPSHandler
from logging import Formatter
import os

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config())
    mongodb = MongoDBItems()
    app.logger.setLevel(os.environ.get('LOG_LEVEL'))
    if app.config['LOGGLY_TOKEN'] is not None:
        handler = HTTPSHandler(f'https://logs-01.loggly.com/inputs/{app.config["LOGGLY_TOKEN"]}/tag/todo-app')
        handler.setFormatter(
            Formatter("[%(asctime)s] %(levelname)s in %(module)s: %(message)s")
        )
        app.logger.addHandler(handler)

    @app.route('/')
    def index():
        items = mongodb.get_items()
        item_view_model = ViewModel(items)
        app.logger.info('Render home page')
        return render_template("index.html", view_model=item_view_model)

    @app.route('/add-item', methods=["GET"])
    def add_item_page():
        app.logger.info('Adding new item')
        return render_template("add_item.html")

    @app.route('/add-item', methods=["POST"])
    def add_item():
        title = request.form.get("title", "")
        mongodb.add_item(title)
        app.logger.info(f'New item added: {title}')
        return redirect('/')

    @app.route('/change-status/<id>', methods=["POST"])
    def change_status(id):
        mongodb.change_item_status(id)
        app.logger.info(f'Changed item status: {id}')
        return redirect('/')

    @app.route('/delete-item/<id>')
    def delete_item(id):
        mongodb.delete_item(id)
        app.logger.info(f'Deleted item: {id}')
        return redirect('/')
    
    return app
