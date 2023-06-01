from flask_app import app
from flask_app.controllers import users
from flask_app.controllers import admins
from flask_app.controllers import feed_backs
from flask_app.controllers import meals
from flask_app.controllers import rooms
from flask_app.controllers import reservations

if __name__ == '__main__':
    app.run(debug=True, port=5005)