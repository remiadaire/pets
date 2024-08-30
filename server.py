from flask_app import app
from flask_app.controllers import users
from flask_app.controllers import pets
from flask import flash

if __name__ == "__main__":
    app.run(debug=True, host="localhost", port=7777)