#Завдання 1 Написати просту обробку запиту метода GET сервером. На запит повертати строку “Hello World!”

from flask import Flask
app = Flask(__name__)

@app.route("/")
def hello_world():
    return "Hello, World!"

if __name__ == '__main__':
 app.run(port=8000)

#Завдання 2 Написати просту обробку запиту метода GET сервером зі шляхом та параметрами в URL

from flask import Flask, request

app = Flask(__name__)

@app.route("/currency", methods=["GET"])
def get_currency():
    today = request.args.get('today')
    key = request.args.get('key')
    return "USD - 41.5"

if __name__ == '__main__':
    app.run(port=8000)

#Завдання 3 Обробка заголовків запиту

from flask import Flask, request, jsonify, Response

app = Flask(__name__)

@app.route("/headers", methods=["GET"])
def headers_handler():
    content_type = request.headers.get('Content-Type')
    if content_type == "application/json":
        return jsonify({"message": "Hello, JSON!"})
    elif content_type == "application/xml":
        return Response("<message>Hello, XML!</message>", mimetype='application/xml')
    else:
        return "Hello, plain text!"

if __name__ == '__main__':
    app.run(port=8000)










