from flask import Flask
app = Flask(__name__)
#session key is required
app.secret_key ="trust the process"
DATABASE="hacienda_schema"