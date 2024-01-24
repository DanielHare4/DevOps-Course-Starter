from flask import Flask, render_template, request, redirect
from todo_app.data.session_items import SessionItems

from todo_app.flask_config import Config

app = Flask(__name__)
app.config.from_object(Config())
si = SessionItems()

@app.route('/')
def index():
    items=si.get_items()
    items = sorted(items, key=lambda x: x['status'], reverse=True)
    return render_template("index.html", items=items)

@app.route('/add-item', methods=["GET", "POST"])
def add_item():
    if request.method == "POST":
        title = request.form.get("title", "")
        si.add_item(title)
        return redirect('/')
    return render_template("add_item.html")

@app.route('/change-status/<id>')
def change_status(id):
    item = si.get_item(id)
    if item['status'] == "Not Started":
        item['status'] = "Completed"
    elif item['status'] == "Completed":
        item['status'] = "Not Started"
    si.save_item(item)
    return redirect('/')

@app.route('/delete-item/<id>')
def delete_item(id):
    si.delete_item(id)
    return redirect('/')
