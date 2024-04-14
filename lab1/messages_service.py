from flask import Flask

app = Flask(__name__)


@app.route('/messages-service', methods= ['GET'])
def handler_function():
    return "This service not implemented yet!"


if __name__ == "__main__":
    app.run(port=5002)