#1 SERVER

from flask import Flask, request, jsonify, make_response
import json
import os
from functools import wraps

app = Flask(__name__)

# Файл для збереження каталогу товарів
ITEMS_FILE = 'items.json'
USERS_FILE = 'users.json'

# Ініціалізація файлів, якщо вони не існують
if not os.path.exists(ITEMS_FILE):
    with open(ITEMS_FILE, 'w') as f:
        json.dump([], f)

if not os.path.exists(USERS_FILE):
    with open(USERS_FILE, 'w') as f:
        json.dump({"admin": "password123"}, f)  # Додати адміністратора за замовчуванням


# Функція для перевірки аутентифікації
def check_auth(username, password):
    with open(USERS_FILE, 'r') as f:
        users = json.load(f)
    return users.get(username) == password


# Обробка помилок аутентифікації
def authenticate():
    return make_response("Authentication required", 401, {"WWW-Authenticate": "Basic realm='Login Required'"})


# Декоратор для захисту ендпоінтів
def requires_auth(func):
    @wraps(func)  # Зберігає атрибути функції (наприклад, ім'я)
    def wrapper(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return func(*args, **kwargs)
    return wrapper


# Ендпоінт: /items (робота з усіма товарами)
@app.route('/items', methods=['GET', 'POST'])
@requires_auth
def items():
    if request.method == 'GET':
        with open(ITEMS_FILE, 'r') as f:
            items = json.load(f)
        return jsonify(items)

    if request.method == 'POST':
        new_item = request.get_json()
        with open(ITEMS_FILE, 'r') as f:
            items = json.load(f)
        items.append(new_item)
        with open(ITEMS_FILE, 'w') as f:
            json.dump(items, f)
        return jsonify(new_item), 201


# Ендпоінт: /items/<id> (робота з конкретним товаром)
@app.route('/items/<int:item_id>', methods=['GET', 'PUT', 'DELETE'])
@requires_auth
def item(item_id):
    with open(ITEMS_FILE, 'r') as f:
        items = json.load(f)

    item = next((item for item in items if item['id'] == item_id), None)

    if request.method == 'GET':
        if not item:
            return jsonify({"error": "Item not found"}), 404
        return jsonify(item)

    if request.method == 'PUT':
        if not item:
            return jsonify({"error": "Item not found"}), 404
        updated_item = request.get_json()
        items = [updated_item if item['id'] == item_id else item for item in items]
        with open(ITEMS_FILE, 'w') as f:
            json.dump(items, f)
        return jsonify(updated_item)

    if request.method == 'DELETE':
        if not item:
            return jsonify({"error": "Item not found"}), 404
        items = [item for item in items if item['id'] != item_id]
        with open(ITEMS_FILE, 'w') as f:
            json.dump(items, f)
        return jsonify({"message": "Item deleted"})


if __name__ == '__main__':
    app.run(port=8000)

##########################################################################################################################################

#2 CLIENT

import requests
from requests.auth import HTTPBasicAuth

BASE_URL = "http://127.0.0.1:8000"
USERNAME = "nure"
PASSWORD = "LB3"

# Додати товар
def add_item(item):
    response = requests.post(f"{BASE_URL}/items", json=item, auth=HTTPBasicAuth(USERNAME, PASSWORD))
    print(response.json())

# Отримати всі товари
def get_items():
    response = requests.get(f"{BASE_URL}/items", auth=HTTPBasicAuth(USERNAME, PASSWORD))
    print(response.json())

# Отримати товар за ID
def get_item(item_id):
    response = requests.get(f"{BASE_URL}/items/{item_id}", auth=HTTPBasicAuth(USERNAME, PASSWORD))
    print(response.json())

# Оновити товар
def update_item(item_id, updated_item):
    response = requests.put(f"{BASE_URL}/items/{item_id}", json=updated_item, auth=HTTPBasicAuth(USERNAME, PASSWORD))
    print(response.json())

# Видалити товар
def delete_item(item_id):
    response = requests.delete(f"{BASE_URL}/items/{item_id}", auth=HTTPBasicAuth(USERNAME, PASSWORD))
    print(response.json())

# Приклад використання
if __name__ == '__main__':
    # Додати новий товар
    add_item({"id": 1, "name": "Coffee", "price": 10.99})
    # Отримати всі товари
    get_items()
    # Оновити товар
    update_item(1, {"id": 1, "name": "Arabica Coffee", "price": 12.99})
    # Отримати товар за ID
    get_item(1)
    # Видалити товар
    delete_item(1)
