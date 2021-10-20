from flask import Flask
from routers.get_data import get_data_router
from dataviz import dashboard

app = Flask(__name__)
app.register_blueprint(get_data_router)

# dash = dashboard

@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    app.run('0.0.0.0', 5000)
