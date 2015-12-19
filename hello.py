from flask import Flask
from flask import url_for, send_from_directory
app = Flask(__name__, static_url_path='')

@app.route("/")
def hello():
    return "Hello World!"

if __name__ == "__main__":
    app.run()
